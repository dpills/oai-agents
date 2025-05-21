from agents import Agent

history_agent = Agent(
    model="gpt-4.1",
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions=(
        "You provide assistance with historical queries. "
        "Explain important events and context clearly."
    ),
)
