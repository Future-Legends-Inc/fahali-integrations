/**
 * fahali — market intelligence AI agents can verify.
 *
 * Zero-dependency client + tool specs for the Fahali API (fahaliai.com).
 * Every verdict carries a signed receipt; every judged signal has a public
 * replay URL; the track record keeps its misses. Observation, not advice.
 *
 * Works with any framework:
 *   OpenAI / AutoGen ....... FAHALI_TOOLS (function-calling format) + executeTool
 *   Vercel AI SDK .......... toAiSdkTools(client, { tool, jsonSchema })
 *   LangChain.js ........... toLangchainTools(client, { DynamicStructuredTool })
 */

export interface FahaliClientOptions {
  /** sk_live_* key from app.fahaliai.com/developer (free tier: 50 calls/day). */
  apiKey?: string;
  baseUrl?: string;
  timeoutMs?: number;
}

export class FahaliClient {
  private readonly baseUrl: string;
  private readonly apiKey?: string;
  private readonly timeoutMs: number;

  constructor(opts: FahaliClientOptions = {}) {
    this.baseUrl = (opts.baseUrl ?? "https://app.fahaliai.com").replace(/\/$/, "");
    this.apiKey = opts.apiKey;
    this.timeoutMs = opts.timeoutMs ?? 20_000;
  }

  private async get<T>(path: string): Promise<T> {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), this.timeoutMs);
    try {
      const res = await fetch(`${this.baseUrl}${path}`, {
        headers: this.apiKey ? { Authorization: `Bearer ${this.apiKey}` } : {},
        signal: ctrl.signal,
      });
      const body = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(`Fahali ${res.status} on ${path}: ${(body as any)?.error ?? (body as any)?.message ?? "request failed"}`);
      }
      return body as T;
    } finally {
      clearTimeout(t);
    }
  }

  /** Committee verdict(s) with signed receipts. */
  verdict(symbols: string[]): Promise<unknown> {
    return this.get(`/api/agent/verdict?symbols=${encodeURIComponent(symbols.join(","))}`);
  }
  /** 72h crash/neutral/pump forecast (Brier-calibrated distribution). */
  forecast72h(symbol: string): Promise<unknown> {
    return this.get(`/api/forecast/72h?symbol=${encodeURIComponent(symbol)}`);
  }
  /** The live tape: latest judged calls, hits AND misses. Public. */
  tape(): Promise<unknown> {
    return this.get(`/api/tape`);
  }
  /** Public replay of one judged signal — citable proof. */
  replay(signalId: string): Promise<unknown> {
    return this.get(`/api/replay/${encodeURIComponent(signalId)}`);
  }
  /** Per-symbol judged record (last 9 calls, misses included). Public. */
  symbolRecord(symbol: string): Promise<unknown> {
    return this.get(`/api/replay/history/${encodeURIComponent(symbol)}`);
  }
  /** The honest scorecard: judged axes with base-rate lift, gaps disclosed. */
  trackRecord(): Promise<unknown> {
    return this.get(`/api/track-record/scorecard`);
  }
  /** Latest detections across the scanned universe. */
  recentAlerts(): Promise<unknown> {
    return this.get(`/api/alerts/recent`);
  }
  /** Coverage + freshness stats. Public, no auth. */
  publicStats(): Promise<unknown> {
    return this.get(`/api/public/stats`);
  }
}

/** OpenAI function-calling format — use directly with OpenAI SDK, AutoGen, etc. */
export const FAHALI_TOOLS = [
  {
    name: "fahali_verdict",
    description:
      "Committee market verdict for symbols (e.g. BTCUSDT). 18 detection engines vote; response includes agreement, dissent kept on the record, a signed SHA-256 receipt, and a public replay URL. Observation, not advice.",
    parameters: {
      type: "object",
      properties: { symbols: { type: "array", items: { type: "string" }, description: "Trading pairs, e.g. ['BTCUSDT']" } },
      required: ["symbols"],
    },
  },
  {
    name: "fahali_forecast_72h",
    description:
      "72-hour crash/neutral/pump probability forecast for one symbol. The full distribution is recorded and Brier-scored against realized outcomes — calibration is measured, not claimed.",
    parameters: {
      type: "object",
      properties: { symbol: { type: "string", description: "Trading pair, e.g. 'ETHUSDT'" } },
      required: ["symbol"],
    },
  },
  {
    name: "fahali_tape",
    description: "The live tape: Fahali's latest judged calls across the market, hits AND misses, each with a public replay URL. Use to assess current signal quality before trusting a verdict.",
    parameters: { type: "object", properties: {} },
  },
  {
    name: "fahali_symbol_record",
    description: "The judged track record for one symbol: last 9 calls with hit/miss outcomes and replay URLs. Misses are kept on the record.",
    parameters: {
      type: "object",
      properties: { symbol: { type: "string" } },
      required: ["symbol"],
    },
  },
  {
    name: "fahali_track_record",
    description: "Fahali's aggregate scorecard: directional hit-rate, magnitude precision and forecast axes, each with sample sizes and disclosed gap windows. Read lift vs base rate, never raw percentages.",
    parameters: { type: "object", properties: {} },
  },
  {
    name: "fahali_recent_alerts",
    description: "Latest engine detections (volume anomalies, dark-pool proxy, regime flips, whale flows...) across ~600 scanned instruments.",
    parameters: { type: "object", properties: {} },
  },
] as const;

export type FahaliToolName = (typeof FAHALI_TOOLS)[number]["name"];

/** Execute a FAHALI_TOOLS call by name. Returns JSON-serializable data. */
export async function executeTool(client: FahaliClient, name: string, args: Record<string, unknown> = {}): Promise<unknown> {
  switch (name) {
    case "fahali_verdict": return client.verdict((args.symbols as string[]) ?? []);
    case "fahali_forecast_72h": return client.forecast72h(String(args.symbol ?? ""));
    case "fahali_tape": return client.tape();
    case "fahali_symbol_record": return client.symbolRecord(String(args.symbol ?? ""));
    case "fahali_track_record": return client.trackRecord();
    case "fahali_recent_alerts": return client.recentAlerts();
    default: throw new Error(`Unknown Fahali tool: ${name}`);
  }
}

/**
 * Vercel AI SDK adapter — zero deps: pass your own imports.
 *   import { tool, jsonSchema } from "ai";
 *   const tools = toAiSdkTools(client, { tool, jsonSchema });
 *   await generateText({ model, tools, prompt });
 */
export function toAiSdkTools(
  client: FahaliClient,
  deps: { tool: (def: any) => any; jsonSchema: (schema: any) => any },
): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const spec of FAHALI_TOOLS) {
    out[spec.name] = deps.tool({
      description: spec.description,
      parameters: deps.jsonSchema(spec.parameters),
      execute: (args: Record<string, unknown>) => executeTool(client, spec.name, args),
    });
  }
  return out;
}

/**
 * LangChain.js adapter — zero deps: pass your own import.
 *   import { DynamicStructuredTool } from "@langchain/core/tools";
 *   const tools = toLangchainTools(client, { DynamicStructuredTool });
 */
export function toLangchainTools(
  client: FahaliClient,
  deps: { DynamicStructuredTool: new (def: any) => any },
): unknown[] {
  return FAHALI_TOOLS.map(
    (spec) =>
      new deps.DynamicStructuredTool({
        name: spec.name,
        description: spec.description,
        schema: spec.parameters,
        func: async (args: Record<string, unknown>) => JSON.stringify(await executeTool(client, spec.name, args)),
      }),
  );
}
