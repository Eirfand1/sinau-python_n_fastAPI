import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
dbtype = "postgresql"

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{user}:{password }@{host}:{port}/{db}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()