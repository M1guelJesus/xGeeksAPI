from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4

from crud.base import CRUDBase
from models.role import Role
from schemas.role import RoleCreate, RoleUpdate
from sql_app.database import db


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, name: str) -> Optional[Role]:
        try:
            return db.query(Role).filter(Role.name == name).first()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail=[{"db": "Error accessing the DB"}])


role = CRUDRole(Role)