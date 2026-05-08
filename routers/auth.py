from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from models import User
from passlib.context import CryptContext
from starlette import status
from db.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return True


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="The user username.")
    email: str = Field()
    first_name: str = Field(min_length=2, description="The user's first name.")
    last_name: str = Field(min_length=2, description="The user's last name.")
    password: str = Field(min_length=3, description="The user's password.")
    role: str


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
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