from datetime import datetime, timezone
import json
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import  ORJSONResponse
from ..utils.helper import convert_to_redis_data, get_assignment_cache_key
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..service.redis_client import r
from sqlalchemy.orm import selectinload
from app.models.assignment_model import Assignment
from app.models.question_model import Question
from app.schemas.assignment_schema import AssignmentCreate, AssignmentOut, AssignmentRead, AssignmentUpdate
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
    full_assignment=await db.execute(select(Assignment).where(Assignment.id == new_assignment.id).options(selectinload(Assignment.questions)))
    full_assignment = full_assignment.scalar_one_or_none()
    res= ORJSONResponse(
        status_code=201,
        content={
            "message": "Assignment created successfully",
            "assignment_id":AssignmentRead.model_validate(full_assignment).model_dump()
        }
    )
    if full_assignment:
        await r.setex(get_assignment_cache_key(full_assignment.id), 60 * 60 * 24, convert_to_redis_data(AssignmentRead,full_assignment))
    return res


@exception_handler()
async def get_assignment(db: AsyncSession, assignment_id: int):
    cache_key= get_assignment_cache_key(assignment_id)
    cached = await r.get(cache_key)
    if cached:
        return ORJSONResponse(
            status_code=200,
            content={
                "message": "Assignment retrieved from cache",
                "assignment": json.loads(cached)
            }
        )
    
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id).options(selectinload(Assignment.questions)))
    assignment= result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    await r.setex(get_assignment_cache_key(assignment_id), 60 * 60 * 24, convert_to_redis_data(AssignmentRead,assignment))
    return ORJSONResponse(
        status_code=200,
        content={
            "message": "Assignment retrieved successfully",
            "assignment": AssignmentRead.model_validate(assignment).model_dump()
        }
    )

@exception_handler()
async def get_assignments(db: AsyncSession,page):
    result = await db.execute(
    select(Assignment).options(selectinload(Assignment.questions).load_only(Question.id)).order_by(Assignment.created_at.desc()).offset((page-1)*10).limit(10)
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
async def get_assignments_by_me(db:AsyncSession,current_user:CurrentUser,page:int):
    result=await db.execute(select(Assignment).where(Assignment.created_by==current_user.id).options(selectinload(Assignment.questions).load_only(Question.id)).order_by(Assignment.created_at.desc()).offset((page-1)*10).limit(10))
    assignments = result.scalars().all()
    if not assignments:
        raise HTTPException(status_code=404, detail="No assignments created by you")
    
    assignments_data = [AssignmentOut.from_orm_with_ids(a).model_dump() for a in assignments]
    return ORJSONResponse(
        status_code=200,
        content={
            "message": "Assignments retrieved successfully",
            "assignments": assignments_data
        }
    )


@exception_handler()
async def get_assignments_for_me(db: AsyncSession, current_user: CurrentUser, page: int):
    result = await db.execute(
        select(Assignment)
        .where(and_(Assignment.class_id == current_user.class_id, Assignment.due_date >= datetime.now(timezone.utc)))
        .options(selectinload(Assignment.questions).load_only(Question.id))
        .order_by(Assignment.created_at.desc()).offset((page-1)*10).limit(10)
    )
    assignments = result.scalars().all()
    if not assignments:
        return ORJSONResponse(
            status_code=200,
            content={
                "message": "Hurray, no assignments available for you",
                "assignments": []
            }
        )
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
    db: AsyncSession, assignment_id: int, assignment_data: AssignmentUpdate,current_user
):
    result = await db.execute(
        select(Assignment)
        .where(Assignment.id == assignment_id)
        .options(selectinload(Assignment.questions))
    )
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    
    if assignment.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this assignment")
    
    
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
    await r.setex(get_assignment_cache_key(assignment_id), 60 * 60 * 24, convert_to_redis_data(AssignmentRead,assignment))
    return ORJSONResponse(
        status_code=200,
        content={
            "message": "Assignment updated successfully",
            "assignment": AssignmentRead.model_validate(assignment).model_dump()
        }
    )


@exception_handler()
async def delete_assignment(db: AsyncSession, assignment_id: int):
    await db.execute(delete(Assignment).where(Assignment.id == assignment_id))
    
    await db.commit()
    await r.delete(get_assignment_cache_key(assignment_id))
    return ORJSONResponse(
        status_code=200,
        content={
            "message":"Assignment deleted sucessfully",
        }
    )