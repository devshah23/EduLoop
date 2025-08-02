from datetime import datetime, timezone
import stat
from fastapi import BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.submitted_answer_model import SubmittedAnswer
from app.models.assignment_model import Assignment
from app.models.question_model import Question
from app.models.submission_model import Submission
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.submission_schema import SubmissionCreate, SubmissionUpdate
from app.service.submission_grade import grade_sumbmission
from app.utils.exception import exception_handler

@exception_handler()
async def create_submission(db: AsyncSession,background_task:BackgroundTasks, submission_data: SubmissionCreate,current_user):
    # result=await db.execute(select(Assignment).where(Assignment.id==submission_data.assignment_id).options(selectinload(Assignment.questions).load_only(Question.id)))
    result=await db.execute(select(Assignment).where(Assignment.id==submission_data.assignment_id).options(selectinload(Assignment.questions)))
    
    assignment=result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )
    assignment.questions.sort(key=lambda q: q.id)
    submission_data.question_answers.sort(key=lambda qa: qa.question_id)
    
    # Check for current student is submitting for themselves
    if(current_user.id!=submission_data.student_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to submit for other student."
        )
        
    # Check if the student has already submitted for this assignment
    existing_submission = (await db.scalars(
    select(Submission)
    .where(
        Submission.student_id == submission_data.student_id,
        Submission.assignment_id == submission_data.assignment_id
    )
    .limit(1)
    )).first()
    
    if existing_submission:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted this assignment."
        )
    
    # Check for submission is late
    current_time= datetime.now(timezone.utc)
    if current_time > assignment.due_date:
        raise HTTPException(
        status_code=400,
        detail="Submission is past the due date."
    )
    question_ids=[qa.question_id for qa in submission_data.question_answers]
    result = await db.execute(
    select(Question.id).where(Question.id.in_(question_ids))
    )
    existing_ids = set([a.id for a in assignment.questions])
    missing_ids = set(question_ids) - existing_ids
    if missing_ids:
        raise HTTPException(
        status_code=400,
        detail=f"These Question IDs do not exist: {list(missing_ids)}"
    )
    
    # Check for the number of question answers matches the number of questions in the assignment
    if len(submission_data.question_answers) != len(existing_ids):
        raise HTTPException(
            status_code=400,
            detail="Not all question IDs provided in the submission match the existing questions for this assignment."
        )

    answer_student=[]
    correct_answer=[a.answer for a in assignment.questions]
    for qa in submission_data.question_answers:
        answer_student.append(qa.answer)
    
    if len(answer_student) != len(correct_answer):
        raise HTTPException(
            status_code=400,
            detail="Notz all question IDs provided in the submission match the existing questions for this assignment."
        )
    
    
    
        
    
    
    
    new_submission=Submission(
        student_id=submission_data.student_id,
        assignment_id=submission_data.assignment_id,
        grade=-1,
        submitted_at=current_time,
       submitted_answers=[
        SubmittedAnswer(
            question_id=qa.question_id,
            text=qa.answer
        ) for qa in submission_data.question_answers
    ],
    )
    db.add(new_submission)
    await db.commit()
    await db.refresh(new_submission)
    
    background_task.add_task(grade_sumbmission,correct_answer,answer_student,submission_id=new_submission.id)
    
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Submission created successfully",
            "submission_id": new_submission.id
        })

@exception_handler()
async def get_submission(db: AsyncSession, submission_id: int,current_user):
    
    result = await db.execute(select(Submission).where(Submission.id == submission_id).options(
        selectinload(Submission.submitted_answers)
    ))
    submission= result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if(current_user.id!=submission.student_id and current_user.role!=UserTypeEnum.FACULTY):
        return JSONResponse(
            status_code=403,
            content={
                "message": "You are not allowed to view other's submission."
            }
        )
    return submission


# Pending Task
@exception_handler()
async def update_submission(db: AsyncSession, submission_id: int, submission_data: SubmissionUpdate):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if submission:
        for key, value in submission_data.model_dump(exclude_unset=True).items():
            setattr(submission, key, value)
        await db.commit()
        await db.refresh(submission)
    return submission


@exception_handler()
async def delete_submission(db: AsyncSession, submission_id: int):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if submission:
        await db.delete(submission)
        await db.commit()
    return JSONResponse(
        status_code=204,
        content={
            "message": "Submission deleted successfully"
        }
    )


@exception_handler()
async def get_student_submission(db:AsyncSession,student_id:int):
    result=await db.execute(select(Submission).where(Submission.student_id==student_id).order_by(Submission.submitted_at.desc()).limit(5))
    return result.scalars().all()