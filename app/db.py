from sqlmodel import create_engine, Session
from .models import SQLModel, Post 
from typing import Annotated
from fastapi import Depends
from .config import settings

# create postgresql url and engine to establish with database
postgresql_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(postgresql_url) 


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session 

    
session_dependency = Annotated[Session, Depends(get_session)]