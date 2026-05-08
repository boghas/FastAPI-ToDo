from sqlalchemy.orm import Session
from models.user_model import User
from core.security import verify_password


def authenticate_user(username: str, password: str, db: Session) -> bool:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return True
