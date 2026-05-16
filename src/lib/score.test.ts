import { describe, it, expect, vi, beforeEach } from "vitest";

const mockCreate = vi.hoisted(() => vi.fn());

vi.mock("@anthropic-ai/sdk", () => ({
  default: class MockAnthropic {
    messages = { create: mockCreate };
    constructor(_opts: unknown) {}
  },
}));

vi.mock("@trigger.dev/sdk/v3", () => ({
  logger: { log: vi.fn(), error: vi.fn() },
}));

import { extractAndScore } from "./score";
import type { RawLead } from "./types";

const raw: RawLead = {
  url: "https://testhr.ae",
  content: "We are an HR consulting firm in Dubai.",
  search_query: "HR consulting Dubai",
};

describe("extractAndScore", () => {
  beforeEach(() => {
    process.env.ANTHROPIC_API_KEY = "test-key";
    mockCreate.mockReset();
  });

  it("returns a ScoredLead when Claude returns valid JSON", async () => {
    mockCreate.mockResolvedValue({
      content: [{
        type: "text",
        text: JSON.stringify({
          company_name: "Test HR Co",
          email: "contact@testhr.ae",
          phone: "+971 4 111 2222",
          description: "HR consulting in Dubai",
          location: "Dubai, UAE",
          services: "HR outsourcing, Recruitment",
          score: 8,
          score_reason: "Dubai-based, has email and phone",
        }),
      }],
    });

    const result = await extractAndScore(raw);

    expect(result).not.toBeNull();
    expect(result!.company_name).toBe("Test HR Co");
    expect(result!.score).toBe(8);
    expect(result!.website).toBe("https://testhr.ae");
    expect(result!.source_url).toBe("https://testhr.ae");
    expect(result!.scraped_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it("returns null when Claude returns invalid JSON", async () => {
    mockCreate.mockResolvedValue({
      content: [{ type: "text", text: "No data available." }],
    });
    const result = await extractAndScore(raw);
    expect(result).toBeNull();
  });

  it("returns null when the API call throws", async () => {
    mockCreate.mockRejectedValue(new Error("API error"));
    const result = await extractAndScore(raw);
    expect(result).toBeNull();
  });
});
