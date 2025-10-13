import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

_ = load_dotenv()

DBHOST = str(os.environ.get("DBHOST"))
POSTGRES_USER = str(os.environ.get("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.environ.get("POSTGRES_PASSWORD"))
DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DBHOST}/petrodb"

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
