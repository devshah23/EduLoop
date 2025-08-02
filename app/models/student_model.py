from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship  
from sqlalchemy import ForeignKey, String
from .submission_model import Submission
from ..db.base import Base
from .class_model import Class

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
    
    # Relationship
    class_details: Mapped["Class"] = relationship("Class", back_populates="students")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="student")

