# Abdo Assistant — Executive Assistant Command Centre

Abderrahim's second brain. An agentic executive assistant built on Claude Code, powered by the Three Engine Model: **Architect** reasons, **Blueprint** guides, **Equipment** executes.

Built for: degiabdo — agentic workflow consultancy, MENA.

---

## What This Is

A full-stack executive assistant system combining:

- **Blueprints** — workflow SOPs that guide Claude through recurring business tasks
- **Subagents** — autonomous Claude Code agents for research, code review, and lead outreach
- **Equipment** — Python scripts for deterministic tasks (PDF generation, API integrations)
- **Trigger.dev automation** — scheduled lead generation pipeline (TypeScript)
- **MCP integrations** — Gmail, Google Drive, Google Calendar, Zapier

---

## Folder Structure

```
├── blueprints/          # Workflow SOPs — one file per repeatable task
├── .claude/
│   ├── agents/          # Claude Code subagent definitions
│   ├── rules/           # Auto-loaded rules (voice, permissions, clients)
│   └── skills/          # Superpowers skill library
├── equipment/           # Python scripts — one job each
├── assets/brand/        # Logo and brand assets for PDF generation
├── intel/               # Founder context, focus, crew, wins
├── live/                # Session state and active project tracker
├── clients/{name}/      # One folder per client (audits, quotes, invoices, emails, proposals, notes)
├── leads/               # raw/, qualified/, contacted/
├── content/             # LinkedIn posts, content calendar
├── templates/           # Reusable document templates
├── references/          # Playbooks, gold-standard outputs, three-engine-model
├── decisions/           # Append-only decision log
├── social-media/        # Output from Social Media Repurposing blueprint
├── landing-page/        # Landing page files
├── archive/             # Nothing gets deleted — moved here
├── src/                 # Trigger.dev automation (TypeScript)
│   ├── lib/             # firecrawl.ts, score.ts, sheets.ts, types.ts
│   └── trigger/         # Scheduled tasks
└── scripts/             # OAuth and utility scripts
```

---

## Blueprints

| Blueprint | File | What it does |
|-----------|------|-------------|
| Client Communication Handler | `blueprints/client-communication.md` | Draft client emails with the right tone |
| Client Proposition | `blueprints/client-proposition.md` | Create Google Doc + Gmail draft for prospects |
| Monday Morning Pipeline | `blueprints/monday-morning-pipeline.md` | Weekly pipeline summary PDF |
| Lead Update + Follow-up | `blueprints/lead-update-followup.md` | Update CRM row + draft follow-up email |
| Client Proposal Document | `blueprints/client-proposal-document.md` | Full proposal via Drive MCP |
| Prioritisation | `blueprints/prioritisation.md` | Weekly priority ranking |
| Research Subagent | `blueprints/research-subagent.md` | Deep research → PDF → Drive → Gmail |
| Trend Research & Analysis | `blueprints/trend-research-analysis.md` | Trend report PDF |
| Social Media Repurposing | `blueprints/social-media-repurposing.md` | Repurpose content for LinkedIn/Twitter/Instagram |
| Client Onboarding | `blueprints/client-onboarding.md` | Full onboarding flow via Drive/Gmail/Zapier |
| Invoice Creation | `blueprints/invoice-creation.md` | Branded invoice PDF + Drive + Gmail draft |
| Quote Generation | `blueprints/quote-generation.md` | Quote PDF + Drive + Gmail draft |
| Morning Briefing | `blueprints/morning-briefing.md` | Daily briefing via Calendar/Gmail/Drive |
| Weekly Pipeline Review | `blueprints/weekly-pipeline-review.md` | Monday 08:30 GMT+1 — pipeline review via Gmail |
| LinkedIn Content Batch | `blueprints/linkedin-content-batch.md` | Wednesday 09:00 GMT+1 — content batch |
| Monthly Business Health Report | `blueprints/monthly-health-report.md` | 1st of month — health report PDF via Drive |

---

## Subagents

Trigger these inside Claude Code by typing the command.

| Agent | Trigger | What it does |
|-------|---------|-------------|
| Research Agent | `Research: [topic]` | Web research → branded PDF → optional Drive/Gmail |
| Code Review Agent | `Review: [file path]` | Code analysis → CRITICAL/WARNING/INFO report PDF |
| Lead Outreach Agent | `Outreach: [Name] — [Company] — [context]` | Prospect research → personalized email → Gmail draft |

---

## Equipment Scripts

Python scripts in `equipment/`. Run directly or called by subagents.

| Script | Job |
|--------|-----|
| `brand.py` | Shared branding module — single source of truth for all PDFs |
| `research_pdf.py` | Convert research markdown → branded PDF |
| `code_review_pdf.py` | Convert code review markdown → branded PDF |
| `invoice_pdf.py` | Generate branded invoice PDF with PAID watermark |
| `md_to_pdf.py` | General markdown → PDF converter (quotes) |
| `pipeline_summary.py` | Monday pipeline summary PDF |
| `trend_report_pdf.py` | Trend report PDF |
| `social_media_pdf.py` | Social media content PDF |
| `health_report_pdf.py` | Monthly business health report PDF |

All PDFs use the shared branding from `brand.py`. Logo lives at `assets/brand/logo.png`.

---

## Lead Generation Pipeline (Trigger.dev)

Automated daily pipeline that finds, scores, and logs HR consultant leads in Dubai.

**Tech stack:** Firecrawl → Claude Haiku (scoring) → Google Sheets

```
src/lib/firecrawl.ts   — Runs 3 Firecrawl search queries, returns RawLead[]
src/lib/score.ts       — Claude Haiku extracts structured data, returns ScoredLead | null
src/lib/sheets.ts      — Appends qualified leads (score >= 5) to Google Sheet
src/trigger/lead-gen-dubai-hr.ts  — Scheduled task, fires daily at 06:00 UTC
```

### Run locally

```bash
npm run dev          # Start Trigger.dev local worker
npm test             # Run all Vitest tests
npm run deploy       # Deploy to Trigger.dev cloud
npx tsc --noEmit     # TypeScript type check
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. Never commit `.env`.

| Variable | Used by |
|----------|---------|
| `TRIGGER_ACCESS_TOKEN` | Trigger.dev authentication |
| `TRIGGER_SECRET_KEY` | Trigger.dev webhook verification |
| `FIRECRAWL_API_KEY` | Lead gen pipeline — web search |
| `ANTHROPIC_API_KEY` | Lead gen pipeline — Claude scoring |
| `GOOGLE_CLIENT_ID` | Google Sheets OAuth2 |
| `GOOGLE_CLIENT_SECRET` | Google Sheets OAuth2 |
| `GOOGLE_REFRESH_TOKEN` | Google Sheets OAuth2 (run `npm run auth:sheets` to generate) |
| `GOOGLE_SHEET_ID` | Target Google Sheet for lead output |

MCP connections (Gmail, Drive, Calendar, Zapier) are configured in `.mcp.json` — not included in this repo.

---

## MCP Integrations

| Tool | Status | MCP prefix |
|------|--------|-----------|
| Gmail | Connected | `mcp__claude_ai_Gmail__*` |
| Google Drive | Connected | `mcp__claude_ai_Google_Drive__*` |
| Google Calendar | Aspirational | `mcp__claude_ai_Google_Calendar__*` |
| Zapier | Connected | `mcp__zapier__*` |

---

## Getting Started

1. Clone the repo
2. Copy `.env.example` → `.env` and fill in credentials
3. Run `npm install`
4. Configure your `.mcp.json` with Gmail, Drive, and Zapier MCP tokens
5. Open in Claude Code — the assistant reads `live/state.md` and `intel/focus.md` on startup
6. Trigger any Blueprint or Subagent by name

---

## Security

- No API keys or secrets are committed to this repo
- `.env`, `.mcp.json`, `credentials.json`, `token.json` are gitignored
- All credentials live in `.env` only
- Generated reports and temporary outputs are gitignored

---

*degiabdo — Executive Assistant Command Centre — Q2 2026*
