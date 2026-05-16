import { describe, it, expect, vi, beforeEach } from "vitest";

const mockAppend = vi.hoisted(() => vi.fn());
const mockSetCredentials = vi.hoisted(() => vi.fn());

vi.mock("googleapis", () => ({
  google: {
    auth: {
      OAuth2: class {
        setCredentials = mockSetCredentials;
        constructor(..._args: unknown[]) {}
      },
    },
    sheets: vi.fn(() => ({
      spreadsheets: {
        values: { append: mockAppend },
      },
    })),
  },
}));

vi.mock("@trigger.dev/sdk/v3", () => ({
  logger: { log: vi.fn(), error: vi.fn() },
}));

import { appendLeads } from "./sheets";
import type { ScoredLead } from "./types";

const makeLead = (): ScoredLead => ({
  company_name: "Test HR",
  website: "https://testhr.ae",
  email: "info@testhr.ae",
  phone: "+971 4 000 0000",
  description: "HR firm in Dubai",
  location: "Dubai, UAE",
  services: "Recruitment",
  score: 7,
  score_reason: "Dubai + email",
  source_url: "https://testhr.ae",
  scraped_at: new Date().toISOString(),
});

describe("appendLeads", () => {
  beforeEach(() => {
    process.env.GOOGLE_SHEET_ID = "sheet-id";
    process.env.GOOGLE_CLIENT_ID = "test-client-id";
    process.env.GOOGLE_CLIENT_SECRET = "test-client-secret";
    process.env.GOOGLE_REFRESH_TOKEN = "test-refresh-token";
    mockAppend.mockReset();
    mockSetCredentials.mockReset();
    mockAppend.mockResolvedValue({ data: {} });
  });

  it("appends one row per lead", async () => {
    await appendLeads([makeLead(), makeLead()]);
    expect(mockAppend).toHaveBeenCalledTimes(2);
  });

  it("passes values in the correct column order", async () => {
    const lead = makeLead();
    await appendLeads([lead]);
    const call = mockAppend.mock.calls[0][0];
    expect(call.requestBody.values[0]).toEqual([
      lead.company_name,
      lead.website,
      lead.email,
      lead.phone,
      lead.description,
      lead.location,
      lead.services,
      lead.score,
      lead.score_reason,
      lead.source_url,
      lead.scraped_at,
    ]);
  });

  it("continues if one append fails", async () => {
    mockAppend
      .mockRejectedValueOnce(new Error("quota exceeded"))
      .mockResolvedValueOnce({ data: {} });
    await expect(appendLeads([makeLead(), makeLead()])).resolves.not.toThrow();
    expect(mockAppend).toHaveBeenCalledTimes(2);
  });
});
