from datetime import datetime

from agents import Agent

from .tools import todo_tools

instructions = f"""
You help users manage their todos tasks.

Current Date: {datetime.now().isoformat()}
"""

todo_agent = Agent(
    model="gpt-4.1",
    name="Todo manager",
    handoff_description="Specialist agent for creating, updating, deleting and getting todo tasks",  # noqa: E501
    instructions=instructions,
    tools=todo_tools,
)
