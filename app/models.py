from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.sql.expression import text 
from datetime import datetime
from typing import Optional

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    title: str = Field(index=True)
    content: str 
    published: bool | None = Field(default=True, sa_column_kwargs={"server_default": 'TRUE'})
    create_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": text('NOW()')}) 
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    
    owner: "User" = Relationship(back_populates="posts") 
        


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str 
    create_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"server_default": text('NOW()')})

    posts: list[Post] = Relationship(back_populates="owner", cascade_delete=True) 


class Vote(SQLModel, table=True):
    post_id: int = Field(primary_key=True, foreign_key="post.id", ondelete="CASCADE")
    user_id: int = Field(primary_key=True, foreign_key="user.id", ondelete="CASCADE") 
    
        