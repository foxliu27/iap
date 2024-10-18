import os

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/db")

if DATABASE_URL is not None:
    engine = create_engine(DATABASE_URL, echo=True)
else:
    raise ValueError("Database URL is not provided.")


def get_db_session():
    with Session(engine) as session:
        yield session
