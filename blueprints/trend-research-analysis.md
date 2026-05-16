# Blueprint: AI & Tech Trend Research & Analysis

**Goal:** Research the latest AI & Tech trends in 2026, analyse what is found, and produce a clean, well-formatted Trend Report PDF.
**Route:** WebSearch → Analysis (customer-research subagent) → Markdown → PDF (equipment/trend_report_pdf.py) → Google Drive
**Trigger:** On demand — "Run Trend Research" or "Run Blueprint 1"
**Feeds into:** Blueprint 2 (Social Media Repurposing) — passes the markdown file path

---

## Inputs Required

| Input | Default | Description |
|-------|---------|-------------|
| DATE | Auto (today YYYY-MM-DD) | Derived at runtime |
| SLUG | `ai-tech-[DATE]` | Lowercase-hyphenated file slug |
| OUTPUT_FOLDER_ID | `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Google Drive folder for output |
| MD_PATH | `.tmp/trend-report-[SLUG].md` | Markdown output path |
| PDF_PATH | `.tmp/trend-report-[SLUG].pdf` | PDF output path |

---

## Pre-flight Checklist

Before starting, confirm:
- [ ] DATE is set (today's date)
- [ ] `.tmp/` directory exists (create if not)
- [ ] Google Drive MCP accessible (`mcp__claude_ai_Google_Drive__*`)
- [ ] `equipment/trend_report_pdf.py` exists

If Google Drive is unavailable, continue — save locally and report.

---

## Sequence

### Step 1 — Research (WebSearch)

Run all 4 searches in parallel:

1. `AI trends 2026 latest breakthroughs`
2. `tech trends 2026 enterprise business impact`
3. `artificial intelligence automation SME 2026`
4. `AI agentic workflows MENA emerging markets 2026`

For each search, take the top 3 results. Use WebFetch to read content where useful.

Collect for each source:
- Title
- URL
- Date published (if visible)
- 2–3 sentence excerpt of the core finding

Target: 10–15 raw sources total.

---

### Step 2 — Analysis (customer-research subagent)

Spawn the `customer-research` subagent using the Agent tool. Pass the following as the prompt:

```
Mode: Online research (sources already collected — analyze these)
Topic: AI & Tech trends 2026
Goal: Identify the top 7 most important trends for SMEs, with a MENA lens where relevant
Deliverable: Synthesis report — structured findings, key insight per trend, confidence level

Sources collected:
[Paste all sources from Step 1 here — title, URL, date, excerpt for each]

Ranking criteria:
1. Relevance to AI and automation in 2026
2. Actionability and business impact for SMEs
3. Relevance to MENA / emerging market context

Each trend must include:
- A clear title (5–8 words)
- 2–3 sentence explanation of the trend
- Why it matters (1 sentence — SME / MENA lens)
- Confidence level: HIGH / MEDIUM / LOW
- Source URL
```

Wait for the subagent to return before proceeding to Step 3.

---

### Step 3 — Draft Report in Markdown

Write the report using this exact structure:

```markdown
# AI & Tech Trends Report — [DATE]

**Prepared by:** Trend Research Agent — degiabdo
**Date:** [DATE]
**Scope:** Latest AI & Tech trends shaping 2026

---

## Executive Summary

[3–4 sentences capturing the most important shifts happening in AI & Tech right now. Include a MENA angle if sources support it.]

---

## Top 7 Trends

### 1. [Trend Title]

[2–3 sentence explanation of the trend.]

**Why it matters:** [1 sentence — SME / MENA relevance.]
**Confidence:** HIGH / MEDIUM / LOW
**Source:** [URL]

### 2. [Trend Title]
...

[Repeat for all 7 trends]

---

## Market Implications

[3–5 bullet points on what these trends mean collectively for businesses in MENA and SMEs globally.]

---

## Key Takeaways

1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

---

## Sources

| # | Title | URL | Date |
|---|-------|-----|------|
| 1 | ... | ... | ... |
...

---

*Trend Research Agent — degiabdo — [DATE]*
```

Save to: `MD_PATH`

---

### Step 4 — Generate Trend Report PDF

Run: `python equipment/trend_report_pdf.py [MD_PATH] [PDF_PATH]`

If the script fails, invoke the `pdf` skill with the markdown content as fallback.

Output: `PDF_PATH`

---

### Step 5 — Upload to Google Drive

Use `mcp__claude_ai_Google_Drive__create_file`:

| Field | Value |
|-------|-------|
| Name | `Trend Report — AI & Tech 2026 — [DATE]` |
| Content | Contents of `PDF_PATH` |
| Folder | OUTPUT_FOLDER_ID |
| MIME type | `application/pdf` |

Capture the returned **file ID** and **shareable link**.

If Drive upload fails, save locally to `.tmp/` only and report.

---

### Step 6 — Report Back

Print a summary:

```
Blueprint 1 complete — Trend Research & Analysis

Date:         [DATE]
Markdown:     [MD_PATH]
PDF:          [PDF_PATH]
Drive file:   [Drive URL or "upload failed — saved locally"]
Sources used: [N]

→ Pass MD_PATH to Blueprint 2 (Social Media Repurposing) to continue.
```

Also return `MD_PATH` so Blueprint 2 can consume it directly.

---

## Failure Handling

| Failure | Response |
|---------|---------|
| WebSearch returns < 4 results total | Report which searches failed. Continue with what was found. |
| Fewer than 5 trends identified | List what was found, ask: "Proceed with fewer trends or retry searches?" |
| `trend_report_pdf.py` fails | Fall back to `pdf` skill. If that also fails, upload the `.md` file as a Google Doc. |
| Drive upload fails | Save PDF locally. Report full local path. Blueprint 2 can still use the `.md` file. |
| Any MCP unavailable | Stop at that step. Report exactly what was produced so far and where. |

---

## Notes

- This blueprint is the upstream dependency for Blueprint 2 (Social Media Repurposing)
- The customer-research subagent handles analysis structure — do not manually rerank findings
- MENA relevance should be surfaced wherever sources support it, not forced
- Output folder defaults to Client Propositions. A dedicated Trends folder can be created if volume warrants it.

---

## Lessons Learned

*(Updated after each run)*

| Date | Issue | Fix |
|------|-------|-----|
