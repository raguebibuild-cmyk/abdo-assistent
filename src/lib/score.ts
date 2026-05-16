import Anthropic from "@anthropic-ai/sdk";
import { logger } from "@trigger.dev/sdk/v3";
import type { RawLead, ScoredLead } from "./types";

function buildPrompt(url: string, content: string): string {
  return `You are extracting structured data about a business from a webpage.

URL: ${url}

Webpage content:
${content}

Extract the following as a JSON object. Use "" for any field you cannot determine — do not guess or invent data.

{
  "company_name": "",
  "email": "",
  "phone": "",
  "description": "",
  "location": "",
  "services": "",
  "score": 0,
  "score_reason": ""
}

Score this lead 1–10 for relevance as a potential client for an agentic workflows consultancy targeting SMEs:
- Located in Dubai or UAE: +3
- Offers HR consulting or related services: +2
- Has a contact email: +2
- Has a phone number: +1
- Appears to be an SME (not a large multinational): +1
- Has a professional, active web presence: +1

Return ONLY the JSON object. No markdown, no explanation.`;
}

export async function extractAndScore(raw: RawLead): Promise<ScoredLead | null> {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY! });
  try {
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 512,
      messages: [{ role: "user", content: buildPrompt(raw.url, raw.content) }],
    });

    const textBlock = response.content.find((b) => b.type === "text");
    const text = textBlock?.type === "text" ? textBlock.text : "";

    let parsed: Record<string, unknown>;
    try {
      parsed = JSON.parse(text);
    } catch {
      logger.error("Claude returned non-JSON", { url: raw.url, text });
      return null;
    }

    logger.log("Lead scored", { url: raw.url, score: parsed.score });

    return {
      company_name: String(parsed.company_name ?? ""),
      website: raw.url,
      email: String(parsed.email ?? ""),
      phone: String(parsed.phone ?? ""),
      description: String(parsed.description ?? ""),
      location: String(parsed.location ?? ""),
      services: String(parsed.services ?? ""),
      score: Number(parsed.score ?? 0),
      score_reason: String(parsed.score_reason ?? ""),
      source_url: raw.url,
      scraped_at: new Date().toISOString(),
    };
  } catch (err) {
    logger.error("Scoring failed", { url: raw.url, error: String(err) });
    return null;
  }
}
