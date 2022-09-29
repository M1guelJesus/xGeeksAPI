# Xgeeks Meets

## Backend

Project developed in Python with FastAPI and SQLAlchemy

Live Demo: https://m1gueljesus.github.io/

## Project Local Setup

-   Clone this repository

```
git clone https://gitlab.com/miguelangelolealjesus/fs-assignment-miguelangelolealjesus.git
```

-   Enter the project directory

```
cd fs-assignment-miguelangelolealjesus/backend
```

-   Instal PostgreSQL 14 (it should also work it some older versions but this was not tested)
    https://www.postgresql.org/docs/current/admin.html

-   Create a new Database

-   Get the connection string and save it in the .env file in the var DATABASE_URL
    DATABASE_URL=postgresql://DB_USER_NAME:DB_USER_PASS@IP_DB:PORT_DB/DATABSE_NAME

example:

```
DATABASE_URL=postgresql://postgres:123@localhost/xgeeks_db
```

#

### In the backend directory of the project:

-   Install poetry
    (https://python-poetry.org/docs/)

-   Instal deppendencies

```
poetry update
```

-   Enter the python enviroment

```
poetry shell
```

-   Run the project

```
uvicorn app:app --reload
```
