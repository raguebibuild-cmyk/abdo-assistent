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

Do not leave any `[bracket]` placeholder in the output.

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

```
Subject: Invoice [INV-CLIENT_CODE-YYYYMMDD] — [service description]

Hi [Contact first name],

Please find your invoice via the link below.

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

## Invoicing Rules

- Always include both setup and monthly when it's the first invoice
- Pricing in euros (€) unless client explicitly requested local currency
- VAT at 5% for UAE clients only — check pipeline for region
- Due date is always 30 days from invoice date
- Never send the invoice directly — Abderrahim reviews all outbound invoices

## Lessons Learned

*(Append after each run)*

| Date | Issue | Fix |
|------|-------|-----|
