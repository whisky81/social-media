from datetime import timedelta, datetime, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from .db import session_dependency
from . import models, schemas
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

token_dependency = Annotated[str, Depends(oauth2_scheme)]

def create_access_token(padload: dict):
    to_encode = padload.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def get_current_user(token: token_dependency, session: session_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        access_keys = {"user_id", "exp"} 
        
        user_id: int = payload.get("user_id")
        if set(payload.keys()) != access_keys or user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    current_user = session.get(models.User, user_id)
    if not current_user:
        raise credentials_exception
    
    current_user = schemas.PublicUser(
        id=current_user.id,
        email=current_user.email,
        create_at=current_user.create_at
    )
    
    return current_user

current_user_dependency = Annotated[schemas.PublicUser, Depends(get_current_user)]