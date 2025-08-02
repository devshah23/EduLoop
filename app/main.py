from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.utils.exception import AppException
from .schemas.error_schema import ErrorDetail, ErrorResponse
from app.api.student import router as StudentR
from app.api.class_ import router as ClassR
from app.api.assignment import router as AssignmentR
from app.api.faculty import router as FacultyR
from app.api.question import router as QuestionR
from app.api.submission import router as SubmissionR
from app.api.auth import app as AuthR
from app.api.grading import app as GradingR

app = FastAPI()

app.include_router(AuthR)
app.include_router(StudentR)
app.include_router(ClassR)
app.include_router(AssignmentR)
app.include_router(FacultyR)
app.include_router(QuestionR)
app.include_router(SubmissionR)
app.include_router(GradingR)


@app.get("/")
async def root():
    return {"message": "FastAPI is working!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        ErrorDetail(loc=e["loc"], msg=e["msg"], type=e["type"])
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message="Validation failed",
            errors=errors,
            code="VALIDATION_ERROR"
        ).model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    status_code_map = {
        401: "AUTH_ERROR",
        403: "FORBIDDEN_ACCESS",
        404: "RESOURCE_NOT_FOUND",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR",
    }

    custom_code = status_code_map.get(exc.status_code, "SERVER_ERROR")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
            code=custom_code,
        ).model_dump()
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.message,
            code=exc.code,
        ).model_dump()
    )
