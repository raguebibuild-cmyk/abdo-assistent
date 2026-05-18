# Blueprint — Client Onboarding

**Type:** Blueprint only — Architect executes via Google Drive + Gmail + Zapier Sheets MCP
**Templates:** `templates/onboarding-welcome-email.md`, `templates/discovery-call-notes.md`
**Voice rules:** `.claude/rules/voice.md`, `.claude/rules/clients.md`
**Pipeline Sheet ID:** 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc
**Clients Drive folder ID:** Resolved at runtime (search Drive for "Clients" folder)

**Trigger:** When a deal is confirmed as Won. Say: "Run onboarding for [Client Name]."

---

## Goal

Take a won deal from confirmed to fully active client in one run:
1. Confirm deal status in the pipeline
2. Create a client folder structure in Google Drive
3. Draft the welcome email in Gmail
4. Update the pipeline stage to Active

---

## Required Inputs

| Input | Where |
|-------|-------|
| Client name | Spoken — or from pipeline |
| Contact first name | Pipeline row |
| Contact email | Pipeline row |
| Package or scope | Pipeline notes |

If the contact email is missing from the pipeline: stop and ask before proceeding to Step 3.

---

## Pre-condition Check

The deal must be at stage Won before onboarding runs. If stage is anything else: stop.

"[Client name]'s deal is at stage [X], not Won. Confirm the deal is closed before running onboarding."

---

## Sequence

### Step 1 — Read the pipeline

Call `mcp__claude_ai_Google_Drive__read_file_content` with pipeline sheet ID:
`1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc`

Find the row where `company` matches the client name. Record:
- Row number
- Contact name and email
- Deal value (USD)
- Stage
- Package (from notes column)

If stage is not Won: stop. Report the current stage. Do not continue.
If client is not found: stop. Report: "[Client name] not found in pipeline. Check spelling or search manually."

---

### Step 2 — Create client Drive folder structure

Resolve the master Clients Drive folder:
- Call `mcp__claude_ai_Google_Drive__search_files` with query `name = "Clients" and mimeType = "application/vnd.google-apps.folder"`
- If found: record the folder ID as `[CLIENTS_FOLDER_ID]`
- If not found: create it with `mcp__claude_ai_Google_Drive__create_file` (mimeType: `application/vnd.google-apps.folder`, name: `Clients`). Record the returned ID.

Then create three items in sequence (each depends on the previous):

**2a — Master folder:**
- `name`: `Client — [ClientName] — [YYYY-MM-DD]`
- `mimeType`: `application/vnd.google-apps.folder`
- `parentId`: `[CLIENTS_FOLDER_ID]`

Record the returned file ID as `[MASTER_FOLDER_ID]`.

**2b — Deliverables subfolder:**
- `name`: `Deliverables`
- `mimeType`: `application/vnd.google-apps.folder`
- `parentId`: `[MASTER_FOLDER_ID]`

**2c — Invoices subfolder:**
- `name`: `Invoices`
- `mimeType`: `application/vnd.google-apps.folder`
- `parentId`: `[MASTER_FOLDER_ID]`

Record the master folder URL: `https://drive.google.com/drive/folders/[MASTER_FOLDER_ID]`

If any creation fails: stop. Report the exact error and which folder failed.

---

### Step 3 — Draft the welcome email

Open `templates/onboarding-welcome-email.md`. Populate:
- `[First name]` → contact first name from pipeline
- `[One sentence confirming what's been agreed]` → plain-language description of the package, including the concrete outcome it achieves
- `[Key milestone]` → standard delivery window for the package (check `intel/pricing.md`)

Call `mcp__claude_ai_Gmail__create_draft` with:
- `to`: contact email from pipeline
- `subject`: `Welcome — here's how we get started`
- `body`: populated email (plain text)

Never send. Save as draft only. Record the Gmail draft ID.

If Gmail draft creation fails: report the error and the already-created folder URL. Stop.

---

### Step 4 — Update pipeline to Active

Call `execute_zapier_write_action` (app: `google sheets`, action: `update_row`) to update the pipeline row found in Step 1:

```
stage:         Active
last_contact:  [TODAY — YYYY-MM-DD]
next_step:     Welcome email drafted — pending Abderrahim review and send
notes:         [existing notes] | [TODAY] — Onboarding started. Drive folder: [master folder URL]
```

If the write fails: report the exact error. Do not retry without confirmation.

---

### Step 5 — Report

Output this block exactly:

```
## Client Onboarding — [Client Name] — [DATE]

[x] Pipeline confirmed: [Client name] — stage: Won → Active
[x] Drive folder created: [Master folder URL]
    ├── Deliverables/
    └── Invoices/
[x] Welcome email draft saved — subject: "Welcome — here's how we get started"
    Gmail draft ID: [ID]
[x] Pipeline updated: stage = Active, next_step logged

Next: review and send the Gmail draft. Then send the onboarding questionnaire link.
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Client not found in pipeline | Stop. "Client [name] not found. Check spelling or search the pipeline manually." |
| Stage not Won | Stop. "Deal is at stage [X]. Confirm the deal is closed before running onboarding." |
| Contact email missing from pipeline | Stop. "No email address for [contact name]. Provide the email and re-run." |
| Drive folder creation fails | Stop. Report which folder failed and the exact error. |
| Gmail draft creation fails | Report the error and the already-created folder URL. Stop. |
| Pipeline update fails | Report exact error. Do not retry without confirmation. Log the folder URL and draft ID so nothing is lost. |

---

## After Running

- Send the Gmail draft after Abderrahim reviews it
- Share the onboarding questionnaire with the client (if one exists)
- Save discovery call notes to the client's Drive folder under Deliverables/
- Create a corresponding folder in local `clients/{name}/` if not already present

## Lessons Learned

*(Append after each run — what failed, what needed adjusting, what worked)*

| Date | Issue | Fix |
|------|-------|-----|
