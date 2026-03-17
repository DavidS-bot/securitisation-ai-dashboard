"""
Build site/data.json from roles.json.

Reads the roles taxonomy with pre-generated scores and writes a compact
JSON file for the frontend treemap dashboard.

Usage:
    python build_site_data.py
"""

import json
import os

REQUIRED_FIELDS = [
    "title", "slug", "sector", "sector_label", "description",
    "headcount", "salary", "education", "key_tasks",
    "ai_exposure", "ai_exposure_rationale",
    "automation_risk", "automation_risk_rationale",
    "regulatory_complexity", "regulatory_complexity_rationale",
]


def main():
    with open("roles.json", encoding="utf-8") as f:
        roles = json.load(f)

    # Validate
    errors = []
    for i, role in enumerate(roles):
        for field in REQUIRED_FIELDS:
            if field not in role:
                errors.append(f"Role {i} ({role.get('title', '?')}): missing '{field}'")

    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        return

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w", encoding="utf-8") as f:
        json.dump(roles, f)

    total_headcount = sum(r["headcount"] for r in roles)
    total_salary = sum(r["headcount"] * r["salary"] for r in roles)
    avg_exposure = sum(r["headcount"] * r["ai_exposure"] for r in roles) / total_headcount
    sectors = sorted(set(r["sector_label"] for r in roles))

    print(f"Wrote {len(roles)} roles to site/data.json")
    print(f"Sectors: {len(sectors)}")
    print(f"Total headcount: {total_headcount:,}")
    print(f"Total annual compensation: EUR {total_salary:,.0f}")
    print(f"Weighted avg AI exposure: {avg_exposure:.1f}/10")


if __name__ == "__main__":
    main()
