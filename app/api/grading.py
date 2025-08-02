from fastapi import APIRouter, Depends

from app.auth.roles import require_role
from app.crud.grading import retry_grading
from app.db.session import get_db
from app.schemas.auth_schema import UserTypeEnum
from sqlalchemy.ext.asyncio import AsyncSession

app=APIRouter(tags=["Grading"],prefix="/grading",dependencies=[Depends(require_role(UserTypeEnum.FACULTY))])
@app.post('/retry_grading/{submission_id}')
async def retry_submission(submission_id:int,db:AsyncSession=Depends(get_db)):
    return await retry_grading(db,submission_id)