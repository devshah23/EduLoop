from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.faculty_schema import FacultyCreate, FacultyUpdate, FacultyRead
from app.db.session import get_db
from app.crud import faculty as faculty_crud

router = APIRouter(prefix="/faculties", tags=["Faculties"])

@router.post("/", response_model=FacultyRead, status_code=status.HTTP_201_CREATED)
async def create_faculty(faculty: FacultyCreate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await faculty_crud.create_faculty(db, faculty,current_user)



@router.get("/{faculty_id}", response_model=FacultyRead)
async def get_faculty(faculty_id: int, db: AsyncSession = Depends(get_db),_=Depends(get_verified_user)):
    faculty = await faculty_crud.get_faculty(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty



@router.put("/{faculty_id}", response_model=FacultyRead)
async def update_faculty(faculty_id: int, faculty: FacultyUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    updated = await faculty_crud.update_faculty(db, faculty_id, faculty,current_user)
    if not updated:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return updated



@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(faculty_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await faculty_crud.delete_faculty(db, faculty_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Faculty not found")