from email import message
import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassRead, ClassUpdate, ClassUpdateRead, MultiClassRead
from app.utils.exception import exception_handler
from ..utils.helper import convert_to_redis_data, get_class_cache_key
from ..service.redis_client import r

@exception_handler()
async def create_class(db: AsyncSession, class_data: ClassCreate, current_user):
    class_data.updated_by=current_user.id
    new_class = Class(**class_data.model_dump())
    db.add(new_class)
    await db.commit()
    return JSONResponse(status_code=201, content={"message": "Class created successfully"})


@exception_handler()
async def get_class(db: AsyncSession, class_id: int):
    # check redis cache first
    cached_key=get_class_cache_key(class_id)
    cached= await r.get(cached_key)
    if cached:
        return JSONResponse(status_code=200, content=json.loads(cached))
    
    result = await db.execute(select(Class).where(Class.id == class_id).options(selectinload(Class.students),selectinload(Class.faculty)))
    class_=result.scalar_one_or_none()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    await r.setex(cached_key , 60 * 60 * 24,convert_to_redis_data(ClassRead, class_)) 
    
    return JSONResponse(status_code=200, content={"class": ClassRead.model_validate(class_).model_dump()})

@exception_handler()
async def get_all_classes(db: AsyncSession):
    result = await db.execute(select(Class).options(selectinload(Class.faculty)))
    classes = result.scalars().all()
    if not classes:
        raise HTTPException(status_code=404, detail="No classes found")
    classes_data = [MultiClassRead.model_validate(class_).model_dump() for class_ in classes]
    return JSONResponse(status_code=200, content={"classes": classes_data})

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
    # invalidate cache
    await r.delete(get_class_cache_key(class_id))
    
    return JSONResponse(status_code=200, content={"message": "Class updated successfully", "class": ClassUpdateRead.model_validate(class_).model_dump()})



@exception_handler()
async def delete_class(db: AsyncSession, class_id: int):
    await db.execute(delete(Class).where(Class.id == class_id))
    await db.commit()
    await r.delete(get_class_cache_key(class_id))
    return JSONResponse(status_code=200,content={"message":"Class Deleted Successfully"})
    