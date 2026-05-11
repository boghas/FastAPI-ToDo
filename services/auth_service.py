import os
from sqlalchemy.orm import Session
from models.user_model import User
from core.security import verify_password
from jose import jwt
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone

load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def authenticate_user(username: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({'exp': expires})

    return jwt.encode(encode, JWT_SECRET_KEY, JWT_ALGORITHM)
