
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from app.auth.roles import require_role
from app.models.assignment_model import Assignment
from app.models.question_model import Question
from sqlalchemy.orm import selectinload
from app.models.submission_model import Submission
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submitted_answer_model import SubmittedAnswer
from app.service.submission_grade import grade_sumbmission


async def retry_grading(db:AsyncSession,submission_id:int):
    submission_query_result=await db.execute(select(Submission).where(Submission.id==submission_id).options(selectinload(Submission.submitted_answers)))
    submission=submission_query_result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(404,detail="Submission not found")
    
    assignment_id=submission.assignment_id
    assignment_query_result= await db.execute(select(Assignment).where(Assignment.id==assignment_id).options(selectinload(Assignment.questions)))
    assignment=assignment_query_result.scalar_one_or_none()
    submission.submitted_answers.sort(key=lambda q: q.question_id)
    assignment.questions.sort(key=lambda q: q.id)
    student_answer=[q.text for q in submission.submitted_answers]
    correct_answer=[q.answer for q in assignment.questions]
    result = await grade_sumbmission(correct_answer,student_answer,submission_id)
    if not result:
        return JSONResponse(status_code=200,content={
            "message":"Result Updated Successfully"
        })
    return JSONResponse(
        status_code=400,
        content={
            "message":"Something went wrong"
        }
    )
    
    
    
    
    