#!/usr/bin/env python3
import ast
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_NATIVE = ROOT / "source/project18_native_chain/json/c_transition_overlay_delta_generator_001.v1.json"
IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
IN_004 = ROOT / "artifacts/json/realized_free_variable_table_004.v1.json"

OUT_JSON = ROOT / "artifacts/json/native_rule_member_alignment_012.v1.json"
OUT_NOTE = ROOT / "notes/native_rule_member_alignment_012.md"


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_transition_key(k):
    if isinstance(k, (list, tuple)) and len(k) == 2:
        return (int(k[0]), int(k[1]))
    if isinstance(k, str):
        try:
            v = ast.literal_eval(k)
            if isinstance(v, (list, tuple)) and len(v) == 2:
                return (int(v[0]), int(v[1]))
        except Exception:
            pass
        bits = k.replace("(", "").replace(")", "").replace(",", " ").split()
        if len(bits) == 2:
            return (int(bits[0]), int(bits[1]))
    raise ValueError("cannot parse transition key: " + repr(k))


def member_signature(m):
    keys = [
        "edge_role",
        "label",
        "from_A",
        "from_B",
        "from_C",
        "from_slot",
        "to_A",
        "to_B",
        "to_C",
        "to_slot",
        "fiber_delta_mod60",
        "slot_delta_mod15",
    ]
    return {k: m.get(k) for k in keys}


def selected_key_from_002(k):
    role_pair, c0, c1, shared_role, reverse_role = k
    return {
        "role_pair": role_pair,
        "c0": int(c0),
        "c1": int(c1),
        "shared_role": shared_role,
        "reverse_role": reverse_role,
    }


def free_var_lookup(records):
    out = {}
    for r in records:
        key = (
            r["role_pair"],
            int(r["c0"]),
            int(r["c1"]),
            r["shared"],
            r["reverse"],
        )
        out[key] = r
    return out


def classify_member(m):
    label = str(m.get("label", "")).lower()
    edge_role = str(m.get("edge_role", ""))
    if "shared" in label:
        return "shared_B"
    if "reverse" in label:
        return "reverse_partner"

    # Fallback by invariant shape.
    if m.get("from_B") == m.get("to_B") and m.get("from_slot") == m.get("to_slot"):
        return "shared_B"
    if m.get("from_A") == m.get("to_A") and m.get("from_B") == m.get("to_C") and m.get("from_C") == m.get("to_B"):
        return "reverse_partner"

    return "unknown"


def main():
    native = load(IN_NATIVE)
    d002 = load(IN_002)
    d004 = load(IN_004)

    selected = [selected_key_from_002(k) for k in d002["selected_pair_keys"]]
    selected_transition_set = {(x["c0"], x["c1"]) for x in selected}
    free_lookup = free_var_lookup(d004["records"])

    rule_members_raw = native.get("rule_members", {})
    native_by_transition = {}
    flat_members = []

    for k, members in rule_members_raw.items():
        tk = parse_transition_key(k)
        native_by_transition[tk] = members
        for m in members:
            mm = dict(m)
            mm["transition_key"] = list(tk)
            mm["classified_role_class"] = classify_member(mm)
            flat_members.append(mm)

    alignments = []
    missing_transition_keys = []
    selected_match_count = 0
    free_variable_match_count = 0
    ambiguous_member_count = 0

    for item in selected:
        tk = (item["c0"], item["c1"])
        members = native_by_transition.get(tk, [])
        if not members:
            missing_transition_keys.append(list(tk))
            continue

        by_class = defaultdict(list)
        for m in members:
            by_class[classify_member(m)].append(m)

        shared_members = by_class.get("shared_B", [])
        reverse_members = by_class.get("reverse_partner", [])

        if len(shared_members) != 1 or len(reverse_members) != 1:
            ambiguous_member_count += 1

        free_key = (
            item["role_pair"],
            item["c0"],
            item["c1"],
            item["shared_role"],
            item["reverse_role"],
        )
        fv = free_lookup.get(free_key)

        free_match = False
        if fv and len(shared_members) == 1 and len(reverse_members) == 1:
            s = shared_members[0]
            r = reverse_members[0]
            free_match = (
                s.get("from_A") == fv["S_from_A"]
                and s.get("from_B") == fv["S_B"]
                and s.get("to_A") == fv["S_to_A"]
                and r.get("from_A") == fv["R_A"]
            )

        if len(members) == 2:
            selected_match_count += 1
        if free_match:
            free_variable_match_count += 1

        alignments.append({
            "role_pair": item["role_pair"],
            "transition_key": list(tk),
            "shared_role_from_002": item["shared_role"],
            "reverse_role_from_002": item["reverse_role"],
            "native_member_count": len(members),
            "native_class_counts": dict(sorted(Counter(classify_member(m) for m in members).items())),
            "free_variable_record_found": fv is not None,
            "free_variable_values_from_004": fv,
            "native_free_variable_match": free_match,
            "shared_B_members": [member_signature(m) for m in shared_members],
            "reverse_partner_members": [member_signature(m) for m in reverse_members],
            "all_native_members": [member_signature(m) for m in members],
            "native_columns": [
                {
                    "class": classify_member(m),
                    "edge_role": m.get("edge_role"),
                    "label": m.get("label"),
                    "from_columns": m.get("from_columns"),
                    "to_columns": m.get("to_columns"),
                    "from_fiber": m.get("from_fiber"),
                    "to_fiber": m.get("to_fiber"),
                }
                for m in members
            ],
        })

    all_transition_keys = sorted(native_by_transition.keys())

    result = {
        "status": "native_rule_member_alignment_recorded",
        "audit_id": "012",
        "input_native_rule_members": str(IN_NATIVE),
        "input_selector_002": str(IN_002),
        "input_free_variable_table_004": str(IN_004),
        "native_transition_count": len(native_by_transition),
        "native_flat_member_count": len(flat_members),
        "selected_transition_count": len(selected),
        "selected_transition_keys": [list(x) for x in sorted(selected_transition_set)],
        "native_transition_keys": [list(x) for x in all_transition_keys],
        "missing_transition_keys": missing_transition_keys,
        "selected_transitions_with_two_members": selected_match_count,
        "free_variable_match_count": free_variable_match_count,
        "ambiguous_member_count": ambiguous_member_count,
        "flat_member_class_counts": dict(sorted(Counter(m["classified_role_class"] for m in flat_members).items())),
        "flat_member_label_counts": dict(sorted(Counter(str(m.get("label")) for m in flat_members).items())),
        "flat_member_edge_role_counts": dict(sorted(Counter(str(m.get("edge_role")) for m in flat_members).items())),
        "alignments": alignments,
        "interpretation": (
            "This audit aligns the native rule_members from the imported Project 18 native-chain "
            "artifact with the 12 selected C-tracks from Project 21. If the native members match "
            "the free variables in 004, then the A/B assignments are not absent; they are present "
            "in the earlier native transition member layer."
        ),
        "boundary": (
            "This is an alignment audit. It does not yet derive the rule_members natively from G60, "
            "and therefore does not close Gap A by itself."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native rule member alignment 012")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append("- native rule members: `" + str(IN_NATIVE) + "`")
    lines.append("- selector 002: `" + str(IN_002) + "`")
    lines.append("- free-variable table 004: `" + str(IN_004) + "`")
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append("- native_transition_count: `" + str(result["native_transition_count"]) + "`")
    lines.append("- native_flat_member_count: `" + str(result["native_flat_member_count"]) + "`")
    lines.append("- selected_transition_count: `" + str(result["selected_transition_count"]) + "`")
    lines.append("- missing_transition_keys: `" + str(result["missing_transition_keys"]) + "`")
    lines.append("- selected_transitions_with_two_members: `" + str(result["selected_transitions_with_two_members"]) + "`")
    lines.append("- free_variable_match_count: `" + str(result["free_variable_match_count"]) + "`")
    lines.append("- ambiguous_member_count: `" + str(result["ambiguous_member_count"]) + "`")
    lines.append("- flat_member_class_counts: `" + str(result["flat_member_class_counts"]) + "`")
    lines.append("- flat_member_label_counts: `" + str(result["flat_member_label_counts"]) + "`")
    lines.append("- flat_member_edge_role_counts: `" + str(result["flat_member_edge_role_counts"]) + "`")
    lines.append("")
    lines.append("## Alignment rows")
    lines.append("")
    for a in alignments:
        lines.append(
            "- role_pair=" + a["role_pair"]
            + ", transition=" + str(tuple(a["transition_key"]))
            + ", native_members=" + str(a["native_member_count"])
            + ", class_counts=" + str(a["native_class_counts"])
            + ", free_match=" + str(a["native_free_variable_match"])
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
    print("native_transition_count", result["native_transition_count"])
    print("native_flat_member_count", result["native_flat_member_count"])
    print("selected_transition_count", result["selected_transition_count"])
    print("missing_transition_keys", result["missing_transition_keys"])
    print("selected_transitions_with_two_members", result["selected_transitions_with_two_members"])
    print("free_variable_match_count", result["free_variable_match_count"])
    print("ambiguous_member_count", result["ambiguous_member_count"])
    print("flat_member_class_counts", result["flat_member_class_counts"])


if __name__ == "__main__":
    main()
