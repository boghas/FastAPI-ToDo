from fastapi import APIRouter, HTTPException, Depends
from models.user_model import User
from passlib.context import CryptContext
from starlette import status
from db.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import CreateUserRequest
from core.security import hash_password
from services.auth_service import authenticate_user


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


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
    

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return "Failed auth"
    
    return "successful auth"