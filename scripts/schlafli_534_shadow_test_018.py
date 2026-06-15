#!/usr/bin/env python3
import csv
import itertools
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_PAIRS = ROOT / "artifacts/csv/native_answer_pairs_013.v1.csv"
P18_G60_CSV = ROOT.parent / "18-g900-kernel-admission/source/kernel_payload/g60_local_edges.csv"

OUT_JSON = ROOT / "artifacts/json/schlafli_534_shadow_test_018.v1.json"
OUT_NOTE = ROOT / "notes/schlafli_534_shadow_test_018.md"

EXPECTED_ROLES = ["IW", "TI", "WX", "XY", "YZ", "ZT"]


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_dicts(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_g60_edges(path):
    if not path.exists():
        return None

    rows = load_csv_dicts(path)
    edges = []
    for r in rows:
        keys = set(r.keys())
        if {"local_u", "local_v"}.issubset(keys):
            u = int(r["local_u"])
            v = int(r["local_v"])
        elif {"u", "v"}.issubset(keys):
            u = int(r["u"])
            v = int(r["v"])
        else:
            continue
        if u != v:
            edges.append(tuple(sorted((u, v))))
    return sorted(set(edges))


def graph_stats(edges):
    if edges is None:
        return {
            "available": False,
            "reason": "g60 edge csv not found or not parsed",
        }

    vertices = sorted(set(x for e in edges for x in e))
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    degs = Counter(len(adj[v]) for v in vertices)

    tri = 0
    for a, b, c in itertools.combinations(vertices, 3):
        if b in adj[a] and c in adj[a] and c in adj[b]:
            tri += 1

    return {
        "available": True,
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "degree_counts": dict(sorted((str(k), v) for k, v in degs.items())),
        "degree_set": sorted(degs.keys()),
        "triangle_count": tri,
        "literal_534_one_skeleton_degree6_expected": True,
        "literal_534_one_skeleton_degree_test_pass": sorted(degs.keys()) == [6],
        "literal_534_one_skeleton_supported": sorted(degs.keys()) == [6],
        "strict_reading": (
            "A literal {5,3,4} 1-skeleton has octahedral vertex figure {3,4}, "
            "so the raw graph valence test expects degree 6. A degree-4 G60 carrier "
            "does not pass literal 1-skeleton identity. It may still be a finite "
            "transport register or quotient shadow."
        ),
    }


def parse_columns(v):
    if isinstance(v, list):
        return [int(x) for x in v]
    if isinstance(v, str):
        s = v.strip()
        if s.startswith("[") and s.endswith("]"):
            body = s[1:-1].strip()
            if not body:
                return []
            return [int(x.strip()) for x in body.split(",")]
    return []


def octahedral_scaffold(roles, axes):
    role_set = sorted(set(roles))
    axis_edges = {tuple(sorted(a)) for a in axes}

    disjoint_axis_roles = sorted(x for a in axis_edges for x in a)
    axes_are_disjoint_matching = (
        len(axis_edges) == 3
        and len(disjoint_axis_roles) == 6
        and sorted(disjoint_axis_roles) == role_set
    )

    all_edges = {tuple(sorted(e)) for e in itertools.combinations(role_set, 2)}
    oct_edges = sorted(all_edges - axis_edges)

    deg = Counter()
    for u, v in oct_edges:
        deg[u] += 1
        deg[v] += 1

    tri = 0
    for a, b, c in itertools.combinations(role_set, 3):
        need = {
            tuple(sorted((a, b))),
            tuple(sorted((a, c))),
            tuple(sorted((b, c))),
        }
        if need.issubset(set(oct_edges)):
            tri += 1

    return {
        "role_count": len(role_set),
        "axes": [list(a) for a in sorted(axis_edges)],
        "axes_are_disjoint_matching": axes_are_disjoint_matching,
        "implied_graph_edge_count": len(oct_edges),
        "implied_graph_degree_counts": dict(sorted((str(k), v) for k, v in Counter(deg.values()).items())),
        "implied_graph_degrees_by_role": dict(sorted(deg.items())),
        "implied_triangle_count": tri,
        "octahedral_vertex_figure_pass": (
            len(role_set) == 6
            and axes_are_disjoint_matching
            and len(oct_edges) == 12
            and set(deg.values()) == {4}
            and tri == 8
        ),
    }


def main():
    overlay = load_json(IN_G60_OVERLAY)
    edge_records = overlay.get("edge_records", [])
    pair_rows = load_csv_dicts(IN_PAIRS) if IN_PAIRS.exists() else []

    role_counts = Counter(str(r.get("edge_role")) for r in edge_records)
    label_counts = Counter(str(r.get("label")) for r in edge_records)
    form_counts = Counter(str(r.get("form_index")) for r in edge_records)

    form_role_matrix = {}
    for r in edge_records:
        f = str(r.get("form_index"))
        role = str(r.get("edge_role"))
        form_role_matrix.setdefault(f, Counter())
        form_role_matrix[f][role] += 1

    form_role_matrix_dict = {
        f: dict(sorted(c.items()))
        for f, c in sorted(form_role_matrix.items())
    }

    forms_have_all_six_roles_once = all(
        sorted(c.keys()) == sorted(EXPECTED_ROLES)
        and all(v == 1 for v in c.values())
        for c in form_role_matrix.values()
    )

    role_has_four_incidents = (
        sorted(role_counts.keys()) == sorted(EXPECTED_ROLES)
        and all(role_counts[r] == 4 for r in EXPECTED_ROLES)
    )

    unique_axes = sorted(set(
        tuple(sorted((r.get("shared_role"), r.get("reverse_role"))))
        for r in pair_rows
    ))
    axis_counts = Counter(
        str(tuple(sorted((r.get("shared_role"), r.get("reverse_role")))))
        for r in pair_rows
    )

    scaffold = octahedral_scaffold(EXPECTED_ROLES, unique_axes)

    all_cols = []
    column_pairs = []
    for r in edge_records:
        for k in ["from_columns", "to_columns"]:
            cols = parse_columns(r.get(k))
            all_cols.extend(cols)
            if len(cols) == 2:
                column_pairs.append(tuple(cols))

    col_set = sorted(set(all_cols))
    column_stats = {
        "distinct_column_count_seen": len(col_set),
        "column_min": min(col_set) if col_set else None,
        "column_max": max(col_set) if col_set else None,
        "columns_within_0_29_register": bool(col_set) and min(col_set) >= 0 and max(col_set) <= 29,
        "distinct_column_pairs_seen": len(set(column_pairs)),
        "column_pair_rows_seen": len(column_pairs),
        "reading": (
            "Columns sit inside a 0..29 register in the observed overlay rows. "
            "That is compatible with a 30-column dodecahedral edge register, but "
            "it is not by itself a proof of dodecahedral cell decomposition."
        ),
    }

    g60_stats = graph_stats(load_g60_edges(P18_G60_CSV))

    shadow_indicators = {
        "four_forms": len(form_counts) == 4 and all(v == 6 for v in form_counts.values()),
        "six_roles": sorted(role_counts.keys()) == sorted(EXPECTED_ROLES),
        "twenty_four_role_incidents": len(edge_records) == 24,
        "role_incidence_four_each": role_has_four_incidents,
        "form_role_grid_4_by_6": forms_have_all_six_roles_once,
        "three_reciprocal_axes": len(unique_axes) == 3,
        "axes_imply_octahedral_vertex_figure": scaffold["octahedral_vertex_figure_pass"],
        "twelve_answer_pairs": len(pair_rows) == 12,
        "answer_pair_count_matches_octahedron_edge_count": len(pair_rows) == scaffold["implied_graph_edge_count"],
        "columns_inside_30_register": column_stats["columns_within_0_29_register"],
    }

    shadow_pass_count = sum(1 for v in shadow_indicators.values() if v)
    shadow_total = len(shadow_indicators)

    if g60_stats.get("available") and not g60_stats.get("literal_534_one_skeleton_supported"):
        literal_verdict = "literal_g60_one_skeleton_identity_not_supported"
    elif g60_stats.get("literal_534_one_skeleton_supported"):
        literal_verdict = "literal_degree_test_passed_but_cell_incidence_still_required"
    else:
        literal_verdict = "literal_test_incomplete_g60_edges_not_available"

    if shadow_pass_count >= 8:
        shadow_verdict = "strong_534_type_shadow_signal"
    elif shadow_pass_count >= 5:
        shadow_verdict = "moderate_534_type_shadow_signal"
    else:
        shadow_verdict = "weak_534_type_shadow_signal"

    result = {
        "status": "schlafli_534_shadow_test_recorded",
        "audit_id": "018",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_pairs": str(IN_PAIRS),
        "input_g60_graph_csv": str(P18_G60_CSV),
        "strict_literal_test": {
            "verdict": literal_verdict,
            "g60_graph_stats": g60_stats,
            "boundary": (
                "This tests literal 1-skeleton identity only. Failing this test does not refute "
                "a quotient, register, or transport-shadow relationship to {5,3,4}."
            ),
        },
        "shadow_test": {
            "verdict": shadow_verdict,
            "pass_count": shadow_pass_count,
            "total": shadow_total,
            "indicators": shadow_indicators,
            "role_counts": dict(sorted(role_counts.items())),
            "label_counts": dict(sorted(label_counts.items())),
            "form_counts": dict(sorted(form_counts.items())),
            "form_role_matrix": form_role_matrix_dict,
            "unique_reciprocal_axes": [list(a) for a in unique_axes],
            "axis_counts": dict(sorted(axis_counts.items())),
            "octahedral_scaffold": scaffold,
            "column_stats": column_stats,
        },
        "interpretation": (
            "The strict literal test asks whether G60 is the raw 1-skeleton of a {5,3,4} "
            "honeycomb quotient. The shadow test asks whether the native overlay has a "
            "{5,3,4}-type finite signature: four forms, six roles, 24 role incidences, "
            "three reciprocal axes, an implied octahedral vertex-figure scaffold, and "
            "12 answer-pairs. Passing the shadow test supports a finite transport-shadow "
            "hypothesis, not literal tessellation identity."
        ),
        "next_needed_for_stronger_claim": [
            "Construct an explicit dodecahedral cell decomposition or cell-shadow.",
            "Show a 30-edge dodecahedral register with accountable incidence.",
            "Show fourfold around-edge incidence or its finite quotient replacement.",
            "Explain why the observed carrier is tetravalent while the literal {5,3,4} 1-skeleton has degree 6.",
            "Derive shared_B column motion from the candidate cell/register incidence.",
        ],
        "boundary": (
            "This does not prove that the Thalean carrier is {5,3,4}. It distinguishes "
            "literal identity from finite shadow evidence and records what remains to prove."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Schlafli 534 shadow test 018")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Strict literal test")
    lines.append("")
    lines.append("- verdict: `" + literal_verdict + "`")
    if g60_stats.get("available"):
        lines.append("- G60 vertex_count: `" + str(g60_stats["vertex_count"]) + "`")
        lines.append("- G60 edge_count: `" + str(g60_stats["edge_count"]) + "`")
        lines.append("- G60 degree_set: `" + str(g60_stats["degree_set"]) + "`")
        lines.append("- G60 triangle_count: `" + str(g60_stats["triangle_count"]) + "`")
        lines.append("- literal degree-6 test pass: `" + str(g60_stats["literal_534_one_skeleton_degree_test_pass"]) + "`")
    else:
        lines.append("- G60 graph stats: `" + str(g60_stats) + "`")
    lines.append("")
    lines.append("## Shadow test")
    lines.append("")
    lines.append("- verdict: `" + shadow_verdict + "`")
    lines.append("- pass_count: `" + str(shadow_pass_count) + " / " + str(shadow_total) + "`")
    lines.append("")
    lines.append("## Indicators")
    lines.append("")
    for k, v in shadow_indicators.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Role/form counts")
    lines.append("")
    lines.append("- role_counts: `" + str(dict(sorted(role_counts.items()))) + "`")
    lines.append("- label_counts: `" + str(dict(sorted(label_counts.items()))) + "`")
    lines.append("- form_counts: `" + str(dict(sorted(form_counts.items()))) + "`")
    lines.append("- forms_have_all_six_roles_once: `" + str(forms_have_all_six_roles_once) + "`")
    lines.append("- form_role_matrix: `" + str(form_role_matrix_dict) + "`")
    lines.append("")
    lines.append("## Reciprocal axes and octahedral scaffold")
    lines.append("")
    lines.append("- unique_reciprocal_axes: `" + str([list(a) for a in unique_axes]) + "`")
    lines.append("- axis_counts: `" + str(dict(sorted(axis_counts.items()))) + "`")
    lines.append("- octahedral_vertex_figure_pass: `" + str(scaffold["octahedral_vertex_figure_pass"]) + "`")
    lines.append("- implied_graph_edge_count: `" + str(scaffold["implied_graph_edge_count"]) + "`")
    lines.append("- implied_graph_degrees_by_role: `" + str(scaffold["implied_graph_degrees_by_role"]) + "`")
    lines.append("- implied_triangle_count: `" + str(scaffold["implied_triangle_count"]) + "`")
    lines.append("")
    lines.append("## Column register")
    lines.append("")
    for k, v in column_stats.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(result["interpretation"])
    lines.append("")
    lines.append("## Next needed for stronger claim")
    lines.append("")
    for item in result["next_needed_for_stronger_claim"]:
        lines.append("- " + item)
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(result["boundary"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("literal_verdict", literal_verdict)
    print("shadow_verdict", shadow_verdict)
    print("shadow_pass_count", str(shadow_pass_count) + "/" + str(shadow_total))
    if g60_stats.get("available"):
        print("g60_degree_set", g60_stats["degree_set"])
        print("g60_triangle_count", g60_stats["triangle_count"])
    print("form_counts", dict(sorted(form_counts.items())))
    print("role_counts", dict(sorted(role_counts.items())))
    print("octahedral_vertex_figure_pass", scaffold["octahedral_vertex_figure_pass"])


if __name__ == "__main__":
    main()
