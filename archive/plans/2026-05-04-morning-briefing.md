# Morning Briefing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a morning briefing workflow that scans Google Calendar, live/state.md, intel/focus.md, and Gmail, then outputs a structured daily digest — what's on today, what's urgent, and what to do first.

**Architecture:** Blueprint-only. The Architect reads four sources, synthesises them into a prioritised briefing, and outputs it directly in the conversation. No Google Doc created, no Gmail draft — this is a read-and-report workflow. Takes under 60 seconds to run.

**Tech Stack:** Google Calendar MCP, Gmail MCP, Google Drive MCP (for state files), Markdown blueprint, Claude (Architect)

---

## Scope Note

The morning briefing is a daily orientation tool — not a full weekly planning session (that's `blueprints/prioritisation.md`). It answers three questions: What's happening today? What's urgent right now? What should I do first?

It does not replace the weekly plan. It references it.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `blueprints/morning-briefing.md` | Master SOP: scan sources, synthesise, output briefing |
| Modify | `live/state.md` | Add morning-briefing to Skills Built table |

No template needed — output is generated inline, not from a template.

**Requires approval before creating the Blueprint** — `permissions.md`: "Create a new Blueprint: Ask first — always."

---

## Task 1: Morning Briefing Blueprint

**Requires approval before starting** — ask: "Ready to create `blueprints/morning-briefing.md`?" Wait for confirmation.

**Files:**
- Create: `blueprints/morning-briefing.md`
- Modify: `live/state.md`

- [ ] **Step 1: Get approval**

Ask Abderrahim: "Ready to create the morning briefing blueprint? It will scan Calendar, live/state.md, focus.md, and Gmail each morning and output a structured daily digest."

Wait for explicit confirmation.

- [ ] **Step 2: Write the Blueprint**

Create `blueprints/morning-briefing.md` with this exact content:

````markdown
# Blueprint — Morning Briefing

**Type:** Blueprint only — Architect reads sources and outputs inline
**Sources:** Google Calendar, live/state.md, intel/focus.md, Gmail (unread, urgent)
**Voice:** Internal — direct, no pleasantries
**Output:** Inline text in the conversation — no Doc created, no email drafted

**Trigger:** At the start of any working day. Say: "Morning briefing" or "Good morning."

---

## Goal

Answer three questions in under 60 seconds of reading:
1. What's on today?
2. What's urgent right now?
3. What should I do first?

---

## Sequence

### Step 1 — Read local state files

Read both files:

1. `live/state.md` — extract:
   - Open tasks (with due dates)
   - Overdue items
   - This week's calls (today's entries specifically)
   - Current priorities

2. `intel/focus.md` — extract:
   - Top priorities right now
   - Hard deadlines

---

### Step 2 — Check today's calendar

Call `mcp__claude_ai_Google_Calendar__list_events` with:
- `calendarId`: primary
- `timeMin`: today at 00:00 (ISO 8601, local time)
- `timeMax`: today at 23:59 (ISO 8601, local time)

Extract: event titles, start times, attendees (if any), and any description/notes.

If no events: note "Calendar clear today."

---

### Step 3 — Scan Gmail for overnight urgents

Call `mcp__claude_ai_Gmail__search_threads` with query:
`is:unread newer_than:16h -category:promotions -category:social`

This catches emails that arrived since yesterday afternoon.

Extract actionable threads only — ignore newsletters, notifications, automated emails, and security alerts. A thread is actionable if it requires a reply, decision, or action from Abderrahim.

If no actionable threads: note "No new urgent emails overnight."

Cap at 5 threads maximum. If more than 5 arrive, list the top 5 by apparent urgency and note "X more threads — review inbox."

---

### Step 4 — Synthesise and output

Output the briefing in this exact format:

```
## Morning Briefing — [DAY, DATE]

### Today
[List calendar events in chronological order]
- [TIME] — [Event title] [attendees if relevant]
[If no events:] Calendar clear.

### Urgent — do these first
[List only P1 items: overdue tasks + tasks due today + urgent overnight emails]
[Format: - [context] — [what to do]]
[If nothing urgent:] No urgent items.

### Open this week
[List P2 items from state.md that are due this week but not today]
[Keep to 5 items max — most important first]

### Overnight email
[List actionable unread threads]
- [Sender / subject] — [one line: what they need]
[If none:] Inbox quiet overnight.

### Focus reminder
[One line — the single most important thing from intel/focus.md today]
```

Rules for the output:
- No more than 3 P1 items in "Urgent" — if there are more, list the top 3 and note "X more overdue items"
- "Open this week" should have no more than 5 items
- Each bullet is one line maximum — no paragraphs
- If today has a call: flag it at the top of "Today" with the time and who it's with
- Total briefing length: under 30 lines

---

## Output Example

```
## Morning Briefing — Monday, 4 May 2026

### Today
- 14:00 — Nadia, Kontrast Personalberatung — LinkedIn automation upsell call

### Urgent — do these first
- CRM quote replies overdue (laboratoiremvcd, biovagoabdorag) — reply today
- Deliver audit — Najim Travel — overdue, unblocked
- AAA Workflow Audit — propose deliverable walkthrough call

### Open this week
- Reply: referral from Hicham — construction firm quote
- Reply: inbound LinkedIn lead — SDR intro call
- Reply: Nadia — LinkedIn content upsell (existing client)
- Build invoice template — due 2026-05-15
- Begin website structure — due 2026-05-15

### Overnight email
- Inbox quiet overnight.

### Focus reminder
Close first paying clients by 2026-05-15 — degiabdo launch is 11 days away.
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Calendar read fails | Note "Calendar unavailable" and continue with state.md data only |
| Gmail scan fails | Note "Gmail scan failed" and continue without the overnight email section |
| live/state.md has no open tasks | Note "No open tasks in state.md — may need updating" |
| More than 5 urgent items | List top 3, then: "⚠️ [N] more overdue items — check state.md" |

---

## After Running

No file updates required. The briefing is a read-only operation.

If the briefing reveals tasks that aren't in live/state.md, flag them: "These items appeared in the briefing but aren't in state.md — should I add them?"

## Lessons Learned
[Append after each run if anything needed adjusting]
````

- [ ] **Step 3: Dry-run the Blueprint verbally**

Walk through each step using today's actual context (2026-05-04):

| Step | Expected output | Passes? |
|------|----------------|---------|
| Step 1: state files | From live/state.md: 9 open tasks, today's call = Nadia 14:00, priorities = clients + website + pricing | [ ] |
| Step 2: calendar | Today's event: Nadia / Kontrast 14:00 LinkedIn upsell call | [ ] |
| Step 3: Gmail scan | Any unread threads from overnight — or "inbox quiet" | [ ] |
| Step 4: output | Briefing under 30 lines, correct format, no paragraphs, call flagged at top of Today section | [ ] |

Confirm the output is fast to read and clearly answers: what's on, what's urgent, what to do first.

- [ ] **Step 4: Update live/state.md**

Add to Skills Built table:

```
| Morning briefing | blueprints/morning-briefing.md | None (Google Calendar + Gmail + Google Drive MCP) |
```

- [ ] **Step 5: Commit**

```bash
git add blueprints/morning-briefing.md live/state.md
git commit -m "feat: add morning briefing blueprint"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|-------------|------|
| Daily digest | Blueprint outputs one structured block per run |
| Calendar | Blueprint Step 2 — Google Calendar MCP, today's events only |
| Open tasks | Blueprint Step 1 — live/state.md |
| Priorities | Blueprint Step 1 — intel/focus.md, surfaced in Focus reminder |
| Urgency filtering | Blueprint Step 4 — P1 items only in "Urgent" section, max 3 |
| Under 60 seconds | Steps 1-3 are parallel reads; output is template-driven with length cap |
| Overnight email | Blueprint Step 3 — Gmail, last 16 hours, actionable only |

### Placeholder scan

No TBDs. Output format is fully specified with an example. All MCP call parameters are defined. Length limits are explicit (30 lines, 5 items, 3 urgent).

### Type consistency

- Calendar call uses `list_events` — consistent with Google Calendar MCP tool naming
- Gmail call uses `search_threads` — consistent with Gmail MCP tool naming
- Output format matches the example exactly — no drift between Steps 4 and the example

---

*Plan written: 2026-05-04*
