from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.exc import SQLAlchemyError
from app.models.question_model import Question
from app.schemas.question_schema import QuestionCreate, QuestionRead, QuestionUpdate
from app.utils.exception import exception_handler

@exception_handler()
async def create_question(db: AsyncSession, question_data: QuestionCreate):    
    new_question = Question(**question_data.model_dump())
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Question created successfully", "question": QuestionRead.model_validate(new_question).model_dump()}
    )



@exception_handler()
async def get_question(db: AsyncSession, question_id: int):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question= result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Question retrieved successfully", "question": QuestionRead.model_validate(question).model_dump()})


@exception_handler()
async def update_question(db: AsyncSession, question_id: int, question_data: QuestionUpdate):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in question_data.model_dump(exclude_unset=True).items():
        setattr(question, key, value)
    await db.commit()
    await db.refresh(question)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Question updated successfully", "question": QuestionRead.model_validate(question).model_dump()})



@exception_handler()
async def delete_question(db: AsyncSession, question_id: int):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    await db.delete(question)
    await db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Question deleted successfully"})