from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate
from app.utils.exception import exception_handler

@exception_handler()
async def create_class(db: AsyncSession, class_data: ClassCreate, current_user):
    class_data.updated_by=current_user.id
    new_class = Class(**class_data.model_dump())
    db.add(new_class)
    await db.commit()
    await db.refresh(new_class)
    return new_class


@exception_handler()
async def get_class(db: AsyncSession, class_id: int):
    result = await db.execute(select(Class).where(Class.id == class_id))
    return result.scalar_one_or_none()


@exception_handler()
async def update_class(db: AsyncSession, class_id: int, class_data: ClassUpdate):
    result = await db.execute(select(Class).where(Class.id == class_id))
    class_ = result.scalar_one_or_none()
    if class_:
        for key, value in class_data.model_dump(exclude_unset=True).items():
            setattr(class_, key, value)
        await db.commit()
        await db.refresh(class_)
    return class_



@exception_handler()
async def delete_class(db: AsyncSession, class_id: int):
    result = await db.execute(select(Class).where(Class.id == class_id))
    class_ = result.scalar_one_or_none()
    if class_:
        await db.delete(class_)
        await db.commit()
    return class_