from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic.types import conint



class BaseUser(BaseModel):
    email: str      

class CreateUser(BaseUser):
    password: str 
    
    model_config = {
        "extra": "forbid"
    }

class PublicUser(BaseUser):
    id: int 
    create_at: datetime 

# POST
class BasePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = Field(default=True)
    
    class Config:
        orm_mode = True


class CreatePost(BasePost):
    model_config = {
        "extra": "forbid"
    }
    

class UpdatePost(BaseModel):
    title: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    published: Optional[bool] = Field(default=None)
    
    class Config:
        orm_mode = True


class PublicPost(BasePost):
    id: int
    # owner_id: int
    create_at: datetime 
    
    owner: PublicUser

# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

class Vote(BaseModel):
    post_id: int 
    dir: bool 
    
class PostOut(BaseModel):
    post: PublicPost
    votes: int 