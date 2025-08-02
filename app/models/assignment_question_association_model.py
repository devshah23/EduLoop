from sqlalchemy import Column, ForeignKey, Table

from app.db.base import Base


assignment_question_association = Table(
    "assignment_question_association",
    Base.metadata,
    Column(
        "assignment_id",
        ForeignKey("assignments.id", ondelete="CASCADE"),  
        primary_key=True
    ),
    Column(
        "question_id",
        ForeignKey("questions.id", ondelete="RESTRICT"),  
        primary_key=True
    ),
)
