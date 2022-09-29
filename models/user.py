import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sql_app.database import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean(), default=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime)

    user_role = relationship("UserRole", back_populates="user", uselist=False)
    meetings = relationship("Meeting", uselist=True, primaryjoin="or_(User.id==Meeting.interviewer_id, User.id==Meeting.candidate_id)")