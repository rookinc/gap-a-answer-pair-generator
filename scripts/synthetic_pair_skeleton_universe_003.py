#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"

OUT_JSON = ROOT / "artifacts/json/synthetic_pair_skeleton_universe_003.v1.json"
OUT_NOTE = ROOT / "notes/synthetic_pair_skeleton_universe_003.md"

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


def deltas(c0, c1):
    integer_delta = int(c1) - int(c0)
    c_delta = integer_delta % 15
    lift_q = 0 if integer_delta >= 0 else 3
    fiber_delta = integer_delta % 60
    return integer_delta, c_delta, fiber_delta, lift_q


def make_shared(role_pair, c0, c1, shared_role, s_from_A, s_B, s_to_A):
    integer_delta, c_delta, fiber_delta, lift_q = deltas(c0, c1)
    return {
        "station_role": shared_role,
        "role_pair": role_pair,
        "role_class": "shared_B",
        "from_A": s_from_A,
        "from_B": s_B,
        "from_C": c0,
        "from_slot": s_B,
        "to_A": s_to_A,
        "to_B": s_B,
        "to_C": c1,
        "to_slot": s_B,
        "integer_C_delta": integer_delta,
        "C_delta": c_delta,
        "fiber_delta": fiber_delta,
        "lift_q": lift_q,
    }


def make_reverse(role_pair, c0, c1, reverse_role, r_A):
    integer_delta, c_delta, fiber_delta, lift_q = deltas(c0, c1)
    return {
        "station_role": reverse_role,
        "role_pair": role_pair,
        "role_class": "reverse_partner",
        "from_A": r_A,
        "from_B": c1,
        "from_C": c0,
        "from_slot": c1,
        "to_A": r_A,
        "to_B": c0,
        "to_C": c1,
        "to_slot": c0,
        "integer_C_delta": integer_delta,
        "C_delta": c_delta,
        "fiber_delta": fiber_delta,
        "lift_q": lift_q,
    }


def sig(row):
    keys = [
        "station_role", "role_pair", "role_class",
        "from_A", "from_B", "from_C", "from_slot",
        "to_A", "to_B", "to_C", "to_slot",
        "integer_C_delta", "C_delta", "fiber_delta", "lift_q",
    ]
    return tuple((k, row.get(k)) for k in keys)


def pair_sig(shared, reverse):
    return (sig(shared), sig(reverse))


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


def compact(row):
    keys = [
        "station_role", "role_pair", "role_class",
        "from_A", "from_B", "from_C", "from_slot",
        "to_A", "to_B", "to_C", "to_slot",
        "integer_C_delta", "C_delta", "fiber_delta", "lift_q",
    ]
    return {k: row.get(k) for k in keys}


def main():
    d002 = load(IN_002)
    drows = load(IN_ROWS)

    selected_keys = d002["selected_pair_keys"]

    rows = []
    for row in drows.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared_rows = [r for r in rows if r["role_class"] == "shared_B"]
    reverse_rows = [r for r in rows if r["role_class"] == "reverse_partner"]

    realized_pair_sigs = set()
    for s in shared_rows:
        for r in reverse_rows:
            if strict_pair(s, r):
                realized_pair_sigs.add(pair_sig(compact(s), compact(r)))

    per_key = []
    total_candidates = 0
    total_realized_matches = 0
    matched_examples = []

    for key in selected_keys:
        role_pair, c0, c1, shared_role, reverse_role = key
        key_count = 0
        key_match_count = 0
        key_matches = []

        for s_from_A in range(15):
            for s_B in range(15):
                for s_to_A in range(15):
                    s = make_shared(role_pair, c0, c1, shared_role, s_from_A, s_B, s_to_A)
                    for r_A in range(15):
                        r = make_reverse(role_pair, c0, c1, reverse_role, r_A)
                        key_count += 1

                        ps = pair_sig(s, r)
                        if ps in realized_pair_sigs:
                            key_match_count += 1
                            item = {
                                "key": key,
                                "shared_B_row": s,
                                "reverse_partner_row": r,
                            }
                            key_matches.append(item)
                            if len(matched_examples) < 20:
                                matched_examples.append(item)

        total_candidates += key_count
        total_realized_matches += key_match_count

        per_key.append({
            "key": key,
            "synthetic_candidate_count": key_count,
            "realized_match_count": key_match_count,
            "free_variables": [
                "S.from_A",
                "S.from_B_or_slot",
                "S.to_A",
                "R.from_A",
            ],
            "matches": key_matches,
        })

    result = {
        "status": "synthetic_pair_skeleton_universe_recorded",
        "audit_id": "003",
        "input_selector_002": str(IN_002),
        "input_realized_rows_for_evaluation_only": str(IN_ROWS),
        "uses_project18_expected_pair_records": False,
        "uses_realized_rows_for_generation": False,
        "uses_realized_rows_for_evaluation": True,
        "selected_key_count": len(selected_keys),
        "free_variable_count_per_key": 4,
        "values_per_free_variable": 15,
        "synthetic_candidate_count_per_key": 15 ** 4,
        "total_synthetic_candidate_count": total_candidates,
        "realized_pair_signature_count": len(realized_pair_sigs),
        "total_realized_match_count": total_realized_matches,
        "overgeneration_factor_per_realized_pair": (
            total_candidates // total_realized_matches if total_realized_matches else None
        ),
        "per_key": per_key,
        "matched_examples_first_20": matched_examples,
        "interpretation": (
            "Given the selected transition key and reciprocal station roles, the pair grammar "
            "still leaves four mod-15 degrees of freedom: S.from_A, S.B/slot, S.to_A, and R.from_A. "
            "The synthetic skeleton universe therefore overgenerates heavily. This identifies the "
            "next native-generator problem: select the missing A/B assignments without using realized rows."
        ),
        "boundary": (
            "This is not Gap A closure. It uses selected transition keys from 002, and it uses "
            "realized rows only for evaluation. It does not yet generate the transition support or "
            "the A/B assignments natively."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Synthetic pair skeleton universe 003")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input discipline")
    lines.append("")
    lines.append("- uses_project18_expected_pair_records: `" + str(result["uses_project18_expected_pair_records"]) + "`")
    lines.append("- uses_realized_rows_for_generation: `" + str(result["uses_realized_rows_for_generation"]) + "`")
    lines.append("- uses_realized_rows_for_evaluation: `" + str(result["uses_realized_rows_for_evaluation"]) + "`")
    lines.append("")
    lines.append("## Synthetic universe")
    lines.append("")
    lines.append("- selected_key_count: `" + str(result["selected_key_count"]) + "`")
    lines.append("- free_variable_count_per_key: `" + str(result["free_variable_count_per_key"]) + "`")
    lines.append("- values_per_free_variable: `" + str(result["values_per_free_variable"]) + "`")
    lines.append("- synthetic_candidate_count_per_key: `" + str(result["synthetic_candidate_count_per_key"]) + "`")
    lines.append("- total_synthetic_candidate_count: `" + str(result["total_synthetic_candidate_count"]) + "`")
    lines.append("- realized_pair_signature_count: `" + str(result["realized_pair_signature_count"]) + "`")
    lines.append("- total_realized_match_count: `" + str(result["total_realized_match_count"]) + "`")
    lines.append("- overgeneration_factor_per_realized_pair: `" + str(result["overgeneration_factor_per_realized_pair"]) + "`")
    lines.append("")
    lines.append("## Free variables")
    lines.append("")
    lines.append("For each selected transition key, the reciprocal skeleton leaves:")
    lines.append("")
    lines.append("- `S.from_A`")
    lines.append("- `S.from_B_or_slot`")
    lines.append("- `S.to_A`")
    lines.append("- `R.from_A`")
    lines.append("")
    lines.append("## Per-key counts")
    lines.append("")
    for item in per_key:
        lines.append(
            "- key=" + str(tuple(item["key"]))
            + ": synthetic=" + str(item["synthetic_candidate_count"])
            + ", realized_matches=" + str(item["realized_match_count"])
        )
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
    print("selected_key_count", result["selected_key_count"])
    print("total_synthetic_candidate_count", result["total_synthetic_candidate_count"])
    print("total_realized_match_count", result["total_realized_match_count"])
    print("overgeneration_factor_per_realized_pair", result["overgeneration_factor_per_realized_pair"])


if __name__ == "__main__":
    main()
