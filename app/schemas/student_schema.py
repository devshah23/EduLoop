from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, List, Optional
from app.schemas.submission_schema import SubmissionRead

TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class StudentBase(BaseModel):
    name: TrimmedStr
    email: EmailStr
    updated_by: Optional[int] = None
    class_id: Optional[int] = None

    model_config={
        'from_attributes':True
    }



class StudentCreate(StudentBase):
    password: str



class StudentUpdate(BaseModel):
    name: Optional[str]=None
    email: Optional[EmailStr]=None
    password: Optional[str]=None
    updated_by:Optional[int]=None
    class_id:Optional[int]=None
    
    



class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True



class StudentReadWithSubmissions(StudentRead):
    submissions: List[SubmissionRead] = [] 
