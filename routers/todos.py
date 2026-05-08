from models.todos_model import Todos
from fastapi import APIRouter, HTTPException, Depends, Path
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.todos import TodoRequest


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found!")


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    try:
        db.add(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating todo!")


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
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
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found!")
    
    try:
        db.delete(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while deleting todo!")