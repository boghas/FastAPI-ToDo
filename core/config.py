from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # JWT settings
    JWT_SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # DB settings
    DATABASE_URL: str = Field(..., description="The database url")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()