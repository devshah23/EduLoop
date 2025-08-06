from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.auth.password import get_password_hash
from app.models.class_model import Class
from app.models.student_model import Student
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.student_schema import StudentCreate, StudentRead, StudentUpdate
from app.utils.exception import exception_handler


@exception_handler()
async def create_student(db: AsyncSession, student_data: StudentCreate,current_user):
    result = await db.execute(select(Student).where(Student.email == student_data.email))
    existing_student = result.scalar_one_or_none()
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email already exists")
    if student_data.class_id is None:
        if current_user.class_id is None:
            raise HTTPException(status_code=400,detail="You are required to provide class_id as you are not class teacher")
        student_data.class_id=current_user.class_id
    if student_data.class_id is not None:
        class_result = await db.execute(select(Class).where(Class.id == student_data.class_id))
        class_ = class_result.scalar_one_or_none()
        if not class_:
            if current_user.class_id is None:
                raise HTTPException(status_code=400,detail="You are required to provide class_id as you are not class teacher")
            student_data.class_id=current_user.class_id
    
    student_data.password=get_password_hash(student_data.password)
    student_data.updated_by=current_user.id
    new_student = Student(**student_data.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return JSONResponse(status_code=201, content={"message": "Student created successfully", "student": StudentRead.model_validate(new_student).model_dump()})

@exception_handler()
async def get_all_students_class(db:AsyncSession,class_id:int):
    class_=await db.execute(select(Class).where(Class.id==class_id))
    class_=class_.scalar_one_or_none()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    result=await db.execute(select(Student).where(Student.class_id==class_id))
    students=result.scalars().all()
    if not students:
        raise HTTPException(status_code=404,detail="No student for this class")
    return JSONResponse(status_code=200,content={"students":[StudentRead.model_validate(student).model_dump() for student in students]})
        


@exception_handler()
async def get_student(db: AsyncSession, student_id: int):
    result = await db.execute(select(Student).where(Student.id == student_id).options(
        selectinload(Student.class_details).selectinload(Class.faculty) 
    ))
    student=result.scalar_one_or_none()
    if not student:
        return JSONResponse(status_code=404, content={"message": "Student not found"})
    return JSONResponse(status_code=200, content={ "student": StudentRead.model_validate(student).model_dump()})


@exception_handler()
async def update_student(db: AsyncSession, student_id: int, student_data: StudentUpdate,current_user):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.id!=current_user.id and current_user.role != UserTypeEnum.FACULTY:
        raise HTTPException(status_code=403, detail="You do not have to update other accounts")
    for key, value in student_data.model_dump(exclude_unset=True).items():
        if key !="id":
            setattr(student, key, value)
    if current_user.role == UserTypeEnum.FACULTY:
        student_data.updated_by=current_user.id
    student_data.password=get_password_hash(student_data.password) if student_data.password else student.password
    await db.commit()
    await db.refresh(student)

    return JSONResponse(status_code=200, content={"message": "Student updated successfully", "student": StudentRead.model_validate(student).model_dump()})



@exception_handler()
async def delete_student(db: AsyncSession, student_id: int,current_user):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student:
        if student.id!=current_user.id and current_user.role != UserTypeEnum.FACULTY:
            raise HTTPException(status_code=403, detail="You do not have rights to delete other accounts")
        await db.delete(student)
        await db.commit()
    return JSONResponse(status_code=200, content={"message": "Student deleted successfully"})



