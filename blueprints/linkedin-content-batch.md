# Blueprint — LinkedIn Content Batch

**Type:** Blueprint only — Architect researches, drafts, and writes files
**Sources:** WebSearch (industry trends), intel/focus.md, content/calendar/ (if exists)
**Voice:** External — professional but direct; no jargon; no corporate speak; confident without arrogance
**Output:** 2 LinkedIn post draft files saved to `content/linkedin/`

**Schedule:** Every Wednesday at 09:00 GMT+1. Trigger manually with: "LinkedIn batch" or "Content batch."

---

## Goal

Produce 2 ready-to-post LinkedIn drafts per week on agentic workflows for SMEs. One draft leads with
a current industry angle; one leads with a client outcome or operational insight. Together they give
Abderrahim two options to pick from — reducing the activation energy to publish to near zero.

---

## Inputs Required

| Input | Source | Default |
|-------|--------|---------|
| DATE | Today's date | Required — use current date |
| TOPIC_ANGLE | Industry trend from WebSearch | Researched in Step 1 |
| BUSINESS_FOCUS | Current priority from intel/focus.md | Pulled in Step 2 |

---

## Sequence

### Step 1 — Research one current industry angle

Run two WebSearch queries in parallel:
1. `"agentic workflows" OR "AI automation" SME 2026 trend`
2. `"business automation" ROI case study 2026`

From the results, extract one concrete angle — a stat, a real example, a tension, or a shift happening
right now. This becomes the hook for Draft 1. The angle must be specific and verifiable (e.g., "X% of
SMEs report..." or "Company Y reduced onboarding time by Z hours using...").

If no strong angle emerges from search: use a universal SME pain point (hiring cost, manual ops,
slow client onboarding) as the hook instead.

---

### Step 2 — Read current business context

Read `intel/focus.md` and extract:
- Top priorities right now
- Any active project or client win worth referencing (without naming clients)

Read `content/calendar/` if the folder exists — check if there is a content theme set for this week.
If so, incorporate it. If not, proceed without it.

---

### Step 3 — Write Draft 1 (trend-led)

Draft 1 leads with the industry angle from Step 1. Structure:

- **Hook** (line 1): One punchy statement or stat — no question marks, no "Did you know"
- **Problem** (lines 2–4): The gap or pain this trend reveals for SMEs
- **Insight** (lines 5–8): What agentic workflows do about it — one concrete example or mechanism
- **CTA** (final line): Low friction — not "buy now", not "DM me" — something like "This is the
  gap we build for." or "If you're still doing this manually, it's worth a conversation."

Word count: 150–220 words. No headers in the post. No bullet points unless genuinely needed.
No emojis unless the tone specifically calls for one — and never more than one.

---

### Step 4 — Write Draft 2 (operations-led)

Draft 2 leads with a specific operational problem that SMEs recognise from daily life. Draw from
the current business context (Step 2) — a workflow Abderrahim has recently built, a friction
point from a client, or an insight from the lead gen work.

Structure:
- **Hook** (line 1): Concrete operational scenario — "Every time a new client signs..." or
  "Most small agencies spend 3 hours a week on..."
- **Stakes** (lines 2–4): Why this matters — cost, time, error rate, missed revenue
- **Solution framing** (lines 5–8): How automation changes it — specific, not generic
- **Close** (final line): Positioning statement — e.g., "This is what we build at degiabdo."

Word count: 150–220 words. Same formatting rules as Draft 1.

---

### Step 5 — Save draft files

Determine today's date: `[YYYY-MM-DD]`.

Write Draft 1 to: `content/linkedin/[YYYY-MM-DD]-draft-1.md`
Write Draft 2 to: `content/linkedin/[YYYY-MM-DD]-draft-2.md`

Each file should contain:
```
# LinkedIn Draft — [DATE] — [ANGLE LABEL: Trend / Operations]

**Hook theme:** [one-line description of the angle used]
**Word count:** [count]

---

[Full draft text]
```

---

### Step 6 — Report back

Output inline:

```
## LinkedIn Batch — [DATE]

2 drafts written and saved:
- content/linkedin/[DATE]-draft-1.md — [one-line hook]
- content/linkedin/[DATE]-draft-2.md — [one-line hook]

Recommend posting: Draft [1 or 2] first — [one sentence why].
Post on: Thursday or Friday, 08:00–09:00 GMT+1 (peak LinkedIn engagement window).
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| WebSearch returns no useful results | Fall back to a universal SME pain point as the hook — note "Search returned no strong angle, used fallback hook" |
| intel/focus.md unavailable | Continue without current context — use the degiabdo north star (agentic workflows for SMEs) as the frame |
| content/linkedin/ folder does not exist | Create it, then write the files |
| One draft is weak | Write it, flag it: "Draft 2 is weaker — recommend editing before posting" |

---

## After Running

No state updates required. The files are the output.

If either draft references a client project or outcome, verify it is anonymised before flagging it as
ready to post. Never name a client in a LinkedIn post without explicit approval.

## Lessons Learned

*(Append after each run if anything needed adjusting)*

| Date | Issue | Fix |
|------|-------|-----|
