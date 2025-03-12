from agents import Agent

from .history import history_agent
from .todos import todo_agent

supervisor_agent = Agent(
    model="gpt-4o",
    name="Supervisor Agent",
    instructions="You determine which agent to use based on the user's question",
    handoffs=[history_agent, todo_agent],
)
