from agents import ComputerTool, FileSearchTool, FunctionTool, WebSearchTool

from .tools import add_todo, delete_todo, get_todos, update_todo

todo_tools: list[FunctionTool | FileSearchTool | WebSearchTool | ComputerTool] = [
    add_todo,
    delete_todo,
    get_todos,
    update_todo,
]

__all__ = ("todo_tools",)
