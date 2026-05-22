# Blueprint: Social Media Repurposing

**Type:** Blueprint + Equipment (social_media_pdf.py) + Google Drive MCP
**Trigger:** On demand — "Repurpose this for social" / "Run Social Media Repurposing" / paste any content
**Depends on:** Nothing — standalone workflow
**Feeds into:** Nothing — output is a PDF for review before publishing

---

## Goal

Take any piece of content — raw text, a topic, or a pasted article — and rewrite it into three platform-ready social media posts (Instagram, LinkedIn, Facebook). Generate a branded PDF with one page per platform and save to the `social-media/` folder.

Never publish directly. All output is for Abderrahim to review before posting.

---

## Inputs Required

| Input | Default | Description |
|-------|---------|-------------|
| CONTENT | Required | The source content: raw text, topic brief, or article body |
| DATE | Auto (today YYYY-MM-DD) | Derived at runtime |
| SLUG | `social-[DATE]` | Lowercase-hyphenated file slug |
| SM_MD_PATH | `social-media/social-[SLUG].md` | Markdown output path |
| SM_PDF_PATH | `social-media/social-[SLUG].pdf` | PDF output path |
| OUTPUT_FOLDER_ID | `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Google Drive folder (optional upload) |

If CONTENT is missing or empty: stop. "Content input is required. Paste the text, topic, or article you want to repurpose."

---

## Pre-flight Checklist

Before starting, confirm:
- [ ] CONTENT is present and non-empty
- [ ] DATE is set (today's date)
- [ ] `social-media/` directory exists (create if not: `os.makedirs("social-media", exist_ok=True)`)
- [ ] `equipment/social_media_pdf.py` exists
- [ ] Google Drive MCP accessible (`mcp__claude_ai_Google_Drive__*`) — optional

If CONTENT is empty: stop. Do not proceed.
If Google Drive is unavailable: continue — save locally and report.

---

## Sequence

### Step 1 — Understand the Source Content

Read CONTENT and extract:

- The **core message or main argument** (one sentence)
- The **key facts, stats, or insights** (up to 5 bullet points)
- The **audience** — who would find this valuable
- The **tone** of the original — adjust per platform

If the input is a topic brief (not an article), generate the posts from your knowledge of that topic. Do not fabricate statistics — use general claims if no data is provided.

---

### Step 2 — Draft Three Platform Posts

Write one post per platform. Follow the guides below exactly.

#### Instagram Post Guide

- **Length:** Max 150 words
- **Tone:** Direct, punchy, scroll-stopping — visual-first
- **Emojis:** Yes — use 3–6 relevant emojis to break up text and add energy
- **Structure:**
  1. Hook (one line — bold, visual, or surprising — use an emoji here)
  2. 3–4 short lines unpacking the core message (each max 15 words)
  3. One closing call to action
  4. 5–8 hashtags on the last line
- **Never:** Long paragraphs, passive voice, more than 8 hashtags, jargon

#### LinkedIn Post Guide

- **Length:** Max 250 words
- **Tone:** Professional, insight-driven, thought leadership — first-person
- **Emojis:** No
- **Structure:**
  1. Hook (one line — bold claim, striking insight, or counterintuitive statement)
  2. 2–3 short paragraphs unpacking the key ideas with evidence or reasoning
  3. Closing call to action (question to prompt comments, or invitation to connect)
  4. 3–5 relevant hashtags on the last line
- **Never:** Emojis, casual language, generic openers ("As you know...", "Excited to share...")

#### Facebook Post Guide

- **Length:** Max 200 words
- **Tone:** Conversational, warm, community-focused — accessible to non-experts
- **Emojis:** 2–3 max, used lightly
- **Structure:**
  1. Opening question or relatable statement (one line — invites the reader in)
  2. 2–3 short paragraphs: the core message + what it means for real people or small businesses
  3. Closing question to prompt engagement and comments
  4. 3–4 hashtags
- **Never:** Jargon, long sentences, bullet lists, corporate speak

---

### Step 3 — Draft Social Media Markdown

Write the output using this exact structure. Do not deviate.

```markdown
# Social Media Content Pack — [DATE]

**Prepared by:** Social Media Repurposing Agent — DEGISaaS
**Date:** [DATE]
**Source:** [First 80 characters of CONTENT or topic title]

---

## Instagram Post

[Full Instagram post text including emojis and hashtags]

---

## LinkedIn Post

[Full LinkedIn post text including hashtags]

---

## Facebook Post

[Full Facebook post text including hashtags]

---

## Content Notes

| Platform  | Word Count | Hashtag Count | Tone Check         |
|-----------|------------|---------------|--------------------|
| Instagram | [N]        | [N]           | Punchy ✓           |
| LinkedIn  | [N]        | [N]           | Professional ✓     |
| Facebook  | [N]        | [N]           | Conversational ✓   |

---

*Social Media Repurposing Agent — DEGISaaS — [DATE]*
```

Save to: `SM_MD_PATH`

---

### Step 4 — Generate PDF

Run: `python equipment/social_media_pdf.py [SM_MD_PATH] [SM_PDF_PATH]`

The script renders each platform on its own page with branded header/footer.

If the script fails: invoke the `pdf` skill with the markdown content as fallback.
If that also fails: upload the `.md` file to Drive as a Google Doc and note the fallback.

Output: `SM_PDF_PATH`

---

### Step 5 — Upload to Google Drive (Optional)

Use `mcp__claude_ai_Google_Drive__create_file`:

| Field | Value |
|-------|-------|
| Name | `Social Media Content Pack — [DATE]` |
| Content | Contents of `SM_PDF_PATH` |
| Folder | `OUTPUT_FOLDER_ID` |
| MIME type | `application/pdf` |

Capture the returned **file ID** and **shareable link**.

If Drive upload fails or is unavailable: save locally only. Report the full local path.

---

### Step 6 — Report Back

```
Social Media Repurposing — complete

Date:       [DATE]
Source:     [First 80 chars of input]
Markdown:   [SM_MD_PATH]
PDF:        [SM_PDF_PATH]
Drive file: [Drive URL or "saved locally only"]

Posts generated:
  Instagram  ✓  [N words]  [N hashtags]
  LinkedIn   ✓  [N words]  [N hashtags]
  Facebook   ✓  [N words]  [N hashtags]
```

---

## Failure Handling

| Failure | Response |
|---------|---------|
| CONTENT not provided | Stop. "Content input is required. Paste the text or topic you want to repurpose." |
| CONTENT too short to work with (<20 words, not a topic) | Ask: "This looks short — is this the full content, or a topic brief?" |
| `social_media_pdf.py` fails | Fall back to `pdf` skill. If that also fails, upload the `.md` as Google Doc. |
| Drive upload fails | Save PDF to `social-media/` only. Report full local path. |
| Any MCP unavailable | Continue without it. Save locally and report what was produced. |

---

## Notes

- **Standalone** — does not require Blueprint 1 (Trend Research). Works on any input.
- Instagram emojis are intentional — standard on that platform, user-requested.
- Word counts are caps, not targets — shorter is fine if the content is complete.
- Nothing gets published from this blueprint — all output is for review.
- Output folder: `social-media/` (created automatically on first run).

---

## Lessons Learned

*(Updated after each run)*

| Date | Issue | Fix |
|------|-------|-----|
