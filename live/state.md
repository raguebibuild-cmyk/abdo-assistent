# Session State

*Updated at the end of each session. Read this FIRST on startup.*

## Last Session
- **Date:** 2026-05-22
- **Summary:** Built branded invoice PDF generator (`equipment/invoice_pdf.py`). Added PAID watermark, Item/Qty/Unit Price/Amount table, Status field. Added PDF generation step to invoice and quote blueprints. Updated templates/invoice.md. Committed as `679b38e`.

## Lead Gen Build — Ready to Deploy
**Plan file:** `C:\Users\admin\.claude\plans\i-want-to-build-compiled-marshmallow.md`
**Branch:** main

| Task | Status |
|------|--------|
| 1. Install deps + env setup | ✅ Done |
| 2. OAuth helper script (`scripts/get-refresh-token.ts`) | ✅ Done |
| 3. Shared types (`src/lib/types.ts`) | ✅ Done |
| 4. Firecrawl wrapper (`src/lib/firecrawl.ts` + tests) | ✅ Done |
| 5. Claude scoring (`src/lib/score.ts` + tests) | ✅ Done — 3/3 tests pass |
| 6. Google Sheets writer (`src/lib/sheets.ts` + tests) | ✅ Done — 3/3 tests pass |
| 7. Scheduled task (`src/trigger/lead-gen-dubai-hr.ts`) | ✅ Done — all 9 tests pass, TSC clean |
| 8. Deploy + configure schedule | ⏳ Manual — steps below |

**To complete Task 8:**
1. Add 6 env vars to cloud.trigger.dev dashboard: `FIRECRAWL_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GOOGLE_SHEET_ID`
2. `npm run deploy`
3. Dashboard → Tasks → `lead-gen-dubai-hr` → Schedules → cron `0 6 * * *`, timezone UTC
4. Manual test run → confirm rows appear in Google Sheet `Leads` tab

## Pending — Google Sheets ADC Switch
- gcloud CLI installed at `C:\Users\admin\AppData\Local\Google\Cloud SDK\`
- `gcloud auth application-default login --scopes=...` was started but browser auth not completed
- **sheets.ts still uses OAuth2 refresh token** — ADC update pending
- To resume: run `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/cloud-platform` in a new terminal, complete browser auth, then update `sheets.ts` to use `google.auth.GoogleAuth`

## This Session — What Changed
- Rewrote `blueprints/social-media-repurposing.md`: now standalone (no Blueprint 1 dependency), accepts any content input, updated word limits (Instagram 150, LinkedIn 250, Facebook 200), emojis on Instagram, output to `social-media/`
- Updated `equipment/social_media_pdf.py`: added `PageBreak` between platform sections — each platform now renders on its own page
- Created `social-media/` output folder
- First run: weight loss topic → `social-media/social-2026-05-22.pdf` (3 pages, branded)

## Open Tasks
- Reply to Sami — Cedar Wealth Advisory **[OVERDUE]**
- Reply to Karim — DeltaLogix **[OVERDUE]**
- Reply to Reem — Hala Ventures **[OVERDUE]**
- Reply to Construction firm Casablanca **[OVERDUE]**
- Reply to Nadia — Kontrast Personalberatung **[OVERDUE]**
- Reply to CRM quote — laboratoiremvcd@gmail.com **[OVERDUE]**
- Reply to CRM quote — biovagoabdorag@gmail.com **[OVERDUE]**
- Deliver audit — Najim Travel **[OVERDUE]**
- Deliver audit — Cotton & Stitch **[OVERDUE]**
- Follow up — Foster & Marsh Legal ($12k quote)
- Follow up — Zayd Property ($6.5k quote)
- Complete Google Sheets ADC auth (gcloud browser step)
- Deploy lead gen task to Trigger.dev (Task 8)

## Current Priorities
1. Finding clients
2. Building visual presence (website / landing page)
3. Working out pricing

## Active Projects
| Project | Status | Deadline |
|---------|--------|----------|
| HR Consultant Automation | Ready to deploy | — |
| degiabdo Launch | Active | 2026-05-15 (overdue) |

## Skills Built
| Skill | Blueprint | Equipment |
|-------|-----------|-----------|
| Client communication handler | blueprints/client-communication.md | None |
| Client proposition | blueprints/client-proposition.md | None (Google Drive + Gmail MCP) |
| Monday pipeline summary | blueprints/monday-morning-pipeline.md | equipment/pipeline_summary.py |
| Lead update + follow-up email | blueprints/lead-update-followup.md | None (Google Drive + Gmail MCP) |
| Client proposal document | blueprints/client-proposal-document.md | None (Google Drive MCP — reads 3 sources, creates Doc) |
| Research Subagent | blueprints/research-subagent.md | None (WebSearch + pdf skill + customer-research skill + Drive/Gmail MCPs) |
| Trend research & analysis | blueprints/trend-research-analysis.md | equipment/trend_report_pdf.py |
| Social media repurposing | blueprints/social-media-repurposing.md | equipment/social_media_pdf.py |
| Client onboarding | blueprints/client-onboarding.md | None (Google Drive + Gmail + Zapier Sheets MCP) |
| Invoice creation | blueprints/invoice-creation.md | equipment/invoice_pdf.py + Drive/Gmail MCP |
| Quote generation | blueprints/quote-generation.md | equipment/md_to_pdf.py + Drive/Gmail MCP |
| Morning briefing | blueprints/morning-briefing.md | None (Google Calendar + Gmail + Drive MCP) |
| Weekly pipeline review | blueprints/weekly-pipeline-review.md | None (Gmail MCP — runs Mondays 08:30 GMT+1) |
| LinkedIn content batch | blueprints/linkedin-content-batch.md | None (WebSearch — runs Wednesdays 09:00 GMT+1) |
| Monthly business health report | blueprints/monthly-health-report.md | equipment/health_report_pdf.py + Drive MCP (runs 1st of month 09:00 GMT+1) |
