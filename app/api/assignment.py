from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.roles import require_role
from app.schemas.assignment_schema import AssignmentCreate, AssignmentRead, AssignmentUpdate, AssignmentMain
from app.db.session import get_db
from app.crud import assignment as assignment_crud
from app.schemas.auth_schema import UserTypeEnum

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assignment(assignment: AssignmentCreate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    return await assignment_crud.create_assignment(db, assignment,current_user)

@router.get("/paginated")
async def get_assignments(db: AsyncSession = Depends(get_db),page:int=1,_=Depends(require_role(UserTypeEnum.FACULTY))):
    assignments = await assignment_crud.get_assignments(db,page)
    return assignments

@router.get("/me")
async def get_assignments_by_me(db: AsyncSession = Depends(get_db), current_user=Depends(require_role(UserTypeEnum.FACULTY)),page:int=1):
    assignments = await assignment_crud.get_assignments_by_me(db, current_user,page)
    return assignments

@router.get('/students-me')
async def get_assignments_for_me(db:AsyncSession = Depends(get_db), current_user=Depends(require_role(UserTypeEnum.STUDENT)), page:int=1):
    assignments = await assignment_crud.get_assignments_for_me(db, current_user,page)
    return assignments

@router.get("/{assignment_id}", response_model=AssignmentRead)
async def get_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    assignment = await assignment_crud.get_assignment(db, assignment_id)
    return assignment


@router.patch("/{assignment_id}")
async def update_assignment(assignment_id: int, assignment: AssignmentUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(require_role(UserTypeEnum.FACULTY))):
    updated = await assignment_crud.update_assignment(db, assignment_id, assignment,current_user)
    return updated

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(assignment_id: int, db: AsyncSession = Depends(get_db),_=Depends(require_role(UserTypeEnum.FACULTY))):
    deleted = await assignment_crud.delete_assignment(db, assignment_id)
    return deleted