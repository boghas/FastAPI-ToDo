from models.todos_model import Todos
from fastapi import APIRouter, HTTPException, Path
from starlette import status
from schemas.todos import TodoRequest
from dependencies.database import DbSession
from dependencies.user import user_dependency
from core.messages import USER_NOT_AUTHORIZED


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: DbSession):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_AUTHORIZED
        )

    return db.query(Todos).filter(Todos.owner == user.get('user_id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: DbSession, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found!")


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: DbSession, todo_request: TodoRequest):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_AUTHORIZED
        )
    
    todo_model = Todos(**todo_request.model_dump(), owner = user.get('user_id'))

    try:
        db.add(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating todo!")


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: DbSession, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    try:
        db.add(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while updating todo!")
    

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DbSession, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found!")
    
    try:
        db.delete(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while deleting todo!")