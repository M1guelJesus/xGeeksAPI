from sql_app.database import db
from sql_app.base import Base
from typing import Optional
import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from core.utils import get_password_hash
from models import User, Role

"""
Script to initialize the Database
Imports from the constants files and populates the BD
"""

#region aux functions
def get_role_by_name(name: str) -> Optional[Role]:
    try:
        return db.query(Role).filter(Role.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail=[{"error": "Error writing to DB"}])

def create_role(obj_in: Role) -> Role:
    db.add(obj_in)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail=[{"error": "Error writing to DB"}])
    db.refresh(obj_in)
    return obj_in
#endregion


def populate_db():
    print("\n=== Started init_db.py script ===\n")

    #region Create Roles
    print("\n=== Creating Roles ===\n")

    roles = json.load(open("./constants/roles.json", "r"))
    for role in roles:
        if get_role_by_name(role["name"]) is None:
            create_role(obj_in=Role(
                name=role["name"],
                description=role["description"],
            ))
            print(f"Created role {role['name']}")
        else:
            print(f"Role {role['name']} already in DB")

    print("\n=== Ended creating Roles ===\n")
    #endregion

    print("=== Ended init_db.py script ===")
