import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

_ = load_dotenv()

DBHOST = str(os.environ.get("DBHOST"))
DBNAME = str(os.environ.get("DBNAME"))
DBUSER = str(os.environ.get("DBUSER"))
DBPASSWORD = str(os.environ.get("DBPASSWORD"))
DATABASE_URL = f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
