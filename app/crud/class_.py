from email import message
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
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
    return JSONResponse(status_code=201, content={"message": "Class created successfully", "class": new_class})


@exception_handler()
async def get_class(db: AsyncSession, class_id: int):
    result = await db.execute(select(Class).where(Class.id == class_id).options(selectinload(Class.students,Class.faculty)))
    class_=result.scalar_one_or_none()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return JSONResponse(status_code=200, content={"class": class_})


@exception_handler()
async def update_class(db: AsyncSession, class_id: int, class_data: ClassUpdate):
    result = await db.execute(select(Class).where(Class.id == class_id))
    class_ = result.scalar_one_or_none()
    
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    for key, value in class_data.model_dump(exclude_unset=True).items():
        if key!="id":
            setattr(class_, key, value)
    await db.commit()
    await db.refresh(class_)
    return JSONResponse(status_code=200, content={"message": "Class updated successfully", "class": class_})



@exception_handler()
async def delete_class(db: AsyncSession, class_id: int):
    result = await db.execute(select(Class).where(Class.id == class_id))
    class_ = result.scalar_one_or_none()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    await db.delete(class_)
    await db.commit()
    return JSONResponse(status_code=200,content={"message":"Class Deleted Successfully"})
    