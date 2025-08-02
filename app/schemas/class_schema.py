from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional

TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class ClassBase(BaseModel):
    name: TrimmedStr
    faculty_id: int

class Class(ClassBase):
    id:int
    updated_by: Optional[int] = None

class ClassCreate(ClassBase):
    updated_by: Optional[int] = None



class ClassUpdate(Class):
    pass    

class ClassRead(ClassBase):
    id: int

    class Config:
        orm_mode = True
