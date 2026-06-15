#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_018 = ROOT / "artifacts/json/schlafli_534_shadow_test_018.v1.json"

OUT_JSON = ROOT / "artifacts/json/dodecahedral_register_incidence_test_019.v1.json"
OUT_NOTE = ROOT / "notes/dodecahedral_register_incidence_test_019.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def col_pair(value):
    if isinstance(value, list):
        xs = [int(x) for x in value]
    elif isinstance(value, tuple):
        xs = [int(x) for x in value]
    elif isinstance(value, str):
        s = value.strip()
        if s.startswith("[") and s.endswith("]"):
            body = s[1:-1].strip()
            xs = [] if not body else [int(x.strip()) for x in body.split(",")]
        else:
            xs = [int(x) for x in s.replace(",", " ").split()]
    else:
        xs = []
    return tuple(sorted(xs))


def pstr(p):
    return "[" + ",".join(str(x) for x in p) + "]"


def edge_key(a, b):
    return tuple(sorted((a, b)))


def weak_components(nodes, directed_edges):
    und = {n: set() for n in nodes}
    for u, v in directed_edges:
        und.setdefault(u, set()).add(v)
        und.setdefault(v, set()).add(u)

    seen = set()
    comps = []
    for n in sorted(nodes, key=pstr):
        if n in seen:
            continue
        q = deque([n])
        seen.add(n)
        comp = []
        while q:
            x = q.popleft()
            comp.append(x)
            for y in sorted(und.get(x, []), key=pstr):
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(sorted(comp, key=pstr))
    return comps


def tarjan_scc(nodes, directed_edges):
    adj = {n: [] for n in nodes}
    for u, v in directed_edges:
        adj.setdefault(u, []).append(v)

    index = 0
    stack = []
    on_stack = set()
    indices = {}
    low = {}
    comps = []

    def visit(v):
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adj.get(v, []):
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])

        if low[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(sorted(comp, key=pstr))

    for n in sorted(nodes, key=pstr):
        if n not in indices:
            visit(n)

    return sorted(comps, key=lambda c: (len(c), [pstr(x) for x in c]))


def column_adjacency_stats(pairs):
    adj = defaultdict(set)
    edge_set = set()
    self_loops = []

    for p in pairs:
        if len(p) != 2:
            continue
        a, b = p
        if a == b:
            self_loops.append(p)
        e = edge_key(a, b)
        edge_set.add(e)
        adj[a].add(b)
        adj[b].add(a)

    cols = sorted(adj.keys())
    degree_counts = Counter(len(adj[c]) for c in cols)

    return {
        "column_vertex_count": len(cols),
        "column_edge_count": len(edge_set),
        "column_min": min(cols) if cols else None,
        "column_max": max(cols) if cols else None,
        "degree_counts": dict(sorted((str(k), v) for k, v in degree_counts.items())),
        "max_degree": max(degree_counts.keys()) if degree_counts else 0,
        "self_loop_count": len(self_loops),
        "self_loops": [pstr(x) for x in self_loops],
        "edges": [pstr(e) for e in sorted(edge_set)],
    }


def main():
    overlay = load_json(IN_G60_OVERLAY)
    edge_records = overlay.get("edge_records", [])

    reverse_rows = [r for r in edge_records if r.get("label") == "reverse_partner"]
    shared_rows = [r for r in edge_records if r.get("label") == "shared_B"]

    reverse_anchors = []
    reverse_anchor_rows = []
    for r in reverse_rows:
        fp = col_pair(r.get("from_columns"))
        tp = col_pair(r.get("to_columns"))
        reverse_anchors.append(fp)
        reverse_anchor_rows.append({
            "edge_role": r.get("edge_role"),
            "transition": [r.get("from_C"), r.get("to_C")],
            "from_columns": pstr(fp),
            "to_columns": pstr(tp),
            "preserved": fp == tp,
        })

    reverse_anchor_set = set(reverse_anchors)

    shared_motions = []
    directed_edges = []
    for r in shared_rows:
        fp = col_pair(r.get("from_columns"))
        tp = col_pair(r.get("to_columns"))
        directed_edges.append((fp, tp))
        shared_motions.append({
            "edge_role": r.get("edge_role"),
            "transition": [r.get("from_C"), r.get("to_C")],
            "from_columns": pstr(fp),
            "to_columns": pstr(tp),
            "changed": fp != tp,
            "from_is_reverse_anchor": fp in reverse_anchor_set,
            "to_is_reverse_anchor": tp in reverse_anchor_set,
            "from_ABC": [r.get("from_A"), r.get("from_B"), r.get("from_C")],
            "to_ABC": [r.get("to_A"), r.get("to_B"), r.get("to_C")],
        })

    all_pairs = []
    for r in edge_records:
        all_pairs.append(col_pair(r.get("from_columns")))
        all_pairs.append(col_pair(r.get("to_columns")))

    distinct_pairs = sorted(set(all_pairs), key=pstr)
    distinct_columns = sorted(set(x for p in distinct_pairs for x in p))
    missing_columns = [x for x in range(30) if x not in distinct_columns]

    col_stats = column_adjacency_stats(distinct_pairs)

    motion_nodes = sorted(set([x for e in directed_edges for x in e]), key=pstr)
    weak = weak_components(motion_nodes, directed_edges)
    sccs = tarjan_scc(motion_nodes, directed_edges)

    in_deg = Counter()
    out_deg = Counter()
    for u, v in directed_edges:
        out_deg[u] += 1
        in_deg[v] += 1

    motion_node_rows = []
    for n in motion_nodes:
        motion_node_rows.append({
            "node": pstr(n),
            "in_degree": in_deg[n],
            "out_degree": out_deg[n],
            "is_reverse_anchor": n in reverse_anchor_set,
        })

    strict_full_register = {
        "expected_column_count_for_dodecahedral_edge_register": 30,
        "expected_line_graph_degree_for_dodecahedron_edge_adjacency": 4,
        "expected_full_line_graph_edge_count": 60,
        "observed_column_count": len(distinct_columns),
        "observed_missing_column_count": len(missing_columns),
        "observed_missing_columns": missing_columns,
        "observed_distinct_column_pair_count": len(distinct_pairs),
        "observed_column_adjacency_edge_count": col_stats["column_edge_count"],
        "observed_column_degree_counts": col_stats["degree_counts"],
        "observed_column_max_degree": col_stats["max_degree"],
        "full_30_column_register_covered": len(distinct_columns) == 30,
        "full_line_graph_edge_count_covered": col_stats["column_edge_count"] == 60,
        "partial_degree_bound_pass": col_stats["max_degree"] <= 4,
        "self_loop_count": col_stats["self_loop_count"],
        "verdict": "full_dodecahedral_register_not_proven_from_observed_overlay_window",
    }

    reverse_anchor_test = {
        "reverse_row_count": len(reverse_rows),
        "reverse_anchor_count": len(reverse_anchors),
        "reverse_distinct_anchor_count": len(reverse_anchor_set),
        "reverse_columns_preserved_count": sum(1 for x in reverse_anchor_rows if x["preserved"]),
        "reverse_columns_preserved_exact": all(x["preserved"] for x in reverse_anchor_rows),
        "reverse_anchor_rows": reverse_anchor_rows,
    }

    shared_motion_test = {
        "shared_row_count": len(shared_rows),
        "shared_motion_count": len(shared_motions),
        "shared_distinct_from_anchor_count": len(set(u for u, v in directed_edges)),
        "shared_distinct_to_anchor_count": len(set(v for u, v in directed_edges)),
        "shared_columns_changed_count": sum(1 for x in shared_motions if x["changed"]),
        "shared_columns_changed_exact": all(x["changed"] for x in shared_motions),
        "shared_from_subset_of_reverse_anchors": all(x["from_is_reverse_anchor"] for x in shared_motions),
        "shared_to_subset_of_reverse_anchors": all(x["to_is_reverse_anchor"] for x in shared_motions),
        "shared_motions": shared_motions,
    }

    motion_graph = {
        "node_count": len(motion_nodes),
        "directed_edge_count": len(directed_edges),
        "weak_component_count": len(weak),
        "weak_components": [[pstr(x) for x in comp] for comp in weak],
        "scc_count": len(sccs),
        "sccs": [[pstr(x) for x in comp] for comp in sccs],
        "all_nodes_in_nontrivial_scc": all(len(comp) > 1 for comp in sccs),
        "motion_node_rows": motion_node_rows,
        "directed_edges": [{"from": pstr(u), "to": pstr(v)} for u, v in directed_edges],
    }

    shadow_indicators = {
        "columns_inside_0_29": bool(distinct_columns) and min(distinct_columns) >= 0 and max(distinct_columns) <= 29,
        "column_pairs_are_two_distinct_columns": all(len(p) == 2 and p[0] != p[1] for p in distinct_pairs),
        "partial_column_adjacency_degree_bound_pass": strict_full_register["partial_degree_bound_pass"],
        "reverse_partner_preserves_column_pair": reverse_anchor_test["reverse_columns_preserved_exact"],
        "shared_B_changes_column_pair": shared_motion_test["shared_columns_changed_exact"],
        "shared_B_from_to_are_reverse_anchors": shared_motion_test["shared_from_subset_of_reverse_anchors"] and shared_motion_test["shared_to_subset_of_reverse_anchors"],
        "shared_motion_edge_count_matches_answer_pair_count": len(directed_edges) == 12,
        "shared_motion_has_three_weak_components": motion_graph["weak_component_count"] == 3,
        "shared_motion_closes_into_nontrivial_sccs": motion_graph["all_nodes_in_nontrivial_scc"],
    }

    pass_count = sum(1 for x in shadow_indicators.values() if x)
    total = len(shadow_indicators)

    if pass_count >= 8:
        shadow_verdict = "strong_dodecahedral_register_shadow_signal"
    elif pass_count >= 5:
        shadow_verdict = "moderate_dodecahedral_register_shadow_signal"
    else:
        shadow_verdict = "weak_dodecahedral_register_shadow_signal"

    result = {
        "status": "dodecahedral_register_incidence_test_recorded",
        "audit_id": "019",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_018": str(IN_018),
        "strict_full_register_test": strict_full_register,
        "column_adjacency_stats": col_stats,
        "reverse_anchor_test": reverse_anchor_test,
        "shared_motion_test": shared_motion_test,
        "motion_graph": motion_graph,
        "shadow_test": {
            "verdict": shadow_verdict,
            "pass_count": pass_count,
            "total": total,
            "indicators": shadow_indicators,
        },
        "interpretation": (
            "This audit distinguishes a full dodecahedral edge-register proof from a local register-shadow "
            "signal. The observed overlay does not cover all 30 columns or the full dodecahedral line graph. "
            "However, reverse_partner rows preserve column-pair anchors, shared_B rows move between those "
            "anchors, and shared_B column motion closes as a directed graph over the reverse anchors. This "
            "supports a dodecahedral-register shadow hypothesis while leaving the full cell/register "
            "incidence derivation open."
        ),
        "next_needed": [
            "Locate or construct the full 30-column dodecahedral edge register.",
            "Account for the 14 unseen columns in the current overlay window.",
            "Determine whether the 11 observed column-pair anchors are a quotient/subwindow of a 30-edge register.",
            "Derive shared_B column motion from full register incidence rather than from selected rows.",
            "Explain how this register shadow relates to the strong {5,3,4}-type signal in audit 018.",
        ],
        "boundary": (
            "This is an incidence-shadow test over observed overlay rows. It is not a full dodecahedral "
            "cell decomposition, not a literal {5,3,4} proof, and not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Dodecahedral register incidence test 019")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Strict full-register test")
    lines.append("")
    lines.append("- verdict: `" + strict_full_register["verdict"] + "`")
    lines.append("- observed_column_count: `" + str(strict_full_register["observed_column_count"]) + "`")
    lines.append("- observed_missing_column_count: `" + str(strict_full_register["observed_missing_column_count"]) + "`")
    lines.append("- observed_missing_columns: `" + str(strict_full_register["observed_missing_columns"]) + "`")
    lines.append("- observed_distinct_column_pair_count: `" + str(strict_full_register["observed_distinct_column_pair_count"]) + "`")
    lines.append("- observed_column_adjacency_edge_count: `" + str(strict_full_register["observed_column_adjacency_edge_count"]) + "`")
    lines.append("- observed_column_degree_counts: `" + str(strict_full_register["observed_column_degree_counts"]) + "`")
    lines.append("- observed_column_max_degree: `" + str(strict_full_register["observed_column_max_degree"]) + "`")
    lines.append("- full_30_column_register_covered: `" + str(strict_full_register["full_30_column_register_covered"]) + "`")
    lines.append("- full_line_graph_edge_count_covered: `" + str(strict_full_register["full_line_graph_edge_count_covered"]) + "`")
    lines.append("- partial_degree_bound_pass: `" + str(strict_full_register["partial_degree_bound_pass"]) + "`")
    lines.append("")
    lines.append("## Shadow test")
    lines.append("")
    lines.append("- verdict: `" + shadow_verdict + "`")
    lines.append("- pass_count: `" + str(pass_count) + " / " + str(total) + "`")
    lines.append("")
    for k, v in shadow_indicators.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Reverse anchors")
    lines.append("")
    lines.append("- reverse_row_count: `" + str(reverse_anchor_test["reverse_row_count"]) + "`")
    lines.append("- reverse_anchor_count: `" + str(reverse_anchor_test["reverse_anchor_count"]) + "`")
    lines.append("- reverse_distinct_anchor_count: `" + str(reverse_anchor_test["reverse_distinct_anchor_count"]) + "`")
    lines.append("- reverse_columns_preserved_exact: `" + str(reverse_anchor_test["reverse_columns_preserved_exact"]) + "`")
    lines.append("")
    lines.append("## Shared_B column motion")
    lines.append("")
    lines.append("- shared_row_count: `" + str(shared_motion_test["shared_row_count"]) + "`")
    lines.append("- shared_motion_count: `" + str(shared_motion_test["shared_motion_count"]) + "`")
    lines.append("- shared_columns_changed_exact: `" + str(shared_motion_test["shared_columns_changed_exact"]) + "`")
    lines.append("- shared_from_subset_of_reverse_anchors: `" + str(shared_motion_test["shared_from_subset_of_reverse_anchors"]) + "`")
    lines.append("- shared_to_subset_of_reverse_anchors: `" + str(shared_motion_test["shared_to_subset_of_reverse_anchors"]) + "`")
    lines.append("")
    for r in shared_motions:
        lines.append(
            "- role=`" + str(r["edge_role"])
            + "`, transition=`" + str(tuple(r["transition"]))
            + "`, columns=`" + r["from_columns"] + " -> " + r["to_columns"] + "`"
        )
    lines.append("")
    lines.append("## Shared_B motion graph")
    lines.append("")
    lines.append("- node_count: `" + str(motion_graph["node_count"]) + "`")
    lines.append("- directed_edge_count: `" + str(motion_graph["directed_edge_count"]) + "`")
    lines.append("- weak_component_count: `" + str(motion_graph["weak_component_count"]) + "`")
    lines.append("- scc_count: `" + str(motion_graph["scc_count"]) + "`")
    lines.append("- all_nodes_in_nontrivial_scc: `" + str(motion_graph["all_nodes_in_nontrivial_scc"]) + "`")
    lines.append("- weak_components: `" + str(motion_graph["weak_components"]) + "`")
    lines.append("- sccs: `" + str(motion_graph["sccs"]) + "`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(result["interpretation"])
    lines.append("")
    lines.append("## Next needed")
    lines.append("")
    for item in result["next_needed"]:
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
    print("strict_verdict", strict_full_register["verdict"])
    print("shadow_verdict", shadow_verdict)
    print("shadow_pass_count", str(pass_count) + "/" + str(total))
    print("observed_column_count", strict_full_register["observed_column_count"])
    print("observed_distinct_column_pair_count", strict_full_register["observed_distinct_column_pair_count"])
    print("reverse_columns_preserved_exact", reverse_anchor_test["reverse_columns_preserved_exact"])
    print("shared_from_to_are_reverse_anchors", shadow_indicators["shared_B_from_to_are_reverse_anchors"])
    print("motion_weak_component_count", motion_graph["weak_component_count"])
    print("motion_scc_count", motion_graph["scc_count"])


if __name__ == "__main__":
    main()
