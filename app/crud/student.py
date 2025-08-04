from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.password import get_password_hash
from app.models.student_model import Student
from app.models.submission_model import Submission
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.student_schema import StudentCreate, StudentRead, StudentUpdate
from app.utils.exception import exception_handler


@exception_handler()
async def create_student(db: AsyncSession, student_data: StudentCreate,current_user):
    student_data.updated_by=current_user.id
    student_data.class_id=current_user.class_id
    new_student = Student(**student_data.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return JSONResponse(status_code=201, content={"message": "Student created successfully", "student": StudentRead.model_validate(new_student).model_dump()})


@exception_handler()
async def get_student(db: AsyncSession, student_id: int):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student=result.scalar_one_or_none()
    if not student:
        return JSONResponse(status_code=404, content={"message": "Student not found"})
    return JSONResponse(status_code=200, content={"message": "Student found", "student": StudentRead.model_validate(student).model_dump()})


@exception_handler()
async def update_student(db: AsyncSession, student_id: int, student_data: StudentUpdate,current_user):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.id!=current_user.id and current_user.role != UserTypeEnum.FACULTY.value:
        raise HTTPException(status_code=403, detail="You do not have to update other accounts")
    student_data.updated_by=current_user.id
    student_data.password=get_password_hash(student_data.password) if student_data.password else student.password
    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
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
        if student.id!=current_user.id and current_user.role != UserTypeEnum.FACULTY.value:
            raise HTTPException(status_code=403, detail="You do not have rights to delete other accounts")
        await db.delete(student)
        await db.commit()
    return JSONResponse(status_code=200, content={"message": "Student deleted successfully"})



