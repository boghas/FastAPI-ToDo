from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="The user username.")
    email: str = Field()
    first_name: str = Field(min_length=2, description="The user's first name.")
    last_name: str = Field(min_length=2, description="The user's last name.")
    password: str = Field(min_length=3, description="The user's password.")
    phone_number: str = Field(min_length=3, description="The user's phone number.")
    role: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=3, description="The new user password")