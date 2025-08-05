from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.question_schema import QuestionCreate, QuestionUpdate, QuestionRead
from app.db.session import get_db
from app.crud import question as question_crud

router = APIRouter(prefix="/questions", tags=["Questions"],dependencies=[Depends(require_role(UserTypeEnum.FACULTY))])

@router.post("/")
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    return await question_crud.create_question(db, question)



@router.get("/{question_id}")
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    return await question_crud.get_question(db, question_id)
   



@router.patch("/{question_id}", response_model=QuestionRead)
async def update_question(question_id: int, question: QuestionUpdate, db: AsyncSession = Depends(get_db)):
    return await question_crud.update_question(db, question_id, question)
    


@router.delete("/{question_id}")
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db),):
    return await question_crud.delete_question(db, question_id)