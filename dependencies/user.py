from .auth import get_current_user
from typing import Annotated
from fastapi import Depends


user_dependency = Annotated[dict, Depends(get_current_user)]