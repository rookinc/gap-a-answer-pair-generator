#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_TARGET = ROOT / "artifacts/csv/native_rule_members_013.v1.csv"
IN_G60 = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"

OUT_JSON = ROOT / "artifacts/json/native_members_vs_g60_overlay_edges_014.v1.json"
OUT_NOTE = ROOT / "notes/native_members_vs_g60_overlay_edges_014.md"

SIG_FIELDS = [
    "edge_role",
    "label",
    "form_index",
    "edge_index",
    "from_A",
    "from_B",
    "from_C",
    "from_slot",
    "from_fiber",
    "from_columns",
    "to_A",
    "to_B",
    "to_C",
    "to_slot",
    "to_fiber",
    "to_columns",
    "fiber_delta_mod60",
    "slot_delta_mod15",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def normalize_value(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return str(v)
    return str(v)


def signature(row):
    return tuple((k, normalize_value(row.get(k))) for k in SIG_FIELDS)


def compact(row):
    return {k: normalize_value(row.get(k)) for k in SIG_FIELDS}


def main():
    target_rows = load_csv(IN_TARGET)
    g60 = load_json(IN_G60)
    edge_records = g60.get("edge_records", [])

    target_sigs = {signature(r) for r in target_rows}
    edge_sigs = {signature(r) for r in edge_records}

    intersection = target_sigs & edge_sigs
    target_only = target_sigs - edge_sigs
    edge_only = edge_sigs - target_sigs

    target_by_sig = {signature(r): r for r in target_rows}
    edge_by_sig = {signature(r): r for r in edge_records}

    matched = []
    for sig in sorted(intersection):
        t = target_by_sig[sig]
        e = edge_by_sig[sig]
        matched.append({
            "transition_key": t.get("transition_key"),
            "edge_role": t.get("edge_role"),
            "label": t.get("label"),
            "from_C": t.get("from_C"),
            "to_C": t.get("to_C"),
            "from_key": e.get("from_key"),
            "to_key": e.get("to_key"),
            "from_columns": t.get("from_columns"),
            "to_columns": t.get("to_columns"),
            "from_fiber": t.get("from_fiber"),
            "to_fiber": t.get("to_fiber"),
        })

    result = {
        "status": "native_members_vs_g60_overlay_edges_recorded",
        "audit_id": "014",
        "input_target_members": str(IN_TARGET),
        "input_g60_overlay": str(IN_G60),
        "signature_fields": SIG_FIELDS,
        "target_member_count": len(target_rows),
        "g60_edge_record_count": len(edge_records),
        "target_signature_count": len(target_sigs),
        "g60_edge_signature_count": len(edge_sigs),
        "intersection_count": len(intersection),
        "target_only_count": len(target_only),
        "g60_only_count": len(edge_only),
        "exact_signature_match": len(target_only) == 0 and len(edge_only) == 0,
        "target_edge_role_counts": dict(sorted(Counter(r.get("edge_role") for r in target_rows).items())),
        "g60_edge_role_counts": dict(sorted(Counter(r.get("edge_role") for r in edge_records).items())),
        "target_label_counts": dict(sorted(Counter(r.get("label") for r in target_rows).items())),
        "g60_label_counts": dict(sorted(Counter(r.get("label") for r in edge_records).items())),
        "matched_rows_first_40": matched[:40],
        "target_only_first_20": [dict(sig) for sig in list(target_only)[:20]],
        "g60_only_first_20": [dict(sig) for sig in list(edge_only)[:20]],
        "interpretation": (
            "This audit compares the Project 21 native rule-member target table against the earlier "
            "G60 native overlay edge_records. An exact signature match means the 24 rule members are "
            "the same 24 native overlay edge records, so the remaining problem shifts from deriving "
            "late answer-pair rows to deriving the native overlay edge-record construction."
        ),
        "boundary": (
            "This is a comparison audit. It does not derive the G60 overlay edge records and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native members vs G60 overlay edges 014")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append("- target members: `" + str(IN_TARGET) + "`")
    lines.append("- G60 overlay: `" + str(IN_G60) + "`")
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append("- target_member_count: `" + str(result["target_member_count"]) + "`")
    lines.append("- g60_edge_record_count: `" + str(result["g60_edge_record_count"]) + "`")
    lines.append("- intersection_count: `" + str(result["intersection_count"]) + "`")
    lines.append("- target_only_count: `" + str(result["target_only_count"]) + "`")
    lines.append("- g60_only_count: `" + str(result["g60_only_count"]) + "`")
    lines.append("- exact_signature_match: `" + str(result["exact_signature_match"]) + "`")
    lines.append("- target_edge_role_counts: `" + str(result["target_edge_role_counts"]) + "`")
    lines.append("- g60_edge_role_counts: `" + str(result["g60_edge_role_counts"]) + "`")
    lines.append("- target_label_counts: `" + str(result["target_label_counts"]) + "`")
    lines.append("- g60_label_counts: `" + str(result["g60_label_counts"]) + "`")
    lines.append("")
    lines.append("## Matched rows first 24")
    lines.append("")
    for r in matched[:24]:
        lines.append(
            "- transition=" + str(r["transition_key"])
            + ", role=" + str(r["edge_role"])
            + ", label=" + str(r["label"])
            + ", C=(" + str(r["from_C"]) + "," + str(r["to_C"]) + ")"
            + ", keys=" + str(r["from_key"]) + " -> " + str(r["to_key"])
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
    print("target_member_count", result["target_member_count"])
    print("g60_edge_record_count", result["g60_edge_record_count"])
    print("intersection_count", result["intersection_count"])
    print("target_only_count", result["target_only_count"])
    print("g60_only_count", result["g60_only_count"])
    print("exact_signature_match", result["exact_signature_match"])


if __name__ == "__main__":
    main()
