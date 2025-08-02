from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..db.base import Base



class SubmittedAnswer(Base):
    __tablename__ = 'submitted_answers'
    id: Mapped[int] = mapped_column(primary_key=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey('submissions.id'), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)

# Relationships
from .question_model import Question
SubmittedAnswer.question: Mapped["Question"] = relationship("Question")