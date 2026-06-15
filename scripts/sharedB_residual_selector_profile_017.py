#!/usr/bin/env python3
import itertools
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60 = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"

OUT_JSON = ROOT / "artifacts/json/sharedB_residual_selector_profile_017.v1.json"
OUT_NOTE = ROOT / "notes/sharedB_residual_selector_profile_017.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

SOURCE_FEATURES = [
    "edge_role",
    "role_pair",
    "from_A",
    "from_B",
    "from_C",
    "from_slot",
    "from_fiber",
    "from_columns",
]

EXTENDED_FEATURES = SOURCE_FEATURES + [
    "fiber_delta_mod60",
    "slot_delta_mod15",
]

TARGETS = [
    "to_A",
    "to_C",
    "to_columns",
    "to_fiber",
    "to_A_to_C",
    "to_endpoint_reduced",
    "A_delta_mod15",
    "C_delta_mod15",
    "columns_change",
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


def value(row, key):
    if key == "role_pair":
        return ROLE_PAIR_BY_EDGE_ROLE.get(str(row.get("edge_role")))
    if key == "from_columns":
        return norm(row.get("from_columns"))
    if key == "to_columns":
        return norm(row.get("to_columns"))
    if key == "to_A_to_C":
        return (row.get("to_A"), row.get("to_C"))
    if key == "to_endpoint_reduced":
        return (
            row.get("to_A"),
            row.get("to_B"),
            row.get("to_C"),
            row.get("to_slot"),
            row.get("to_fiber"),
            norm(row.get("to_columns")),
        )
    if key == "A_delta_mod15":
        return (row.get("to_A") - row.get("from_A")) % 15
    if key == "C_delta_mod15":
        return (row.get("to_C") - row.get("from_C")) % 15
    if key == "columns_change":
        return (norm(row.get("from_columns")), norm(row.get("to_columns")))
    return row.get(key)


def feature_tuple(row, features):
    return tuple((f, value(row, f)) for f in features)


def deterministic_test(rows, features, target):
    groups = defaultdict(set)
    sizes = Counter()
    for r in rows:
        k = feature_tuple(r, features)
        groups[k].add(norm(value(r, target)))
        sizes[k] += 1

    ambiguous = []
    for k, vals in groups.items():
        if len(vals) > 1:
            ambiguous.append({
                "feature_value": str(k),
                "target_values": [str(v) for v in sorted(vals, key=str)],
            })

    group_count = len(groups)
    exact = len(ambiguous) == 0

    if not exact:
        strength = "not_exact"
    elif group_count <= 4:
        strength = "strong"
    elif group_count <= 8:
        strength = "medium"
    elif group_count <= 10:
        strength = "weak"
    else:
        strength = "row_identity_like"

    return {
        "features": list(features),
        "target": target,
        "exact": exact,
        "group_count": group_count,
        "max_group_size": max(sizes.values()) if sizes else 0,
        "strength": strength,
        "ambiguous_group_count": len(ambiguous),
        "ambiguous_groups_first_10": ambiguous[:10],
    }


def all_combos(features, max_size):
    for n in range(1, max_size + 1):
        for combo in itertools.combinations(features, n):
            yield combo


def rank_exact(tests):
    xs = [t for t in tests if t["exact"]]
    xs.sort(key=lambda t: (len(t["features"]), t["group_count"], t["target"], str(t["features"])))
    return xs


def named_tests(rows):
    tests = []

    def add(name, features, target):
        tests.append(dict(name=name, **deterministic_test(rows, features, target)))

    add("edge_role_from_C_to_to_C", ["edge_role", "from_C"], "to_C")
    add("edge_role_from_B_to_to_C", ["edge_role", "from_B"], "to_C")
    add("edge_role_from_C_from_B_to_to_C", ["edge_role", "from_C", "from_B"], "to_C")
    add("role_pair_from_C_from_B_to_to_C", ["role_pair", "from_C", "from_B"], "to_C")

    add("edge_role_from_A_to_to_A", ["edge_role", "from_A"], "to_A")
    add("edge_role_from_B_to_to_A", ["edge_role", "from_B"], "to_A")
    add("edge_role_from_A_from_B_to_to_A", ["edge_role", "from_A", "from_B"], "to_A")
    add("role_pair_from_A_from_B_to_to_A", ["role_pair", "from_A", "from_B"], "to_A")

    add("edge_role_from_columns_to_to_columns", ["edge_role", "from_columns"], "to_columns")
    add("role_pair_from_columns_to_to_columns", ["role_pair", "from_columns"], "to_columns")
    add("edge_role_from_C_from_columns_to_to_columns", ["edge_role", "from_C", "from_columns"], "to_columns")

    add("edge_role_from_C_from_B_to_reduced_endpoint", ["edge_role", "from_C", "from_B"], "to_endpoint_reduced")
    add("edge_role_from_A_from_B_to_reduced_endpoint", ["edge_role", "from_A", "from_B"], "to_endpoint_reduced")
    add("edge_role_from_columns_to_reduced_endpoint", ["edge_role", "from_columns"], "to_endpoint_reduced")

    return tests


def summarize_rows(rows):
    by_role = defaultdict(list)
    for r in rows:
        by_role[str(r.get("edge_role"))].append(r)

    role_rows = []
    for role, rs in sorted(by_role.items()):
        role_rows.append({
            "edge_role": role,
            "role_pair": ROLE_PAIR_BY_EDGE_ROLE.get(role),
            "row_count": len(rs),
            "transitions": sorted((r.get("from_C"), r.get("to_C")) for r in rs),
            "from_A_values": sorted(set(r.get("from_A") for r in rs)),
            "from_B_values": sorted(set(r.get("from_B") for r in rs)),
            "from_C_values": sorted(set(r.get("from_C") for r in rs)),
            "to_A_values": sorted(set(r.get("to_A") for r in rs)),
            "to_C_values": sorted(set(r.get("to_C") for r in rs)),
            "A_delta_counts": dict(sorted(Counter(str((r.get("to_A") - r.get("from_A")) % 15) for r in rs).items())),
            "C_delta_counts": dict(sorted(Counter(str((r.get("to_C") - r.get("from_C")) % 15) for r in rs).items())),
            "from_columns": [r.get("from_columns") for r in rs],
            "to_columns": [r.get("to_columns") for r in rs],
        })

    row_table = []
    for r in sorted(rows, key=lambda x: (str(x.get("edge_role")), x.get("from_C"), x.get("to_C"), x.get("from_A"))):
        row_table.append({
            "edge_role": r.get("edge_role"),
            "role_pair": ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role"))),
            "transition": [r.get("from_C"), r.get("to_C")],
            "from_ABC": [r.get("from_A"), r.get("from_B"), r.get("from_C")],
            "to_ABC": [r.get("to_A"), r.get("to_B"), r.get("to_C")],
            "from_slot": r.get("from_slot"),
            "to_slot": r.get("to_slot"),
            "from_fiber": r.get("from_fiber"),
            "to_fiber": r.get("to_fiber"),
            "from_columns": r.get("from_columns"),
            "to_columns": r.get("to_columns"),
            "A_delta_mod15": (r.get("to_A") - r.get("from_A")) % 15,
            "C_delta_mod15": (r.get("to_C") - r.get("from_C")) % 15,
            "B_preserved": r.get("to_B") == r.get("from_B"),
            "slot_preserved": r.get("to_slot") == r.get("from_slot"),
            "fiber_mod15_tracks_C": (
                r.get("from_fiber") % 15 == r.get("from_C")
                and r.get("to_fiber") % 15 == r.get("to_C")
            ),
        })

    return role_rows, row_table


def main():
    data = load(IN_G60)
    all_rows = data.get("edge_records", [])
    rows = [dict(r, role_pair=ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))) for r in all_rows if r.get("label") == "shared_B"]

    source_tests = []
    extended_tests = []

    for target in TARGETS:
        for combo in all_combos(SOURCE_FEATURES, 3):
            source_tests.append(deterministic_test(rows, combo, target))
        for combo in all_combos(EXTENDED_FEATURES, 3):
            extended_tests.append(deterministic_test(rows, combo, target))

    source_exact = rank_exact(source_tests)
    extended_exact = rank_exact(extended_tests)
    named = named_tests(rows)

    strength_counts_source = Counter(t["strength"] for t in source_tests)
    strength_counts_extended = Counter(t["strength"] for t in extended_tests)

    exact_by_target = {}
    for target in TARGETS:
        exact_by_target[target] = {
            "source_first_20": [t for t in source_exact if t["target"] == target][:20],
            "extended_first_20": [t for t in extended_exact if t["target"] == target][:20],
        }

    compact_source = [t for t in source_exact if t["strength"] in ("strong", "medium", "weak")]
    compact_extended = [t for t in extended_exact if t["strength"] in ("strong", "medium", "weak")]

    role_rows, row_table = summarize_rows(rows)

    result = {
        "status": "sharedB_residual_selector_profile_recorded",
        "audit_id": "017",
        "input_g60_overlay": str(IN_G60),
        "row_count": len(rows),
        "source_features": SOURCE_FEATURES,
        "extended_features": EXTENDED_FEATURES,
        "targets": TARGETS,
        "source_test_count": len(source_tests),
        "extended_test_count": len(extended_tests),
        "source_exact_count": len(source_exact),
        "extended_exact_count": len(extended_exact),
        "strength_counts_source": dict(sorted(strength_counts_source.items())),
        "strength_counts_extended": dict(sorted(strength_counts_extended.items())),
        "compact_source_exact_first_80": compact_source[:80],
        "compact_extended_exact_first_80": compact_extended[:80],
        "named_tests": named,
        "exact_by_target": exact_by_target,
        "role_rows": role_rows,
        "sharedB_rows": row_table,
        "global_laws": {
            "B_preserved_count": sum(1 for r in rows if r.get("to_B") == r.get("from_B")),
            "slot_preserved_count": sum(1 for r in rows if r.get("to_slot") == r.get("from_slot")),
            "fiber_mod15_tracks_C_count": sum(
                1 for r in rows
                if r.get("from_fiber") % 15 == r.get("from_C")
                and r.get("to_fiber") % 15 == r.get("to_C")
            ),
            "columns_preserved_count": sum(1 for r in rows if norm(r.get("from_columns")) == norm(r.get("to_columns"))),
        },
        "interpretation": (
            "This audit isolates the shared_B residual after reverse_partner has been treated as solved. "
            "It searches for compact context-dependent selectors for to_A, to_C, to_columns, and the "
            "reduced endpoint, while excluding row-id fields such as edge_index, form_index, and from_key. "
            "Compact exact tests suggest reusable structure; row-identity-like tests suggest the remaining "
            "selector still needs a native candidate universe or additional provenance."
        ),
        "boundary": (
            "This is a residual profile over the 12 already selected shared_B rows. It does not derive "
            "shared_B from a candidate universe and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Shared_B residual selector profile 017")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input")
    lines.append("")
    lines.append("- G60 overlay artifact: `" + str(IN_G60) + "`")
    lines.append("- shared_B row_count: `" + str(len(rows)) + "`")
    lines.append("")
    lines.append("## Search")
    lines.append("")
    lines.append("- source_test_count: `" + str(result["source_test_count"]) + "`")
    lines.append("- extended_test_count: `" + str(result["extended_test_count"]) + "`")
    lines.append("- source_exact_count: `" + str(result["source_exact_count"]) + "`")
    lines.append("- extended_exact_count: `" + str(result["extended_exact_count"]) + "`")
    lines.append("- strength_counts_source: `" + str(result["strength_counts_source"]) + "`")
    lines.append("- strength_counts_extended: `" + str(result["strength_counts_extended"]) + "`")
    lines.append("")
    lines.append("## Global shared_B laws")
    lines.append("")
    for k, v in result["global_laws"].items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Named tests")
    lines.append("")
    for t in named:
        lines.append(
            "- " + t["name"]
            + ": exact=`" + str(t["exact"])
            + "`, strength=`" + str(t["strength"])
            + "`, groups=`" + str(t["group_count"])
            + "`, ambiguous=`" + str(t["ambiguous_group_count"]) + "`"
        )
    lines.append("")
    lines.append("## Compact source exact tests first 40")
    lines.append("")
    if compact_source:
        for t in compact_source[:40]:
            lines.append("- target=`" + t["target"] + "`, features=`" + str(t["features"]) + "`, strength=`" + t["strength"] + "`, groups=`" + str(t["group_count"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Best exact tests by target")
    lines.append("")
    for target in TARGETS:
        lines.append("- target: `" + target + "`")
        tests = exact_by_target[target]["source_first_20"]
        if tests:
            for t in tests[:5]:
                lines.append("  - features=`" + str(t["features"]) + "`, strength=`" + t["strength"] + "`, groups=`" + str(t["group_count"]) + "`")
        else:
            lines.append("  - none")
    lines.append("")
    lines.append("## Role rows")
    lines.append("")
    for r in role_rows:
        lines.append(
            "- role=`" + str(r["edge_role"]) + "`, transitions=`" + str(r["transitions"])
            + "`, A_delta_counts=`" + str(r["A_delta_counts"])
            + "`, C_delta_counts=`" + str(r["C_delta_counts"]) + "`"
        )
    lines.append("")
    lines.append("## Shared_B rows")
    lines.append("")
    for r in row_table:
        lines.append(
            "- role=`" + str(r["edge_role"])
            + "`, transition=`" + str(tuple(r["transition"]))
            + "`, from_ABC=`" + str(tuple(r["from_ABC"]))
            + "`, to_ABC=`" + str(tuple(r["to_ABC"]))
            + "`, columns=`" + str(r["from_columns"]) + " -> " + str(r["to_columns"]) + "`"
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
    print("sharedB_row_count", len(rows))
    print("source_exact_count", result["source_exact_count"])
    print("extended_exact_count", result["extended_exact_count"])
    print("strength_counts_source", result["strength_counts_source"])
    print("strength_counts_extended", result["strength_counts_extended"])


if __name__ == "__main__":
    main()
