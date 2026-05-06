# Client Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the missing "Won → Active" onboarding layer — two templates and a master Blueprint that takes a confirmed deal to fully set-up client in one run.

**Architecture:** No Equipment needed. The Architect calls MCPs directly: Google Drive (create folders), Gmail (draft welcome email), Zapier Sheets (pipeline update). Templates feed the email draft and the discovery debrief. The Blueprint is the controller.

**Tech Stack:** Google Drive MCP, Gmail MCP, Zapier Google Sheets MCP, Markdown blueprints, Claude (Architect)

---

## Scope Note

The pre-onboarding arc (lead qualification → proposal → close) is already built:
- `blueprints/client-communication.md` — email drafting
- `blueprints/client-proposition.md` — proposition doc + email
- `blueprints/client-proposal-document.md` — full proposal from pipeline data
- `blueprints/lead-update-followup.md` — pipeline update + follow-up

This plan covers only what's missing: the transition from Won to Active.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `templates/discovery-call-notes.md` | Structured capture sheet for a discovery call — filled during or immediately after the call |
| Create | `templates/onboarding-welcome-email.md` | Welcome email shell for new clients — feeds the Gmail draft in the Blueprint |
| Create | `blueprints/client-onboarding.md` | Master SOP: confirms deal, creates Drive folder, drafts welcome email, updates pipeline to Active |
| Modify | `live/state.md` | Add client-onboarding to Skills Built table |

**Requires approval before creating the Blueprint** — `permissions.md`: "Create a new Blueprint: Ask first — always."

---

## Task 1: Discovery Call Notes Template

**Files:**
- Create: `templates/discovery-call-notes.md`

- [ ] **Step 1: Write the template**

Create `templates/discovery-call-notes.md` with this exact content:

```markdown
# Discovery Call — [Client Name]

**Date:** [YYYY-MM-DD]
**Contact:** [Name, Role]
**Company:** [Company name — industry — ~size in employees]
**Call duration:** [X min]

---

## Their Situation

**Current process (the pain):**
[How they handle this today — what's broken, slow, or costing time/money]

**Trigger for this call:**
[Why now — what changed, who referred them, what they saw or heard]

---

## What They Want

**Desired outcome:**
[What does "fixed" look like for them — in their words, not yours]

**Timeline:**
[When do they need this? Any hard deadlines?]

**Budget indication:**
[ ] No budget mentioned
[ ] Aligned with pricing (~AED [X])
[ ] Hesitation — address in proposal

---

## Fit Assessment

**Services that match:**
[ ] Workflow Audit
[ ] Growth package
[ ] Automation build
[ ] LinkedIn content automation
[ ] Other: ___

**Red flags or scope risks:**
[Anything that could complicate delivery — tech stack, team resistance, vague requirements, procurement process]

---

## Agreed Next Step

[ ] Sending proposal by [DATE]
[ ] Booking follow-up call — [DATE / TIME]
[ ] They're sending more info — expected by [DATE]
[ ] Other: ___

---

## Post-Call Debrief

**What went well:**
[...]

**What to address in the proposal:**
[Any objection, concern, or open question to handle proactively in the proposal]

**Confidence level:**
[ ] High — likely to close
[ ] Medium — needs the right proposal
[ ] Low — may not be a fit, flag before investing more time
```

- [ ] **Step 2: Verify completeness**

Read the template. Confirm all of these are present:
- [ ] Client and contact identity fields
- [ ] Pain point capture (their situation)
- [ ] Outcome and timeline
- [ ] Budget signal with three-option checkbox
- [ ] Service fit checkboxes matching current degiabdo offers
- [ ] Agreed next step
- [ ] Post-call confidence rating

- [ ] **Step 3: Test with a recent call**

Fill in the template using one of this week's calls from memory — Nadia/Kontrast (2026-05-04 14:00) or Reem/Hala Ventures (2026-05-07 08:00). Confirm the structure captures everything needed to write a proposal without going back to notes.

- [ ] **Step 4: Commit**

```bash
git add templates/discovery-call-notes.md
git commit -m "feat: add discovery call notes template"
```

---

## Task 2: Welcome Email Template

**Files:**
- Create: `templates/onboarding-welcome-email.md`

- [ ] **Step 1: Write the template**

Create `templates/onboarding-welcome-email.md` with this exact content:

```markdown
# Welcome Email Template

**Stage:** Onboarding — send after deal is confirmed, before kick-off questionnaire
**Voice:** Professional but warm. Confident. One clear next step.
**Length target:** Under 150 words.

---

Subject: Welcome — here's how we get started

Hi [First name],

Great to have you on board. [One sentence confirming what's been agreed — the package and the outcome it will achieve. Example: "We're building your client onboarding automation — the goal is to cut your intake process from two days to under two hours."]

Here's what happens next:

- I'll send a short questionnaire — takes about 10 minutes to fill in
- Once that's back, we kick off within 48 hours
- [Key milestone — e.g. "You'll have the first workflow running within three weeks"]

Any questions before we start, just reply here.

Abderrahim
degiabdo

---

## Drafting Notes

When populating this template, confirm you have:
- [ ] Client first name
- [ ] Package name or a plain-language description of what's being built
- [ ] A concrete outcome (lift from pipeline notes or discovery call notes)
- [ ] A realistic timeline (check intel/pricing.md for standard delivery windows per package)

Do not send. Save as Gmail draft and flag for Abderrahim's review.
```

- [ ] **Step 2: Verify against voice rules**

Open `.claude/rules/voice.md`. Check the draft against every rule:
- [ ] No filler openers ("Great question!", "As you know...")
- [ ] No tech jargon
- [ ] Short paragraphs, straight to the point
- [ ] One clear ask at the end (questionnaire)
- [ ] Subject line describes the action, not the process
- [ ] Under 150 words in the email body

- [ ] **Step 3: Test draft with a real client**

Substitute Sahel Cafe Group (Growth package, comms automation, ~3-week delivery). Read the result aloud. Confirm it sounds like Abderrahim wrote it, not a template.

Expected output:

```
Subject: Welcome — here's how we get started

Hi [Contact first name],

Great to have you on board. We're building your client communications automation — the goal is to cut your team's manual follow-up time and keep every lead moving without things falling through the cracks.

Here's what happens next:

- I'll send a short questionnaire — takes about 10 minutes to fill in
- Once that's back, we kick off within 48 hours
- You'll have the first automated workflow running within three weeks

Any questions before we start, just reply here.

Abderrahim
degiabdo
```

Confirm: reads naturally, correct tone, one ask, under 150 words.

- [ ] **Step 4: Commit**

```bash
git add templates/onboarding-welcome-email.md
git commit -m "feat: add client onboarding welcome email template"
```

---

## Task 3: Client Onboarding Blueprint

**Requires approval before starting** — ask: "Tasks 1 and 2 are done. Ready to create `blueprints/client-onboarding.md`?" Wait for confirmation before proceeding.

**Files:**
- Create: `blueprints/client-onboarding.md`
- Modify: `live/state.md` (Skills Built table)

**Dependencies:** Tasks 1 and 2 must be complete and committed.

- [ ] **Step 1: Get approval**

Ask Abderrahim: "Tasks 1 and 2 are complete. Ready to create `blueprints/client-onboarding.md`? It will cover the full Won → Active sequence: pipeline confirm, Drive folder creation, welcome email draft, pipeline update to Active."

Wait for explicit confirmation. Do not proceed without it.

- [ ] **Step 2: Identify the Clients Drive folder ID**

Before writing the Blueprint, confirm the ID of the master "Clients" folder in Google Drive where per-client folders will be created.

Call `mcp__claude_ai_Google_Drive__search_files` with query: `name = "Clients" and mimeType = "application/vnd.google-apps.folder"`

If a "Clients" folder exists: record the ID. Use it in Step 3.

If no folder exists: create one now.
- Call `mcp__claude_ai_Google_Drive__create_file` with:
  - `name`: `Clients`
  - `mimeType`: `application/vnd.google-apps.folder`
- Record the returned file ID.

Report: "Clients folder ID: [ID]" — this ID goes into the Blueprint.

- [ ] **Step 3: Write the Blueprint**

Create `blueprints/client-onboarding.md` with this exact content (replace `[CLIENTS_FOLDER_ID]` with the ID from Step 2):

````markdown
# Blueprint — Client Onboarding

**Type:** Blueprint only — Architect executes via Google Drive + Gmail + Zapier Sheets MCP
**Templates:** `templates/onboarding-welcome-email.md`, `templates/discovery-call-notes.md`
**Voice rules:** `.claude/rules/voice.md`, `.claude/rules/clients.md`
**Pipeline Sheet ID:** 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc
**Clients Drive folder ID:** [CLIENTS_FOLDER_ID]

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

Call `mcp__claude_ai_Google_Drive__create_file` to build three items in sequence (each depends on the previous):

**2a — Master folder:**
- `name`: `Client — [ClientName] — [YYYY-MM-DD]`
- `mimeType`: `application/vnd.google-apps.folder`
- `parentId`: [CLIENTS_FOLDER_ID]

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

If any creation fails: stop. Report the exact error and which folder failed. Do not continue — the folder is needed for all future file saves for this client.

---

### Step 3 — Draft the welcome email

Open `templates/onboarding-welcome-email.md`. Populate:
- `[First name]` → contact first name from pipeline
- `[One sentence confirming what's been agreed]` → plain-language description of the package from pipeline notes, including the concrete outcome it achieves
- `[Key milestone]` → standard delivery window for the package (check `intel/pricing.md` for delivery timelines per package)

Call `mcp__claude_ai_Gmail__create_draft` with:
- `to`: contact email from pipeline
- `subject`: `Welcome — here's how we get started`
- `body`: populated email (plain text)

Never send. Save as draft only. Record the Gmail draft ID.

If Gmail draft creation fails: report the error. The folder was already created — log the folder URL and stop. Do not proceed to Step 4 without the draft confirmed.

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
| Drive folder creation fails | Stop. Report which folder failed and the exact error. The folder is a hard dependency — do not continue. |
| Gmail draft creation fails | Report the error and the already-created folder URL. Stop — do not update the pipeline until the draft is confirmed. |
| Pipeline update fails | Report exact error. Do not retry without confirmation. Log the folder URL and draft ID so nothing is lost. |

---

## After Running

- Send the Gmail draft after Abderrahim reviews it
- Share the onboarding questionnaire with the client (if one exists)
- Save discovery call notes to the client's Drive folder under Deliverables/

## Lessons Learned
[Append after each run — what failed, what needed adjusting, what worked]
````

- [ ] **Step 4: Dry-run the Blueprint verbally**

Walk through each step of the Blueprint using this hypothetical:
- Client: "Noor Beauty Group" (R.Abdo — call booked 2026-05-05 08:00)
- Package: assume Growth package, AED 14,680 + VAT
- Contact email: to be confirmed from pipeline

Check each step mentally:

| Step | Expected output | Passes? |
|------|----------------|---------|
| Step 1: pipeline read | Row found, stage = Won, contact data extracted | [ ] |
| Step 2a: master folder created | Folder `Client — NoorBeautyGroup — 2026-05-05` — URL returned | [ ] |
| Step 2b: Deliverables subfolder | Created under master | [ ] |
| Step 2c: Invoices subfolder | Created under master | [ ] |
| Step 3: welcome email draft | Draft in Gmail, subject "Welcome — here's how we get started" | [ ] |
| Step 4: pipeline update | Row updated — stage = Active, folder URL in notes | [ ] |
| Step 5: report | Clean summary, all links present | [ ] |

Flag any step that doesn't produce a clean expected output. Fix the Blueprint before committing.

- [ ] **Step 5: Update live/state.md**

In `live/state.md`, add this row to the Skills Built table:

```
| Client onboarding | blueprints/client-onboarding.md | None (Google Drive + Gmail + Zapier Sheets MCP) |
```

- [ ] **Step 6: Commit everything**

```bash
git add blueprints/client-onboarding.md live/state.md
git commit -m "feat: add client onboarding blueprint"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|-------------|------|
| Full arc from first contact to active client | Scoped to Won→Active (pre-onboarding arc already built) |
| Discovery call capture | Task 1 |
| Welcome email draft | Task 2 + Task 3 Step 3 |
| Client Drive folder creation | Task 3 Step 2 |
| Pipeline update to Active | Task 3 Step 4 |
| No send without review | Enforced in Template (Task 2) and Blueprint Step 3 |
| Failure handling at every step | Task 3 — Failure Handling table covers 6 failure modes |

### Placeholder scan

No TBDs, no "add appropriate error handling", no "similar to above." Every step contains the actual content.

One known gap: **Clients Drive folder ID** is determined at runtime in Task 3 Step 2, not hardcoded here. That's by design — it may not exist yet and must be retrieved or created first.

### Type consistency

- Pipeline Sheet ID used consistently: `1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc`
- MCP tool names match existing blueprints: `mcp__claude_ai_Google_Drive__read_file_content`, `mcp__claude_ai_Google_Drive__create_file`, `mcp__claude_ai_Gmail__create_draft`, `execute_zapier_write_action`
- Template file paths match what will be created in Tasks 1 and 2

---

*Plan written: 2026-05-04*
