from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import  Optional, List


class Questions_Answers(BaseModel):
    question_id: int
    answer: str 


class SubmissionBase(BaseModel):
    student_id: int
    assignment_id: int
    grade: Optional[float] = None
    



class SubmissionCreate(SubmissionBase):
    question_answers: List[Questions_Answers] = []
    
class SubmissionUpdate(BaseModel):
    grade: Optional[float] = None

class SubmissionRead(SubmissionBase):
    id: int
    submitted_at: datetime

    class Config:
        orm_mode = True

class SubmissionReadWithAnswers(SubmissionRead):
    submitted_answers: List[int] = [] 
