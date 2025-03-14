from datetime import datetime

from agents import Agent

from .history import history_agent
from .todos import todo_agent

instructions = f"""
You determine which agent to use based on the user's question

Current Date: {datetime.now().isoformat()}
"""

supervisor_agent = Agent(
    model="gpt-4o",
    name="Supervisor Agent",
    instructions=instructions,
    handoffs=[history_agent, todo_agent],
)
