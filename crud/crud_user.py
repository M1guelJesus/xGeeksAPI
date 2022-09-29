from typing import Any, Dict, List, Optional, Union
import json
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from models import User, UserRole, Role
from schemas import UserCreate, UserUpdate
from sql_app.database import db
from core.utils import get_password_hash, verify_password
from core.utils import validate_uuid4


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email == email).first()

    def get_by_name(self, name: str) -> Optional[User]:
        return db.query(self.model).filter(User.name == name).first()

    def get_interviewers(self) -> List[User]:
        return db.query(User).join(UserRole).join(Role).filter(Role.name == "INTERVIEWER").all()

    def register(self, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name
        )

        db.add(db_obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error writing to DB")
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
