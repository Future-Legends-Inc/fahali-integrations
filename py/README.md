# fahali

**Market intelligence AI agents can verify.** Every verdict carries a signed SHA-256 receipt. Every judged signal has a public replay URL. The track record keeps its misses and publishes its methodology. Forecast probabilities are Brier-scored against realized outcomes.

Zero dependencies. Works with any agent framework. *Observation, not advice.*

```bash
pip install fahali    # Python
npm install fahali    # JS/TS
```

Free key (50 calls/day, no card): [app.fahaliai.com/developer](https://app.fahaliai.com/developer) · Docs: [fahaliai.com/developer](https://fahaliai.com/developer) · MCP: `https://mcp.fahaliai.com/mcp`

## Direct

```ts
import { FahaliClient } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY });
const verdict = await fahali.verdict(["BTCUSDT"]);   // committee read + signed receipt
const record  = await fahali.symbolRecord("BTCUSDT"); // judged record, misses included
```

## OpenAI (and anything using function-calling format)

```ts
import { FahaliClient, FAHALI_TOOLS, executeTool } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY });
const tools = FAHALI_TOOLS.map((t) => ({ type: "function", function: t }));
// ...pass `tools` to chat.completions.create; on a tool call:
const result = await executeTool(fahali, call.function.name, JSON.parse(call.function.arguments));
```

## LangChain (Python)

```python
from fahali import FahaliClient
from fahali.langchain import get_langchain_tools
tools = get_langchain_tools(FahaliClient(api_key=...))
```

## CrewAI

```python
from fahali.crewai import get_crewai_tools
```

## LlamaIndex

```python
from fahali.llamaindex import get_llamaindex_tools
```

## AutoGen / smolagents / Semantic Kernel / raw OpenAI

```python
from fahali import FahaliClient, TOOL_SPECS, execute_tool  # function-calling format
```

## Vercel AI SDK

```ts
import { tool, jsonSchema, generateText } from "ai";
import { FahaliClient, toAiSdkTools } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY });
const { text } = await generateText({
  model,
  tools: toAiSdkTools(fahali, { tool, jsonSchema }),
  prompt: "Is anything threatening a BTC-heavy portfolio right now? Cite replays.",
});
```

## LangChain.js

```ts
import { DynamicStructuredTool } from "@langchain/core/tools";
import { FahaliClient, toLangchainTools } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY });
const tools = toLangchainTools(fahali, { DynamicStructuredTool });
```

## Tools

| Tool | What your agent gets |
|---|---|
| `fahali_verdict` | 18-engine committee read: agreement, dissent on the record, signed receipt, replay URL |
| `fahali_forecast_72h` | Crash/neutral/pump distribution, Brier-calibrated |
| `fahali_tape` | Latest judged calls market-wide: hits **and misses** |
| `fahali_symbol_record` | Per-symbol judged record with replay URLs |
| `fahali_track_record` | Aggregate scorecard: lift vs base rate, sample sizes, disclosed gaps |
| `fahali_recent_alerts` | Live detections across covered crypto and US equities |

## Why this instead of a terminal or search

Terminals were built for human eyes; search gives agents unaccountable text. Fahali's answers are **claims your agent can check**: methodology at [fahaliai.com/methodology](https://fahaliai.com/methodology), pricing free → metered at [fahaliai.com/developer](https://fahaliai.com/developer).

MIT © Future Legends AI. Nothing here is a recommendation to buy or sell anything.
