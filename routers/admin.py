from fastapi import APIRouter, HTTPException, Path
from starlette import status
from dependencies.database import DbSession
from dependencies.user import user_dependency
from core import messages
from models.todos_model import Todos


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: DbSession):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHENTICATED_ERROR
        )
    
    if not user.get('role') == 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHORIZED
        )
    
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: DbSession, todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHENTICATED_ERROR
        )
    
    if not user.get('role') == 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_AUTHORIZED
        )
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.DATABASE_ERROR_TODO_NOT_FOUND
        )
    
    try:
        db.delete(todo)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=messages.DATABASE_ERROR_DELETE_TODO
        )