"""
LangChain / LangGraph agent with Fahali risk tools.

    pip install fahali langchain-core langchain-openai
    FAHALI_API_KEY=sk_live_... OPENAI_API_KEY=... python agent.py
"""
import os

from fahali import FahaliClient
from fahali.langchain import get_langchain_tools

client = FahaliClient(api_key=os.environ["FAHALI_API_KEY"])
tools = get_langchain_tools(client)  # StructuredTools built from Fahali's tool specs

print(f"Fahali exposed {len(tools)} tools to LangChain:")
for t in tools:
    print(f"  - {t.name}")

# Bind them to any tool-calling model:
#   from langchain_openai import ChatOpenAI
#   llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)
#   llm.invoke("Is there hidden downside risk in BTC and NVDA right now?")
#
# The agent gets a judged read with confidence and missing inputs — not raw prices
# it has to interpret on its own.
