import os
from sqlalchemy.orm import Session
from models.user_model import User
from core.security import verify_password
from jose import jwt
from datetime import timedelta, datetime, timezone
from core.config import settings


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return 
    
    if not verify_password(password, user.hashed_password):
        return
    
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({'exp': expires})

    return jwt.encode(encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
