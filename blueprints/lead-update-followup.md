# Blueprint — Lead Update + Follow-up Email

**Goal:** Update a lead's pipeline record in the Google Sheet, then draft a professional follow-up email to the contact. Designed for leads in active stages (Quote sent, Discovery booked, Audit in progress).

**Route:** Google Drive MCP (reads Sheets + Docs) + Zapier Google Sheets (writes) + Gmail MCP (email drafts).

**Trigger:** On demand. Say: "Run lead update and follow-up for [Lead Name]."

---

## Inputs Required

| Input | Example |
|-------|---------|
| Lead name | Foster & Marsh Legal |
| Contact name | James Foster |
| Deal value (USD) | 12,000 |
| Email subject context | Follow-up on sent sales proposal |
| Identity document ID | 1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c |
| Pipeline Sheet ID | 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc |
| Pipeline worksheet | Sheet1 |

**Before starting:** confirm all inputs are provided. If any are missing, stop and ask.

---

## Step 1 — Read the Pipeline Sheet

Call `mcp__claude_ai_Google_Drive__read_file_content` with the pipeline sheet ID.

- Locate the row where `company` matches the lead name.
- Record: row number, `email`, `stage`, `last_contact`, `next_step`, `notes`.
- If the lead is not found: stop. Report: "Lead [name] not found in the pipeline sheet."

---

## Step 2 — Write the Pipeline Update

Use `execute_zapier_write_action` (app: `google sheets`, action: `update_row`) to update the row found in Step 1.

**Params to pass:**
```
spreadsheet: 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc
worksheet:   Sheet1
row:         [row number from Step 1]
last_contact: [TODAY'S DATE — YYYY-MM-DD]
next_step:   Follow-up email sent — expecting response within 48 hours
notes:       [existing notes] | [TODAY'S DATE] - Q2 Proposal Follow-up
```

- If the write succeeds: continue.
- If it fails: report the exact error. Do not retry without confirmation.

---

## Step 3 — Read the Identity Document

Call `mcp__claude_ai_Google_Drive__read_file_content` with the identity document ID.

Extract:
- Agency trading name
- Founder name and role
- Primary email
- Phone number
- Website

These populate the email signature. If the document is not found: stop. Report the error.

---

## Step 4 — Draft the Follow-up Email

**Tone rules (always apply):**
- Professional but warm — not stiff, not casual
- Lead with value — one clear benefit, plain language
- Light urgency — capacity or timing, never pressure
- One clear ask — a specific call time or a yes/no question
- No jargon, no filler, no corporate speak

**Email structure:**
1. Brief opening — reference the proposal without being needy
2. Value reiteration — one sentence, outcome-focused, plain language
3. Light urgency — capacity window or natural deadline, low pressure
4. Single CTA — offer a 15-minute call with specific day options
5. Signature — from identity document

**Draft the email, then call `mcp__claude_ai_Gmail__create_draft`** with:
- `to`: contact's email address (from the sheet)
- `subject`: as instructed by Abderrahim, or a professional equivalent
- `body`: the drafted email (plain text)

**NEVER send.** Always save as draft only. Report the Gmail draft ID.

---

## Step 5 — Report

At the end of the run, output:

```
## Lead Update + Follow-up — [Lead Name] — [DATE]

### Pipeline sheet
[x] Row found: [lead name], row [N], stage: [stage]
[x] Sheet updated:
    - last_contact → [DATE]
    - next_step → Follow-up email sent — expecting response within 48 hours
    - notes → [updated notes string]

### Email
[x] Draft created — Gmail draft ID: [ID]
[x] To: [email]
[x] Subject: [subject]

Review the draft in Gmail before sending.
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Lead not found in sheet | Stop. Report: "Lead [name] not found. Check spelling or run a manual search." |
| Zapier write fails | Report exact error. Do not retry without confirmation. |
| Identity doc not found | Stop. Report: "Identity document not readable. Check file ID and permissions." |
| Gmail draft creation fails | Report the exact error. Do not retry without confirmation. |
| Email address missing from sheet | Stop. Ask Abderrahim to confirm the contact's email before proceeding. |

---

## After Running

If anything broke and was fixed, log it here:

## Lessons Learned
- 2026-04-29 — Zapier Google Sheets `update_row` requires auth at first use. Auth URL: https://mcp.zapier.com/mcp/servers/00e75c81-0d38-4d8e-981a-dd0895e98f9a/app-auth/GoogleSheetsV2CLIAPI — auth is persistent, only needed once.
- 2026-04-29 — Worksheet name is "Sheet1". Columns map to: H=last_contact, I=next_step, J=notes.
