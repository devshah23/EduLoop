from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.submission_schema import SubmissionCreate
from app.db.session import get_db
from app.crud import submission as submission_crud

router = APIRouter(prefix="/submissions", tags=["Submissions"],dependencies=[Depends(get_verified_user)])

@router.post("/")
async def create_submission(submission: SubmissionCreate,background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user),):
    return await submission_crud.create_submission(db, submission_data=submission,current_user=current_user,background_task=background_tasks)

    
@router.get("/student-latest/{student_id}")
async def get_student_submission(student_id: int, db: AsyncSession = Depends(get_db),_=Depends(require_role(UserTypeEnum.FACULTY))):
    return await submission_crud.get_student_submission(db, student_id)


@router.get("/assign-list/{assignment_id}")
async def get_assignment_submissions(assignment_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await submission_crud.get_assignment_submissions(db, assignment_id, current_user)

@router.get("/list/{student_id}")
async def submissions_sort(
    student_id: int,
    sort_fields: List[str] = Query(default=["-submitted_at"]),
    db: AsyncSession = Depends(get_db)
    , current_user=Depends(get_verified_user)
):
    return await submission_crud.get_submission_sorted(db,student_id,current_user,sort_fields)


@router.get("/{submission_id}")
async def get_submission(submission_id: int, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user)):
    return await submission_crud.get_submission(db, submission_id,current_user)
    


@router.delete("/{submission_id}")
async def delete_submission(submission_id: int, db: AsyncSession = Depends(get_db),_=Depends(require_role(UserTypeEnum.FACULTY))):
    return await submission_crud.delete_submission(db, submission_id)
