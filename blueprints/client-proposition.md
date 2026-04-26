# Blueprint: Client Proposition

**Type:** Blueprint only — Architect executes via Google Drive + Gmail MCP tools
**Voice rules:** `.claude/rules/voice.md`, `.claude/rules/clients.md`
**Template:** `templates/proposition-doc.md`
**Drive folder:** Client Propositions (ID: 1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2)

---

## Goal

When Abderrahim wants to send a proposition to a client or prospect:
1. Create a Google Doc in the "Client Propositions" Drive folder
2. Write the proposition content inside it
3. Draft a Gmail to the client with a link to the doc

All three steps happen in one run. Output is always a draft — never sent directly.

---

## Required Inputs

| Input | Description |
|-------|-------------|
| Client name | First name + last name or company name |
| Client email | Required for the Gmail draft |
| Lifecycle stage | Prospect or Active |
| Services proposed | Which degiabdo services are being offered |
| Pricing | Exact amounts — must be confirmed before proceeding |
| Context | Why this proposition, what problem it solves |
| Timeline | When work starts, when it delivers |

If pricing is not confirmed: stop and ask. Do not draft a proposition without confirmed numbers.

---

## Sequence

**Step 1 — Gather and confirm inputs**
Run through the required inputs table. If anything is missing, list what's needed and stop.
Pricing specifically: confirm the exact figure before moving to Step 2.

**Step 2 — Create the Google Doc**
- Use Google Drive MCP: `create_file`
- Title: `Proposition — [Client Name] — [YYYY-MM-DD]`
- mimeType: `application/vnd.google-apps.document`
- parentId: `1dK5wbdK3TaVKdc1gP19Itg0b3sce8lm2` (Client Propositions folder)
- Content: populated from `templates/proposition-doc.md`

**Step 3 — Draft the Gmail**
- Use Gmail MCP: `create_draft`
- To: client email
- Subject: `Proposition for [Client Name / Company]`
- Body: short covering note (see template below) + link to the Google Doc
- Never send — draft only

**Step 4 — Output for review**
Report back:
```
PROPOSITION CREATED
---
Google Doc: [title] — [view URL]
Gmail draft: saved to drafts — subject: [subject]
---
Review the doc and the email draft before sending anything.
```

---

## Gmail Covering Note Template

```
Hi [Name],

I've put together a proposition for you based on what we discussed.

[One sentence on what the proposition covers.]

You can review it here: [Google Doc link]

Happy to walk you through it or answer any questions — just let me know.

Abderrahim
degiabdo
```

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Pricing not confirmed | Stop — "What's the price for this? I won't draft without confirmed numbers." |
| Client email missing | Ask before proceeding to Step 3 |
| Google Drive call fails | Report the error, do not retry without confirmation |
| Client already has a proposition | Flag it — "There's already a proposition for [name] in Drive. Create a new one or update the existing?" |

---

## Naming Convention

Google Docs in the Client Propositions folder follow this format:
`Proposition — [Client Name] — [YYYY-MM-DD]`

One doc per proposition. If a client gets a revised proposition, create a new doc — do not overwrite.
