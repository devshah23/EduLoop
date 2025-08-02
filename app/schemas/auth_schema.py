from typing import Optional
from pydantic import BaseModel, EmailStr


from enum import Enum

class UserTypeEnum(str, Enum):
    FACULTY="faculty"
    STUDENT="student"


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr
    name: str | None = None
    type: UserTypeEnum
    class_id: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserTypeEnum


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    class_id: int | None = None 

class CurrentUser(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    role: UserTypeEnum
    class_id: Optional[int]  = None
    exp:int

    class Config:
        orm_mode = True