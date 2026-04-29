# Blueprint — Client Proposal Document

**Goal:** Generate a complete, structured business proposal as a Google Doc by reading three data sources: the pipeline (client context), the pricing sheet (package selection), and the identity doc (legal and banking details). Designed for any client in Won or Quote sent stage.

**Route:** Google Drive MCP (read pipeline + pricing + identity, create Google Doc).

**Trigger:** On demand. Say: "Build proposal document for [Client Name]."

---

## Inputs Required

| Input | Example |
|-------|---------|
| Client name | Sahel Cafe Group |
| Pipeline Sheet ID | 1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc |
| Pricing Sheet ID | 1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI |
| Identity Document ID | 1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c |
| Output folder | Client Propositions (ID: 1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2) |
| Currency | AED (MENA pricing) |

**Before starting:** confirm the client exists in the pipeline and pricing has been confirmed. If deal_value_usd is 0 or stage is Cold/Lost, stop and ask before proceeding.

---

## Sequence

### Step 1 — Read all three sources

Call `mcp__claude_ai_Google_Drive__read_file_content` three times in parallel:
1. Pipeline sheet — find the client row: contact name, role, email, deal value, notes, stage
2. Pricing sheet — match the package to the deal value and the notes (package name often mentioned)
3. Identity document — extract: legal name, founder, VAT number, bank details, payment terms, disclaimers

If any read fails: stop. Report which source failed and its ID.

### Step 2 — Derive package and pricing

- Match the pipeline notes (e.g. "signed Growth package") to the pricing sheet row
- Convert USD deal value to AED if needed (reference rate: 1 USD ≈ 3.67 AED)
- Apply VAT at 5% if client is UAE-based
- Calculate 50/50 payment schedule with VAT split

### Step 3 — Build the proposal content

Six-section structure:

| Section | Content |
|---------|---------|
| 1. Cover page | Agency name + tagline, client name + contact, date, reference number (PROP-[CLIENT_CODE]-[YYYYMMDD]), quote validity (30 days) |
| 2. Executive Summary | Client context (from notes), objective, approach in plain language |
| 3. Scope of Services | Package name, line-by-line deliverables, timeline |
| 4. Investment | AED pricing table: base price + VAT + total, 50/50 payment schedule |
| 5. General Terms | Quote validity, scope change policy, IP ownership, VAT registration, dispute resolution, liability cap |
| 6. Bank Details | All bank details from identity doc, accepted methods, payment reference, late fee policy |

### Step 4 — Create the Google Doc

Call `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: `Proposal_[ClientNameNoSpaces]_[YYYY-MM-DD]`
- `mimeType`: `text/plain` (auto-converts to Google Doc)
- `content`: base64-encoded proposal text
- `parentId`: `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2`

Report the Google Doc URL and file ID.

### Step 5 — Report

```
## Proposal Document — [Client Name] — [DATE]

[x] Sources read: pipeline, pricing, identity
[x] Package matched: [package name] — [AED] AED + VAT = [total] AED
[x] Google Doc created: [URL]
[x] Stored in: Client Propositions folder

Review the document before sharing with the client.
Note: logo and branding must be added manually.
```

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Client not found in pipeline | Stop. Report: "Client [name] not found." |
| Package not matched | Stop. Ask Abderrahim which package to use before proceeding. |
| Pricing is 0 or unconfirmed | Stop. Flag: "Pricing not confirmed for this client." |
| create_file fails | Report exact error. Do not retry without confirmation. |
| VAT unclear | Default to applying 5% for UAE clients. Flag if unsure. |

---

## Notes

- Always price in AED for MENA clients — use the AED pricing sheet
- USD amounts in the pipeline are reference only — the proposal uses AED
- The logo placeholder must be added manually in Google Drive after creation
- Quote reference format: PROP-[3-letter client code]-[YYYYMMDD]

---

## After Running

## Lessons Learned
- 2026-04-29 — First execution: Sahel Cafe Group. Pipeline notes confirmed "Growth package". USD-to-AED conversion at 3.67 matched pricing sheet closely. VAT at 5% applied (UAE client).
