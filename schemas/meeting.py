from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from .user import User


class MeetingBase(BaseModel):
    interviewer_id: UUID4
    candidate_id: Optional[UUID4] = None

class MeetingCreate(MeetingBase):
    date: str


class MeetingUpdate(BaseModel):
    candidate_id: Optional[UUID4] = None


class MeetingInDBBase(MeetingBase):
    id: UUID4
    interviewer: User
    candidate: Optional[User] = None
    date: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Meeting(MeetingInDBBase):
    pass


# Additional properties stored in DB
class MeetingInDB(MeetingInDBBase):
    pass
