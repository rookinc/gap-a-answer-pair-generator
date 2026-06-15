#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"

OUT_JSON = ROOT / "artifacts/json/triangle_frame_synthetic_reduction_audit_007.v1.json"
OUT_NOTE = ROOT / "notes/triangle_frame_synthetic_reduction_audit_007.md"

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


def row_sig(row):
    keys = [
        "station_role", "role_pair", "role_class",
        "from_A", "from_B", "from_C", "from_slot",
        "to_A", "to_B", "to_C", "to_slot",
        "integer_C_delta", "C_delta", "fiber_delta", "lift_q",
    ]
    return tuple((k, row.get(k)) for k in keys)


def pair_sig(s, r):
    return (row_sig(s), row_sig(r))


def triangle_frame_closure(s, r):
    same_role_pair = s["role_pair"] == r["role_pair"]

    shared_B_fixed = (
        s["from_B"] == s["to_B"]
        and s["from_slot"] == s["to_slot"]
        and s["from_B"] == s["from_slot"]
        and s["to_B"] == s["to_slot"]
    )

    reverse_A_fixed = r["from_A"] == r["to_A"]

    reverse_swaps_BC = (
        r["from_B"] == r["to_C"]
        and r["from_C"] == r["to_B"]
    )

    same_C_track = (
        s["from_C"] == r["from_C"]
        and s["to_C"] == r["to_C"]
    )

    forward_answer_seam = s["to_C"] == r["from_B"]
    return_seam = s["from_C"] == r["to_B"]

    same_delta_register = (
        s["integer_C_delta"] == r["integer_C_delta"]
        and s["C_delta"] == r["C_delta"]
        and s["lift_q"] == r["lift_q"]
    )

    return (
        same_role_pair
        and shared_B_fixed
        and reverse_A_fixed
        and reverse_swaps_BC
        and same_C_track
        and forward_answer_seam
        and return_seam
        and same_delta_register
    )


def build_realized_signatures():
    drows = load(IN_ROWS)
    rows = []
    for row in drows.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared = [r for r in rows if r["role_class"] == "shared_B"]
    reverse = [r for r in rows if r["role_class"] == "reverse_partner"]

    sigs = set()
    for s in shared:
        for r in reverse:
            if triangle_frame_closure(s, r):
                sigs.add(pair_sig(s, r))
    return sigs


def main():
    d002 = load(IN_002)
    selected_keys = d002["selected_pair_keys"]
    realized_sigs = build_realized_signatures()

    total = 0
    frame_selected = 0
    realized_matches = 0
    per_key = []
    role_pair_counts = Counter()
    frame_role_pair_counts = Counter()

    for key in selected_keys:
        role_pair, c0, c1, shared_role, reverse_role = key

        key_total = 0
        key_frame_selected = 0
        key_realized_matches = 0

        for s_from_A in range(15):
            for s_B in range(15):
                for s_to_A in range(15):
                    s = make_shared(role_pair, c0, c1, shared_role, s_from_A, s_B, s_to_A)

                    for r_A in range(15):
                        r = make_reverse(role_pair, c0, c1, reverse_role, r_A)

                        key_total += 1
                        total += 1
                        role_pair_counts[role_pair] += 1

                        closes = triangle_frame_closure(s, r)
                        if closes:
                            key_frame_selected += 1
                            frame_selected += 1
                            frame_role_pair_counts[role_pair] += 1

                        if pair_sig(s, r) in realized_sigs:
                            key_realized_matches += 1
                            realized_matches += 1

        per_key.append({
            "key": key,
            "synthetic_candidate_count": key_total,
            "triangle_frame_selected_count": key_frame_selected,
            "realized_match_count": key_realized_matches,
            "triangle_frame_reduction_factor": (
                key_total / key_frame_selected if key_frame_selected else None
            ),
        })

    result = {
        "status": "triangle_frame_synthetic_reduction_recorded",
        "audit_id": "007",
        "input_selector_002": str(IN_002),
        "input_realized_rows_for_evaluation_only": str(IN_ROWS),
        "uses_project18_expected_pair_records": False,
        "uses_realized_rows_for_generation": False,
        "uses_realized_rows_for_evaluation": True,
        "selected_key_count": len(selected_keys),
        "total_synthetic_candidate_count": total,
        "triangle_frame_selected_count": frame_selected,
        "realized_match_count": realized_matches,
        "triangle_frame_accepts_all_synthetic_skeletons": frame_selected == total,
        "triangle_frame_reduction_factor": total / frame_selected if frame_selected else None,
        "realized_reduction_factor_needed_after_frame": (
            frame_selected / realized_matches if realized_matches else None
        ),
        "role_pair_candidate_counts": dict(sorted(role_pair_counts.items())),
        "role_pair_frame_selected_counts": dict(sorted(frame_role_pair_counts.items())),
        "per_key": per_key,
        "interpretation": (
            "The triangle-frame rule is already built into the synthetic skeleton construction. "
            "It accepts the whole synthetic skeleton universe rather than selecting the realized "
            "A/B assignments. Therefore the hand-sketch frame explains the pair closure grammar, "
            "but the missing generator problem remains the native selection of A/B assignments."
        ),
        "boundary": (
            "This is not Gap A closure. It uses selected transition keys from 002 and realized rows "
            "only for evaluation. It shows that triangle-frame closure alone does not solve the "
            "synthetic overgeneration problem."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Triangle-frame synthetic reduction audit 007")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input discipline")
    lines.append("")
    lines.append("- uses_project18_expected_pair_records: `" + str(result["uses_project18_expected_pair_records"]) + "`")
    lines.append("- uses_realized_rows_for_generation: `" + str(result["uses_realized_rows_for_generation"]) + "`")
    lines.append("- uses_realized_rows_for_evaluation: `" + str(result["uses_realized_rows_for_evaluation"]) + "`")
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append("- selected_key_count: `" + str(result["selected_key_count"]) + "`")
    lines.append("- total_synthetic_candidate_count: `" + str(result["total_synthetic_candidate_count"]) + "`")
    lines.append("- triangle_frame_selected_count: `" + str(result["triangle_frame_selected_count"]) + "`")
    lines.append("- realized_match_count: `" + str(result["realized_match_count"]) + "`")
    lines.append("- triangle_frame_accepts_all_synthetic_skeletons: `" + str(result["triangle_frame_accepts_all_synthetic_skeletons"]) + "`")
    lines.append("- triangle_frame_reduction_factor: `" + str(result["triangle_frame_reduction_factor"]) + "`")
    lines.append("- realized_reduction_factor_needed_after_frame: `" + str(result["realized_reduction_factor_needed_after_frame"]) + "`")
    lines.append("")
    lines.append("## Per-key counts")
    lines.append("")
    for item in per_key:
        lines.append(
            "- key=" + str(tuple(item["key"]))
            + ": synthetic=" + str(item["synthetic_candidate_count"])
            + ", frame_selected=" + str(item["triangle_frame_selected_count"])
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
    print("total_synthetic_candidate_count", result["total_synthetic_candidate_count"])
    print("triangle_frame_selected_count", result["triangle_frame_selected_count"])
    print("realized_match_count", result["realized_match_count"])
    print("triangle_frame_accepts_all_synthetic_skeletons", result["triangle_frame_accepts_all_synthetic_skeletons"])
    print("realized_reduction_factor_needed_after_frame", result["realized_reduction_factor_needed_after_frame"])


if __name__ == "__main__":
    main()
