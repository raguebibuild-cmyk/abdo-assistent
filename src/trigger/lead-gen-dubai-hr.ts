import { logger, schedules } from "@trigger.dev/sdk/v3";
import { gatherLeads } from "../lib/firecrawl";
import { extractAndScore } from "../lib/score";
import { appendLeads } from "../lib/sheets";

const MIN_SCORE = 5;

export const leadGenDubaiHR = schedules.task({
  id: "lead-gen-dubai-hr",
  maxDuration: 600,
  run: async (payload) => {
    logger.log("Lead gen started", { scheduledAt: payload.timestamp });

    const rawLeads = await gatherLeads();
    logger.log("Raw leads gathered", { count: rawLeads.length });

    if (rawLeads.length === 0) {
      logger.log("No raw leads — task complete");
      return { raw: 0, scored: 0, qualified: 0 };
    }

    const scored = [];
    for (const raw of rawLeads) {
      const result = await extractAndScore(raw);
      if (result) scored.push(result);
    }
    logger.log("Leads scored", { total: rawLeads.length, scored: scored.length });

    const qualified = scored.filter((l) => l.score >= MIN_SCORE);
    logger.log("Qualified leads", { count: qualified.length, minScore: MIN_SCORE });

    if (qualified.length > 0) {
      await appendLeads(qualified);
    }

    logger.log("Lead gen complete", {
      raw: rawLeads.length,
      scored: scored.length,
      qualified: qualified.length,
    });

    return { raw: rawLeads.length, scored: scored.length, qualified: qualified.length };
  },
});
