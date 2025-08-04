from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.student_schema import StudentCreate, StudentUpdate, StudentRead
from app.db.session import get_db
from app.crud import student as student_crud

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/")
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await student_crud.create_student(db, student,current_user)




@router.get("/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db),_=Depends(get_verified_user)):
    return await student_crud.get_student(db, student_id)
    



@router.put("/{student_id}")
async def update_student(student_id: int, student: StudentUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user)):
    updated = await student_crud.update_student(db, student_id, student,current_user)
    return updated

@router.delete("/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user)):
    deleted = await student_crud.delete_student(db, student_id,current_user)
    return deleted