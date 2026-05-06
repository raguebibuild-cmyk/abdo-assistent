# Invoice Creation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an invoice generation workflow that reads client and pricing data from three Drive sources, creates a formatted Google Doc invoice, and drafts a Gmail to the client — all in one run.

**Architecture:** Blueprint-only. Architect reads pipeline + pricing + identity in parallel, assembles invoice content, creates the Google Doc in the client's Invoices folder (created during onboarding), then drafts the Gmail. No Equipment needed — same pattern as client-proposal-document.md.

**Tech Stack:** Google Drive MCP, Gmail MCP, Markdown blueprint, Claude (Architect)

---

## Scope Note

This plan covers the invoice generation workflow only. Quote generation is a separate plan. The client onboarding plan creates the per-client Drive folder (including an Invoices/ subfolder) — this workflow writes into that subfolder.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `templates/invoice.md` | Invoice layout — feeds the Google Doc content |
| Create | `blueprints/invoice-creation.md` | Master SOP: read sources, build invoice, create Doc, draft email |
| Modify | `live/state.md` | Add invoice-creation to Skills Built table |

**Requires approval before creating the Blueprint** — `permissions.md`: "Create a new Blueprint: Ask first — always."

---

## Data Sources (already exist)

| Source | ID | What we read |
|--------|-----|--------------|
| Pipeline sheet | `1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc` | Contact name, email, package, deal value |
| Pricing sheet | `1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI` | Package line items, setup and monthly amounts |
| Identity doc | `1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c` | Bank details, VAT number, legal name |

---

## Task 1: Invoice Template

**Files:**
- Create: `templates/invoice.md`

- [ ] **Step 1: Write the template**

Create `templates/invoice.md` with this exact content:

```markdown
# Invoice

**From:** degiabdo — Abderrahim  
**To:** [Client Name / Company]  
**Invoice number:** INV-[CLIENT_CODE]-[YYYYMMDD]  
**Date:** [YYYY-MM-DD]  
**Due:** [DUE_DATE] (30 days from invoice date)  

---

## Services Rendered

| Service | Period | Amount |
|---------|--------|--------|
| [Service line 1 — e.g. "Growth CRM Setup"] | [Month YYYY] | €[amount] |
| [Service line 2 — e.g. "Monthly retainer"] | [Month YYYY] | €[amount] |

---

## Summary

| | |
|-|--|
| Subtotal | €[subtotal] |
| VAT (5%) | €[vat_amount] |
| **Total due** | **€[total]** |

---

## Payment Details

**Bank:** [bank_name from identity doc]  
**IBAN:** [IBAN from identity doc]  
**BIC / SWIFT:** [BIC from identity doc]  
**Payment reference:** INV-[CLIENT_CODE]-[YYYYMMDD]  

---

Payment terms: 30 days from invoice date.  
Late payment: 2% per month on overdue balances.  
VAT registration: [vat_number from identity doc]  

Questions? Reply to this email.

---

Abderrahim  
degiabdo
```

- [ ] **Step 2: Verify against invoicing requirements**

Read the template. Confirm:
- [ ] Invoice number follows format: `INV-[CLIENT_CODE]-[YYYYMMDD]`
- [ ] From / To / Date / Due fields are present
- [ ] Line items table has: service, period, amount
- [ ] Summary table has: subtotal, VAT, total
- [ ] Payment details section references all identity doc fields needed
- [ ] Payment reference matches the invoice number (for bank reconciliation)
- [ ] Late payment clause is present

- [ ] **Step 3: Test the template mentally**

Substitute: Sahel Cafe Group, Growth CRM package, setup €1,200 + first month €250, UAE client (5% VAT). Confirm the layout produces a clean, professional invoice.

Expected subtotal: €1,450. VAT: €72.50. Total: €1,522.50.

- [ ] **Step 4: Commit**

```bash
git add templates/invoice.md
git commit -m "feat: add invoice template"
```

---

## Task 2: Invoice Creation Blueprint

**Requires approval before starting** — ask: "Task 1 done. Ready to create `blueprints/invoice-creation.md`?" Wait for confirmation.

**Files:**
- Create: `blueprints/invoice-creation.md`
- Modify: `live/state.md`

**Dependencies:** Task 1 must be complete and committed.

- [ ] **Step 1: Get approval**

Ask Abderrahim: "Invoice template is done. Ready to create `blueprints/invoice-creation.md`? It will read pipeline + pricing + identity, generate a Google Doc invoice, and draft the Gmail — one run."

Wait for explicit confirmation.

- [ ] **Step 2: Write the Blueprint**

Create `blueprints/invoice-creation.md` with this exact content:

````markdown
# Blueprint — Invoice Creation

**Type:** Blueprint only — Architect executes via Google Drive + Gmail MCP
**Template:** `templates/invoice.md`
**Voice rules:** `.claude/rules/clients.md`
**Pipeline Sheet ID:** 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc
**Pricing Sheet ID:** 1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI
**Identity Doc ID:** 1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c

**Trigger:** When work has been delivered and it's time to bill. Say: "Create invoice for [Client Name]."

---

## Goal

Generate a complete invoice as a Google Doc and draft a Gmail to the client for review. One run. Never send without Abderrahim reviewing the draft first.

---

## Required Inputs

| Input | Source |
|-------|--------|
| Client name | Spoken |
| Invoice line items | Spoken — "setup fee + first month" or "monthly retainer for May" |
| Billing period | Spoken — e.g. "May 2026" |
| Client Drive folder ID | From onboarding run — or search Drive for "Client — [Name]" |

If the client folder ID is unknown: call `mcp__claude_ai_Google_Drive__search_files` with query `name contains "Client — [ClientName]"`. Record the Invoices/ subfolder ID from the results.

If pricing amounts are not confirmed: stop. "What amounts should this invoice include? I won't draft without confirmed numbers."

---

## Sequence

### Step 1 — Read all three sources in parallel

Call `mcp__claude_ai_Google_Drive__read_file_content` three times simultaneously:

1. **Pipeline sheet** — find client row. Record: contact name, contact email, deal value, package, stage.
2. **Pricing sheet** — match the package from pipeline notes. Record: setup amount, monthly amount.
3. **Identity doc** — extract: legal name, bank name, IBAN, BIC/SWIFT, VAT number.

If any read fails: stop. Report which source failed and its ID.

If client is not in pipeline: stop. "Client [name] not found in pipeline."

---

### Step 2 — Calculate invoice amounts

From the spoken line items and the pricing sheet data:

**Line items to include (confirm with Abderrahim if unclear):**
- Setup fee: €[setup from pricing sheet] — if this is the first invoice
- Monthly retainer: €[monthly from pricing sheet] — for [billing period]
- Or both, or just one — based on what was spoken

**Calculations:**
- Subtotal = sum of all line item amounts
- VAT = Subtotal × 0.05 (apply only for UAE-based clients — check pipeline for country/region)
- Total = Subtotal + VAT
- Due date = today's date + 30 days (YYYY-MM-DD)
- Client code = first 3 letters of company name, uppercase (e.g. SAH for Sahel Cafe Group)
- Invoice number = `INV-[CLIENT_CODE]-[YYYYMMDD]`

---

### Step 3 — Build invoice content

Open `templates/invoice.md`. Populate every placeholder:

| Placeholder | Value |
|-------------|-------|
| `[Client Name / Company]` | From pipeline |
| `[CLIENT_CODE]` | First 3 letters of company, uppercase |
| `[YYYYMMDD]` | Today's date, no dashes |
| `[YYYY-MM-DD]` (date) | Today's date |
| `[DUE_DATE]` | Today + 30 days |
| Service line 1 | First line item + period + amount |
| Service line 2 | Second line item if applicable |
| `[subtotal]` | Calculated subtotal |
| `[vat_amount]` | Subtotal × 0.05 (or 0 if non-UAE) |
| `[total]` | Subtotal + VAT |
| `[bank_name]` | From identity doc |
| `[IBAN]` | From identity doc |
| `[BIC]` | From identity doc |
| `[vat_number]` | From identity doc |

---

### Step 4 — Create the Google Doc

Call `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: `Invoice_[ClientCode]_[YYYYMMDD]`
- `contentMimeType`: `text/plain`
- `disableConversionToGoogleType`: false (convert to Google Doc)
- `textContent`: populated invoice text from Step 3
- `parentId`: client's Invoices/ subfolder ID

Record the returned file URL and file ID.

If creation fails: report the exact error. Do not continue to Step 5.

---

### Step 5 — Draft the Gmail

Draft the email body:

```
Subject: Invoice [INV-CLIENT_CODE-YYYYMMDD] — [service description]

Hi [Contact first name],

Please find your invoice attached via the link below.

Invoice: [Google Doc URL]
Amount due: €[total]
Due date: [DUE_DATE]

Payment details are included in the document. If you have any questions, just reply here.

Abderrahim
degiabdo
```

Call `mcp__claude_ai_Gmail__create_draft` with:
- `to`: contact email from pipeline
- `subject`: `Invoice [INV-CLIENT_CODE-YYYYMMDD] — [service description]`
- `body`: above text (plain text)

Never send. Save as draft only. Record the Gmail draft ID.

---

### Step 6 — Report

```
## Invoice Created — [Client Name] — [DATE]

[x] Sources read: pipeline, pricing, identity
[x] Amounts: subtotal €[subtotal] + VAT €[vat] = total €[total]
[x] Google Doc: [URL]
    Saved to: Client — [Name]/Invoices/
[x] Gmail draft saved — subject: Invoice [invoice number]
    Draft ID: [ID]

Review the Google Doc and the Gmail draft before sending.
Due date on invoice: [DUE_DATE].
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Client not found in pipeline | Stop. "Client [name] not found. Check spelling." |
| Pricing not confirmed | Stop. "What amounts should this invoice include?" |
| Any source read fails | Stop. Report which source and its ID. |
| Client Invoices folder not found | Search Drive for "Client — [Name]". If still not found, ask for the folder ID. |
| Google Doc creation fails | Report exact error. Do not continue. |
| Gmail draft fails | Report exact error. Log the Google Doc URL. |

---

## Invoicing Rules (from intel/pricing.md)

- Always include both setup and monthly when it's the first invoice
- Pricing in euros (€) unless client explicitly requested local currency
- VAT at 5% for UAE clients only — check pipeline for region
- Due date is always 30 days from invoice date
- Never send the invoice directly — Abderrahim reviews all outbound invoices

## Lessons Learned
[Append after each run]
````

- [ ] **Step 3: Dry-run the Blueprint verbally**

Walk through each step using: Sahel Cafe Group, Growth CRM setup (€1,200) + first month retainer (€250), May 2026, UAE client.

| Step | Expected output | Passes? |
|------|----------------|---------|
| Step 1: sources read | Pipeline: contact + email found. Pricing: Growth = €1,200 setup, €250/month. Identity: IBAN + VAT number extracted. | [ ] |
| Step 2: amounts | Subtotal €1,450. VAT €72.50. Total €1,522.50. Due date = today + 30 days. | [ ] |
| Step 3: content | All 14 placeholders in invoice.md filled. No [brackets] remaining. | [ ] |
| Step 4: Google Doc | File `Invoice_SAH_20260504` created in Sahel's Invoices/ folder. URL returned. | [ ] |
| Step 5: Gmail draft | Draft saved. Subject: "Invoice INV-SAH-20260504 — Growth CRM Setup + May Retainer". | [ ] |
| Step 6: report | Clean summary with URL, draft ID, total, due date. | [ ] |

Fix any step that doesn't produce a clean output before committing.

- [ ] **Step 4: Update live/state.md**

Add to Skills Built table:

```
| Invoice creation | blueprints/invoice-creation.md | None (Google Drive + Gmail MCP) |
```

- [ ] **Step 5: Commit**

```bash
git add blueprints/invoice-creation.md live/state.md
git commit -m "feat: add invoice creation blueprint"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|-------------|------|
| Automate generation from template | Template (Task 1) + Blueprint reads it and fills it |
| Pull pricing automatically | Blueprint Step 1 reads pricing sheet |
| Pull identity/bank details automatically | Blueprint Step 1 reads identity doc |
| Never send without review | Enforced in Blueprint Step 5 and Failure Handling |
| Correct VAT logic | Blueprint Step 2 — UAE only, explicitly flagged |
| Invoice number format | Blueprint Step 2 — INV-[CODE]-[YYYYMMDD] |

### Placeholder scan

No TBDs. All placeholders are defined with exact sources. One runtime dependency: client's Invoices/ subfolder ID — Blueprint Step 1 handles the search if unknown.

### Type consistency

- Pipeline Sheet ID, Pricing Sheet ID, Identity Doc ID match IDs used in `blueprints/client-proposal-document.md`
- MCP tool names match existing blueprints

---

*Plan written: 2026-05-04*
