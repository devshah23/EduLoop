from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserTypeEnum(str, Enum):
    FACULTY="faculty"
    STUDENT="student"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserTypeEnum

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    class_id: int | None = None 
    

class SignupFacultyRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class UpdateStudent(BaseModel):
    name:Optional[str]=None
    class_id:Optional[int]=None
    email:Optional[EmailStr]=None
    password: Optional[str]=None
    

class CurrentUser(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    role: UserTypeEnum
    class_id: Optional[int]  = None
    exp:int

    model_config = {
        "from_attributes": True
    }