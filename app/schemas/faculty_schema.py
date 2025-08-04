from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, Optional

TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class FacultyBase(BaseModel):
    name: TrimmedStr
    email: EmailStr
    updated_by: Optional[int] = None

class FacultyInDB(FacultyBase):
    id:int

class FacultyCreate(FacultyBase):
    password: TrimmedStr

class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    updated_by: Optional[int] = None

class FacultyRead(FacultyInDB):
    class Config:
        orm_mode = True
