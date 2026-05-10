# Blueprint: Research Subagent — AI Agentic Trends

**Goal:** Research the latest AI Agentic trends for a given TOPIC, analyse them, generate a formatted PDF summary of the top 5 findings, upload to Google Drive, and create a Gmail draft linking to it.
**Route:** WebSearch → Analysis (customer-research skill) → Markdown → PDF (pdf skill) → Google Drive → Gmail draft
**Trigger:** On demand — "Run the Research Subagent on [TOPIC]"

---

## Inputs Required

| Input | Default | Description |
|-------|---------|-------------|
| TOPIC | AI Agentic | The trend domain to research |
| DATE | Auto (today YYYY-MM-DD) | Derived at runtime |
| SLUG | Auto (TOPIC → lowercase-hyphenated) | e.g. `ai-agentic` |
| OUTPUT_FOLDER_ID | `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Google Drive folder for output |
| TO_EMAIL | `raguebi.mba@gmail.com` | Always Abderrahim |

---

## Pre-flight Checklist

Before starting, confirm:
- [ ] TOPIC is defined (use default if not provided)
- [ ] Google Drive MCP accessible (`mcp__claude_ai_Google_Drive__*`)
- [ ] Gmail MCP accessible (`mcp__claude_ai_Gmail__*`)
- [ ] `.tmp/` directory exists (create if not)

If any MCP is unavailable, stop and report.

---

## Sequence

### Step 1 — Research (WebSearch)

Run all 3 searches in parallel:

1. `[TOPIC] AI agentic trends 2025 2026`
2. `autonomous agents [TOPIC] latest developments`
3. `agentic AI [TOPIC] use cases enterprise SME`

For each search, take the top 2–3 results. Use WebFetch to read the content where useful.

Collect for each source:
- Title
- URL
- Date published (if visible)
- 2–3 sentence excerpt of the core finding

Target: 8–12 raw sources total.

---

### Step 2 — Analysis (customer-research subagent)

Spawn the `customer-research` subagent using the Agent tool. Pass the following as the prompt:

```
Mode: Online research (sources already collected — analyze these)
Topic: [TOPIC] AI Agentic trends
Goal: Identify the top 5 most important findings for SMEs, with a MENA lens
Deliverable: Synthesis report + quote bank

Sources collected:
[Paste all sources from Step 1 here — title, URL, date, excerpt for each]

Ranking criteria for findings:
1. Relevance to AI Agentic workflows
2. Actionability for SMEs
3. Relevance to MENA market context

Each finding must include:
- A clear title (5–8 words)
- 2–3 sentence explanation
- Why it matters (1 sentence — SME / MENA lens)
- Source URL
```

Wait for the subagent to return its structured report before proceeding to Step 3.

---

### Step 3 — Draft Report in Markdown

Write the report using this structure:

```markdown
# [TOPIC] AI Agentic Trends — [DATE]

**Prepared by:** Research Subagent  
**Date:** [DATE]  
**Scope:** Latest trends in [TOPIC] AI Agentic workflows

---

## Executive Summary

[2–3 sentences capturing the most important shift happening right now in this space.]

---

## Top 5 Findings

### 1. [Finding Title]

[2–3 sentence explanation.]

**Why it matters:** [1 sentence — SME / MENA relevance.]  
**Source:** [URL]

### 2. [Finding Title]
...

### 3. [Finding Title]
...

### 4. [Finding Title]
...

### 5. [Finding Title]
...

---

## Sources

| # | Title | URL | Date |
|---|-------|-----|------|
| 1 | ... | ... | ... |
...

---

*Research Subagent — degiabdo — [DATE]*
```

Save to: `.tmp/research-[SLUG]-[DATE].md`

---

### Step 4 — Generate PDF

Invoke the `pdf` skill with the markdown content from Step 3.

Output: `.tmp/research-[SLUG]-[DATE].pdf`

If the `pdf` skill fails: fall back to uploading the `.md` file as a Google Doc in Step 5 — note the fallback in the final report.

---

### Step 5 — Upload to Google Drive

Use `mcp__claude_ai_Google_Drive__create_file`:

| Field | Value |
|-------|-------|
| Name | `Research Brief — [TOPIC] AI Agentic Trends [DATE]` |
| Content | Contents of `.tmp/research-[SLUG]-[DATE].pdf` |
| Folder | OUTPUT_FOLDER_ID |
| MIME type | `application/pdf` |

Capture the returned **file ID** and **shareable link**.

---

### Step 6 — Create Gmail Draft

Use `mcp__claude_ai_Gmail__create_draft`:

**To:** TO_EMAIL  
**Subject:** `Research Brief: [TOPIC] AI Agentic Trends — [DATE]`

**Body:**

```
Hi Abderrahim,

Your research brief on [TOPIC] AI Agentic trends is ready.

Top finding: [One-line summary of Finding #1]

Full report (PDF): [Drive shareable link]

---

Top 5 findings:
1. [Finding 1 title]
2. [Finding 2 title]
3. [Finding 3 title]
4. [Finding 4 title]
5. [Finding 5 title]

---
Research Subagent — degiabdo — [DATE]
```

**Rule:** Never send directly. Always save as draft. Abderrahim reviews before sending.

---

### Step 7 — Report Back

Print a summary:

```
Research Subagent complete.

Topic:        [TOPIC]
Date:         [DATE]
PDF:          .tmp/research-[SLUG]-[DATE].pdf
Drive file:   [Drive URL]
Gmail draft:  [Draft link or "check Gmail Drafts"]
Sources used: [N]
```

---

## Failure Handling

| Failure | Response |
|---------|---------|
| WebSearch returns < 3 results | Report which searches failed. Ask: "Retry with adjusted keywords or proceed with fewer sources?" |
| Fewer than 5 findings identified | List what was found, ask Abderrahim if findings should be padded or brief should be shorter |
| `pdf` skill fails | Upload the `.md` file to Drive as a Google Doc instead. Note fallback in final report. |
| Drive upload fails | Save PDF to `.tmp/` only. Report full local path. |
| Gmail draft fails | Print the full email body in conversation for manual copy-paste. |
| Any MCP unavailable | Stop at that step. Report exactly which step failed and what was produced so far. |

---

## Notes

- SLUG: replace spaces with hyphens, lowercase. "AI Agentic HR" → `ai-agentic-hr`
- The `customer-research` skill guides the analysis structure — it does not replace reading the sources
- The `pdf` skill handles formatting — do not manually style the PDF
- Output Drive folder defaults to Client Propositions. A dedicated Research folder can be created if volume warrants it.
- This Blueprint is TOPIC-agnostic despite being named for AI Agentic trends — the searches in Step 1 are the only hardcoded constraint

---

## Lessons Learned

*(Updated after each run)*

| Date | Issue | Fix |
|------|-------|-----|
| 2026-05-10 | Client Propositions folder (1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2) returned "cannot add children" error | Upload to Drive root instead — file lands in raguebi.build@gmail.com root. Move manually if needed, or create a dedicated Research folder and update OUTPUT_FOLDER_ID. |
