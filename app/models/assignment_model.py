from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, func
from .question_model import Question, assignment_question_association
from .faculty_model import Faculty
from ..db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)

    # Relationships
    faculty: Mapped["Faculty"] = relationship("Faculty")
    


from .question_model import Question

Assignment.questions: Mapped[List["Question"]] = relationship(
        "Question",
        secondary=assignment_question_association,
        back_populates="assignments",
        passive_deletes=True
    )