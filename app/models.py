from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: str = Field(title="Unique identifier of the todo task")
    title: str = Field(title="Title of the todo task")
    completed: bool = Field(title="Indicates if the todo is completed")
