from fastapi import APIRouter, HTTPException, Query
from starlette import status
from dependencies.database import DbSession
from dependencies.user import user_dependency
from core import messages
from models.user_model import User
from core.security import hash_password, bcrypt_context
from schemas.user import UserVerification


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: DbSession):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHENTICATED_ERROR
        )
    
    return db.query(User).filter(User.id == user.get('user_id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: DbSession, user_verification: UserVerification):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHENTICATED_ERROR
        )
    
    user_model = db.query(User).filter(User.id == user.get('user_id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.DATABASE_ERROR_CHANGE_PASSWORD
        )
    
    user_model.hashed_password = hash_password(user_verification.new_password)

    try:
        db.add(user_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=messages.DATABASE_ERROR_CHANGE_PASSWORD
        )

    
    