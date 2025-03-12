from agents import Agent

from .tools import todo_tools

handoff_description = """\
Specialist agent for creating, updating, deleting and getting todo tasks"
"""

instructions = """\
You help users manage their todos tasks.
"""

todo_agent = Agent(
    model="gpt-4o",
    name="Todo manager",
    handoff_description=handoff_description,
    instructions=instructions,
    tools=todo_tools,
)
