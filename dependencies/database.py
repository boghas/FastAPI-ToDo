from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db

DbSession = Annotated[Session, Depends(get_db)]