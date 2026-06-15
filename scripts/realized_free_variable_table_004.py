#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"

OUT_JSON = ROOT / "artifacts/json/realized_free_variable_table_004.v1.json"
OUT_NOTE = ROOT / "notes/realized_free_variable_table_004.md"

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


def strict_pair(s, r):
    return (
        s["role_pair"] == r["role_pair"]
        and s["from_C"] == r["from_C"]
        and s["to_C"] == r["to_C"]
        and s["C_delta"] == r["C_delta"]
        and s["integer_C_delta"] == r["integer_C_delta"]
        and s["lift_q"] == r["lift_q"]
        and s["from_B"] == s["to_B"]
        and s["from_slot"] == s["to_slot"]
        and r["from_A"] == r["to_A"]
        and r["to_C"] == r["from_B"]
        and r["to_B"] == r["from_C"]
        and r["from_B"] == s["to_C"]
        and r["from_slot"] == s["to_C"]
        and r["to_B"] == s["from_C"]
        and r["to_slot"] == s["from_C"]
    )


def md_table(rows):
    headers = [
        "role_pair", "c0", "c1", "shared", "reverse",
        "S_from_A", "S_B", "S_to_A", "R_A",
        "S_A_delta", "R_minus_S_from_A", "S_B_minus_c1",
    ]
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(str(r[h]) for h in headers) + " |")
    return "\n".join(out)


def main():
    drows = load(IN_ROWS)
    d002 = load(IN_002)

    selected_keys = {tuple(k) for k in d002["selected_pair_keys"]}

    rows = []
    for row in drows.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared = [r for r in rows if r["role_class"] == "shared_B"]
    reverse = [r for r in rows if r["role_class"] == "reverse_partner"]

    records = []
    for s in shared:
        for r in reverse:
            if not strict_pair(s, r):
                continue
            key = (s["role_pair"], s["from_C"], s["to_C"], s["station_role"], r["station_role"])
            if key not in selected_keys:
                continue

            rec = {
                "role_pair": s["role_pair"],
                "c0": s["from_C"],
                "c1": s["to_C"],
                "shared": s["station_role"],
                "reverse": r["station_role"],
                "S_from_A": s["from_A"],
                "S_B": s["from_B"],
                "S_to_A": s["to_A"],
                "R_A": r["from_A"],
                "S_A_delta": (s["to_A"] - s["from_A"]) % 15,
                "R_minus_S_from_A": (r["from_A"] - s["from_A"]) % 15,
                "S_B_minus_c1": (s["from_B"] - s["to_C"]) % 15,
                "key": list(key),
            }
            records.append(rec)

    records = sorted(records, key=lambda x: (x["role_pair"], x["c0"], x["c1"]))

    result = {
        "status": "realized_free_variable_table_recorded",
        "audit_id": "004",
        "input_rows": str(IN_ROWS),
        "input_selector_002": str(IN_002),
        "record_count": len(records),
        "records": records,
        "role_pair_counts": dict(sorted(Counter(r["role_pair"] for r in records).items())),
        "S_A_delta_counts": dict(sorted(Counter(r["S_A_delta"] for r in records).items())),
        "R_minus_S_from_A_counts": dict(sorted(Counter(r["R_minus_S_from_A"] for r in records).items())),
        "S_B_minus_c1_counts": dict(sorted(Counter(r["S_B_minus_c1"] for r in records).items())),
        "interpretation": (
            "This table exposes the four free variables left by the synthetic skeleton: "
            "S.from_A, S.B/slot, S.to_A, and R.from_A. It is a preparation step for "
            "finding the missing A/B assignment law."
        ),
        "boundary": (
            "This table uses realized selected pairs. It is descriptive and preparatory, "
            "not a native generator and not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Realized free-variable table 004")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- record_count: `" + str(result["record_count"]) + "`")
    lines.append("- role_pair_counts: `" + str(result["role_pair_counts"]) + "`")
    lines.append("- S_A_delta_counts: `" + str(result["S_A_delta_counts"]) + "`")
    lines.append("- R_minus_S_from_A_counts: `" + str(result["R_minus_S_from_A_counts"]) + "`")
    lines.append("- S_B_minus_c1_counts: `" + str(result["S_B_minus_c1_counts"]) + "`")
    lines.append("")
    lines.append("## Free-variable table")
    lines.append("")
    lines.append(md_table(records))
    lines.append("")
    lines.append("## Reading")
    lines.append("")
    lines.append(result["interpretation"])
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(result["boundary"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("record_count", result["record_count"])
    print("S_A_delta_counts", result["S_A_delta_counts"])
    print("R_minus_S_from_A_counts", result["R_minus_S_from_A_counts"])
    print("S_B_minus_c1_counts", result["S_B_minus_c1_counts"])


if __name__ == "__main__":
    main()
