# Quote Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a quote generation workflow that reads pricing and identity data, produces a clean one-page Google Doc quote for a prospect, and drafts a Gmail with a link — all in one run.

**Architecture:** Blueprint-only. Lighter than a proposal — no pipeline scan required if the client isn't in the system yet. Reads pricing sheet + identity doc, builds quote content from a template, creates Google Doc, drafts Gmail. No Equipment needed.

**Tech Stack:** Google Drive MCP, Gmail MCP, Markdown blueprint, Claude (Architect)

---

## Scope Note

A quote is a pricing document only — no narrative, no scope details, no terms. It answers: "What does this cost?" A proposal (already built in `blueprints/client-proposal-document.md`) answers: "Here's the full engagement." Quotes come first; proposals follow if the client wants to proceed.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `templates/quote.md` | Quote layout — clean, pricing-only format |
| Create | `blueprints/quote-generation.md` | Master SOP: confirm service + package, read pricing, create Doc, draft email |
| Modify | `live/state.md` | Add quote-generation to Skills Built table |

**Requires approval before creating the Blueprint** — `permissions.md`: "Create a new Blueprint: Ask first — always."

---

## Data Sources (already exist)

| Source | ID | What we read |
|--------|-----|--------------|
| Pricing sheet | `1cAWYT0nodYFeznP4uChN2pFUITkjav5CAwU5MU6FGWI` | Setup and monthly amounts per package |
| Identity doc | `1ujBao7Z89YjyVFpWAAk_CaIAi8tH9_JmhBfr16Rp79c` | Agency name, founder name, contact email, website |
| Output folder | Client Propositions — `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` | Where quotes are stored |

---

## Task 1: Quote Template

**Files:**
- Create: `templates/quote.md`

- [ ] **Step 1: Write the template**

Create `templates/quote.md` with this exact content:

```markdown
# Quote — [Service Name]

**From:** degiabdo — Abderrahim  
**For:** [Client Name / Company]  
**Date:** [YYYY-MM-DD]  
**Valid until:** [VALID_UNTIL] (30 days)  
**Reference:** QUO-[CLIENT_CODE]-[YYYYMMDD]  

---

## Package: [Package Name]

### What's included

[Deliverables list — 3-5 bullet points drawn from the pricing sheet description for this package]

---

## Investment

| | Setup fee | Monthly retainer |
|-|-----------|-----------------|
| [Package name] | €[setup] | €[monthly]/month |
| Annual option (15% off) | €[setup] | €[annual_monthly]/month |

*Annual retainer billed upfront: €[annual_total] (equivalent to ~2 months free).*

---

## How it works

- **Setup** covers discovery, build, and delivery — completed within [delivery_timeline]
- **Monthly retainer** begins after delivery — covers maintenance, optimisation, and support
- No lock-in on the monthly plan — cancel anytime with 30 days notice

---

## Founding client rate

[INCLUDE THIS SECTION ONLY IF THIS IS ONE OF THE FIRST 1-2 CLIENTS]

As a founding client, this quote includes a 20% discount in exchange for a written testimonial and permission to reference this project as a case study. This rate is not available after the first two clients.

---

## Next steps

Reply "I'm in" and we'll get started. If you'd like to discuss before deciding, just say the word and we'll set up a quick call.

---

Abderrahim  
degiabdo  
[email from identity doc]  
[website from identity doc]  

*Quote valid for 30 days from the date above. Pricing in euros (€).*
```

- [ ] **Step 2: Verify the template**

Read the template. Confirm:
- [ ] Reference format: `QUO-[CLIENT_CODE]-[YYYYMMDD]`
- [ ] Both monthly and annual pricing options are present (quoting rules: always include both)
- [ ] Annual calculation is correct: monthly × 12 × 0.85, billed upfront
- [ ] Founding client section exists but is marked "include only if..." — this must be removed before sending to non-founding clients
- [ ] No pricing numbers are hardcoded — all are placeholders
- [ ] Valid-until date is 30 days from quote date
- [ ] Signature includes email and website (pulled from identity doc at runtime)
- [ ] Delivery timeline is a placeholder (varies by package)

- [ ] **Step 3: Test the template mentally**

Substitute: Nadia / Kontrast Personalberatung, Smart CRM Growth package (€1,200 setup, €250/month), date 2026-05-04, non-founding client.

Expected:
- Reference: QUO-KON-20260504
- Annual monthly = €250 × 0.85 = €212.50/month
- Annual total = €212.50 × 12 = €2,550 upfront
- Valid until: 2026-06-03
- Founding client section: OMITTED (non-founding)

Confirm the layout reads as a clean, professional one-pager.

- [ ] **Step 4: Commit**

```bash
git add templates/quote.md
git commit -m "feat: add quote template"
```

---

## Task 2: Quote Generation Blueprint

**Requires approval before starting** — ask: "Quote template is done. Ready to create `blueprints/quote-generation.md`?" Wait for confirmation.

**Files:**
- Create: `blueprints/quote-generation.md`
- Modify: `live/state.md`

**Dependencies:** Task 1 must be complete and committed.

- [ ] **Step 1: Get approval**

Ask Abderrahim: "Quote template is ready. Ready to create `blueprints/quote-generation.md`? It will ask for service + package, read pricing + identity, create the Google Doc quote, and draft the Gmail."

Wait for explicit confirmation.

- [ ] **Step 2: Write the Blueprint**

Create `blueprints/quote-generation.md` with this exact content:

````markdown
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

1. **Pricing sheet** — find the row matching the requested service and package. Record: setup amount, monthly amount, deliverables list (if present in the sheet).
2. **Identity doc** — extract: founder name, agency name, email address, website URL.

If either read fails: stop. Report the source and its ID.

---

### Step 2 — Calculate quote figures

From the pricing sheet data:

| Figure | Calculation |
|--------|-------------|
| Setup | From pricing sheet |
| Monthly | From pricing sheet |
| Annual monthly | Monthly × 0.85 (round to nearest €0.50) |
| Annual total | Annual monthly × 12 |
| Client code | First 3 letters of company name, uppercase |
| Reference | `QUO-[CLIENT_CODE]-[YYYYMMDD]` |
| Quote date | Today (YYYY-MM-DD) |
| Valid until | Today + 30 days (YYYY-MM-DD) |
| Delivery timeline | Lookup from the table below |

**Standard delivery timelines by package:**
| Package | Timeline |
|---------|----------|
| Starter | 2 weeks |
| Growth | 3 weeks |
| Scale | Agreed separately |
| Standard (other services) | 2–3 weeks |
| Advanced (other services) | 3–4 weeks |

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
| Deliverables list | 3–5 bullet points from pricing sheet, or standard list for the service |
| `[setup]` | From pricing sheet |
| `[monthly]` | From pricing sheet |
| `[annual_monthly]` | Calculated: monthly × 0.85 |
| `[annual_total]` | Calculated: annual_monthly × 12 |
| `[delivery_timeline]` | From timeline table above |
| Founding client section | Include only if founding_client = Yes. Remove entirely if No. |
| `[email from identity doc]` | From identity doc |
| `[website from identity doc]` | From identity doc |

Do not leave any `[bracket]` placeholder in the output.

---

### Step 4 — Create the Google Doc

Call `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: `Quote_[ClientCode]_[YYYYMMDD]_[ServiceShortName]`
- `contentMimeType`: `text/plain`
- `disableConversionToGoogleType`: false
- `textContent`: populated quote text from Step 3
- `parentId`: `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` (Client Propositions folder)

Record the returned file URL.

If creation fails: report the exact error. Do not continue.

---

### Step 5 — Draft the Gmail

Draft the email body:

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

Compute annual_saving = monthly × 12 - annual_total. Round to nearest euro.

---

### Step 6 — Report

```
## Quote Generated — [Client Name] — [DATE]

[x] Pricing read: [Service] — [Package]
    Setup: €[setup] | Monthly: €[monthly] | Annual: €[annual_monthly]/month
[x] Google Doc: [URL]
    Reference: [QUO-CODE-DATE]
    Valid until: [VALID_UNTIL]
[x] Gmail draft saved — subject: Quote — [Service] for [Client]
    Draft ID: [ID]

Review the Google Doc and the Gmail draft before sending.
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

## Quoting Rules (from intel/pricing.md)

- Always include both setup and monthly — never quote just one
- Always include the annual option — don't lead with it, but show it
- Default for inbound Smart CRM requests: Growth package
- Founding client rate (20% off): first 1–2 clients only — always ask before applying
- Pricing in euros unless client requested local currency
- Do not quote services not in the pricing sheet without confirming first

## Lessons Learned
[Append after each run]
````

- [ ] **Step 3: Dry-run the Blueprint verbally**

Walk through each step using: Nadia / Kontrast Personalberatung, Smart CRM Growth package, non-founding client, date 2026-05-04.

| Step | Expected output | Passes? |
|------|----------------|---------|
| Step 1: pricing read | Growth CRM: setup €1,200, monthly €250. Identity: Abderrahim, degiabdo, email, website. | [ ] |
| Step 2: figures | Annual monthly = €212.50. Annual total = €2,550. Client code = KON. Reference = QUO-KON-20260504. Valid until = 2026-06-03. | [ ] |
| Step 3: content | All placeholders filled. Founding client section removed (non-founding). | [ ] |
| Step 4: Google Doc | File `Quote_KON_20260504_CRM` created in Client Propositions folder. URL returned. | [ ] |
| Step 5: Gmail draft | Annual saving = (€250 × 12) − €2,550 = €450. Draft saved. Subject: "Quote — Smart CRM Automation for Kontrast Personalberatung". | [ ] |
| Step 6: report | Clean summary with all figures, URL, draft ID. | [ ] |

Fix any step that doesn't produce clean output before committing.

- [ ] **Step 4: Update live/state.md**

Add to Skills Built table:

```
| Quote generation | blueprints/quote-generation.md | None (Google Drive + Gmail MCP) |
```

- [ ] **Step 5: Commit**

```bash
git add blueprints/quote-generation.md live/state.md
git commit -m "feat: add quote generation blueprint"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|-------------|------|
| Standard pricing into formatted quote | Template (Task 1) pulls from pricing sheet at runtime |
| Both setup and monthly always shown | Template has both; Blueprint Step 2 calculates both |
| Annual option included | Template and Blueprint Step 5 email both show it |
| Founding client rate handled | Template has conditional section; Blueprint Step 3 removes it if not applicable |
| Never send without review | Enforced in Blueprint Step 5 |
| Annual saving calculation | Blueprint Step 5 — annual_saving formula defined |

### Placeholder scan

No TBDs. All placeholders have defined sources. Founding client section is the only conditional — clearly marked with include/remove instruction.

### Type consistency

- Pricing Sheet ID and Identity Doc ID match IDs in `blueprints/client-proposal-document.md`
- Output folder ID matches `blueprints/client-proposition.md`
- QUO- prefix distinguishes quotes from PROP- (proposals) and INV- (invoices)

---

*Plan written: 2026-05-04*
