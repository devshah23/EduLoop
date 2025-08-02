from pydantic import BaseModel



class SubmittedAnswerBase(BaseModel):
    submission_id: int
    question_id: int
    text: str



class SubmittedAnswerCreate(SubmittedAnswerBase):
    pass


class SubmittedAnswerUpdate(SubmittedAnswerBase):
    pass



class SubmittedAnswerRead(SubmittedAnswerBase):
    id: int

    class Config:
        orm_mode = True
