from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel
from .user_role import UserRole

class UserBase(BaseModel):
    email: str
    name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    interviewer: bool
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    pass


class UserInDBBase(UserBase):
    id: UUID4
    is_active: Optional[bool] = True
    user_role: UserRole
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
