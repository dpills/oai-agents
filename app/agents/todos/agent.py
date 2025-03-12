from agents import Agent

from .tools import todo_tools

todo_agent = Agent(
    model="gpt-4o",
    name="Todo manager",
    handoff_description="Specialist agent for creating, updating, deleting and getting todo tasks",  # noqa: E501
    instructions="You help users manage their todos tasks.",
    tools=todo_tools,
)
