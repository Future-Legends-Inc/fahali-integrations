"""CrewAI adapter: `pip install fahali crewai-tools`."""
from __future__ import annotations
from . import FahaliClient, execute_tool


def get_crewai_tools(client: FahaliClient) -> list:
    """BaseTool list for CrewAI agents."""
    import json
    from crewai.tools import tool  # lazy

    @tool("fahali_verdict")
    def fahali_verdict(symbols: str) -> str:
        """Committee market verdict for comma-separated symbols (e.g. 'BTCUSDT,ETHUSDT'). 18 engines vote; includes agreement, dissent on the record, a signed receipt and a public replay URL. Observation, not advice."""
        return json.dumps(execute_tool(client, "fahali_verdict", {"symbols": symbols.split(",")}))

    @tool("fahali_forecast_72h")
    def fahali_forecast_72h(symbol: str) -> str:
        """72-hour crash/neutral/pump probability forecast for one symbol, Brier-calibrated."""
        return json.dumps(execute_tool(client, "fahali_forecast_72h", {"symbol": symbol}))

    @tool("fahali_tape")
    def fahali_tape() -> str:
        """The live tape: latest judged calls, hits AND misses, with replay URLs."""
        return json.dumps(execute_tool(client, "fahali_tape"))

    @tool("fahali_symbol_record")
    def fahali_symbol_record(symbol: str) -> str:
        """Judged track record for one symbol - last 9 calls, misses included."""
        return json.dumps(execute_tool(client, "fahali_symbol_record", {"symbol": symbol}))

    @tool("fahali_track_record")
    def fahali_track_record() -> str:
        """Aggregate scorecard with sample sizes and disclosed gaps - read lift vs base rate."""
        return json.dumps(execute_tool(client, "fahali_track_record"))

    return [fahali_verdict, fahali_forecast_72h, fahali_tape, fahali_symbol_record, fahali_track_record]
