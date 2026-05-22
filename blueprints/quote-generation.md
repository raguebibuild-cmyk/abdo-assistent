# Blueprint — Quote Generation

**Type:** Blueprint only — Architect executes via Google Drive + Gmail MCP
**Template:** `templates/quote.md`
**Pricing rules:** `intel/pricing.md`
**Voice rules:** `.claude/rules/voice.md`, `.claude/rules/clients.md`
**Pricing Sheet ID:** 1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI
**Identity Doc ID:** 1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c
**Output folder:** Client Propositions (ID: 1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2)

**Trigger:** When a prospect asks for pricing or is ready for a quote. Say: "Generate a quote for [Client Name] — [service] — [package]."

---

## Goal

Produce a clean, professional one-page quote as a Google Doc and draft a Gmail to the prospect with a link. One run. Never send without Abderrahim reviewing first.

---

## Required Inputs

| Input | Example |
|-------|---------|
| Client / prospect name | Nadia, Kontrast Personalberatung |
| Client email | nadia@kontrast.de |
| Service | Smart CRM Automation |
| Package | Growth |
| Founding client? | Yes / No (first 1–2 clients only — check intel/pricing.md) |

Confirm these before proceeding. If the service or package is ambiguous, present the options from `intel/pricing.md` and ask Abderrahim to select.

Do not quote a service not listed in `intel/pricing.md`. Stop and flag it: "That service isn't in the pricing sheet. Confirm pricing before quoting."

---

## Pre-condition Check

Read `intel/pricing.md` before quoting. Confirm:
- The requested service exists
- The requested package exists for that service
- If founding client rate applies: confirm this is client 1 or 2

---

## Sequence

### Step 1 — Read pricing + identity in parallel

Call `mcp__claude_ai_Google_Drive__read_file_content` twice simultaneously:

1. **Pricing sheet** — find the row matching the requested service and package. Record: setup amount, monthly amount, deliverables list.
2. **Identity doc** — extract: founder name, agency name, email address, website URL.

If either read fails: stop. Report the source and its ID.

---

### Step 2 — Calculate quote figures

| Figure | Calculation |
|--------|-------------|
| Setup | From pricing sheet |
| Monthly | From pricing sheet |
| Annual monthly | Monthly × 0.85 (round to nearest €0.50) |
| Annual total | Annual monthly × 12 |
| Annual saving | Monthly × 12 − Annual total |
| Client code | First 3 letters of company name, uppercase |
| Reference | `QUO-[CLIENT_CODE]-[YYYYMMDD]` |
| Quote date | Today (YYYY-MM-DD) |
| Valid until | Today + 30 days (YYYY-MM-DD) |
| Delivery timeline | From table below |

**Standard delivery timelines by package:**

| Package | Timeline |
|---------|----------|
| Starter | 2 weeks |
| Growth | 3 weeks |
| Scale | Agreed separately |
| Standard | 2–3 weeks |
| Advanced | 3–4 weeks |

---

### Step 3 — Build quote content

Open `templates/quote.md`. Populate every placeholder:

| Placeholder | Value |
|-------------|-------|
| `[Service Name]` | Service name from pricing sheet |
| `[Client Name / Company]` | As provided |
| `[YYYY-MM-DD]` | Today's date |
| `[VALID_UNTIL]` | Today + 30 days |
| `[CLIENT_CODE]` | 3-letter code |
| `[YYYYMMDD]` | Today's date, no dashes |
| `[Package Name]` | Package name (e.g. Growth) |
| Deliverables list | 3–5 bullet points from pricing sheet |
| `[setup]` | From pricing sheet |
| `[monthly]` | From pricing sheet |
| `[annual_monthly]` | Monthly × 0.85 |
| `[annual_total]` | Annual monthly × 12 |
| `[delivery_timeline]` | From timeline table above |
| Founding client section | Include only if founding_client = Yes. Remove entirely if No. |
| `[email from identity doc]` | From identity doc |
| `[website from identity doc]` | From identity doc |

Do not leave any `[bracket]` placeholder in the output.

---

### Step 4 — Generate the branded PDF

Save the populated quote content (from Step 3) to:
```
clients/[ClientName]/quotes/Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName].md
```

Then run:
```bash
python equipment/md_to_pdf.py "clients/[ClientName]/quotes/Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName].md" "clients/[ClientName]/quotes/Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName].pdf"
```

Record the PDF path. This is the file to attach when sending to the prospect.

If the script fails: report the error. Do not continue until the PDF is confirmed.

---

### Step 5 — Create the Google Doc

Call `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: `Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName]`
- `contentMimeType`: `text/plain`
- `disableConversionToGoogleType`: false
- `textContent`: populated quote text from Step 3
- `parentId`: `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` (Client Propositions folder)

Record the returned file URL. If creation fails: report the exact error. Do not continue.

---

### Step 6 — Draft the Gmail

```
Subject: Quote — [Service Name] for [Client / Company name]

Hi [First name],

Here's the quote you asked for.

[Google Doc URL]

Quick summary:
- [Package name]: €[setup] setup + €[monthly]/month
- Annual option: €[annual_monthly]/month (saves €[annual_saving] per year)
- Delivery: within [delivery_timeline] of confirmation

Valid for 30 days. Any questions, just reply here.

Abderrahim
degiabdo
```

Call `mcp__claude_ai_Gmail__create_draft` with:
- `to`: client email
- `subject`: `Quote — [Service Name] for [Client / Company]`
- `body`: above text

Never send. Save as draft only. Record the Gmail draft ID.

---

### Step 7 — Report

```
## Quote Generated — [Client Name] — [DATE]

[x] Pricing read: [Service] — [Package]
    Setup: €[setup] | Monthly: €[monthly] | Annual: €[annual_monthly]/month
[x] PDF generated: clients/[ClientName]/quotes/Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName].pdf
[x] Google Doc: [URL]
    Reference: [QUO-CODE-DATE]
    Valid until: [VALID_UNTIL]
[x] Gmail draft saved — subject: Quote — [Service] for [Client]
    Draft ID: [ID]

Review the PDF and the Gmail draft before sending. Attach the PDF to the email.
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Service not in pricing sheet | Stop. "That service isn't priced yet. Confirm the price first." |
| Package not found for service | Present available packages and ask which to use. |
| Pricing sheet read fails | Stop. Report the ID. |
| Identity doc read fails | Stop. Report the ID. |
| Google Doc creation fails | Report exact error. Do not continue. |
| Gmail draft fails | Report exact error. Log the Google Doc URL. |
| Founding client rate unclear | Ask: "Is this one of the first 1–2 clients?" |

---

## Quoting Rules

- Always include both setup and monthly — never quote just one
- Always include the annual option — don't lead with it, but show it
- Default for inbound Smart CRM requests: Growth package
- Founding client rate (20% off): first 1–2 clients only — always ask before applying
- Pricing in euros unless client requested local currency
- Do not quote services not in the pricing sheet without confirming first

## Lessons Learned

*(Append after each run)*

| Date | Issue | Fix |
|------|-------|-----|
