import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from sql_app.database import Base, engine, DATABASE_URL, database
from init_db import populate_db
from routes import auth_router, user_router, meeting_router
from core.environment import config

Base.metadata.create_all(bind=engine)

app = FastAPI()

ORIGINS = config.get("cors.allowed")
origins = ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", name="App route")
async def root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup():
    asyncio.create_task(task())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def task():
    print("Connecting to the database...")
    await database.connect()
    print("Connected to the database")
    populate_db()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

# Includes all app routers in the app

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(meeting_router)