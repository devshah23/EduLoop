from dotenv import load_dotenv
load_dotenv()  

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils.exception import AppException
from .schemas.error_schema import ErrorResponse
from app.api.student import router as StudentRouter
from app.api.class_ import router as ClassRouter
from app.api.assignment import router as AssignmentRouter
from app.api.faculty import router as FacultyRouter
from app.api.question import router as QuestionRouter
from app.api.submission import router as SubmissionRouter
from app.api.auth import router as AuthRouter
from app.api.grading import router as GradingRouter

app = FastAPI()

app.include_router(AuthRouter)
app.include_router(StudentRouter)
app.include_router(ClassRouter)
app.include_router(AssignmentRouter)
app.include_router(FacultyRouter)
app.include_router(QuestionRouter)
app.include_router(SubmissionRouter)
app.include_router(GradingRouter)


@app.get("/")
async def root():
    return {"message": "EduLoop is working!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    simplified_errors = {
        e["loc"][-1]: e["msg"]
        for e in exc.errors()
        if e["loc"][0] == "body"
    }
    return JSONResponse(
        status_code=422,
        content={"message": "Validation failed", "errors": simplified_errors}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
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
async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.message,
            code=exc.code or "SERVER_ERROR",
        ).model_dump()
    )
