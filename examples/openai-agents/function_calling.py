"""
Raw OpenAI function calling (also works for AutoGen, smolagents, Semantic Kernel).

Fahali ships TOOL_SPECS in OpenAI function-calling format, so there is no adapter
to learn: hand the specs to the model, dispatch whatever it calls.

    pip install fahali openai
    FAHALI_API_KEY=sk_live_... OPENAI_API_KEY=... python function_calling.py
"""
import json
import os

from fahali import TOOL_SPECS, FahaliClient, execute_tool

client = FahaliClient(api_key=os.environ["FAHALI_API_KEY"])

print("Tools available to the model:")
for spec in TOOL_SPECS:
    print(f"  - {spec['name']}: {spec['description'][:70]}...")

# Dispatch a call the model asked for:
result = execute_tool(client, "fahali_verdict", {"symbols": ["BTCUSDT"]})
print("\nfahali_verdict(BTCUSDT) ->")
print(json.dumps(result, indent=2)[:600])

# With the OpenAI SDK:
#   from openai import OpenAI
#   msg = OpenAI().chat.completions.create(
#       model="gpt-4o",
#       messages=[{"role": "user", "content": "What is the risk on BTC right now?"}],
#       tools=[{"type": "function", "function": s} for s in TOOL_SPECS],
#   )
#   then: execute_tool(client, call.function.name, json.loads(call.function.arguments))
