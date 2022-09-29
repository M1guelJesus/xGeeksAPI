from fastapi import APIRouter, Depends
from typing import List

import crud
from core.auth import get_active_user
from schemas import User

user_router = APIRouter(prefix="/users", tags=["User"])

@user_router.get("/me", response_model=User, name="Returns logged user")
async def get_self(current_user: User = Depends(get_active_user)):
    """
    get_self gets logged user

    :param current_user: forces the user to be logged and saves its information
    :return: User logged
    """
    return current_user


@user_router.get("/interviewers", response_model=List[User], name="Returns all users that are interviewers")
async def get_interviewers():
    """
    get_interviewers gets all interviewers

    :return: List with all users with the role INTERVIEWER
    """
    return crud.user.get_interviewers()