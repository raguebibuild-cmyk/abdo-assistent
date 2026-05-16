import { google } from "googleapis";
import { logger } from "@trigger.dev/sdk/v3";
import type { ScoredLead } from "./types";

export async function appendLeads(leads: ScoredLead[]): Promise<void> {
  const auth = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID!,
    process.env.GOOGLE_CLIENT_SECRET!,
  );
  auth.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN! });
  const sheets = google.sheets({ version: "v4", auth });

  for (const lead of leads) {
    try {
      await sheets.spreadsheets.values.append({
        spreadsheetId: process.env.GOOGLE_SHEET_ID!,
        range: "Leads!A:K",
        valueInputOption: "USER_ENTERED",
        requestBody: {
          values: [[
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
          ]],
        },
      });
      logger.log("Lead written to sheet", { company: lead.company_name, score: lead.score });
    } catch (err) {
      logger.error("Sheet write failed", { company: lead.company_name, error: String(err) });
    }
  }
}
