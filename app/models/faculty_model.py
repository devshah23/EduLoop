from sqlalchemy.orm import Mapped, mapped_column, relationship  
from sqlalchemy import ForeignKey, String
from ..db.base import Base

class Faculty(Base):
    __tablename__ = "faculties"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    updated_by:Mapped[int]=mapped_column(ForeignKey("faculties.id"), nullable=False)
    
    # Relationship
    class_details: Mapped["Class"] = relationship("Class", back_populates="faculty",uselist=False,foreign_keys="Class.faculty_id")