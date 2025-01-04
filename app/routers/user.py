from fastapi import APIRouter 
from ..db import session_dependency
from .. import schemas, models, utils 
from ..oauth2 import current_user_dependency
from fastapi import Body, Path, HTTPException, status
from typing import Annotated
from sqlmodel import select

router = APIRouter(
    prefix="/users",
    tags=["Users"] 
)


@router.post("/", response_model=schemas.PublicUser, status_code=status.HTTP_201_CREATED)
def create_user(
    session: session_dependency,
    user: Annotated[schemas.CreateUser, Body()]
):
    """
    Create a new user
    - **email**: Each user must have a unique email(string) 
    - **password**: Each user must have a password(string)
    """
    user_data = user.model_dump() 
    
    
    new_user_email = user_data['email']
    existing_user = session.exec(select(models.User).where(models.User.email == new_user_email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {new_user_email} already exists")
    
    
    hashed_password = utils.get_hashed_password(plain_password = user_data['password'])
    new_user = models.User(
        email=new_user_email,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user 

@router.get("/me", response_model=schemas.PublicUser)
def get_current_user(current_user: current_user_dependency):
    return current_user

@router.get("/{user_id}", response_model=schemas.PublicUser)
def get_user(
    session: session_dependency,
    current_user: current_user_dependency,
    user_id: Annotated[int, Path(gt=0)]
):
    
    user = session.get(models.User, user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} not found")
    
    return user
    