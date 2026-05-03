# Blueprint: Weekly Prioritisation

**Type:** Blueprint only — no Equipment required  
**Runs:** Start of each week (Sunday evening or Monday morning)  
**Sources:** Gmail, Google Calendar, Tasks List (Google Sheets), intel/focus.md, live/state.md  
**Skills available:** See Skills Reference section below  

---

## Goal

Produce a prioritised weekly plan by scanning all active inputs, identifying the highest-leverage actions, and sequencing them across the week. Output is a named weekly plan saved in this file under Weekly Plans.

---

## Required Inputs

| Input | Where |
|-------|-------|
| Open tasks | live/state.md + Tasks List sheet |
| Current priorities | intel/focus.md |
| Unread / actionable emails | Gmail scan — last 30 days, unread |
| Calendar events | Google Calendar — current week |
| Active deadlines | intel/focus.md + live/state.md |

---

## Prioritisation Framework

Score each task across two axes:

| Axis | Question |
|------|----------|
| Urgency | Does waiting cost money, a client, or a deadline? |
| Leverage | Does completing this unblock other tasks or move the north star? |

**Tiers:**

| Tier | Definition | Action |
|------|-----------|--------|
| P1 — Do first | Urgent AND high leverage (client revenue, hard deadlines, blockers) | This week, early |
| P2 — Do next | High leverage, not urgent — or urgent but low leverage | This week |
| P3 — Schedule | Important but not this week | Log to Tasks List, set a due date |
| Drop | Low urgency, low leverage | Remove from list |

**Blocker rule:** If Task A blocks Tasks B, C, D — Task A is always P1, regardless of its own urgency score.

---

## Sequence

**Step 1 — Scan sources**  
- Read live/state.md and intel/focus.md  
- Search Gmail: `is:unread newer_than:30d` — extract actionable threads only (ignore newsletters, notifications, security alerts)  
- Check Google Calendar for the current week  
- Read Tasks List sheet  

**Step 2 — Extract actionable items**  
List every item that requires an action. Discard informational or passive items.

**Step 3 — Apply prioritisation framework**  
Assign each item a tier (P1/P2/P3/Drop). Identify blockers and sequence them first.

**Step 4 — Build the weekly plan**  
Map P1 and P2 tasks across Monday–Friday. Group by day. Flag blockers explicitly.

**Step 5 — Output**  
Write the plan in the Weekly Plans section below. Label it with the week start date.

**Step 6 — Update state**  
After confirming the plan, update live/state.md with current priorities and any new open tasks.

---

## Rules

- Never schedule more than 3 P1 tasks in a single day — solo founder, no team
- Client-facing actions always sit above internal build tasks, at the same tier
- A task with a due date within 7 days is automatically P1
- If pricing is unconfirmed and a task depends on it — flag pricing as the P1 blocker
- Calendar gaps = capacity. No meetings this week = full execution week

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Tasks List unreadable | Fall back to live/state.md and intel/focus.md |
| Gmail scan returns no actionable items | Note it — don't invent tasks |
| Calendar unavailable | Assume full capacity, note caveat |
| Conflicting priorities | Flag the conflict — "Focus.md says X, but client urgency suggests Y. Which takes priority?" |

---

## Weekly Plans

---

### Week of 2026-05-03 (refreshed 2026-05-03)

**Sources scanned:** Gmail (30d unread), Google Calendar (May 2026), Tasks List2 sheet, live/state.md, intel/focus.md  
**Calendar:** Empty — no external commitments. Full execution week.  
**Pricing:** Locked — intel/pricing.md. No longer a blocker.  
**Hard deadline:** 2026-05-15 — degiabdo official launch (12 days)

---

#### New This Scan — 5 Inbound Gmail Threads

| Thread | Context | Action needed |
|--------|---------|---------------|
| "Re: Picking this back up" | Client returning after 2-month gap — partner transition resolved, wants comms automation | Reply — re-engage |
| "Intro from Hicham — quote automation" | Referral via Sahel Cafe Group — construction firm Casablanca ~40 people | Reply within 24h — referral = warm |
| "Outbound automation — intro call?" | Inbound via LinkedIn post — B2B SaaS, Saudi F&B, SDR drowning | Reply — book intro call |
| "Re: AAA — Workflow Audit proposal" | Prospect aligned on scope, wants deliverable format walkthrough before signing | Reply — this is near-close |
| "Adding LinkedIn content automation to our scope?" | Existing client — senior partners asking about LinkedIn content automation | Reply — upsell opportunity |

---

#### Blocker Status

None. Pricing resolved (intel/pricing.md). All quote and lead replies can proceed immediately.

---

#### Priority Stack

| # | Task | Tier | Due | Notes |
|---|------|------|-----|-------|
| 1 | Reply: CRM quote — laboratoiremvcd@gmail.com | P1 | 2026-05-05 | 7 days old — reply now |
| 2 | Reply: CRM quote — biovagoabdorag@gmail.com | P1 | 2026-05-05 | 7 days old — reply now |
| 3 | Reply: AAA Workflow Audit — propose deliverable walkthrough call | P1 | ASAP | Prospect aligned and almost ready to sign — highest revenue proximity this week |
| 4 | Reply: client returning — comms automation reactivation | P1 | ASAP | They re-initiated — momentum is there |
| 5 | Reply: referral from Hicham — construction firm quote | P1 | ASAP | Referral = warm, 24h response window |
| 6 | Reply: inbound LinkedIn lead — SDR/outbound intro call | P1 | ASAP | High-intent inbound |
| 7 | Reply: existing client — LinkedIn content automation upsell | P2 | 2026-05-07 | Existing relationship — lower urgency |
| 8 | Launch website / landing page | P2 | 2026-05-15 | 12 days — start this week |
| 9 | Build invoice template | P2 | 2026-05-15 | Pricing locked — unblocked |
| 10 | Build audit template | P2 | 2026-05-15 | Needed before close |
| 11 | Close first paying clients | P2 | 2026-05-15 | Follows from quote replies above |
| 12 | Define Q2 goals collaboratively | P3 | — | Important — not this week |

---

#### Day-by-Day Plan

| Day | Focus | Tasks (max 3 P1) |
|-----|-------|-----------------|
| Sun 2026-05-03 | Plan + prep | Weekly plan (this). Pre-draft replies for Monday. |
| Mon 2026-05-04 | Client replies — batch 1 | Reply: CRM quote laboratoiremvcd. Reply: CRM quote biovagoabdorag. Reply: AAA Audit — propose walkthrough call. |
| Tue 2026-05-05 | Client replies — batch 2 | Reply: client returning — comms automation. Reply: referral from Hicham — quote. Reply: LinkedIn inbound — SDR intro call. |
| Wed 2026-05-06 | Upsell + build | Reply: LinkedIn content upsell (existing client). Begin invoice template. Begin website structure. |
| Thu 2026-05-07 | Build | Build audit template. Continue website. |
| Fri 2026-05-08 | Build + review | Website push. Review all lead statuses. Flag non-responders. |
| Weekend buffer | Catch-up | Slip tasks only. |

---

#### What Success Looks Like by Sunday 2026-05-10

- All 6 inbound threads replied to — leads advanced
- AAA Audit walkthrough call booked
- Invoice template built
- Audit template in draft
- Website 60%+ complete
- Upsell conversation with existing client opened

---

## Skills Reference

When a blocker or gap is identified during weekly planning, apply the relevant skill before proceeding.

| Blocker / Gap | Skill to Apply | When |
|---------------|---------------|------|
| Pricing not defined | `pricing-strategy` | Before quoting any client |
| Launch plan needed | `launch-strategy` | Any product or service launch |
| Revenue pipeline stalled | `revops` | When leads go cold or pipeline is unclear |
| Content for LinkedIn / outreach | `social-content` or `copywriting` | Pre-launch and ongoing |
| Landing page not converting | `page-cro` | Post-launch, first 30 days |
| Email outreach needed | `cold-email` | When direct outreach is a weekly action |
| Quote or proposal needed | `sales-enablement` | Before sending any formal proposal |
| Build task needs decomposing before execution | `writing-plans` | When a P2 build task (template, website, script) is about to start — decompose it into granular steps first |
| Plan written and ready to step through | `executing-plans` | When running a written plan task-by-task with checkpoints and defined stopping conditions |

### Skills Applied This Week (2026-05-03)

| Skill | Output | File |
|-------|--------|------|
| `pricing-strategy` | Pricing structure for all degiabdo services | intel/pricing.md |
| `launch-strategy` | 12-day sprint plan to 2026-05-15 launch | references/playbooks/launch-plan-2026-05-15.md |

---
