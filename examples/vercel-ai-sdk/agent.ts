/**
 * Vercel AI SDK agent with Fahali risk tools.
 *
 *   npm install fahali ai @ai-sdk/openai zod
 *   FAHALI_API_KEY=sk_live_... OPENAI_API_KEY=... npx tsx agent.ts
 */
import { openai } from "@ai-sdk/openai";
import { generateText, jsonSchema, tool } from "ai";
import { FahaliClient, toAiSdkTools } from "fahali";

const fahali = new FahaliClient({ apiKey: process.env.FAHALI_API_KEY! });

// The adapter takes the SDK primitives it needs, so it stays version-agnostic.
const tools = toAiSdkTools(fahali, { tool, jsonSchema });

const { text } = await generateText({
  model: openai("gpt-4o"),
  tools,
  maxSteps: 4,
  prompt:
    "Check BTCUSDT and NVDA for building risk. Quote the confidence and say " +
    "explicitly what data was missing. Do not give trading advice.",
});

console.log(text);
