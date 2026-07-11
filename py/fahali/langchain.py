"""LangChain adapter: `pip install fahali langchain-core`."""
from __future__ import annotations
from typing import Any
from . import FahaliClient, TOOL_SPECS, execute_tool


def get_langchain_tools(client: FahaliClient) -> list:
    """StructuredTool list for LangChain / LangGraph agents."""
    from langchain_core.tools import StructuredTool  # lazy

    tools = []
    for spec in TOOL_SPECS:
        def _make(name: str):
            def _run(**kwargs: Any) -> str:
                import json
                return json.dumps(execute_tool(client, name, kwargs))
            return _run
        tools.append(StructuredTool.from_function(
            func=_make(spec["name"]), name=spec["name"],
            description=spec["description"], args_schema=None,
        ))
    return tools
