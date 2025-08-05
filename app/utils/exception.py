from functools import wraps
from fastapi import HTTPException, status
from redis import RedisError
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code



def exception_handler():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get("db") or (args[0] if args else None)

            try:
                return await func(*args, **kwargs)

            except HTTPException:
                raise

            except SQLAlchemyError as e:
                orig = getattr(e, "orig", None)
                if db:
                    await db.rollback()
                if isinstance(e, IntegrityError) and getattr(orig, 'pgcode', None) == '23503':
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot delete this resource because it is still referenced elsewhere.",
                    ) from e

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e),
                    
                ) from e
            except RedisError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Redis service is unavailable. Please try again later.",
                ) from e
                
            except Exception as e:
                if db:
                    await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e) or "An unexpected error occurred.",
                ) from e

        return wrapper
    return decorator
