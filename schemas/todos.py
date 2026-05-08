from pydantic import BaseModel, Field


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