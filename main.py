import models
from models import Todos
from fastapi import FastAPI, Depends, HTTPException, Path
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(description="The name of the todo.", min_length=3, max_length=30)
    description: str = Field(description="Additional details about the todo.", min_length=3, max_length=100)
    priority: int = Field(description="The priority of the todo. Must be between 1 to 5, where 5 is highest priority.", gt=0, lt=6)
    complete: bool = Field(description="Whether the todo has been completed or not. Defaults to False.", default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The name of the todo. Must be between 3 and 30 characters.",
                "description": "Additional details about the todo. Must be between 3 and 100 characters.",
                "priority": "The priority of the todo. Must be between 1 to 5, where 5 is highest priority.",
                "complete": "Whether the todo has been completed or not. Defaults to False",
            }
        }
    }


@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found!")


@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    try:
        db.add(todo_model)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating todo!")


@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
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
    

@app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
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

        
