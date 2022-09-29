import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sql_app.database import Base
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship


class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    date = Column(DateTime, nullable=False)
    interviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime)

    interviewer = relationship("User", back_populates="meetings", uselist=False, foreign_keys="Meeting.interviewer_id")
    candidate = relationship("User", back_populates="meetings", uselist=False, foreign_keys="Meeting.candidate_id")