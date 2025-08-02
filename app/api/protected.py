from os import getenv
from fastapi import Request, HTTPException, status, Depends
from app.auth.jwt import decode_access_token
from app.schemas.auth_schema import CurrentUser


COOKIE_NAME=getenv("COOKIE_NAME", "SubmitAssignment")
async def get_verified_user(request: Request):
    token = request.cookies.get(COOKIE_NAME)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return CurrentUser(**payload)
