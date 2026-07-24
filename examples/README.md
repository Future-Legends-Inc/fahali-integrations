# Fahali examples

Working examples, newest developer first. Every API call here is real — no
pseudo-code.

| Example | Needs a key? | What it shows |
|---|---|---|
| [`quickstart/`](quickstart) | **No** | Fahali's verified lead-time record in ~10 seconds. Start here. |
| [`pre-trade-risk-gate/`](pre-trade-risk-gate) | Yes (free) | The pattern most agents miss: check risk *before* opening a position |
| [`openai-agents/`](openai-agents) | Yes (free) | Raw OpenAI function calling — also AutoGen, smolagents, Semantic Kernel |
| [`langchain/`](langchain) | Yes (free) | LangChain / LangGraph `StructuredTool`s |
| [`crewai/`](crewai) | Yes (free) | A CrewAI risk-analyst agent |
| [`vercel-ai-sdk/`](vercel-ai-sdk) | Yes (free) | TypeScript, Vercel AI SDK tool calling |

Free key (50 calls/day, no card): https://app.fahaliai.com/developer

## The 10-second version

```bash
python quickstart/no_key_demo.py
```

Prints Fahali's real, outcome-scored warning record — how many hours ahead each
engine warned, its precision, and the base rate to judge that precision against.
Engines without enough resolved history are absent rather than guessed.

> **Observation, not advice.** Read-only: no order routing, no path to capital.
