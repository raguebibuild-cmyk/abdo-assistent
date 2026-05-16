import { describe, it, expect, vi, beforeEach } from "vitest";

const mockSearch = vi.hoisted(() => vi.fn());

vi.mock("@mendable/firecrawl-js", () => ({
  Firecrawl: class MockFirecrawl {
    search = mockSearch;
    constructor(_opts: unknown) {}
  },
}));

vi.mock("@trigger.dev/sdk/v3", () => ({
  logger: { log: vi.fn(), error: vi.fn() },
}));

import { gatherLeads } from "./firecrawl";

describe("gatherLeads", () => {
  beforeEach(() => {
    process.env.FIRECRAWL_API_KEY = "test-key";
    mockSearch.mockReset();
  });

  it("returns leads from all search queries", async () => {
    mockSearch.mockResolvedValue({
      web: [
        { url: "https://hr1.ae", markdown: "HR consulting in Dubai" },
        { url: "https://hr2.ae", markdown: "HR services UAE" },
      ],
    });
    const leads = await gatherLeads();
    expect(leads.length).toBe(6); // 3 queries × 2 results each
    expect(leads[0].url).toBe("https://hr1.ae");
  });

  it("skips results missing url or markdown", async () => {
    mockSearch.mockResolvedValue({
      web: [
        { url: "https://hr1.ae", markdown: "good" },
        { url: "", markdown: "no url" },
        { url: "https://hr2.ae", markdown: "" },
      ],
    });
    const leads = await gatherLeads();
    expect(leads.length).toBe(3); // 1 valid per query × 3 queries
  });

  it("continues if a search query throws", async () => {
    mockSearch
      .mockRejectedValueOnce(new Error("rate limit"))
      .mockResolvedValue({
        web: [{ url: "https://hr.ae", markdown: "content" }],
      });
    const leads = await gatherLeads();
    expect(leads.length).toBe(2); // 2 remaining queries × 1 result each
  });
});
