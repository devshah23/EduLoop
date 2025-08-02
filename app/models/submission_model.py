from typing import List
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

class Submission(Base):
    __tablename__ = 'submissions'
    id:Mapped[int]=mapped_column(primary_key=True)
    student_id:Mapped[int]=mapped_column(ForeignKey('students.id'), nullable=False,index=True)
    assignment_id:Mapped[int]=mapped_column(ForeignKey('assignments.id'), nullable=False,index=True)
    grade:Mapped[float]=mapped_column(nullable=True)
    submitted_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True))

    student: Mapped["Student"] = relationship("Student", back_populates="submissions") 


from .submitted_answer_model import SubmittedAnswer
Submission.submitted_answers = relationship("SubmittedAnswer")
