from fastapi import APIRouter
from pydantic import BaseModel, Field
from models import User


router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="The user username.")
    email: str = Field()
    first_name: str = Field(min_length=2, description="The user's first name.")
    last_name: str = Field(min_length=2, description="The user's last name.")
    password: str = Field(min_length=3, description="The user's password.")
    role: str


@router.get("/auth/")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request.password,
        is_active=True
    )

    return create_user_model