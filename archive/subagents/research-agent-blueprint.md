# Blueprint: Research Agent

**Type:** Blueprint + Equipment (research_pdf.py) + optional Drive/Gmail MCPs
**Trigger:** `Research: [topic or question]`
**Goal:** Research any topic, synthesise findings into a structured report, and deliver a branded PDF saved to `reports/`.

---

## Required Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| TOPIC | Yes | — | The research topic or question |
| DEPTH | No | standard | `quick` (3–5 sources), `standard` (8–12), `deep` (15+) |
| DATE | No | Auto | Today's date YYYY-MM-DD |
| SLUG | No | Auto | TOPIC → lowercase-hyphenated, e.g. `ai-adoption-mena` |

If TOPIC is not provided, stop and ask: "What should I research?"

---

## Pre-flight Checklist

- [ ] TOPIC is defined
- [ ] DATE derived (today's date)
- [ ] SLUG derived from TOPIC
- [ ] `.tmp/` directory exists (create if not)
- [ ] `reports/` directory exists (created automatically by script — no action needed)
- [ ] `subagents/research-agent/research_pdf.py` is present

---

## Sequence

### Step 1 — Search

Generate 3 search queries adapted to the topic. Do not use hardcoded templates — construct queries that match the TOPIC's domain, intent, and recency.

**Example queries for "AI adoption in MENA SMEs":**
1. `AI adoption MENA small business 2025 2026`
2. `artificial intelligence SME Middle East North Africa trends`
3. `agentic AI automation MENA market opportunities`

Run all 3 searches in parallel using WebSearch.

For each result:
- Capture: title, URL, date (if visible), 2–3 sentence excerpt of the core finding
- Use WebFetch on the top 3–5 most relevant URLs to get full content

Target per depth:
| Depth | Sources |
|-------|---------|
| quick | 3–5 |
| standard | 8–12 |
| deep | 15+ |

---

### Step 2 — Synthesise

Spawn the `customer-research` subagent using the Agent tool. Pass this prompt:

```
Mode: Online research (sources already collected — analyze these)
Topic: [TOPIC]
Goal: Identify the top findings relevant to SMEs and [TOPIC] domain — actionable insights, not just observations
Deliverable: Structured synthesis

Sources collected:
[Paste all sources here — title, URL, date, excerpt for each]

For each finding provide:
- Title (5–8 words)
- 2–3 sentence explanation
- Why it matters (1 sentence — SME / practical lens)
- Source URL

Return 5 findings by default. If fewer than 5 are supported by the sources, return what the evidence supports — do not pad.
```

Wait for the subagent to return before proceeding.

---

### Step 3 — Draft Markdown Report

Write the report to `.tmp/research-[SLUG]-[DATE].md` using this structure:

```markdown
# [TOPIC] — Research Brief

**Prepared by:** Research Agent
**Date:** [DATE]
**Scope:** [One sentence describing what was researched and why]

---

## Executive Summary

[2–3 sentences: the most important shift or insight from the research. Write for a busy founder — what's the headline?]

---

## Key Findings

### 1. [Finding Title]

[2–3 sentence explanation.]

**Why it matters:** [1 sentence — practical SME relevance.]
**Source:** [URL]

### 2. [Finding Title]
...

---

## Sources

| # | Title | URL | Date |
|---|-------|-----|------|
| 1 | ... | ... | ... |
...

---

*Research Agent — degiabdo — [DATE]*
```

---

### Step 4 — Generate PDF

Run the Equipment script:

```bash
python subagents/research-agent/research_pdf.py .tmp/research-[SLUG]-[DATE].md reports/research-[SLUG]-[DATE].pdf
```

The script creates `reports/` if it doesn't exist. If it exits with a non-zero code, report the error and offer the `.md` file as fallback.

---

### Step 5 — Report Back

Print:

```
Research Agent complete.

Topic:     [TOPIC]
Depth:     [quick / standard / deep] — [N] sources used
PDF:       reports/research-[SLUG]-[DATE].pdf
Markdown:  .tmp/research-[SLUG]-[DATE].md

Want me to upload the PDF to Google Drive and draft an email with the link?
```

---

### Step 6 — Optional: Drive Upload + Gmail Draft (on confirmation only)

If Abderrahim confirms:

**Drive upload** — use `mcp__claude_ai_Google_Drive__create_file`:
- Name: `Research Brief — [TOPIC] — [DATE]`
- Content: PDF file contents
- MIME type: `application/pdf`
- Parent: Drive root (do not use Client Propositions folder — known permission issue)

**Gmail draft** — use `mcp__claude_ai_Gmail__create_draft`:
- To: `raguebi.build@gmail.com`
- Subject: `Research Brief: [TOPIC] — [DATE]`
- Body:

```
Hi Abderrahim,

Your research brief on [TOPIC] is ready.

Top finding: [One-line summary of Finding #1]

Full report (PDF): [Drive shareable link]

---
[List all finding titles numbered 1–N]
---
Research Agent — degiabdo — [DATE]
```

Never send directly. Save as draft only.

---

## Failure Handling

| Failure | Response |
|---------|---------|
| TOPIC not provided | Stop. Ask: "What should I research?" |
| WebSearch returns < 3 results total | Report which queries failed. Ask: "Retry with adjusted keywords, or proceed with fewer sources?" |
| Fewer than 5 findings from synthesis | Use what the evidence supports. State count in output: "Found 3 well-supported findings." |
| `research_pdf.py` not found | Stop at Step 4. Report: "Equipment script missing at subagents/research-agent/research_pdf.py" |
| PDF generation fails | Offer `.md` file as deliverable. Report: "PDF failed — markdown report available at .tmp/research-[SLUG]-[DATE].md" |
| Drive upload fails | Report error, skip Gmail draft. Local PDF is the primary output. |
| Gmail draft fails | Print full email body in conversation for manual copy-paste. |

---

## Notes

- **SLUG derivation:** replace spaces with hyphens, lowercase, strip special characters. `"AI adoption in MENA"` → `ai-adoption-in-mena`
- **Search query construction:** match queries to the TOPIC's domain. Avoid generic terms when the topic is specific.
- **DEPTH guidance:** default to `standard`. Use `quick` for rapid overviews, `deep` for strategic decisions or competitive intelligence.
- **Output is local first:** `reports/` is the primary destination. Drive upload is optional and on-demand.
- **Drive folder note:** the Client Propositions folder (`1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2`) has returned "cannot add children" errors in the past. Always upload to Drive root.
