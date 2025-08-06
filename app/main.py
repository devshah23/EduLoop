import json
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

@app.middleware("http")
async def catch_malformed_json(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            skip_paths = ["/logout", "/grading/retry_grading"]
            if not any(request.url.path.endswith(p) for p in skip_paths):
                await request.json()
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Malformed JSON. Please check your request body.",
                    "errors": {
                        "body": "Invalid JSON format"
                    }
                }
            )
    return await call_next(request)


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
    simplified_errors = {}
    print(exc.errors())
    for error in exc.errors():
        if error["loc"][0] == "body":
            field_name = error["loc"][-1]
            message = error["msg"]

            # If multiple errors for same field, accumulate them
            if field_name in simplified_errors:
                if isinstance(simplified_errors[field_name], list):
                    simplified_errors[field_name].append(message)
                else:
                    simplified_errors[field_name] = [simplified_errors[field_name], message]
            else:
                simplified_errors[field_name] = message

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "errors": simplified_errors
        }
    )



@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    status_code_map = {
        400: "BAD_REQUEST",
        401: "AUTH_ERROR",
        403: "FORBIDDEN_ACCESS",
        404: "RESOURCE_NOT_FOUND",
        409: "CONFLICT",
        405: "METHOD_NOT_ALLOWED",
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
