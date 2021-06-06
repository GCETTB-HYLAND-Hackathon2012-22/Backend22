from .environ import Config
from .router import router
from fastapi import Request, Response, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# 'postgres://' must be replaced with 'postgresql://' for proper working of sqlalchemy
SQLALCHEMY_DATABASE_URL = Config.get('DATABASE_URL', cast=str).replace('postgres://', 'postgresql://')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Acts as the base class of all schemas in schema.py
Base = declarative_base()


@router.middleware("http")
async def db_session_middleware(request: Request, call_next):
    '''HTTP Middleware to add database session to each request entity'''
    response = Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request) -> Session:
    '''Extracts Database session from the request entity'''
    return request.state.db