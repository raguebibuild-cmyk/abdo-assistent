#!/usr/bin/env python3
"""
Input:  CSV via stdin — columns: company, contact_name, stage, deal_value_usd, next_step
Output: JSON to stdout — stage counts, active pipeline value, top 3 hottest leads
"""
import csv
import json
import sys

STAGES = [
    "Discovery booked",
    "Quote sent",
    "Audit in progress",
    "Won",
    "Contacted",
    "Cold",
    "On hold",
    "Lost",
]

ACTIVE_STAGES = ["Quote sent", "Discovery booked", "Audit in progress"]
HOT_PRIORITY  = ["Quote sent", "Discovery booked", "Audit in progress"]


def main():
    reader = csv.DictReader(sys.stdin)
    counts = {s: 0 for s in STAGES}
    active_value = 0.0
    hot_leads = []

    for row in reader:
        stage = row.get("stage", "").strip()

        if stage in counts:
            counts[stage] += 1

        if stage in ACTIVE_STAGES:
            try:
                value = float(row.get("deal_value_usd") or 0)
            except ValueError:
                value = 0.0
            active_value += value
            hot_leads.append({
                "company":   row.get("company", "").strip(),
                "contact":   row.get("contact_name", "").strip(),
                "value":     value,
                "stage":     stage,
                "next_step": row.get("next_step", "").strip(),
            })

    hot_leads.sort(
        key=lambda x: HOT_PRIORITY.index(x["stage"]) if x["stage"] in HOT_PRIORITY else 99
    )

    result = {
        "stage_counts":        counts,
        "active_pipeline_usd": round(active_value, 2),
        "top_leads":           hot_leads[:3],
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
