from datetime import datetime
from typing import Optional

import bson
from agents import function_tool

from app.clients import db

from .models import Todo


@function_tool
async def get_todos() -> list[Todo]:
    """
    Get todos
    """
    todos: list[Todo] = []
    async for item in db.todos.find():
        todos.append(
            Todo(
                id=str(item["_id"]),
                title=item["title"],
                completed=item["completed"],
                due_date=item.get("due_date"),
            )
        )

    return todos


@function_tool
async def add_todo(
    title: str,
    due_date_str: Optional[str] = None,
) -> str:
    """
    Add a new todo item

    Args:
        title: Title of the todo
        due_date_str: An iso formatted datetime string. Example: 2024-12-03T16:32:15.085639+00:00
    """  # noqa: E501
    due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
    res = await db.todos.insert_one(
        {"title": title, "due_date": due_date, "completed": False}
    )

    return f"Todo created with id {res.inserted_id}"


@function_tool
async def update_todo(
    todo_id: str,
    title: Optional[str] = None,
    completed: Optional[bool] = None,
    due_date_str: Optional[str] = None,
) -> str:
    """
    Update a todo

    Args:
        title: Title of the todo
        todo_id: The id of the todo
        completed: If the todo has been completed
        due_date_str: An iso formatted datetime string. Example: 2024-12-03T16:32:15.085639+00:00
    """  # noqa: E501

    update_data: dict[str, str | bool | datetime] = {}
    if completed is not None:
        update_data["completed"] = completed

    if due_date_str:
        update_data["due_date"] = datetime.fromisoformat(due_date_str)

    if title:
        update_data["title"] = title

    res = await db.todos.update_one(
        {"_id": bson.ObjectId(todo_id)}, {"$set": update_data}
    )

    if res.matched_count == 0:
        return "Todo not found"

    return "Todo updated"


@function_tool
async def delete_todo(todo_id: str) -> str:
    """
    Delete a todo

    Args:
        todo_id: The id of the todo
    """
    res = await db.todos.delete_one({"_id": bson.ObjectId(todo_id)})

    if res.deleted_count == 0:
        return "Todo not found"

    return "Todo deleted"
