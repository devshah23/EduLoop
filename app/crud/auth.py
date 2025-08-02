from typing import cast
from fastapi import  status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.cookies import create_cookie
from app.auth.jwt import create_access_token
from app.auth.password import get_password_hash, verify_password
from app.models.class_model import Class
from app.models.faculty_model import Faculty
from app.models.student_model import Student
from app.schemas.auth_schema import LoginRequest, SignupRequest, UserTypeEnum
from app.utils.exception import AppException, exception_handler
from os import getenv
from sqlalchemy.orm import selectinload

COOKIE_NAME=getenv("COOKIE_NAME", "SubmitAssignment")

async def get_student_by_email( db: AsyncSession,email: str,) -> Student | None:
    result = await db.execute(select(Student).where(Student.email == email))
    return result.scalar_one_or_none()

async def get_faculty_by_email( db: AsyncSession,email: str) -> Faculty | None:
    result = await db.execute(select(Faculty).options(selectinload(Faculty.class_details)).where(Faculty.email == email))  
    return result.scalar_one_or_none()

@exception_handler()
async def login(db: AsyncSession,request_data: LoginRequest):
    user=None
    if request_data.role== UserTypeEnum.FACULTY.value:
        user=await get_faculty_by_email(db, request_data.email)

    if request_data.role == UserTypeEnum.STUDENT.value:
        user = await get_student_by_email(db, request_data.email)

    if not user or not verify_password(request_data.password, user.password):
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Incorrect email or password",code="AUTH_ERROR")
    
    token_data={"id":user.id,"email":user.email,"name":user.name}
    if(request_data.role==UserTypeEnum.FACULTY.value):
        token_data["role"]=UserTypeEnum.FACULTY.value
        token_data["class_id"]=user.class_details.id
    else:
        student = cast(Student, user)
        token_data["role"]=UserTypeEnum.STUDENT.value
        token_data["class_id"]=student.class_id

    value = create_access_token(data=token_data)
    response = JSONResponse(content={"message": "Login successful"})
    response=create_cookie(response,COOKIE_NAME,value,3600)
    return response

@exception_handler()
async def signup( db: AsyncSession,request_data: SignupRequest):
    existing_student=await get_student_by_email(db, request_data.email)
    if existing_student:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message="Email already exists", code="EMAIL_EXISTS")
    
    class_result=await db.execute(select(Class).where(Class.id == request_data.class_id))
    exist_class=class_result.scalar_one_or_none()

    if exist_class is None:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message="Class not found", code="CLASS_NOT_FOUND")
    
    hashed_password=get_password_hash(request_data.password)
    new_student = Student(
        email=request_data.email,
        name=request_data.name,
        class_id=exist_class.id,
        password=hashed_password
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    response= JSONResponse(content={"message": "Signup successful"}, status_code=status.HTTP_201_CREATED)
    value=create_access_token(data={"sub": new_student.email, "name": new_student.name, "type": UserTypeEnum.STUDENT, "class_id": exist_class.id})
    response=create_cookie(response,COOKIE_NAME,value,3600)
    return response

@exception_handler()
def logout():
    response = JSONResponse(content={"message": "Logout successful"}, status_code=status.HTTP_200_OK)
    response.delete_cookie(COOKIE_NAME)
    return response