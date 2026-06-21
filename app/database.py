from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DB_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="settings.database_hostname",
#             database="settings.database_name",
#             user="settings.database_username",
#             password="settings.database_password",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(2)
