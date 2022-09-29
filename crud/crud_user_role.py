from typing import Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

from crud.base import CRUDBase
from models.user_role import UserRole
from schemas.user_role import UserRoleCreate, UserRoleUpdate
from sql_app.database import db
from core.utils import validate_uuid4


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def get_by_user_id(self, user_id: UUID4) -> Optional[UserRole]:
        if not validate_uuid4(user_id):
            raise HTTPException(status_code=422, detail=[{"id": "Invalid ID"}])
        try:
            return db.query(UserRole).filter(UserRole.user_id == user_id).first()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail=[{"db": "Error accessing the DB"}])


user_role = CRUDUserRole(UserRole)