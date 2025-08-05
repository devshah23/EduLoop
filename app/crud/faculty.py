from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from app.auth.password import get_password_hash
from app.models.faculty_model import Faculty
from app.schemas.faculty_schema import FacultyCreate, FacultyRead, FacultyUpdate
from app.utils.exception import exception_handler


@exception_handler()
async def create_faculty(db: AsyncSession, faculty_data: FacultyCreate,current_user):
    result=await db.execute(select(Faculty).where(Faculty.email == faculty_data.email))
    existing_faculty = result.scalar_one_or_none()
    if existing_faculty:
        raise HTTPException(status_code=400, detail="Faculty with this email already exists")
    
    faculty_data.updated_by=current_user.id
    faculty_data.password=get_password_hash(faculty_data.password)
    new_faculty = Faculty(**faculty_data.model_dump())
    db.add(new_faculty)
    await db.commit()
    await db.refresh(new_faculty)
    faculty_return=FacultyRead.model_validate(new_faculty)
    return JSONResponse(status_code=201,content={"message":"Faculty created successfully", "faculty": faculty_return})



@exception_handler()
async def get_faculty(db: AsyncSession, faculty_id: int):
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    faculty=result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return JSONResponse(status_code=200,content={"faculty":FacultyRead.model_validate(faculty)})



@exception_handler()
async def update_faculty(db: AsyncSession, faculty_id: int, faculty_data: FacultyUpdate,current_user):
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    if faculty_data.password:
        faculty_data.password = get_password_hash(faculty_data.password)
    faculty_data.updated_by=current_user.id
    for key, value in faculty_data.model_dump(exclude_unset=True).items():
        setattr(faculty, key, value)
    await db.commit()
    await db.refresh(faculty)
    return JSONResponse(status_code=200, content={"message": "Faculty updated successfully", "faculty": FacultyRead.model_validate(faculty)})


@exception_handler()
async def delete_faculty(db: AsyncSession, faculty_id: int):
    await db.execute(delete(Faculty).where(Faculty.id == faculty_id))
    
    await db.commit()
    return JSONResponse(status_code=204, content={"message": "Faculty deleted successfully"})
