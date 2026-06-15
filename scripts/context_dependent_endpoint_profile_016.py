#!/usr/bin/env python3
import itertools
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60 = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"

OUT_JSON = ROOT / "artifacts/json/context_dependent_endpoint_profile_016.v1.json"
OUT_NOTE = ROOT / "notes/context_dependent_endpoint_profile_016.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

SOURCE_ONLY_FEATURES = [
    "label",
    "edge_role",
    "role_pair",
    "form_index",
    "edge_index",
    "from_A",
    "from_B",
    "from_C",
    "from_slot",
    "from_fiber",
    "from_columns",
    "from_key",
]

EXTENDED_FEATURES = SOURCE_ONLY_FEATURES + [
    "fiber_delta_mod60",
    "slot_delta_mod15",
]

TARGETS = [
    "to_endpoint",
    "to_ABC",
    "to_key",
    "to_columns",
    "to_fiber",
    "to_A",
    "to_B",
    "to_C",
    "to_slot",
    "fiber_delta_mod60",
    "slot_delta_mod15",
]


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def norm(v):
    if isinstance(v, list):
        return tuple(v)
    if isinstance(v, dict):
        return tuple(sorted((k, norm(x)) for k, x in v.items()))
    return v


def row_value(row, key):
    if key == "role_pair":
        return ROLE_PAIR_BY_EDGE_ROLE.get(str(row.get("edge_role")))
    if key == "to_endpoint":
        return (
            row.get("to_A"),
            row.get("to_B"),
            row.get("to_C"),
            row.get("to_slot"),
            row.get("to_fiber"),
            norm(row.get("to_columns")),
            row.get("to_key"),
        )
    if key == "to_ABC":
        return (row.get("to_A"), row.get("to_B"), row.get("to_C"))
    if key == "from_columns":
        return norm(row.get("from_columns"))
    if key == "to_columns":
        return norm(row.get("to_columns"))
    return row.get(key)


def feature_value(row, features):
    return tuple((f, row_value(row, f)) for f in features)


def target_value(row, target):
    return row_value(row, target)


def deterministic_test(rows, features, target):
    groups = defaultdict(set)
    for r in rows:
        groups[feature_value(r, features)].add(norm(target_value(r, target)))

    ambiguous = []
    for k, values in groups.items():
        if len(values) > 1:
            ambiguous.append({
                "feature_value": str(k),
                "target_values": [str(v) for v in sorted(values, key=str)],
            })

    return {
        "features": list(features),
        "target": target,
        "exact": len(ambiguous) == 0,
        "group_count": len(groups),
        "max_group_size": max(Counter(feature_value(r, features) for r in rows).values()) if rows else 0,
        "ambiguous_group_count": len(ambiguous),
        "ambiguous_groups_first_10": ambiguous[:10],
    }


def rank_tests(tests):
    exact = [t for t in tests if t["exact"]]
    exact.sort(key=lambda t: (len(t["features"]), t["group_count"], t["target"], str(t["features"])))
    return exact


def all_combos(features, max_size):
    for n in range(1, max_size + 1):
        for combo in itertools.combinations(features, n):
            yield combo


def law_checks(rows):
    by_label = defaultdict(list)
    by_role = defaultdict(list)
    by_pair = defaultdict(list)

    for r in rows:
        by_label[str(r.get("label"))].append(r)
        by_role[str(r.get("edge_role"))].append(r)
        by_pair[ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))].append(r)

    def count_true(rs, pred):
        return sum(1 for r in rs if pred(r))

    label_checks = {}
    for label, rs in sorted(by_label.items()):
        label_checks[label] = {
            "row_count": len(rs),
            "edge_role_counts": dict(sorted(Counter(str(r.get("edge_role")) for r in rs).items())),
            "A_preserved_count": count_true(rs, lambda r: r.get("to_A") == r.get("from_A")),
            "B_preserved_count": count_true(rs, lambda r: r.get("to_B") == r.get("from_B")),
            "C_preserved_count": count_true(rs, lambda r: r.get("to_C") == r.get("from_C")),
            "slot_preserved_count": count_true(rs, lambda r: r.get("to_slot") == r.get("from_slot")),
            "fiber_mod15_tracks_C_count": count_true(rs, lambda r: r.get("from_fiber") % 15 == r.get("from_C") and r.get("to_fiber") % 15 == r.get("to_C")),
            "reverse_swap_BC_count": count_true(rs, lambda r: r.get("to_A") == r.get("from_A") and r.get("to_B") == r.get("from_C") and r.get("to_C") == r.get("from_B")),
            "shared_B_face_count": count_true(rs, lambda r: r.get("to_B") == r.get("from_B") and r.get("to_slot") == r.get("from_slot")),
            "from_columns_equal_to_columns_count": count_true(rs, lambda r: norm(r.get("from_columns")) == norm(r.get("to_columns"))),
        }

    role_rows = []
    for role, rs in sorted(by_role.items()):
        role_rows.append({
            "edge_role": role,
            "row_count": len(rs),
            "label_counts": dict(sorted(Counter(str(r.get("label")) for r in rs).items())),
            "role_pair": ROLE_PAIR_BY_EDGE_ROLE.get(role),
            "from_C_values": sorted(set(r.get("from_C") for r in rs)),
            "to_C_values": sorted(set(r.get("to_C") for r in rs)),
            "fiber_delta_counts": dict(sorted(Counter(str(r.get("fiber_delta_mod60")) for r in rs).items())),
            "slot_delta_counts": dict(sorted(Counter(str(r.get("slot_delta_mod15")) for r in rs).items())),
            "from_key_values": sorted(set(str(r.get("from_key")) for r in rs)),
            "to_key_values": sorted(set(str(r.get("to_key")) for r in rs)),
        })

    pair_rows = []
    for pair, rs in sorted(by_pair.items()):
        pair_rows.append({
            "role_pair": pair,
            "row_count": len(rs),
            "edge_role_counts": dict(sorted(Counter(str(r.get("edge_role")) for r in rs).items())),
            "label_counts": dict(sorted(Counter(str(r.get("label")) for r in rs).items())),
            "from_C_values": sorted(set(r.get("from_C") for r in rs)),
            "to_C_values": sorted(set(r.get("to_C") for r in rs)),
            "transition_pairs": sorted(set((r.get("from_C"), r.get("to_C")) for r in rs)),
        })

    return {
        "label_checks": label_checks,
        "role_rows": role_rows,
        "role_pair_rows": pair_rows,
    }


def main():
    data = load(IN_G60)
    rows = data.get("edge_records", [])

    # Add derived role_pair to rows for easier inspection.
    rows = [dict(r, role_pair=ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))) for r in rows]

    source_tests = []
    extended_tests = []

    for target in TARGETS:
        for combo in all_combos(SOURCE_ONLY_FEATURES, 3):
            source_tests.append(deterministic_test(rows, combo, target))
        for combo in all_combos(EXTENDED_FEATURES, 3):
            extended_tests.append(deterministic_test(rows, combo, target))

    source_exact = rank_tests(source_tests)
    extended_exact = rank_tests(extended_tests)

    endpoint_source_exact = [t for t in source_exact if t["target"] == "to_endpoint"]
    endpoint_extended_exact = [t for t in extended_exact if t["target"] == "to_endpoint"]

    best_by_target_source = {}
    best_by_target_extended = {}
    for target in TARGETS:
        best_by_target_source[target] = [t for t in source_exact if t["target"] == target][:10]
        best_by_target_extended[target] = [t for t in extended_exact if t["target"] == target][:10]

    laws = law_checks(rows)

    result = {
        "status": "context_dependent_endpoint_profile_recorded",
        "audit_id": "016",
        "input_g60_overlay": str(IN_G60),
        "row_count": len(rows),
        "source_only_features": SOURCE_ONLY_FEATURES,
        "extended_features": EXTENDED_FEATURES,
        "targets": TARGETS,
        "source_test_count": len(source_tests),
        "extended_test_count": len(extended_tests),
        "source_exact_count": len(source_exact),
        "extended_exact_count": len(extended_exact),
        "endpoint_source_exact_count": len(endpoint_source_exact),
        "endpoint_extended_exact_count": len(endpoint_extended_exact),
        "endpoint_source_exact_first_30": endpoint_source_exact[:30],
        "endpoint_extended_exact_first_30": endpoint_extended_exact[:30],
        "best_by_target_source_first_10": best_by_target_source,
        "best_by_target_extended_first_10": best_by_target_extended,
        "law_checks": laws,
        "interpretation": (
            "This audit profiles the 24 G60 native overlay edge records as a context-dependent "
            "endpoint map. It does not search for one global permutation. Instead it asks which "
            "small context fields determine endpoint targets and records the exact visible laws for "
            "reverse_partner and shared_B rows."
        ),
        "boundary": (
            "This is a context profile over the already selected 24 edge records. It does not derive "
            "the 24 records from a candidate universe and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Context-dependent endpoint profile 016")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input")
    lines.append("")
    lines.append("- G60 overlay artifact: `" + str(IN_G60) + "`")
    lines.append("- row_count: `" + str(len(rows)) + "`")
    lines.append("")
    lines.append("## Search")
    lines.append("")
    lines.append("- source_test_count: `" + str(result["source_test_count"]) + "`")
    lines.append("- extended_test_count: `" + str(result["extended_test_count"]) + "`")
    lines.append("- source_exact_count: `" + str(result["source_exact_count"]) + "`")
    lines.append("- extended_exact_count: `" + str(result["extended_exact_count"]) + "`")
    lines.append("- endpoint_source_exact_count: `" + str(result["endpoint_source_exact_count"]) + "`")
    lines.append("- endpoint_extended_exact_count: `" + str(result["endpoint_extended_exact_count"]) + "`")
    lines.append("")
    lines.append("## Best source-only endpoint tests")
    lines.append("")
    if endpoint_source_exact:
        for t in endpoint_source_exact[:20]:
            lines.append("- features=`" + str(t["features"]) + "`, groups=`" + str(t["group_count"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Best extended endpoint tests")
    lines.append("")
    if endpoint_extended_exact:
        for t in endpoint_extended_exact[:20]:
            lines.append("- features=`" + str(t["features"]) + "`, groups=`" + str(t["group_count"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Best source-only component tests")
    lines.append("")
    for target in TARGETS:
        lines.append("- target: `" + target + "`")
        tests = best_by_target_source.get(target, [])
        if tests:
            for t in tests[:5]:
                lines.append("  - features=`" + str(t["features"]) + "`, groups=`" + str(t["group_count"]) + "`")
        else:
            lines.append("  - none")
    lines.append("")
    lines.append("## Label law checks")
    lines.append("")
    for label, checks in laws["label_checks"].items():
        lines.append("- label: `" + label + "`")
        for k, v in checks.items():
            lines.append("  - " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Role rows")
    lines.append("")
    for r in laws["role_rows"]:
        lines.append(
            "- role=`" + str(r["edge_role"]) + "`, label_counts=`" + str(r["label_counts"])
            + "`, from_C=`" + str(r["from_C_values"]) + "`, to_C=`" + str(r["to_C_values"]) + "`"
        )
    lines.append("")
    lines.append("## Role-pair rows")
    lines.append("")
    for r in laws["role_pair_rows"]:
        lines.append(
            "- role_pair=`" + str(r["role_pair"]) + "`, roles=`" + str(r["edge_role_counts"])
            + "`, transitions=`" + str(r["transition_pairs"]) + "`"
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
    print("row_count", len(rows))
    print("source_exact_count", result["source_exact_count"])
    print("extended_exact_count", result["extended_exact_count"])
    print("endpoint_source_exact_count", result["endpoint_source_exact_count"])
    print("endpoint_extended_exact_count", result["endpoint_extended_exact_count"])


if __name__ == "__main__":
    main()
