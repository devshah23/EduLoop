from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.submitted_answer_model import SubmittedAnswer
from app.schemas.submitted_answer_schema import SubmittedAnswerCreate, SubmittedAnswerUpdate
from app.utils.exception import exception_handler


@exception_handler()
async def create_submitted_answer(db: AsyncSession, answer_data: SubmittedAnswerCreate):
    new_answer = SubmittedAnswer(**answer_data.model_dump())
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    return new_answer


@exception_handler()
async def get_submitted_answers_by_submission(db: AsyncSession, submission_id: int):
    result= await db.execute(select(SubmittedAnswer).where(SubmittedAnswer.submission_id == submission_id))
    return result.scalars().all()



@exception_handler()
async def get_submitted_answer(db: AsyncSession, answer_id: int):
    result = await db.execute(select(SubmittedAnswer).where(SubmittedAnswer.id == answer_id))
    return result.scalar_one_or_none()



@exception_handler()
async def update_submitted_answer(db: AsyncSession, answer_id: int, answer_data: SubmittedAnswerUpdate):
    result = await db.execute(select(SubmittedAnswer).where(SubmittedAnswer.id == answer_id))
    answer = result.scalar_one_or_none()
    if answer:
        for key, value in answer_data.model_dump(exclude_unset=True).items():
            setattr(answer, key, value)
        await db.commit()
        await db.refresh(answer)
    return answer



@exception_handler()
async def delete_submitted_answer(db: AsyncSession, answer_id: int):
    result = await db.execute(select(SubmittedAnswer).where(SubmittedAnswer.id == answer_id))
    answer = result.scalar_one_or_none()
    if answer:
        await db.delete(answer)
        await db.commit()
    return answer