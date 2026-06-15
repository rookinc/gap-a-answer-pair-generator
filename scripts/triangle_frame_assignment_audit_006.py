#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"

OUT_JSON = ROOT / "artifacts/json/triangle_frame_assignment_audit_006.v1.json"
OUT_NOTE = ROOT / "notes/triangle_frame_assignment_audit_006.md"

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


def triangle_flags(s, r):
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

    triangle_frame_closure = (
        same_role_pair
        and shared_B_fixed
        and reverse_A_fixed
        and reverse_swaps_BC
        and same_C_track
        and forward_answer_seam
        and return_seam
        and same_delta_register
    )

    strict_pair_grammar = triangle_frame_closure

    return {
        "same_role_pair": same_role_pair,
        "shared_B_fixed_corner": "B" if shared_B_fixed else None,
        "reverse_partner_fixed_corner": "A" if reverse_A_fixed else None,
        "reverse_partner_swaps": "B/C" if reverse_swaps_BC else None,
        "same_C_track": same_C_track,
        "forward_answer_seam_S_to_C_equals_R_from_B": forward_answer_seam,
        "return_seam_S_from_C_equals_R_to_B": return_seam,
        "same_delta_register": same_delta_register,
        "triangle_frame_closure": triangle_frame_closure,
        "strict_pair_grammar": strict_pair_grammar,
    }


def frame_record(s, r, flags):
    return {
        "role_pair": s["role_pair"],
        "shared_role": s["station_role"],
        "reverse_role": r["station_role"],
        "C_track": [s["from_C"], s["to_C"]],
        "shared_B_face": {
            "fixed_corner": "B",
            "source_triangle": [s["from_A"], s["from_B"], s["from_C"]],
            "target_triangle": [s["to_A"], s["to_B"], s["to_C"]],
            "reading": "B fixed; A/C move",
        },
        "reverse_partner_face": {
            "fixed_corner": "A",
            "source_triangle": [r["from_A"], r["from_B"], r["from_C"]],
            "target_triangle": [r["to_A"], r["to_B"], r["to_C"]],
            "reading": "A fixed; B/C swap",
        },
        "seams": {
            "forward": "S.to_C = R.from_B",
            "return": "S.from_C = R.to_B",
        },
        "flags": flags,
        "shared_B_row": compact(s),
        "reverse_partner_row": compact(r),
    }


def main():
    data = load(IN_ROWS)

    rows = []
    for row in data.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared_rows = [r for r in rows if r["role_class"] == "shared_B"]
    reverse_rows = [r for r in rows if r["role_class"] == "reverse_partner"]

    candidates = []
    selected = []

    for s in shared_rows:
        for r in reverse_rows:
            if s["role_pair"] != r["role_pair"]:
                continue
            flags = triangle_flags(s, r)
            rec = frame_record(s, r, flags)
            candidates.append(rec)
            if flags["triangle_frame_closure"]:
                selected.append(rec)

    result = {
        "status": "triangle_frame_assignment_audit_recorded",
        "audit_id": "006",
        "input_rows": str(IN_ROWS),
        "candidate_universe": "All shared_B rows crossed with all reverse_partner rows having the same role_pair.",
        "candidate_count": len(candidates),
        "selected_count": len(selected),
        "selected_role_pair_counts": dict(sorted(Counter(r["role_pair"] for r in selected).items())),
        "selected_C_tracks": [
            {
                "role_pair": r["role_pair"],
                "shared_role": r["shared_role"],
                "reverse_role": r["reverse_role"],
                "C_track": r["C_track"],
            }
            for r in selected
        ],
        "selected_frames": selected,
        "sketch_reading": (
            "The hand sketch is interpreted as one ABC triangle with two complementary readings. "
            "The shared_B reading fixes B and lets A/C move. The reverse_partner reading fixes A "
            "and swaps B/C. A selected answer-pair is where both readings close on the same C-track."
        ),
        "interpretation": (
            "The triangle-frame predicate selects the same 12-style structure from the 48 row-pair "
            "candidate universe, but phrases the selector geometrically: fixed B face plus fixed A "
            "answer face, joined by forward and return C seams."
        ),
        "boundary": (
            "This is an exploratory frame audit over realized WXYZTI rows. It does not generate "
            "the C-transition support or the A/B assignments natively. It is not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Triangle frame assignment audit 006")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Sketch reading")
    lines.append("")
    lines.append(result["sketch_reading"])
    lines.append("")
    lines.append("## Candidate universe")
    lines.append("")
    lines.append(result["candidate_universe"])
    lines.append("")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- selected_role_pair_counts: `" + str(result["selected_role_pair_counts"]) + "`")
    lines.append("")
    lines.append("## Frame rule")
    lines.append("")
    lines.append("A candidate closes as a triangle-frame answer-pair when:")
    lines.append("")
    lines.append("- shared_B fixes corner `B`")
    lines.append("- reverse_partner fixes corner `A`")
    lines.append("- reverse_partner swaps `B/C`")
    lines.append("- both readings use the same `C` track")
    lines.append("- forward seam holds: `S.to_C = R.from_B`")
    lines.append("- return seam holds: `S.from_C = R.to_B`")
    lines.append("- delta/lift registers agree")
    lines.append("")
    lines.append("## Selected C tracks")
    lines.append("")
    for item in result["selected_C_tracks"]:
        lines.append(
            "- role_pair=" + item["role_pair"]
            + ", roles=" + item["shared_role"] + "/" + item["reverse_role"]
            + ", C_track=" + str(tuple(item["C_track"]))
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
    print("candidate_count", result["candidate_count"])
    print("selected_count", result["selected_count"])
    print("selected_role_pair_counts", result["selected_role_pair_counts"])


if __name__ == "__main__":
    main()
