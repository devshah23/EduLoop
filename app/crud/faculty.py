from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.faculty_model import Faculty
from app.schemas.faculty_schema import FacultyCreate, FacultyUpdate
from app.utils.exception import exception_handler


@exception_handler()
async def create_faculty(db: AsyncSession, faculty_data: FacultyCreate,current_user):
    faculty_data.updated_by=current_user.id
    new_faculty = Faculty(**faculty_data.model_dump())
    db.add(new_faculty)
    await db.commit()
    await db.refresh(new_faculty)
    return new_faculty



@exception_handler()
async def get_faculty(db: AsyncSession, faculty_id: int):
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    return result.scalar_one_or_none()



@exception_handler()
async def update_faculty(db: AsyncSession, faculty_id: int, faculty_data: FacultyUpdate,current_user):
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    faculty = result.scalar_one_or_none()
    faculty_data.updated_by=current_user.id
    if faculty:
        for key, value in faculty_data.model_dump(exclude_unset=True).items():
            setattr(faculty, key, value)
        await db.commit()
        await db.refresh(faculty)
    return faculty



@exception_handler()
async def delete_faculty(db: AsyncSession, faculty_id: int):
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    faculty = result.scalar_one_or_none()
    if faculty:
        await db.delete(faculty)
        await db.commit()
    return faculty