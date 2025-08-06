from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
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
async def get_questions_paginated(db:AsyncSession, page:int=1):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")
    total_count = await db.execute(select(func.count()).select_from(Question))
    total_count = total_count.scalar_one()
    if page > (total_count // 10) + (1 if total_count % 10 > 0 else 0):
        raise HTTPException(status_code=404, detail="No questions found for the requested page")
    
    result=await db.execute(select(Question).offset((page-1)*10).limit(10))
    questions = result.scalars().all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"questions":[QuestionRead.model_validate(question).model_dump() for question in questions],
                 "page": page,
                 "total_pages": (total_count // 10) + (1 if total_count % 10 > 0 else 0),
                 })

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