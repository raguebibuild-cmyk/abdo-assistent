# Blueprint — Invoice Creation

**Type:** Blueprint + Equipment (invoice_pdf.py) + Drive/Gmail MCPs  
**Template:** `templates/invoice.md`  
**Voice rules:** `.claude/rules/clients.md`  
**Pipeline Sheet ID:** 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc  
**Pricing Sheet ID:** 1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI  
**Identity Doc ID:** 1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c  

**Trigger:** When work has been delivered and it's time to bill. Say: "Create invoice for [Client Name]."

---

## Goal

Generate a professional branded PDF invoice, save it to `invoices/`, create a Google Doc copy in Drive, and draft a Gmail ready to send. One run. Never send without Abderrahim reviewing first.

---

## Required Inputs

| Input | Source |
|-------|--------|
| Client name | Spoken |
| Invoice line items | Spoken — item description, qty, unit price per line |
| Billing period | Spoken — e.g. "May 2026" |
| Invoice status | Spoken — "Due" (default) or "Paid" |
| Client Drive folder ID | From onboarding run — or search Drive for "Client — [Name]" |

If the client folder ID is unknown: call `mcp__claude_ai_Google_Drive__search_files` with query `name contains "Client — [ClientName]"`. Record the Invoices/ subfolder ID from the results.

If pricing amounts are not confirmed: stop. "What amounts should this invoice include? I won't draft without confirmed numbers."

---

## Sequence

### Step 1 — Read all three sources in parallel

Call `mcp__claude_ai_Google_Drive__read_file_content` three times simultaneously:

1. **Pipeline sheet** — find client row. Record: contact name, contact email, deal value, package, stage, region.
2. **Pricing sheet** — match the package from pipeline notes. Record: setup amount, monthly amount.
3. **Identity doc** — extract: legal name, bank name, IBAN, BIC/SWIFT, tax number.

If any read fails: stop. Report which source failed and its ID.  
If client is not in pipeline: stop. "Client [name] not found in pipeline."

---

### Step 2 — Calculate invoice amounts

From the spoken line items and the pricing sheet data:

- Each line: description, qty, unit price, amount (qty × unit price)
- Subtotal = sum of all line amounts
- Tax = Subtotal × 0.05 (apply only for UAE-based clients — check pipeline for region)
- Total = Subtotal + Tax
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
| `Status` | "Paid" or "Due" (as spoken — default Due) |
| Line item rows | One row per item: description \| qty \| €unit_price \| €amount |
| `[subtotal]` | Calculated subtotal |
| `[tax_amount]` | Subtotal × 0.05 (or €0.00 if non-UAE) |
| `[total]` | Subtotal + Tax |
| `[bank_name]` | From identity doc |
| `[IBAN]` | From identity doc |
| `[BIC]` | From identity doc |
| `[vat_number]` | From identity doc — used as "Tax registration" |

Do not leave any `[bracket]` placeholder in the output.

---

### Step 4 — Generate the branded PDF

Save the populated invoice content to:
```
invoices/INV-[YYYY-MM-DD]-[ClientName].md
```
Where `[ClientName]` = company name with spaces replaced by hyphens (e.g. Cedar-Wealth-Advisory).

Then run:
```bash
python equipment/invoice_pdf.py "invoices/INV-[YYYY-MM-DD]-[ClientName].md" "invoices/INV-[YYYY-MM-DD]-[ClientName].pdf"
```

**Behaviour by status:**
- `Status: Due` — clean branded PDF
- `Status: Paid` — same layout with a bold diagonal **PAID** watermark in green over every page

Record the PDF path. Confirm the script printed `Invoice PDF: invoices/...` with no errors before continuing.

---

### Step 5 — Create the Google Doc (source of truth)

Call `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: `Invoice_[ClientCode]_[YYYYMMDD]`
- `contentMimeType`: `text/plain`
- `disableConversionToGoogleType`: false (convert to Google Doc)
- `textContent`: populated invoice text from Step 3
- `parentId`: client's Invoices/ subfolder ID

Record the returned file URL and file ID.

If creation fails: report the exact error. Do not continue to Step 6.

---

### Step 6 — Draft the Gmail

```
Subject: Invoice [INV-CLIENT_CODE-YYYYMMDD] — [service description]

Hi [Contact first name],

Please find your invoice attached.

Amount due: €[total]
Due date: [DUE_DATE]

Payment details are in the attached PDF. You can also view it online: [Google Doc URL]

Any questions, just reply here.

Abderrahim
degiabdo
```

Call `mcp__claude_ai_Gmail__create_draft` with:
- `to`: contact email from pipeline
- `subject`: `Invoice [INV-CLIENT_CODE-YYYYMMDD] — [service description]`
- `body`: above text (plain text)

Never send. Save as draft only. Record the Gmail draft ID.

Note: manually attach the PDF (`invoices/INV-[YYYY-MM-DD]-[ClientName].pdf`) before sending — Gmail MCP creates text drafts only.

---

### Step 7 — Report

```
## Invoice Created — [Client Name] — [DATE]

[x] Sources read: pipeline, pricing, identity
[x] Line items: [n] items
    Subtotal: €[subtotal] | Tax: €[tax] | Total: €[total]
[x] PDF: invoices/INV-[YYYY-MM-DD]-[ClientName].pdf
    Status: [Due / Paid] [— PAID watermark applied if Paid]
[x] Google Doc: [URL]
    Saved to: Client — [Name]/Invoices/
[x] Gmail draft saved — subject: Invoice [invoice number]
    Draft ID: [ID]

Review the PDF and the Gmail draft before sending.
Attach the PDF to the Gmail draft before sending.
Due date: [DUE_DATE].
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Client not found in pipeline | Stop. "Client [name] not found. Check spelling." |
| Pricing not confirmed | Stop. "What amounts should this invoice include?" |
| Any source read fails | Stop. Report which source and its ID. |
| Client Invoices folder not found | Search Drive for "Client — [Name]". If still not found, ask for the folder ID. |
| invoice_pdf.py fails | Report exact error. Do not continue. |
| Google Doc creation fails | Report exact error. Do not continue. |
| Gmail draft fails | Report exact error. Log the Google Doc URL and PDF path. |

---

## Invoicing Rules

- Always include both setup and monthly when it's the first invoice
- Pricing in euros (€) unless client explicitly requested local currency
- Tax at 5% for UAE clients only — check pipeline for region
- Due date is always 30 days from invoice date
- Never send the invoice directly — Abderrahim reviews all outbound invoices
- Status defaults to "Due" — only set "Paid" when explicitly instructed

## Lessons Learned

*(Append after each run)*

| Date | Issue | Fix |
|------|-------|-----|
