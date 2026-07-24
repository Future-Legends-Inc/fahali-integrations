"""
CrewAI risk-analyst agent backed by Fahali.

    pip install fahali crewai
    FAHALI_API_KEY=sk_live_... python crew.py
"""
import os

from fahali import FahaliClient
from fahali.crewai import get_crewai_tools

client = FahaliClient(api_key=os.environ["FAHALI_API_KEY"])
tools = get_crewai_tools(client)

print(f"{len(tools)} Fahali tools ready for CrewAI.")

# from crewai import Agent, Task, Crew
# risk_analyst = Agent(
#     role="Risk analyst",
#     goal="Flag positions where the structure under the price is turning",
#     backstory="You never claim certainty. You cite the read, its confidence, "
#               "and what data was missing.",
#     tools=tools,
# )
# Crew(agents=[risk_analyst], tasks=[Task(
#     description="Assess BTCUSDT and ETHUSDT for building downside risk.",
#     agent=risk_analyst, expected_output="A short risk note with citations.",
# )]).kickoff()
