from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import settings


SQL_ALCHEMY_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine=create_engine(SQL_ALCHEMY_URL)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()