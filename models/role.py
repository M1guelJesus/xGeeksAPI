from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sql_app.database import Base
from sqlalchemy import Column, String


class Role(Base):
    __tablename__ = "roles"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(String(255), index=True)
    description = Column(String(1024))