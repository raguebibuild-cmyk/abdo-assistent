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

Read both files in parallel:

1. `live/state.md` — extract:
   - Open tasks (with due dates)
   - Overdue items
   - Any calls or events logged for today
   - Current priorities

2. `intel/focus.md` — extract:
   - Top priorities right now
   - Hard deadlines

---

### Step 2 — Check today's calendar

Call `mcp__claude_ai_Google_Calendar__list_events` with:
- `calendarId`: primary
- `timeMin`: today at 00:00 (ISO 8601, local time GMT+1)
- `timeMax`: today at 23:59 (ISO 8601, local time GMT+1)

Extract: event titles, start times, attendees (if any), and any description/notes.

If no events: note "Calendar clear today."

---

### Step 3 — Scan Gmail for overnight urgents

Call `mcp__claude_ai_Gmail__search_threads` with query:
`is:unread newer_than:16h -category:promotions -category:social`

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

## Failure Handling

| Failure | Response |
|---------|----------|
| Calendar read fails | Note "Calendar unavailable" and continue with state.md data only |
| Gmail scan fails | Note "Gmail scan failed" and continue without the overnight email section |
| live/state.md has no open tasks | Note "No open tasks in state.md — may need updating" |
| More than 5 urgent items | List top 3, then: "X more overdue items — check state.md" |

---

## After Running

No file updates required. The briefing is a read-only operation.

If the briefing reveals tasks that aren't in live/state.md, flag them: "These items appeared in the briefing but aren't in state.md — should I add them?"

## Lessons Learned

*(Append after each run if anything needed adjusting)*

| Date | Issue | Fix |
|------|-------|-----|
