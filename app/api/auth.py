from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.roles import require_role
from app.db.session import get_db
from app.schemas.auth_schema import LoginRequest, SignupRequest, UpdateStudent, UserTypeEnum
from os import getenv
from app.crud import auth

COOKIE_NAME = getenv("COOKIE_NAME", "SubmitAssignment")
app = APIRouter(tags=["Authentication"],prefix="/auth")



@app.post("/login")
async def login(request_data: LoginRequest,db: AsyncSession = Depends(get_db)):
   return await auth.login(db, request_data)



@app.post("/signup")
async def signup(request_data:SignupRequest,db:AsyncSession=Depends(get_db),current_user=require_role(UserTypeEnum.FACULTY)):
    return await auth.signup( db,request_data)


@app.patch("/update-student")
async def update_student(id:int,request_data:UpdateStudent,db:AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await auth.update_student(db,request_data,id,current_user)


@app.post("/logout")
async def logout():
    return auth.logout()