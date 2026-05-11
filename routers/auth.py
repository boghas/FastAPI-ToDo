from fastapi import APIRouter, HTTPException, Depends
from models.user_model import User
from schemas.token import Token
from starlette import status
from db.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas.user import CreateUserRequest
from core.security import hash_password
from services.auth_service import authenticate_user, create_access_token
from datetime import timedelta
from jose import jwt, JWTError
from core.config import settings


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=hash_password(create_user_request.password),
        is_active=True
    )

    try:
        db.add(create_user_model)
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="Database error when creating user.")
    

@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token = create_access_token(user.username, user.id, timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials."
            )
        
        return {'username': username, 'user_id': user_id}
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials."
            )