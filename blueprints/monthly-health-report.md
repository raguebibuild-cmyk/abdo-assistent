# Blueprint — Monthly Business Health Report

**Type:** Blueprint + Equipment — Architect collects data, Equipment generates PDF, Drive MCP uploads
**Sources:** clients/*/invoices/, clients/*/quotes/, live/state.md, intel/wins.md, leads/qualified/, leads/contacted/
**Voice:** Internal — direct, no pleasantries
**Output:** Branded PDF uploaded to Google Drive + inline summary

**Schedule:** 1st of every month at 09:00 GMT+1. Trigger manually with: "Monthly health report" or "Run health report."

---

## Goal

On the first of each month, review the business as a system: which clients are active, which invoices
are outstanding, how the lead pipeline is moving, and whether the quarter is tracking toward its goals.
Produce a branded PDF report — one document that answers "how's the business doing?" without manual
digging.

---

## Inputs Required

| Input | Default | Description |
|-------|---------|-------------|
| DATE | Auto (today YYYY-MM-DD) | Derived at runtime |
| MONTH_LABEL | Auto (e.g., "May 2026") | Human-readable month label |
| OUTPUT_FOLDER_ID | `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Google Drive destination folder |
| JSON_PATH | `.tmp/health-[DATE].json` | Structured data file for equipment |
| PDF_PATH | `.tmp/health-report-[DATE].pdf` | PDF output path |

---

## Pre-flight Checklist

Before starting, confirm:
- [ ] DATE and MONTH_LABEL are set
- [ ] `.tmp/` directory exists (create if not)
- [ ] Google Drive MCP accessible (`mcp__claude_ai_Google_Drive__*`)
- [ ] `equipment/health_report_pdf.py` exists

If Drive is unavailable: generate PDF locally, report full path, and note "Upload manually."

---

## Sequence

### Step 1 — Scan all client folders

For each folder in `clients/`:
- Read any files in `clients/{name}/invoices/` — extract: invoice number (if visible), amount, and
  whether the invoice shows PAID status or is outstanding
- Read any files in `clients/{name}/quotes/` — extract: quote amount and whether it converted to
  a project or is still open
- Note the client name and their apparent status: Active (has an open invoice or recent work),
  Prospect (has a quote but no invoice), Closed (all invoices marked PAID, no open work)

If a client folder has no invoices and no quotes: mark as "No documents."

Compile a client table:
```
[
  { "name": "...", "status": "Active|Prospect|Closed|No documents",
    "open_invoice_amount": 0.00, "open_quote_amount": 0.00, "notes": "..." },
  ...
]
```

---

### Step 2 — Read state.md and wins.md

Read `live/state.md` and extract:
- Open tasks count (total and overdue)
- Active projects list with status
- Current priorities

Read `intel/wins.md` and extract:
- Q2 2026 goals (even if TBD)
- Milestones hit vs. not hit

---

### Step 3 — Count lead pipeline

List all files in `leads/qualified/` → count = qualified leads total
List all files in `leads/contacted/` → count = contacted leads total
List all files in `leads/raw/` → count = raw leads total

Conversion rate: contacted / qualified × 100 (if qualified > 0, else N/A)

---

### Step 4 — Compile summary totals

From the client data (Step 1) compute:
- Total outstanding invoices: sum of all `open_invoice_amount`
- Total open quotes: sum of all `open_quote_amount`
- Count of active clients
- Count of prospects (open quotes, no invoice)
- Count of closed clients

From state.md: total open tasks, overdue count

From leads: qualified count, contacted count, conversion rate

---

### Step 5 — Write JSON data file

Assemble all data into a JSON file at `JSON_PATH`:

```json
{
  "date": "YYYY-MM-DD",
  "month_label": "Month YYYY",
  "clients": [...],
  "summary": {
    "active_clients": 0,
    "prospects": 0,
    "closed_clients": 0,
    "outstanding_invoices_total": 0.00,
    "open_quotes_total": 0.00
  },
  "pipeline": {
    "raw_leads": 0,
    "qualified_leads": 0,
    "contacted_leads": 0,
    "conversion_rate_pct": 0.0
  },
  "tasks": {
    "open": 0,
    "overdue": 0
  },
  "goals": {
    "q2_goals": "...",
    "milestones_hit": [...],
    "milestones_pending": [...]
  }
}
```

Write this file to `JSON_PATH`.

---

### Step 6 — Generate Health Report PDF

Run: `python equipment/health_report_pdf.py [JSON_PATH] [PDF_PATH]`

The script reads the JSON, builds a branded PDF with:
- Cover section: month label, summary KPIs
- Client status table
- Pipeline metrics section
- Goals & milestones section

If the script fails: invoke the `pdf` skill with a markdown version of the data as fallback.
If both fail: upload the JSON file to Drive as a plain document and report.

Output: `PDF_PATH`

---

### Step 7 — Upload to Google Drive

Use `mcp__claude_ai_Google_Drive__create_file`:

| Field | Value |
|-------|-------|
| Name | `Business Health Report — [MONTH_LABEL]` |
| Content | Contents of `PDF_PATH` |
| Folder | `OUTPUT_FOLDER_ID` |
| MIME type | `application/pdf` |

Capture the returned file ID and shareable link.

---

### Step 8 — Report back inline

```
## Business Health Report — [MONTH_LABEL]

### Summary
Active clients:      [N]
Prospects (open quotes): [N]
Outstanding invoices: [CURRENCY AMOUNT]
Open quotes:         [CURRENCY AMOUNT]

### Pipeline
Qualified leads:   [N]
Contacted:         [N]
Conversion rate:   [N%]

### Tasks
Open:    [N]
Overdue: [N]

### Report
PDF: [PDF_PATH]
Drive: [Drive URL or "upload failed — saved locally"]

[Any flags — e.g., "3 invoices overdue > 30 days", "2 qualified leads not yet contacted"]
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Client folder unreadable | Skip that client, note "Folder unreadable: {name}" in report |
| No invoices or quotes found anywhere | Report zero totals — do not stop |
| `health_report_pdf.py` fails | Fall back to `pdf` skill with markdown summary |
| Drive upload fails | Save PDF locally, report full path |
| state.md or wins.md unreadable | Continue without that section; note in the report |

---

## After Running

Clean up `.tmp/health-[DATE].json` after the PDF is confirmed uploaded.

Flag any business health risks inline after the report:
- Any invoice outstanding > 30 days
- Any prospect (open quote) with no activity for > 14 days
- More than 3 overdue tasks

## Lessons Learned

*(Append after each run if anything needed adjusting)*

| Date | Issue | Fix |
|------|-------|-----|
