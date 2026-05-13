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


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
