from fastapi import Depends, status

from app.api.protected import get_verified_user
from app.schemas.auth_schema import CurrentUser, UserTypeEnum
from app.utils.exception import AppException

def require_role(required_role: UserTypeEnum):
    async def role_dependency(current_user:CurrentUser = Depends(get_verified_user)):
        if current_user.role != required_role.value:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message=f"{required_role.capitalize()} access required",
                code="FORBIDDEN_ACCESS"
            )
        return current_user
    return role_dependency
