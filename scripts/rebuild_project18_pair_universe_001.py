#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
IN_PAIRS = ROOT / "source/project18_artifacts/json/wxyzti_shared_reverse_pair_coupling_audit_021.v1.json"

OUT_JSON = ROOT / "artifacts/json/project18_pair_universe_rebuild_001.v1.json"
OUT_NOTE = ROOT / "notes/project18_pair_universe_rebuild_001.md"

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


def row_id(row):
    return (
        row.get("station_role"),
        row.get("role_pair"),
        row.get("from_A"),
        row.get("from_B"),
        row.get("from_C"),
        row.get("to_A"),
        row.get("to_B"),
        row.get("to_C"),
    )


def pair_id(shared, reverse):
    return (row_id(shared), row_id(reverse))


def compact(row):
    keys = [
        "station_role", "role_pair", "role_class",
        "from_A", "from_B", "from_C", "from_slot",
        "to_A", "to_B", "to_C", "to_slot",
        "integer_C_delta", "C_delta", "fiber_delta", "lift_q",
    ]
    return {k: row.get(k) for k in keys}


def flags(shared, reverse):
    same_role_pair = shared["role_pair"] == reverse["role_pair"]
    same_from_C = shared["from_C"] == reverse["from_C"]
    same_to_C = shared["to_C"] == reverse["to_C"]
    same_C_delta = shared["C_delta"] == reverse["C_delta"]
    same_integer_C_delta = shared["integer_C_delta"] == reverse["integer_C_delta"]
    same_lift_q = shared["lift_q"] == reverse["lift_q"]

    S_preserves_B = shared["from_B"] == shared["to_B"]
    S_preserves_slot = shared["from_slot"] == shared["to_slot"]

    R_preserves_A = reverse["from_A"] == reverse["to_A"]
    R_swaps_BC = reverse["to_C"] == reverse["from_B"] and reverse["to_B"] == reverse["from_C"]

    answer = reverse["from_B"] == shared["to_C"] and reverse["from_slot"] == shared["to_C"]
    returned = reverse["to_B"] == shared["from_C"] and reverse["to_slot"] == shared["from_C"]

    reciprocal_answer_pair = (
        same_role_pair
        and same_from_C
        and answer
        and returned
        and R_swaps_BC
        and S_preserves_B
        and S_preserves_slot
    )

    strict_pair_grammar = (
        reciprocal_answer_pair
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
        "S_preserves_B": S_preserves_B,
        "S_preserves_slot": S_preserves_slot,
        "R_preserves_A": R_preserves_A,
        "R_swaps_BC": R_swaps_BC,
        "answer_R_supplies_S_to_C": answer,
        "return_R_returns_S_from_C": returned,
        "reciprocal_answer_pair": reciprocal_answer_pair,
        "strict_pair_grammar": strict_pair_grammar,
    }


def selector_score(candidates, expected_ids, name):
    accepted = [c for c in candidates if c["flags"][name]]
    accepted_ids = {c["pair_id"] for c in accepted}
    false_positive = accepted_ids - expected_ids
    misses = expected_ids - accepted_ids
    return {
        "selector": name,
        "accepted_count": len(accepted),
        "expected_count": len(expected_ids),
        "false_positive_count": len(false_positive),
        "miss_count": len(misses),
        "exact": len(false_positive) == 0 and len(misses) == 0,
    }


def main():
    rows_data = load(IN_ROWS)
    pairs_data = load(IN_PAIRS)

    rows = []
    for r in rows_data.get("rows", []):
        rr = dict(r)
        rr["role_class"] = role_class(rr["station_role"])
        rows.append(rr)

    shared = [r for r in rows if r["role_class"] == "shared_B"]
    reverse = [r for r in rows if r["role_class"] == "reverse_partner"]

    expected_ids = set()
    for pr in pairs_data.get("pair_records", []):
        expected_ids.add(pair_id(pr["shared_B_row"], pr["reverse_partner_row"]))

    candidates = []
    for s in shared:
        for r in reverse:
            if s["role_pair"] != r["role_pair"]:
                continue
            candidates.append({
                "pair_id": pair_id(s, r),
                "expected": pair_id(s, r) in expected_ids,
                "role_pair": s["role_pair"],
                "shared_role": s["station_role"],
                "reverse_role": r["station_role"],
                "shared_B_row": compact(s),
                "reverse_partner_row": compact(r),
                "flags": flags(s, r),
            })

    selectors = [
        "same_from_C",
        "same_to_C",
        "same_C_delta",
        "same_integer_C_delta",
        "same_lift_q",
        "answer_R_supplies_S_to_C",
        "return_R_returns_S_from_C",
        "reciprocal_answer_pair",
        "strict_pair_grammar",
    ]

    scores = [selector_score(candidates, expected_ids, s) for s in selectors]
    exact = [s["selector"] for s in scores if s["exact"]]

    result = {
        "status": "project18_pair_universe_rebuild_recorded",
        "audit_id": "001",
        "input_rows": str(IN_ROWS),
        "input_pairs": str(IN_PAIRS),
        "shared_row_count": len(shared),
        "reverse_row_count": len(reverse),
        "candidate_count": len(candidates),
        "expected_pair_count": len(expected_ids),
        "candidate_role_pair_counts": dict(sorted(Counter(c["role_pair"] for c in candidates).items())),
        "selector_scores": scores,
        "exact_selectors": exact,
        "accepted_strict_count": sum(1 for c in candidates if c["flags"]["strict_pair_grammar"]),
        "boundary": (
            "This rebuilds the Project 18 realized row-pair universe inside Project 21. "
            "It is a baseline reproduction, not a native generator and not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Project 18 pair universe rebuild 001")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Rebuild")
    lines.append("")
    lines.append("- shared_row_count: `" + str(result["shared_row_count"]) + "`")
    lines.append("- reverse_row_count: `" + str(result["reverse_row_count"]) + "`")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- expected_pair_count: `" + str(result["expected_pair_count"]) + "`")
    lines.append("- candidate_role_pair_counts: `" + str(result["candidate_role_pair_counts"]) + "`")
    lines.append("")
    lines.append("## Selector scores")
    lines.append("")
    for s in scores:
        lines.append(
            "- " + s["selector"]
            + ": accepted=" + str(s["accepted_count"])
            + ", false_positive=" + str(s["false_positive_count"])
            + ", miss=" + str(s["miss_count"])
            + ", exact=" + str(s["exact"])
        )
    lines.append("")
    lines.append("## Exact selectors")
    lines.append("")
    for s in exact:
        lines.append("- " + s)
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(result["boundary"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("candidate_count", result["candidate_count"])
    print("expected_pair_count", result["expected_pair_count"])
    print("exact_selectors", result["exact_selectors"])


if __name__ == "__main__":
    main()
