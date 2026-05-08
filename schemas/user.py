from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="The user username.")
    email: str = Field()
    first_name: str = Field(min_length=2, description="The user's first name.")
    last_name: str = Field(min_length=2, description="The user's last name.")
    password: str = Field(min_length=3, description="The user's password.")
    role: str