from fastapi import Depends, HTTPException, status

from app.api.protected import get_verified_user
from app.schemas.auth_schema import CurrentUser, UserTypeEnum

def require_role(required_role: UserTypeEnum):
    async def role_dependency(current_user:CurrentUser = Depends(get_verified_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
               detail='You do not have permission to perform this action.'
            )
        return current_user
    return role_dependency
