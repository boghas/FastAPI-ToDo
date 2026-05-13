from fastapi import APIRouter, HTTPException, Depends
from models.user_model import User
from schemas.token import Token
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import CreateUserRequest
from core.security import hash_password
from services.auth_service import authenticate_user, create_access_token
from datetime import timedelta
from core.config import settings
from dependencies.database import DbSession


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: DbSession, create_user_request: CreateUserRequest):
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
    db: DbSession
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        role=user.role, 
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {'access_token': token, 'token_type': 'bearer'}