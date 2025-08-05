from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.question_schema import  QuestionRead


class AssignmentBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    class_id: int
    questions: Optional[List[int]] = None  

class AssignmentInDB(AssignmentBaseSchema):
    id:int
    created_at:datetime
    created_by: int


class AssignmentMain(AssignmentInDB):
    class Config:
        from_attributes = True


class AssignmentCreate(AssignmentBaseSchema):
    class Config:
        from_attributes = True


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    class_id: Optional[int] = None
    questions: Optional[List[int]] = None  


class AssignmentRead(BaseModel):
    id:int
    title: str
    description: Optional[str] = None
    due_date: datetime
    class_id: int
    created_at: datetime
    questions:Optional[List[QuestionRead]] = None
    created_by: int
    class Config:
        from_attributes = True

class AssignmentOut(AssignmentMain):
    @classmethod
    def from_orm_with_ids(cls, assignment):
        return cls(
            id=assignment.id,
            title=assignment.title,
            description=assignment.description,
            due_date=assignment.due_date,
            created_by=assignment.created_by,
            created_at=assignment.created_at,
            class_id=assignment.class_id,
            questions=[q.id for q in assignment.questions]
        )