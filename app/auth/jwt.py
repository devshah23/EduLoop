from datetime import datetime, timedelta
from jose import JWTError, jwt
from os import getenv

SECRET_KEY = getenv("SECRET_KEY","")
ALGORITHM = getenv("ALGORITHM", "HS256")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=60*24))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) or ""




def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
