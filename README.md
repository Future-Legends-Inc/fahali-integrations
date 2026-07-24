# Fahali SDKs and AI Agent Integrations

**Financial risk for AI agents — portfolio risk, crypto risk, contagion, crash
precursors and market verdicts, callable from Python or TypeScript.**

Your agent already fetches prices. Fahali tells it what those prices mean for
capital at risk — with the confidence, the missing inputs, and a signed receipt.

> **Observation, not advice.** Read-only: no order routing, no path to capital.

Official SDKs and framework adapters for [Fahali](https://fahaliai.com).
Looking for the MCP server instead? → [Future-Legends-Inc/fahali-mcp](https://github.com/Future-Legends-Inc/fahali-mcp)

---

## Install

```bash
pip install fahali
```

```bash
npm install fahali
```

Get a free API key (50 calls/day, no card) at
[app.fahaliai.com/developer](https://app.fahaliai.com/developer).

**Version note (honest):** the Python package is current (`0.1.2`). The npm
package is still at `0.1.1` and predates the latest wording pass — the API is the
same, the copy is older.

## Python

```python
from fahali import FahaliClient

client = FahaliClient(api_key="YOUR_API_KEY")

# A judged read on the symbols you care about
print(client.verdict(["BTCUSDT", "NVDA"]))

# The public, outcome-scored track record — hits AND misses
print(client.track_record())

# Coverage + freshness (no key required)
print(client.public_stats())
```

Every method above exists in the client; nothing here is illustrative.
Also available: `tape()`, `recent_alerts()`, `symbol_record(symbol)`,
`replay(signal_id)`.

### OpenAI function-calling / AutoGen / smolagents

```python
from fahali import FahaliClient, TOOL_SPECS, execute_tool

client = FahaliClient(api_key="YOUR_API_KEY")
# TOOL_SPECS is OpenAI function-calling format — hand it straight to the model,
# then dispatch whatever it calls:
result = execute_tool(client, "fahali_verdict", {"symbols": ["BTCUSDT"]})
```

### LangChain / CrewAI / LlamaIndex

```python
from fahali import FahaliClient
from fahali.langchain import get_langchain_tools
from fahali.crewai import get_crewai_tools
from fahali.llamaindex import get_llamaindex_tools

client = FahaliClient(api_key="YOUR_API_KEY")
tools = get_langchain_tools(client)   # or get_crewai_tools / get_llamaindex_tools
```

## TypeScript

```ts
import { FahaliClient, toAiSdkTools, toLangchainTools } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY });

// Vercel AI SDK
const tools = toAiSdkTools(fahali);

// LangChain JS
const lcTools = toLangchainTools(fahali);
```

## Why an agent uses Fahali instead of a price feed

- **Verified lead time** — per engine, the median hours ahead of the move on its
  correct material warnings, with the misses in the same record. Public, no key:
  `curl https://app.fahaliai.com/api/track-record/lead-time`
- **Signed receipts** — every verdict carries a SHA-256 receipt, so your agent can
  attach proof of what was said and when.
- **Honest absence** — missing data says so; quiet markets resolve as unresolved,
  never as wins. Tools with no data source abstain rather than invent a number.

## Repository layout

```
py/    Python SDK (published to PyPI as `fahali`)
js/    TypeScript SDK (published to npm as `fahali`)
```

## Links

- Developer docs: [fahaliai.com/developer](https://fahaliai.com/developer)
- MCP server: [Future-Legends-Inc/fahali-mcp](https://github.com/Future-Legends-Inc/fahali-mcp)
- Methodology (how signals are graded, misses included): [fahaliai.com/methodology](https://fahaliai.com/methodology)

Built by [Future Legends Inc](https://fahaliai.com). Observation, not advice.
