from fastapi import APIRouter


router = APIRouter()


@router.get("/auth/")
async def authenticate_user():
    return {"user": "authenticated"}