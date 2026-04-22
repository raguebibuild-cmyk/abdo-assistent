# Blueprint: Client Communication Handler

**Type:** Blueprint only — no Equipment required
**Voice rules:** `.claude/rules/voice.md`, `.claude/rules/clients.md`
**Gold standard:** `references/goldstandard/client-delivery-email.md`
**Template:** `templates/client-email.md`

---

## Goal

Produce a draft client email for any stage of the client lifecycle. Never send directly — all output is a draft for Abderrahim to review.

---

## Required Inputs

Before drafting, confirm you have all four:

| Input | Description |
|-------|-------------|
| Client name | First name is enough |
| Lifecycle stage | Prospect / Onboarding / Active / Invoice / Closed |
| Message type | See list below |
| Key points | What needs to be said — context, outcome, ask |

If any input is missing: stop and ask. No assumptions.

---

## Lifecycle Stage Guide

| Stage | What's happening | Tone emphasis |
|-------|-----------------|---------------|
| Prospect | Not yet a client — exploring fit | Warm, confident, low pressure |
| Onboarding | Just signed — getting started | Reassuring, clear, action-oriented |
| Active | Work in progress | Direct, professional, progress-focused |
| Invoice | Work delivered — billing stage | Friendly, clear, prompt |
| Closed | Engagement complete | Warm close, door open for future |

---

## Message Types

| Type | When to use |
|------|-------------|
| Initial outreach | First contact with a prospect |
| Follow-up | Checking in after no response, or progressing a conversation |
| Work delivered | Notifying client that a workflow or deliverable is ready |
| Common question reply | Answering a question the client asked |
| Quote | Sending pricing for a proposed service — confirm pricing first |
| Project update | Progress update mid-engagement |
| Invoice | Sending payment request — confirm amounts first |

---

## Sequence

**Step 1 — Gather inputs**
Confirm: client name, lifecycle stage, message type, key points.
If pricing is involved (quote or invoice): confirm the numbers before drafting. Stop if unconfirmed.

**Step 2 — Identify stage and message type**
Match to the tables above. This determines tone emphasis and structure.

**Step 3 — Apply voice rules**
- Professional but warm (never casual, never stiff)
- Lead with the result or purpose — never filler openers
- One clear ask or next step at the end
- Plain language — no jargon, no corporate speak
- Short paragraphs, 2–3 max

**Step 4 — Draft**
Use `templates/client-email.md` as the shell.
Benchmark against `references/goldstandard/client-delivery-email.md` — match that standard.

**Step 5 — Output for review**
Present the draft clearly labelled:

```
DRAFT — [Message Type] to [Client Name] ([Stage])
---
Subject: ...

Hi [Name],

...

Abderrahim
degiabdo
---
Waiting for your review. Reply "send" to approve or give edits.
```

Do not send. Do not ask if you should send. Wait for explicit approval.

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Missing client name | Ask before drafting |
| Stage unknown | Ask — "What stage is [name] at?" |
| Pricing unconfirmed | Stop — "Pricing hasn't been confirmed for this. What should the number be?" |
| Unclear ask or context | Stop — list exactly what's missing |
| Audit requested | Confirm client details before drafting — audits are always customised, never generic |

---

## Output Standard

Every draft must have:
- A subject line that describes the outcome or action (not the process)
- An opening line that gets straight to the point
- A body of 2–3 short paragraphs
- One clear ask or next step
- Abderrahim's signature (Abderrahim / degiabdo)

No draft should ever be longer than it needs to be. If in doubt, cut.
