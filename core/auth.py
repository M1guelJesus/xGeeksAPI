from typing import List

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from models import User as UserModel
from schemas import User
from sql_app.database import db


async def get_active_user(authorize: AuthJWT = Depends()) -> User:
    authorize.jwt_required()
    uid = authorize.get_jwt_subject()
    user = db.query(UserModel).get(uid)
    return user

async def verify_role(user: User, authorized_roles: List[str]):
    user_role = user.user_role.role.name

    if not user.is_active:
        raise HTTPException(status_code=403, detail=[{"block": "Blocked"}])

    if user_role is None:
        raise HTTPException(status_code=403, detail=[{"permissions": "Insufficient Permissions."}])

    if user_role in authorized_roles:
        return

    raise HTTPException(status_code=403, detail=[{"permissions": "Insufficient Permissions."}])
