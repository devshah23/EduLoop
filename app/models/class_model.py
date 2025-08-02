from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  ForeignKey, String
from ..db.base import Base


class Class(Base):
    __tablename__="classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
    updated_by: Mapped[int]=mapped_column(ForeignKey("faculties.id"), nullable=False)

    # Relationships
    faculty: Mapped["Faculty"] = relationship("Faculty",back_populates="class_details",foreign_keys=[faculty_id])
    students:Mapped[List["Student"]]=relationship("Student",back_populates="class_details")

