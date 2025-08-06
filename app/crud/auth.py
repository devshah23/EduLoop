from typing import cast
from fastapi import  HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.cookies import create_cookie
from app.auth.jwt import create_access_token
from app.auth.password import get_password_hash, verify_password
from app.models.class_model import Class
from app.models.faculty_model import Faculty
from app.models.student_model import Student
from app.schemas.auth_schema import CurrentUser, LoginRequest, SignupFacultyRequest, SignupRequest, UserTypeEnum
from app.utils.exception import exception_handler
from os import getenv
from sqlalchemy.orm import selectinload

COOKIE_NAME=getenv("COOKIE_NAME", "SubmitAssignment")

async def get_student_by_email( db: AsyncSession,email: str,):
    result = await db.execute(select(Student).where(Student.email == email).options(selectinload(Student.class_details)))
    return result.scalar_one_or_none()

async def get_faculty_by_email( db: AsyncSession,email: str) -> Faculty | None:
    result = await db.execute(select(Faculty).where(Faculty.email == email).options(selectinload(Faculty.class_details)))  
    return result.scalar_one_or_none()

@exception_handler()
async def login(db: AsyncSession,request_data: LoginRequest):
    user=None
    if request_data.role== UserTypeEnum.FACULTY:
        user=await get_faculty_by_email(db, request_data.email)
    if request_data.role == UserTypeEnum.STUDENT:
        user = await get_student_by_email(db, request_data.email)
    if not user or not verify_password(request_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    
    token_data={"id":user.id,"email":user.email,"name":user.name}
    if(request_data.role==UserTypeEnum.FACULTY):
        token_data["role"]=UserTypeEnum.FACULTY
        if user.class_details:
            token_data["class_id"]=user.class_details.id
        else:
            token_data["class_id"]=None
    else:
        student = cast(Student, user)
        token_data["role"]=UserTypeEnum.STUDENT
        token_data["class_id"]=student.class_id

    value = create_access_token(data=token_data)
    response = JSONResponse(content={"message": "Login successful"})
    response=create_cookie(response,COOKIE_NAME,value,3600*24)
    return response

@exception_handler()
async def signup( db: AsyncSession,request_data: SignupRequest,current_user: CurrentUser):
    existing_student=await get_student_by_email(db, request_data.email)
    if existing_student:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    class_result=await db.execute(select(Class).where(Class.id == request_data.class_id))
    exist_class=class_result.scalar_one_or_none()

    if exist_class is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    print(exist_class.id)
    print("Hello",current_user.email, current_user.id)
    hashed_password=get_password_hash(request_data.password)
    new_student = Student(
        email=request_data.email,
        name=request_data.name,
        class_id=exist_class.id,
        password=hashed_password,
        updated_by=current_user.id
    )
    db.add(new_student)
    await db.commit()
    response= JSONResponse(content={"message": "Student Account Creation successful"}, status_code=status.HTTP_201_CREATED)
    return response

@exception_handler()
async def create_faculty( db: AsyncSession,request_data: SignupFacultyRequest,current_user: CurrentUser):
    existing_faculty=await get_faculty_by_email(db, request_data.email)
    if existing_faculty:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    hashed_password=get_password_hash(request_data.password)
    new_faculty = Faculty(
        email=request_data.email,
        name=request_data.name,
        password=hashed_password,
        updated_by=current_user.id
    )
    db.add(new_faculty)
    await db.commit()
    response= JSONResponse(content={"message": "Faculty Account Creation successful"}, status_code=status.HTTP_201_CREATED)
    return response


@exception_handler()
async def logout():
    response = JSONResponse(content={"message": "Logout successful"}, status_code=status.HTTP_200_OK)
    response.delete_cookie(COOKIE_NAME)
    return response