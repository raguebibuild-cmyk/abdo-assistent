# Blueprint — Weekly Sales Pipeline Review

**Type:** Blueprint only — Architect reads sources and outputs inline
**Sources:** Gmail (client/lead threads, past 7 days), live/state.md, leads/qualified/, leads/contacted/
**Voice:** Internal — direct, no pleasantries
**Output:** Inline ranked action list — no Doc created, no email drafted

**Schedule:** Every Monday at 08:30 GMT+1. Trigger manually with: "Weekly pipeline review" or "Pipeline review."

---

## Goal

Start every week with one clear view of the commercial pipeline: who needs a reply, what's overdue,
what quotes are floating, and which leads haven't been contacted yet. Output a ranked action stack
for the week — P1 items get done today, P2 this week.

---

## Sequence

### Step 1 — Read state.md

Read `live/state.md` and extract:
- All items listed under **Open Tasks** — note which are flagged `[OVERDUE]`
- Active projects and their status
- Current priorities

---

### Step 2 — Scan Gmail for unread client and lead threads

Call `mcp__claude_ai_Gmail__search_threads` with query:
`is:unread newer_than:7d -category:promotions -category:social -category:updates`

For each thread, determine if the sender is a client, lead, or unknown. Filter to:
- Threads requiring a reply, decision, or action
- Ignore automated notifications, newsletters, order confirmations

Cap at 10 threads. If more arrive, note "X more unread — review inbox."

For each actionable thread extract: sender name, subject, one-line summary of what they need.

---

### Step 3 — Check open quotes and audits

Read `live/state.md` again (already in memory from Step 1) and cross-reference with the Open Tasks list:
- Any item mentioning "quote", "proposal", or "audit" that has no completion marker
- Note the client name, amount (if visible), and how long it's been open

---

### Step 4 — Check uncontacted qualified leads

List all files in `leads/qualified/`. Then list all files in `leads/contacted/`.

Any file that appears in `leads/qualified/` but NOT in `leads/contacted/` is an uncontacted lead.
Report count and names.

---

### Step 5 — Synthesise and output

Output in this exact format:

```
## Pipeline Review — [WEEK OF DATE]

### P1 — Do today
[Overdue items + any client/lead thread older than 3 days requiring reply]
- [Client/Lead name] — [what they need] — [overdue by X days if applicable]
[If nothing:] No P1 items. Good shape.

### P2 — Do this week
[Quotes and audits open + uncontacted leads + unread threads from past 3 days]
- [Item] — [context / what the action is]
[Max 7 items — most commercially valuable first]

### Open quotes
[List: client name — amount — days open]
[If none:] No open quotes.

### Uncontacted qualified leads
[Count + names from leads/qualified/ not yet in leads/contacted/]
[If none:] All qualified leads contacted.

### Gmail — unread client threads
[List: sender — subject — one-line what they need]
[If none:] Inbox clear of client threads.
```

Rules:
- P1 = anything overdue or a client reply outstanding more than 72 hours
- P2 = everything else that needs action this week
- Keep each bullet to one line
- No P1 item should appear again in P2
- Total output: under 40 lines

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Gmail scan fails | Note "Gmail unavailable" — continue with state.md items only |
| leads/qualified/ or leads/contacted/ empty or unreadable | Note "Leads folders unreadable" — skip Step 4 |
| live/state.md has no open tasks | Note "state.md shows no open tasks — may need updating" |
| More than 10 P1 items | List the 5 highest priority and note "X more overdue — check state.md" |

---

## After Running

No file updates required. Read-only operation.

If the review surfaces items missing from `live/state.md`, flag them: "These items appeared in the
review but aren't tracked in state.md — should I add them?"

## Lessons Learned

*(Append after each run if anything needed adjusting)*

| Date | Issue | Fix |
|------|-------|-----|
