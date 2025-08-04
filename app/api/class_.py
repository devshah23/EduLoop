from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.class_schema import ClassCreate, ClassUpdate
from app.db.session import get_db
from app.crud import class_ as class_crud

router = APIRouter(prefix="/classes", tags=["Classes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_class(class_: ClassCreate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await class_crud.create_class(db, class_,current_user)




@router.get("/{class_id}")
async def get_class(class_id: int, db: AsyncSession = Depends(get_db),_: dict = Depends(get_verified_user)):
    class_obj = await class_crud.get_class(db, class_id)
    return class_obj




@router.patch("/{class_id}")
async def update_class(class_id: int, class_: ClassUpdate, db: AsyncSession = Depends(get_db),_=Depends(require_role(UserTypeEnum.FACULTY))):
    updated = await class_crud.update_class(db, class_id, class_)
    return updated




@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(class_id: int, db: AsyncSession = Depends(get_db),_=Depends(require_role(UserTypeEnum.FACULTY))):
    result = await class_crud.delete_class(db, class_id)
    return result