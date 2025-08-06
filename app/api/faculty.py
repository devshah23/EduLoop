from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.faculty_schema import FacultyCreate, FacultyUpdate, FacultyRead
from app.db.session import get_db
from app.crud import faculty as faculty_crud

router = APIRouter(prefix="/faculties", tags=["Faculties"])

@router.post("/")
async def create_faculty(faculty: FacultyCreate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await faculty_crud.create_faculty(db, faculty,current_user)

@router.get("/all")
async def get_all_faculties(db: AsyncSession = Depends(get_db),_=Depends(get_verified_user)):
    return await faculty_crud.get_all_faculties(db)

@router.get("/{faculty_id}")
async def get_faculty(faculty_id: int, db: AsyncSession = Depends(get_db),_=Depends(get_verified_user)):
    return await faculty_crud.get_faculty(db, faculty_id)
    

@router.patch("/{faculty_id}")
async def update_faculty(faculty_id: int, faculty: FacultyUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await faculty_crud.update_faculty(db, faculty_id, faculty,current_user)



@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(faculty_id: int, db: AsyncSession = Depends(get_db)):
    return await faculty_crud.delete_faculty(db, faculty_id)
    
    