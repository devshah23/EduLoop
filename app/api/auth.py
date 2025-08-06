from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.roles import require_role
from app.db.session import get_db
from app.schemas.auth_schema import LoginRequest, SignupFacultyRequest, SignupRequest, UserTypeEnum
from os import getenv
from app.crud import auth

router = APIRouter(tags=["Authentication"],prefix="/auth")


@router.post("/login")
async def login(request_data: LoginRequest,db: AsyncSession = Depends(get_db)):
   return await auth.login(db, request_data)


@router.post("/faculty-create")
async def faculty_signup(request_data: SignupFacultyRequest, db: AsyncSession = Depends(get_db), current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await auth.create_faculty(db, request_data, current_user)

@router.post("/student-create")
async def signup(request_data:SignupRequest,db:AsyncSession=Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await auth.signup( db,request_data,current_user)


@router.post("/logout")
async def logout():
    return await auth.logout()