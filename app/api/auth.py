from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth_schema import LoginRequest, SignupRequest
from os import getenv
from app.crud import auth

COOKIE_NAME = getenv("COOKIE_NAME", "SubmitAssignment")
app = APIRouter(tags=["Authentication"],prefix="/auth")



@app.post("/login")
async def login(request_data: LoginRequest,db: AsyncSession = Depends(get_db)):
   return await auth.login(db, request_data)



# @app.post("/signup")
# async def signup(request_data:SignupRequest,db:AsyncSession=Depends(get_db)):
#     return await auth.signup( db,request_data)




@app.post("/logout")
async def logout():
    return auth.logout()