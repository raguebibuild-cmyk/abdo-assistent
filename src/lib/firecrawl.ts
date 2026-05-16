import { Firecrawl } from "@mendable/firecrawl-js";
import { logger } from "@trigger.dev/sdk/v3";
import type { RawLead } from "./types";

const SEARCH_QUERIES = [
  "HR consulting firms Dubai",
  "human resources consultancy Dubai UAE",
  "HR outsourcing companies Dubai",
];

const CONTENT_LIMIT = 4000;

export async function gatherLeads(): Promise<RawLead[]> {
  const app = new Firecrawl({ apiKey: process.env.FIRECRAWL_API_KEY! });
  const leads: RawLead[] = [];

  for (const query of SEARCH_QUERIES) {
    logger.log("Firecrawl search", { query });
    try {
      const result = await app.search(query, {
        limit: 5,
        scrapeOptions: { formats: ["markdown"] },
      });
      for (const item of result.web ?? []) {
        const doc = item as { url?: string; markdown?: string };
        if (!doc.url || !doc.markdown) continue;
        leads.push({
          url: doc.url,
          content: doc.markdown.slice(0, CONTENT_LIMIT),
          search_query: query,
        });
      }
      logger.log("Search complete", { query, found: result.web?.length ?? 0 });
    } catch (err) {
      logger.error("Search failed", { query, error: String(err) });
    }
  }

  return leads;
}
