#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
OUT_JSON = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
OUT_NOTE = ROOT / "notes/admission_blind_row_pair_selector_002.md"

REVERSE_ROLES = {"WX", "YZ", "TI"}
SHAREDB_ROLES = {"XY", "ZT", "IW"}

def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def role_class(role):
    if role in REVERSE_ROLES:
        return "reverse_partner"
    if role in SHAREDB_ROLES:
        return "shared_B"
    return "unknown"

def compact(row):
    keys = [
        "station_role", "role_pair", "role_class",
        "from_A", "from_B", "from_C", "from_slot",
        "to_A", "to_B", "to_C", "to_slot",
        "integer_C_delta", "C_delta", "fiber_delta", "lift_q",
    ]
    return {k: row.get(k) for k in keys}

def strict_flags(s, r):
    same_role_pair = s["role_pair"] == r["role_pair"]
    same_from_C = s["from_C"] == r["from_C"]
    same_to_C = s["to_C"] == r["to_C"]
    same_C_delta = s["C_delta"] == r["C_delta"]
    same_integer_C_delta = s["integer_C_delta"] == r["integer_C_delta"]
    same_lift_q = s["lift_q"] == r["lift_q"]

    s_preserves_B = s["from_B"] == s["to_B"]
    s_preserves_slot = s["from_slot"] == s["to_slot"]

    r_preserves_A = r["from_A"] == r["to_A"]
    r_swaps_BC = r["to_C"] == r["from_B"] and r["to_B"] == r["from_C"]

    answer = r["from_B"] == s["to_C"] and r["from_slot"] == s["to_C"]
    returned = r["to_B"] == s["from_C"] and r["to_slot"] == s["from_C"]

    reciprocal = (
        same_role_pair
        and same_from_C
        and answer
        and returned
        and s_preserves_B
        and s_preserves_slot
        and r_preserves_A
        and r_swaps_BC
    )

    strict = (
        reciprocal
        and same_to_C
        and same_C_delta
        and same_integer_C_delta
        and same_lift_q
    )

    return {
        "same_role_pair": same_role_pair,
        "same_from_C": same_from_C,
        "same_to_C": same_to_C,
        "same_C_delta": same_C_delta,
        "same_integer_C_delta": same_integer_C_delta,
        "same_lift_q": same_lift_q,
        "S_preserves_B": s_preserves_B,
        "S_preserves_slot": s_preserves_slot,
        "R_preserves_A": r_preserves_A,
        "R_swaps_BC": r_swaps_BC,
        "answer_R_supplies_S_to_C": answer,
        "return_R_returns_S_from_C": returned,
        "reciprocal_answer_pair": reciprocal,
        "strict_pair_grammar": strict,
    }

def main():
    data = load(IN_ROWS)
    rows = []
    for row in data.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared = [r for r in rows if r["role_class"] == "shared_B"]
    reverse = [r for r in rows if r["role_class"] == "reverse_partner"]

    candidates = []
    for s in shared:
        for r in reverse:
            if s["role_pair"] != r["role_pair"]:
                continue
            flags = strict_flags(s, r)
            candidates.append({
                "role_pair": s["role_pair"],
                "shared_role": s["station_role"],
                "reverse_role": r["station_role"],
                "pair_key": [
                    s["role_pair"],
                    s["from_C"],
                    s["to_C"],
                    s["station_role"],
                    r["station_role"],
                ],
                "selected": flags["strict_pair_grammar"],
                "shared_B_row": compact(s),
                "reverse_partner_row": compact(r),
                "flags": flags,
            })

    selected = [c for c in candidates if c["selected"]]

    result = {
        "status": "admission_blind_row_pair_selector_recorded",
        "audit_id": "002",
        "uses_project18_expected_pair_records": False,
        "input_rows": str(IN_ROWS),
        "shared_row_count": len(shared),
        "reverse_row_count": len(reverse),
        "candidate_count": len(candidates),
        "selected_count": len(selected),
        "candidate_role_pair_counts": dict(sorted(Counter(c["role_pair"] for c in candidates).items())),
        "selected_role_pair_counts": dict(sorted(Counter(c["role_pair"] for c in selected).items())),
        "selected_pair_keys": [c["pair_key"] for c in selected],
        "boundary": (
            "This is admission-blind relative to Project 18 expected pair records, "
            "but it still uses realized WXYZTI station rows. It is not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Admission-blind row-pair selector 002")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input discipline")
    lines.append("")
    lines.append("- uses_project18_expected_pair_records: `" + str(result["uses_project18_expected_pair_records"]) + "`")
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append("- shared_row_count: `" + str(result["shared_row_count"]) + "`")
    lines.append("- reverse_row_count: `" + str(result["reverse_row_count"]) + "`")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- candidate_role_pair_counts: `" + str(result["candidate_role_pair_counts"]) + "`")
    lines.append("- selected_role_pair_counts: `" + str(result["selected_role_pair_counts"]) + "`")
    lines.append("")
    lines.append("## Selected pair keys")
    lines.append("")
    for key in result["selected_pair_keys"]:
        lines.append("- `" + str(tuple(key)) + "`")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(result["boundary"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("uses_project18_expected_pair_records", result["uses_project18_expected_pair_records"])
    print("candidate_count", result["candidate_count"])
    print("selected_count", result["selected_count"])
    print("selected_role_pair_counts", result["selected_role_pair_counts"])

if __name__ == "__main__":
    main()
