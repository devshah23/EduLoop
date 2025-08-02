from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.protected import get_verified_user
from app.auth.roles import require_role
from app.schemas.auth_schema import UserTypeEnum
from app.schemas.submission_schema import SubmissionCreate, SubmissionUpdate, SubmissionRead
from app.db.session import get_db
from app.crud import submission as submission_crud

router = APIRouter(prefix="/submissions", tags=["Submissions"],dependencies=[Depends(get_verified_user)])

@router.post("/",  status_code=status.HTTP_201_CREATED)
async def create_submission(submission: SubmissionCreate,background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user),):
    return await submission_crud.create_submission(db, submission_data=submission,current_user=current_user,background_task=background_tasks)



@router.get("/{submission_id}")
async def get_submission(submission_id: int, db: AsyncSession = Depends(get_db),current_user=Depends(get_verified_user)):
    submission = await submission_crud.get_submission(db, submission_id,current_user)
    
    return submission

# @router.put("/{submission_id}", response_model=SubmissionRead)
# async def update_submission(submission_id: int, submission: SubmissionUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
#     updated = await submission_crud.update_submission(db, submission_id, submission)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Submission not found")
#     return updated

@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submission(submission_id: int, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    deleted = await submission_crud.delete_submission(db, submission_id)
    return deleted
    