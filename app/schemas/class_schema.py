from pydantic import BaseModel, StringConstraints
from typing import Annotated, List, Optional

from app.api import faculty
from app.schemas.faculty_schema import FacultyRead
from app.schemas.student_schema import StudentRead

TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class ClassBase(BaseModel):
    name: TrimmedStr
    faculty_id: int

class ClassInDb(ClassBase):
    id:int
    updated_by: Optional[int] = None


class ClassCreate(ClassBase):
    updated_by: Optional[int] = None



class ClassUpdate(BaseModel):
    name:Optional[TrimmedStr]
    faculty_id: Optional[int]

class ClassRead(BaseModel):
    id: int
    name: TrimmedStr
    faculty_id: int
    updated_by: Optional[int] = None
    students:Optional[List[StudentRead]]
    faculty:Optional[FacultyRead]
    model_config = {
        "from_attributes": True,
    }
     
class ClassUpdateRead(BaseModel):
    id: int
    name: TrimmedStr
    faculty_id: int
    updated_by: Optional[int] = None
    model_config = {
        "from_attributes": True,
    }   

