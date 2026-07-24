"""fahali — market intelligence AI agents can verify.

Signed receipts on every verdict, a judged track record that keeps its
misses, Brier-calibrated forecasts, public replays. Observation, not advice.

Free key (50 calls/day): https://app.fahaliai.com/developer
Adapters: fahali.langchain, fahali.crewai, fahali.llamaindex — plus
TOOL_SPECS (OpenAI function-calling format) for AutoGen, smolagents,
Semantic Kernel, or anything else.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any, Optional

__version__ = "0.1.2"
DEFAULT_BASE_URL = "https://app.fahaliai.com"


class FahaliError(RuntimeError):
    pass


class FahaliClient:
    """Minimal, dependency-free client for the Fahali API."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL, timeout: float = 20.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str) -> Any:
        req = urllib.request.Request(self.base_url + path)
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:300]
            raise FahaliError(f"Fahali {e.code} on {path}: {body}") from None

    def verdict(self, symbols: list[str]) -> Any:
        """Committee verdict(s) with signed receipts."""
        return self._get(f"/api/agent/verdict?symbols={','.join(symbols)}")

    def forecast_72h(self, symbol: str) -> Any:
        """72h crash/neutral/pump forecast (Brier-calibrated distribution)."""
        return self._get(f"/api/forecast/72h?symbol={symbol}")

    def tape(self) -> Any:
        """Latest judged calls market-wide: hits AND misses. Public."""
        return self._get("/api/tape")

    def replay(self, signal_id: str) -> Any:
        """Public replay of one judged signal, citable proof."""
        return self._get(f"/api/replay/{signal_id}")

    def symbol_record(self, symbol: str) -> Any:
        """Per-symbol judged record (last 9 calls, misses included). Public."""
        return self._get(f"/api/replay/history/{symbol}")

    def track_record(self) -> Any:
        """Aggregate scorecard: lift vs base rates, samples, disclosed gaps."""
        return self._get("/api/track-record/scorecard")

    def recent_alerts(self) -> Any:
        """Latest detections across the scanned universe."""
        return self._get("/api/alerts/recent")

    def public_stats(self) -> Any:
        """Coverage + freshness. Public, no auth."""
        return self._get("/api/public/stats")


# OpenAI function-calling format — AutoGen, Semantic Kernel, raw OpenAI, etc.
TOOL_SPECS: list[dict[str, Any]] = [
    {
        "name": "fahali_verdict",
        "description": "Committee market verdict for symbols (e.g. BTCUSDT): the engine committee's agreement and dissent kept on the record, with a signed SHA-256 receipt and a public replay URL. Observation, not advice.",
        "parameters": {"type": "object", "properties": {"symbols": {"type": "array", "items": {"type": "string"}}}, "required": ["symbols"]},
    },
    {
        "name": "fahali_forecast_72h",
        "description": "72-hour crash/neutral/pump probability forecast for one symbol; the distribution is Brier-scored against realized outcomes.",
        "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]},
    },
    {
        "name": "fahali_tape",
        "description": "The live tape: latest judged calls across the market, hits AND misses, each with a public replay URL.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "fahali_symbol_record",
        "description": "Judged track record for one symbol: last 9 calls with hit/miss outcomes and replay URLs.",
        "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]},
    },
    {
        "name": "fahali_track_record",
        "description": "Aggregate scorecard: directional/magnitude/forecast axes with sample sizes and disclosed gap windows. Read lift vs base rate, never raw percentages.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "fahali_recent_alerts",
        "description": "Latest engine detections (volume anomalies, dark-pool proxy, regime flips, funding stress) across covered crypto and US equities.",
        "parameters": {"type": "object", "properties": {}},
    },
]


def execute_tool(client: FahaliClient, name: str, args: Optional[dict[str, Any]] = None) -> Any:
    """Execute a TOOL_SPECS call by name."""
    a = args or {}
    if name == "fahali_verdict":
        return client.verdict(list(a.get("symbols") or []))
    if name == "fahali_forecast_72h":
        return client.forecast_72h(str(a.get("symbol", "")))
    if name == "fahali_tape":
        return client.tape()
    if name == "fahali_symbol_record":
        return client.symbol_record(str(a.get("symbol", "")))
    if name == "fahali_track_record":
        return client.track_record()
    if name == "fahali_recent_alerts":
        return client.recent_alerts()
    raise FahaliError(f"Unknown Fahali tool: {name}")
