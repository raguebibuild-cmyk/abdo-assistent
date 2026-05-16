# Blueprint: Social Media Repurposing

**Type:** Blueprint + Equipment (social_media_pdf.py) + Google Drive MCP
**Trigger:** On demand — "Run Social Media Repurposing" or "Run Blueprint 2"
**Depends on:** Blueprint 1 (Trend Research & Analysis) — requires MD_PATH output
**Feeds into:** Nothing — this is the final step in the pipeline

---

## Goal

Take the Trend Report markdown from Blueprint 1, repurpose the top insights into three platform-specific social media posts (LinkedIn, Facebook, Instagram), save everything as a formatted Social Media Content PDF, and upload to Google Drive for review.

Never post directly. All output is saved to Drive — Abderrahim reviews before publishing.

---

## Inputs Required

| Input | Default | Description |
|-------|---------|-------------|
| MD_PATH | Required — passed from Blueprint 1 | Path to the trend report markdown file |
| DATE | Auto (today YYYY-MM-DD) | Derived at runtime |
| SLUG | `social-media-[DATE]` | Lowercase-hyphenated file slug |
| OUTPUT_FOLDER_ID | `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Google Drive folder for output |
| SM_MD_PATH | `.tmp/social-media-[SLUG].md` | Social media markdown output path |
| SM_PDF_PATH | `.tmp/social-media-[SLUG].pdf` | Social media PDF output path |

If MD_PATH is missing: stop. "Blueprint 1 output path (MD_PATH) is required. Run Blueprint 1 first, or provide the path manually."

---

## Pre-flight Checklist

Before starting, confirm:
- [ ] MD_PATH is set and the file exists at that path
- [ ] DATE is set (today's date)
- [ ] `.tmp/` directory exists (create if not)
- [ ] `equipment/social_media_pdf.py` exists
- [ ] Google Drive MCP accessible (`mcp__claude_ai_Google_Drive__*`)

If the MD_PATH file does not exist: stop. Do not proceed.
If Google Drive is unavailable: continue — save locally and report.

---

## Sequence

### Step 1 — Read Trend Report

Read the file at MD_PATH. Extract:

- The **Executive Summary** section (copy verbatim — 2–4 sentences)
- The **top 3 trend titles** and their one-line "Why it matters" statements
- Any **MENA-relevant angle** if present in the report

Do not re-research or re-analyse. Use only what Blueprint 1 produced.

---

### Step 2 — Draft Three Social Media Posts

Write one post per platform. Follow the guides below exactly.

#### LinkedIn Post Guide

- **Length:** 150–250 words
- **Tone:** Thought leadership — professional, confident, first-person plural ("we", "our research")
- **Structure:**
  1. Hook (one line — bold claim or striking stat from the trend report)
  2. 2–3 short paragraphs unpacking the top 2–3 insights
  3. Closing call to action (question or invitation to comment)
  4. 3–5 hashtags on the last line (relevant, not generic)
- **Never:** emojis, casual language, generic openers like "As you know..."

#### Facebook Post Guide

- **Length:** 80–130 words
- **Tone:** Conversational, warm, accessible — not corporate
- **Structure:**
  1. Opening question or relatable statement (one line)
  2. 2 short paragraphs: the trend + what it means for small businesses
  3. Closing question to prompt engagement
  4. 3 hashtags
- **Never:** jargon, long sentences, bullet lists

#### Instagram Post Guide

- **Length:** 60–100 words (caption only — no image required)
- **Tone:** Direct, punchy, scroll-stopping
- **Structure:**
  1. Hook (one line — striking, visual-first)
  2. 3 bullet points (top 3 trend findings, each max 10 words)
  3. One closing line (call to action)
  4. 5–8 hashtags on the last line
- **Never:** long paragraphs, passive voice, more than 8 hashtags

---

### Step 3 — Draft Social Media Markdown

Write the output using this exact structure. Do not deviate from the template.

```markdown
# Social Media Content Pack — AI & Tech Trends [DATE]

**Prepared by:** Social Media Repurposing Agent — degiabdo
**Date:** [DATE]
**Source report:** [MD_PATH]

---

## LinkedIn Post

[Full LinkedIn post text]

---

## Facebook Post

[Full Facebook post text]

---

## Instagram Post

[Full Instagram post text]

---

## Content Notes

| Platform | Word Count | Hashtag Count | Tone Check |
|----------|-----------|---------------|------------|
| LinkedIn | [N] | [N] | Professional ✓ |
| Facebook | [N] | [N] | Conversational ✓ |
| Instagram | [N] | [N] | Punchy ✓ |

---

*Social Media Repurposing Agent — degiabdo — [DATE]*
```

Save to: `SM_MD_PATH`

---

### Step 4 — Generate Social Media PDF

Run: `python equipment/social_media_pdf.py [SM_MD_PATH] [SM_PDF_PATH]`

If the script fails: invoke the `pdf` skill with the markdown content as fallback.
If that also fails: upload the `.md` file to Drive as a Google Doc and note the fallback.

Output: `SM_PDF_PATH`

---

### Step 5 — Upload to Google Drive

Use `mcp__claude_ai_Google_Drive__create_file`:

| Field | Value |
|-------|-------|
| Name | `Social Media Content Pack — AI & Tech Trends [DATE]` |
| Content | Contents of `SM_PDF_PATH` |
| Folder | `OUTPUT_FOLDER_ID` |
| MIME type | `application/pdf` |

Capture the returned **file ID** and **shareable link**.

If Drive upload fails: save locally only. Report the full local path.

---

### Step 6 — Report Back

Print a summary:

```
Blueprint 2 complete — Social Media Repurposing

Date:         [DATE]
Source:       [MD_PATH]
Markdown:     [SM_MD_PATH]
PDF:          [SM_PDF_PATH]
Drive file:   [Drive URL or "upload failed — saved locally"]

Posts generated:
  LinkedIn  ✓  [N words]
  Facebook  ✓  [N words]
  Instagram ✓  [N words]
```

---

## Failure Handling

| Failure | Response |
|---------|---------|
| MD_PATH not provided | Stop immediately. "MD_PATH is required. Run Blueprint 1 first or provide the path." |
| MD_PATH file not found on disk | Stop immediately. "File not found at [MD_PATH]. Check the path and try again." |
| Trend report has fewer than 3 trends | Use all trends available. Adjust posts accordingly — do not fabricate. |
| `social_media_pdf.py` fails | Fall back to `pdf` skill. If that also fails, upload the `.md` as a Google Doc. |
| Drive upload fails | Save PDF to `.tmp/` only. Report full local path. |
| Any MCP unavailable | Stop at that step. Report exactly what was produced so far and where it was saved. |

---

## Notes

- This blueprint is the downstream consumer of Blueprint 1 (Trend Research & Analysis)
- Do not re-research — use only what Blueprint 1 produced in its markdown file
- Post lengths are caps, not targets — shorter is fine if content is complete
- MENA angle: include only if it appeared in the trend report — do not force it
- All output is for review — nothing gets published directly from this blueprint
- Output Drive folder defaults to Client Propositions. A dedicated Social Media folder can be created if volume warrants it.

---

## Lessons Learned

*(Updated after each run)*

| Date | Issue | Fix |
|------|-------|-----|
