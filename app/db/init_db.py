import asyncio
from app.db.session import engine
from .base import Base
from ..models.class_model import Class
from ..models.faculty_model import Faculty
from ..models.student_model import Student
from ..models.question_model import Question
from ..models.submission_model import Submission
from ..models.submitted_answer_model import SubmittedAnswer
from ..models.assignment_model import Assignment
from ..models.assignment_question_association_model import assignment_question_association


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

if __name__ == "__main__":
    asyncio.run(init())
