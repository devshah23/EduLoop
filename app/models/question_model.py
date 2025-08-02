from typing import List

from sqlalchemy import String

from .assignment_question_association_model import assignment_question_association
from ..db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)

from .assignment_model import Assignment

Question.assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment",
        secondary=assignment_question_association,
        back_populates="questions",
        passive_deletes=True
)

