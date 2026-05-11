from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from jose import jwt, JWTError

from core.security import oauth2_bearer
from core.config import settings


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