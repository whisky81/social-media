from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..db import session_dependency
from .. import schemas, models, oauth2, utils
from typing import Annotated
from sqlmodel import select 

router = APIRouter(
    tags=["Authentication"] 
)


@router.post("/login", response_model=schemas.Token)
def login(
    session: session_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    oauth2_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    user = session.exec(select(models.User).where(models.User.email == form_data.username)).first()
    
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise oauth2_exception
    
    access_token = oauth2.create_access_token(padload={"user_id": user.id})
    
    return schemas.Token(access_token=access_token, token_type="bearer")
        
    