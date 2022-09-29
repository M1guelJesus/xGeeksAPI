import os
import databases
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Creates the Base and Session for Database

load_dotenv()
DATABASE_URL_AUX = os.getenv("DATABASE_URL", "DATABASE URL NOT FOUND")

if DATABASE_URL_AUX and DATABASE_URL_AUX.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL_AUX.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = DATABASE_URL_AUX

print("DATABASE URL in database.py: " + DATABASE_URL)

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
my_session: Session = sessionmaker(bind=engine)
db = my_session()
Base: DeclarativeMeta = declarative_base(metadata=metadata)
