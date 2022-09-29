from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT, AuthJWTRefresh
from pydantic import BaseModel
from starlette import status
from core.environment import config

import crud
from schemas import UserCreate, User, UserRoleCreate

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET = config.get("jwt.secret")

#region JWT Token Setup
# Settings for the JWT Token
class Settings(BaseModel):
    authjwt_secret_key: str = SECRET
    authjwt_refresh_token_expires: timedelta = timedelta(days=1)


@AuthJWT.load_config
def get_config():
    return Settings()
#endregion

@auth_router.post("/register", response_model=User, name="Registers a new user")
def register(user_in: UserCreate):
    """
    Registers a new user.
    """

    error_exists = False
    error_message: Dict[str, str] = {}

    if user_in.name is None or user_in.name.strip() == "":
        error_message["name"] = "userNoName"
        error_exists = True

    if user_in.email is None or user_in.name.strip() == "":
        error_message["email"] = "userNoEmail"
        error_exists = True

    if user_in.password is None or user_in.password.strip() == "":
        error_message["password"] = "userNoPassword"
        error_exists = True

    if user_in.interviewer is None:
        error_message["interviewer"] = "userNoInterviewer"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    if crud.user.get_by_email(user_in.email) is not None:
        raise HTTPException(status_code=409, detail=[{"email": "alreadyRegistered"}])

    role_aux = None
    print(user_in.interviewer)
    if user_in.interviewer:
        role_aux = crud.role.get_by_name("INTERVIEWER")
    else:
        role_aux = crud.role.get_by_name("CANDIDATE")


    user: User = crud.user.register(obj_in=user_in)
    crud.user_role.create(
        obj_in=UserRoleCreate(
            user_id=user.id,
            role_id=role_aux.id,
        ),
    )

    return crud.user.get(user.id)


@auth_router.post("/login", name="Login endpoint")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    authorize: AuthJWT = Depends(),
):
    """
    Login
    """
    user = crud.user.authenticate(credentials.username, credentials.password)

    if user is None:
        raise HTTPException(status_code=400, detail=[{"credentials": "Invalid Credentials"}])

    if not user.is_active:
        raise HTTPException(status_code=403, detail=[{"block": "Blocked"}])


    """
    create_access_token supports an optional 'fresh' argument,
    which marks the token as fresh or non-fresh accordingly.
    As we just verified their username and password, we are
    going to mark the token as fresh here.
    """
    access_token = authorize.create_access_token(
        subject=str(user.id),
        fresh=True,
    )
    refresh_token = authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.post(
    "/refresh",
    name="Provides an access token if valid refresh token is provided",
)
def refresh(authorize: AuthJWTRefresh = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
