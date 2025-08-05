from pydantic import BaseModel
from datetime import datetime
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

    model_config = {
        "from_attributes": True
    }

class SubmissionReadWithAnswers(SubmissionRead):
    submitted_answers: List[int] = [] 
