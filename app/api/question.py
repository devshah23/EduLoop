from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.question_schema import QuestionCreate, QuestionUpdate, QuestionRead
from app.db.session import get_db
from app.crud import question as question_crud

router = APIRouter(prefix="/questions", tags=["Questions"],dependencies=[Depends(require_role(UserTypeEnum.FACULTY))])

@router.post("/", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    return await question_crud.create_question(db, question)



@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    question = await question_crud.get_question(db, question_id)
    return question



@router.put("/{question_id}", response_model=QuestionRead)
async def update_question(question_id: int, question: QuestionUpdate, db: AsyncSession = Depends(get_db)):
    updated = await question_crud.update_question(db, question_id, question)
    return updated

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await question_crud.delete_question(db, question_id)
    return deleted