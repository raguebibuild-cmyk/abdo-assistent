# Blueprint — Monday Morning Pipeline Summary

**Goal:** Read the "Leads & Pipeline" Google Sheet and produce a structured French report every Monday morning covering: leads by stage, total active pipeline value, and top 3 hottest leads.

**Trigger:** Scheduled — every Monday at 08:00 GMT+1. Can also be run on demand: say "Run Monday pipeline summary."

---

## Inputs Required

| Input | Value |
|-------|-------|
| Sheet ID | `1LZFrpC75AgGiUtNJVbjhTVkg1YNHco0uYEf7l9elAIc` |
| Sheet name | Leads & Pipeline |
| Column headers | `company`, `contact_name`, `stage`, `deal_value_usd`, `next_step` |
| Equipment script | `equipment/pipeline_summary.py` |
| Output folder | `.tmp/` |

**Stages (8):** Discovery booked | Quote sent | Audit in progress | Won | Contacted | Cold | On hold | Lost

**Active stages (for value sum):** Quote sent + Discovery booked + Audit in progress

**Hot lead priority order:** Quote sent → Discovery booked → Audit in progress

---

## Sequence

### Step 1 — Read the sheet
Call `mcp__claude_ai_Google_Drive__read_file_content` with the sheet ID.

- If the result is plain CSV text: proceed to Step 2.
- If the result is not readable CSV: call `mcp__claude_ai_Google_Drive__download_file_content` with `mimeType: text/csv`.
- If both fail: stop and report the error. Do not guess or proceed.

### Step 2 — Save raw data
Write the CSV content to:
```
.tmp/pipeline-raw-YYYY-MM-DD.csv
```
Use today's date in the filename.

### Step 3 — Run Equipment
```
python equipment/pipeline_summary.py < .tmp/pipeline-raw-YYYY-MM-DD.csv
```
This outputs a JSON object to stdout. Save it to:
```
.tmp/pipeline-data-YYYY-MM-DD.json
```

### Step 4 — Format the French report
Read the JSON from `.tmp/pipeline-data-YYYY-MM-DD.json` and render the report using the template below. Write it to:
```
.tmp/monday-summary-YYYY-MM-DD.md
```

### Step 5 — Display
Print the full report to the conversation.

---

## Output Template

```
## Résumé Pipeline — Lundi [DATE]

### 📊 LEADS PAR ÉTAPE

| Étape               | Nombre |
|---------------------|--------|
| Quote sent          | X      |
| Discovery booked    | X      |
| Audit in progress   | X      |
| Won                 | X      |
| Contacted           | X      |
| Cold                | X      |
| On hold             | X      |
| Lost                | X      |

### 💰 VALEUR TOTALE DES ÉTAPES ACTIVES

**$X,XXX USD** (Quote sent + Discovery booked + Audit in progress)

### 🔥 TOP 3 LEADS LES PLUS CHAUDS

**1. [Entreprise] — [Contact]**
- Deal : $X,XXX USD
- Étape : [étape]
- Prochaine action : [next_step]

**2. [Entreprise] — [Contact]**
- Deal : $X,XXX USD
- Étape : [étape]
- Prochaine action : [next_step]

**3. [Entreprise] — [Contact]**
- Deal : $X,XXX USD
- Étape : [étape]
- Prochaine action : [next_step]
```

If fewer than 3 active leads exist, list what's available. Do not pad with inactive leads.

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Google Drive MCP returns non-CSV | Retry with `download_file_content`, `mimeType: text/csv` |
| Both MCP calls fail | Stop. Report exact error. Do not proceed. |
| Script exits with error | Read the full error before touching anything. Fix the script properly. Re-run. Update this Blueprint with what was learned. |
| Column name mismatch | Stop. Report which column is missing. Confirm headers with Abderrahim before continuing. |
| Empty sheet (zero data rows) | Report: "Pipeline vide — aucune donnée à traiter." Do not run the Equipment script. |
| `deal_value_usd` is blank for a lead | Treat as $0. Continue. |

---

## Equipment Reference

**`equipment/pipeline_summary.py`**
- Input: CSV from stdin
- Output: JSON to stdout
- Fields returned: `stage_counts` (dict), `active_pipeline_usd` (float), `top_leads` (list of 3)
- No credentials needed — stdlib only

---

## After Running

If anything broke and was fixed, update this Blueprint under a new section:

```
## Lessons Learned
- [DATE] — [what broke] → [what was fixed]
```

This keeps the system from breaking the same way twice.

## Lessons Learned
- 2026-04-29 — Column headers assumed incorrectly at build time. Actual sheet headers are `company` and `contact_name`, not `company_name` and `contact`. Equipment script and Blueprint updated to match. Scheduled routine prompt also corrected.
