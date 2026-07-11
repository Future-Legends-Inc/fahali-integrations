"""LlamaIndex adapter: `pip install fahali llama-index-core`."""
from __future__ import annotations
from . import FahaliClient, TOOL_SPECS, execute_tool


def get_llamaindex_tools(client: FahaliClient) -> list:
    """FunctionTool list for LlamaIndex agents."""
    import json
    from llama_index.core.tools import FunctionTool  # lazy

    tools = []
    for spec in TOOL_SPECS:
        def _make(name: str):
            def _run(**kwargs) -> str:
                return json.dumps(execute_tool(client, name, kwargs))
            _run.__name__ = name
            return _run
        tools.append(FunctionTool.from_defaults(fn=_make(spec["name"]), name=spec["name"], description=spec["description"]))
    return tools
