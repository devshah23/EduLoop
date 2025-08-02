from datetime import datetime, timezone
from re import A
from turtle import st
from fastapi import HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.auth.roles import require_role
from app.models.assignment_model import Assignment
from app.models.question_model import Question
from app.schemas.assignment_schema import AssignmentCreate, AssignmentMain, AssignmentOut, AssignmentRead, AssignmentUpdate
from app.schemas.auth_schema import CurrentUser
from app.utils.exception import exception_handler


@exception_handler()
async def create_assignment(
    db: AsyncSession, 
    assignment_data: AssignmentCreate,
    current_user: CurrentUser
):
    stmt = select(Question).where(Question.id.in_(assignment_data.questions or []))
    result = await db.execute(stmt)
    questions = result.scalars().all()

    new_assignment = Assignment(
        title=assignment_data.title.strip(),
        description=assignment_data.description.strip() if assignment_data.description else None,
        due_date=assignment_data.due_date,
        class_id=assignment_data.class_id,
        created_by=current_user.id,
        questions=questions
    )

    db.add(new_assignment)
    await db.commit()
    await db.refresh(new_assignment)
    stmt = (
    select(Assignment)
    .options(selectinload(Assignment.questions))
    .where(Assignment.id == new_assignment.id)
)
    result = await db.execute(stmt)
    assignment_with_questions = result.scalar_one()
    assignment_dict = assignment_with_questions.__dict__.copy()
    assignment_dict["questions"] = [q.id for q in assignment_with_questions.questions]

    
    return ORJSONResponse(
        status_code=201,
        content={
            "message": "Assignment created successfully",
            "assignment": AssignmentMain.model_validate(assignment_dict).model_dump()
        }
    )


@exception_handler()
async def get_assignment(db: AsyncSession, assignment_id: int):
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id).options(selectinload(Assignment.questions)))
    assignment= result.scalar_one_or_none()
    if not assignment:
        return HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@exception_handler()
async def get_assignments(db: AsyncSession):
    result = await db.execute(
    select(Assignment).options(selectinload(Assignment.questions).load_only(Question.id))
)
    assignments = result.scalars().all()

    assignments_data = [AssignmentOut.from_orm_with_ids(a).model_dump() for a in assignments]

    return ORJSONResponse(
        status_code=200,
        content={
        "message": "Assignments retrieved successfully",
        "assignments": assignments_data
    }
)



@exception_handler()
async def update_assignment(
    db: AsyncSession, assignment_id: int, assignment_data: AssignmentUpdate
):
    result = await db.execute(
        select(Assignment)
        .where(Assignment.id == assignment_id)
        .options(selectinload(Assignment.questions))
    )
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for key, value in assignment_data.model_dump(exclude_unset=True).items():
        if key != "questions": 
            setattr(assignment, key, value)

    if assignment_data.questions is not None:
        q_result = await db.execute(
            select(Question).where(Question.id.in_(assignment_data.questions))
        )
        existing_questions = q_result.scalars().all()

        if len(existing_questions) != len(set(q for q in assignment_data.questions)):
            raise HTTPException(status_code=400, detail="Some question IDs are invalid")

        assignment.questions = existing_questions  

    await db.commit()
    await db.refresh(assignment)

    return ORJSONResponse(
        status_code=200,
        content={
            "message": "Assignment updated successfully",
            "assignment": AssignmentRead.model_validate(assignment).model_dump()
        }
    )



@exception_handler()
async def delete_assignment(db: AsyncSession, assignment_id: int):
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404,detail="Assignment not found")
    if assignment:
        await db.delete(assignment)
        await db.commit()
    return ORJSONResponse(
        status_code=200,
        content={
            "message":"Assignment deleted sucessfully",
        }
    )