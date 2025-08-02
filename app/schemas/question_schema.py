from pydantic import BaseModel, StringConstraints
from typing import Annotated, List, Optional

TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class QuestionBase(BaseModel):
    text: TrimmedStr
    answer: TrimmedStr




class QuestionCreate(QuestionBase):
    pass



class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    answer: Optional[str] = None



class QuestionRead(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuestionReadWithAssignments(QuestionRead):
    assignment_ids: List[int] = []

