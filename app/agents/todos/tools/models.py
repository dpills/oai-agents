from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Todo(BaseModel):
    id: str
    title: str
    completed: bool
    due_date: Optional[datetime] = None
