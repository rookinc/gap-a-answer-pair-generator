#!/usr/bin/env python3
import ast
import csv
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_NATIVE = ROOT / "source/project18_native_chain/json/c_transition_overlay_delta_generator_001.v1.json"
IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"

OUT_JSON = ROOT / "artifacts/json/native_rule_member_target_table_013.v1.json"
OUT_NOTE = ROOT / "notes/native_rule_member_target_table_013.md"
OUT_MEMBER_CSV = ROOT / "artifacts/csv/native_rule_members_013.v1.csv"
OUT_PAIR_CSV = ROOT / "artifacts/csv/native_answer_pairs_013.v1.csv"


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


def classify_member(m):
    label = str(m.get("label", "")).lower()
    if "shared" in label:
        return "shared_B"
    if "reverse" in label:
        return "reverse_partner"

    if m.get("from_B") == m.get("to_B") and m.get("from_slot") == m.get("to_slot"):
        return "shared_B"
    if m.get("from_A") == m.get("to_A") and m.get("from_B") == m.get("to_C") and m.get("from_C") == m.get("to_B"):
        return "reverse_partner"

    return "unknown"


def selected_key_map(d002):
    out = {}
    for k in d002["selected_pair_keys"]:
        role_pair, c0, c1, shared_role, reverse_role = k
        out[(int(c0), int(c1))] = {
            "role_pair": role_pair,
            "shared_role": shared_role,
            "reverse_role": reverse_role,
        }
    return out


def member_row(tk, role_pair, m):
    c0, c1 = tk
    return {
        "transition_key": str(tk),
        "from_C_key": c0,
        "to_C_key": c1,
        "role_pair": role_pair,
        "edge_role": m.get("edge_role"),
        "label": m.get("label"),
        "classified_role_class": classify_member(m),
        "form_index": m.get("form_index"),
        "edge_index": m.get("edge_index"),
        "from_A": m.get("from_A"),
        "from_B": m.get("from_B"),
        "from_C": m.get("from_C"),
        "from_slot": m.get("from_slot"),
        "from_fiber": m.get("from_fiber"),
        "from_columns": str(m.get("from_columns")),
        "to_A": m.get("to_A"),
        "to_B": m.get("to_B"),
        "to_C": m.get("to_C"),
        "to_slot": m.get("to_slot"),
        "to_fiber": m.get("to_fiber"),
        "to_columns": str(m.get("to_columns")),
        "fiber_delta_mod60": m.get("fiber_delta_mod60"),
        "slot_delta_mod15": m.get("slot_delta_mod15"),
    }


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})


def pair_signature(shared, reverse):
    return {
        "S_from_A": shared.get("from_A"),
        "S_B": shared.get("from_B"),
        "S_to_A": shared.get("to_A"),
        "R_A": reverse.get("from_A"),
    }


def main():
    native = load(IN_NATIVE)
    d002 = load(IN_002)

    selected_by_transition = selected_key_map(d002)
    rule_members = native.get("rule_members", {})

    member_rows = []
    pair_rows = []
    errors = []

    for raw_key, members in sorted(rule_members.items(), key=lambda kv: parse_transition_key(kv[0])):
        tk = parse_transition_key(raw_key)
        selected = selected_by_transition.get(tk)
        role_pair = selected["role_pair"] if selected else None

        class_buckets = defaultdict(list)
        for m in members:
            class_buckets[classify_member(m)].append(m)
            member_rows.append(member_row(tk, role_pair, m))

        shared = class_buckets.get("shared_B", [])
        reverse = class_buckets.get("reverse_partner", [])

        if len(shared) != 1 or len(reverse) != 1:
            errors.append({
                "transition_key": list(tk),
                "class_counts": {k: len(v) for k, v in class_buckets.items()},
            })
            continue

        s = shared[0]
        r = reverse[0]

        expected_shared_role = selected["shared_role"] if selected else None
        expected_reverse_role = selected["reverse_role"] if selected else None

        pair_rows.append({
            "transition_key": str(tk),
            "from_C": tk[0],
            "to_C": tk[1],
            "role_pair": role_pair,
            "shared_role": s.get("edge_role"),
            "reverse_role": r.get("edge_role"),
            "expected_shared_role_from_002": expected_shared_role,
            "expected_reverse_role_from_002": expected_reverse_role,
            "roles_match_002": (
                s.get("edge_role") == expected_shared_role
                and r.get("edge_role") == expected_reverse_role
            ),
            "S_from_A": s.get("from_A"),
            "S_B": s.get("from_B"),
            "S_to_A": s.get("to_A"),
            "R_A": r.get("from_A"),
            "S_A_delta": (s.get("to_A") - s.get("from_A")) % 15,
            "R_minus_S_from_A": (r.get("from_A") - s.get("from_A")) % 15,
            "S_B_minus_to_C": (s.get("from_B") - s.get("to_C")) % 15,
            "shared_from_columns": str(s.get("from_columns")),
            "shared_to_columns": str(s.get("to_columns")),
            "reverse_from_columns": str(r.get("from_columns")),
            "reverse_to_columns": str(r.get("to_columns")),
            "shared_from_fiber": s.get("from_fiber"),
            "shared_to_fiber": s.get("to_fiber"),
            "reverse_from_fiber": r.get("from_fiber"),
            "reverse_to_fiber": r.get("to_fiber"),
        })

    selected_transition_count = len(selected_by_transition)
    native_transition_count = len(rule_members)
    native_pair_count = len(pair_rows)
    native_member_count = len(member_rows)

    synthetic_candidate_count_per_key = 15 ** 4
    total_synthetic_candidate_count = selected_transition_count * synthetic_candidate_count_per_key

    member_fields = [
        "transition_key", "from_C_key", "to_C_key", "role_pair",
        "edge_role", "label", "classified_role_class",
        "form_index", "edge_index",
        "from_A", "from_B", "from_C", "from_slot", "from_fiber", "from_columns",
        "to_A", "to_B", "to_C", "to_slot", "to_fiber", "to_columns",
        "fiber_delta_mod60", "slot_delta_mod15",
    ]

    pair_fields = [
        "transition_key", "from_C", "to_C", "role_pair",
        "shared_role", "reverse_role",
        "expected_shared_role_from_002", "expected_reverse_role_from_002", "roles_match_002",
        "S_from_A", "S_B", "S_to_A", "R_A",
        "S_A_delta", "R_minus_S_from_A", "S_B_minus_to_C",
        "shared_from_columns", "shared_to_columns",
        "reverse_from_columns", "reverse_to_columns",
        "shared_from_fiber", "shared_to_fiber",
        "reverse_from_fiber", "reverse_to_fiber",
    ]

    write_csv(OUT_MEMBER_CSV, member_rows, member_fields)
    write_csv(OUT_PAIR_CSV, pair_rows, pair_fields)

    result = {
        "status": "native_rule_member_target_table_recorded",
        "audit_id": "013",
        "input_native_rule_members": str(IN_NATIVE),
        "input_selector_002": str(IN_002),
        "member_csv": str(OUT_MEMBER_CSV),
        "pair_csv": str(OUT_PAIR_CSV),
        "native_transition_count": native_transition_count,
        "native_member_count": native_member_count,
        "native_pair_count": native_pair_count,
        "selected_transition_count": selected_transition_count,
        "all_native_transitions_selected_in_002": set(rule_members.keys()) is not None and native_transition_count == selected_transition_count,
        "member_class_counts": dict(sorted(Counter(r["classified_role_class"] for r in member_rows).items())),
        "member_edge_role_counts": dict(sorted(Counter(str(r["edge_role"]) for r in member_rows).items())),
        "pair_role_pair_counts": dict(sorted(Counter(str(r["role_pair"]) for r in pair_rows).items())),
        "all_pairs_have_two_members": len(errors) == 0,
        "all_pair_roles_match_002": all(r["roles_match_002"] for r in pair_rows),
        "synthetic_candidate_count_per_key": synthetic_candidate_count_per_key,
        "total_synthetic_candidate_count": total_synthetic_candidate_count,
        "native_pair_target_count": native_pair_count,
        "reduction_factor_synthetic_to_native_pairs": (
            total_synthetic_candidate_count / native_pair_count if native_pair_count else None
        ),
        "errors": errors,
        "native_answer_pairs": pair_rows,
        "interpretation": (
            "This audit promotes the native rule_members layer to an explicit Project 21 target table. "
            "The A/B assignments are present as native transition members: two members per selected "
            "C-transition, one shared_B and one reverse_partner. The remaining generator problem is "
            "therefore to derive these 24 native member rows, not to infer A/B assignments from the "
            "late row-pair table."
        ),
        "boundary": (
            "This is a target-table extraction and comparison audit. It does not derive the native "
            "rule_members from G60, and therefore does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native rule member target table 013")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("- member_csv: `" + str(OUT_MEMBER_CSV) + "`")
    lines.append("- pair_csv: `" + str(OUT_PAIR_CSV) + "`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- native_transition_count: `" + str(native_transition_count) + "`")
    lines.append("- native_member_count: `" + str(native_member_count) + "`")
    lines.append("- native_pair_count: `" + str(native_pair_count) + "`")
    lines.append("- selected_transition_count: `" + str(selected_transition_count) + "`")
    lines.append("- member_class_counts: `" + str(result["member_class_counts"]) + "`")
    lines.append("- member_edge_role_counts: `" + str(result["member_edge_role_counts"]) + "`")
    lines.append("- pair_role_pair_counts: `" + str(result["pair_role_pair_counts"]) + "`")
    lines.append("- all_pairs_have_two_members: `" + str(result["all_pairs_have_two_members"]) + "`")
    lines.append("- all_pair_roles_match_002: `" + str(result["all_pair_roles_match_002"]) + "`")
    lines.append("")
    lines.append("## Synthetic comparison")
    lines.append("")
    lines.append("- synthetic_candidate_count_per_key: `" + str(synthetic_candidate_count_per_key) + "`")
    lines.append("- total_synthetic_candidate_count: `" + str(total_synthetic_candidate_count) + "`")
    lines.append("- native_pair_target_count: `" + str(native_pair_count) + "`")
    lines.append("- reduction_factor_synthetic_to_native_pairs: `" + str(result["reduction_factor_synthetic_to_native_pairs"]) + "`")
    lines.append("")
    lines.append("## Native answer-pair target rows")
    lines.append("")
    for r in pair_rows:
        lines.append(
            "- transition=" + r["transition_key"]
            + ", role_pair=" + str(r["role_pair"])
            + ", roles=" + str(r["shared_role"]) + "/" + str(r["reverse_role"])
            + ", free_vars=(S.from_A=" + str(r["S_from_A"])
            + ", S.B=" + str(r["S_B"])
            + ", S.to_A=" + str(r["S_to_A"])
            + ", R.A=" + str(r["R_A"]) + ")"
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
    print("wrote", OUT_MEMBER_CSV)
    print("wrote", OUT_PAIR_CSV)
    print("status", result["status"])
    print("native_transition_count", native_transition_count)
    print("native_member_count", native_member_count)
    print("native_pair_count", native_pair_count)
    print("all_pairs_have_two_members", result["all_pairs_have_two_members"])
    print("all_pair_roles_match_002", result["all_pair_roles_match_002"])
    print("reduction_factor_synthetic_to_native_pairs", result["reduction_factor_synthetic_to_native_pairs"])


if __name__ == "__main__":
    main()
