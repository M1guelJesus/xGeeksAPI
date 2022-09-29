from typing import Optional
from pydantic import UUID4, BaseModel
from schemas.role import Role


class UserRoleBase(BaseModel):
    user_id: UUID4
    role_id: UUID4


class UserRoleCreate(UserRoleBase):
    user_id: Optional[UUID4]
    role_id: Optional[UUID4]


class UserRoleUpdate(BaseModel):
    role_id: UUID4


class UserRoleInDBBase(UserRoleBase):
    role: Role

    class Config:
        orm_mode = True


class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass