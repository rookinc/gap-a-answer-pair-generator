#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_019 = ROOT / "artifacts/json/dodecahedral_register_incidence_test_019.v1.json"

OUT_JSON = ROOT / "artifacts/json/sharedB_motion_component_structure_020.v1.json"
OUT_NOTE = ROOT / "notes/sharedB_motion_component_structure_020.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

SHARED_ROLE_ORDER = ["XY", "IW", "ZT"]
COLUMN_ROLE_ORDER = ["XY", "ZT", "IW"]


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


def weak_components(nodes, directed_edges):
    und = {n: set() for n in nodes}
    for u, v, _row in directed_edges:
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


def component_edges(comp_nodes, directed_edges):
    s = set(comp_nodes)
    return [(u, v, r) for u, v, r in directed_edges if u in s and v in s]


def cycle_check(edges):
    # Enumerate all simple directed 3-cycles in C-transition space.
    # This avoids the greedy "used edge" bug that can miss a second cycle
    # when two cycles share a column anchor.
    out = []
    seen = set()

    for e1 in edges:
        for e2 in edges:
            if e2 is e1:
                continue
            for e3 in edges:
                if e3 is e1 or e3 is e2:
                    continue

                c10 = int(e1[2]["from_C"])
                c11 = int(e1[2]["to_C"])
                c20 = int(e2[2]["from_C"])
                c21 = int(e2[2]["to_C"])
                c30 = int(e3[2]["from_C"])
                c31 = int(e3[2]["to_C"])

                if not (c11 == c20 and c21 == c30 and c31 == c10):
                    continue

                key_edges = tuple(sorted(id(e) for e in (e1, e2, e3)))
                if key_edges in seen:
                    continue
                seen.add(key_edges)

                cyc = [e1, e2, e3]
                out.append({
                    "length": 3,
                    "roles_in_c_order": [x[2]["edge_role"] for x in cyc],
                    "c_transitions": [[int(x[2]["from_C"]), int(x[2]["to_C"])] for x in cyc],
                    "column_edges_in_c_order": [[pstr(x[0]), pstr(x[1])] for x in cyc],
                    "roles_match_XY_IW_ZT_order": [x[2]["edge_role"] for x in cyc] == SHARED_ROLE_ORDER,
                })

    out.sort(key=lambda c: (c["c_transitions"], c["column_edges_in_c_order"]))
    return out


def find_branch_nodes(edges):
    indeg = Counter()
    outdeg = Counter()
    for u, v, _r in edges:
        outdeg[u] += 1
        indeg[v] += 1
    nodes = sorted(set([x for e in edges for x in e[:2]]), key=pstr)
    return [
        {
            "node": pstr(n),
            "in_degree": indeg[n],
            "out_degree": outdeg[n],
            "branch_like": indeg[n] > 1 or outdeg[n] > 1,
        }
        for n in nodes
        if indeg[n] > 1 or outdeg[n] > 1
    ]


def main():
    overlay = load_json(IN_G60_OVERLAY)
    prior = load_json(IN_019) if IN_019.exists() else {}

    shared_rows = []
    for r in overlay.get("edge_records", []):
        if r.get("label") != "shared_B":
            continue
        rr = dict(r)
        rr["role_pair"] = ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))
        rr["from_col_pair"] = col_pair(r.get("from_columns"))
        rr["to_col_pair"] = col_pair(r.get("to_columns"))
        shared_rows.append(rr)

    directed_edges = [(r["from_col_pair"], r["to_col_pair"], r) for r in shared_rows]
    nodes = sorted(set([x for e in directed_edges for x in e[:2]]), key=pstr)
    comps = weak_components(nodes, directed_edges)

    component_rows = []
    all_cycles = []

    for i, comp in enumerate(comps):
        edges = component_edges(comp, directed_edges)
        cycles = cycle_check(edges)
        all_cycles.extend(cycles)

        roles = [e[2]["edge_role"] for e in edges]
        transitions = [[int(e[2]["from_C"]), int(e[2]["to_C"])] for e in edges]
        c_nodes = sorted(set(x for t in transitions for x in t))

        branch_nodes = find_branch_nodes(edges)

        component_rows.append({
            "component_index": i,
            "node_count": len(comp),
            "edge_count": len(edges),
            "nodes": [pstr(x) for x in comp],
            "role_counts": dict(sorted(Counter(roles).items())),
            "roles_in_column_edge_order": roles,
            "transitions": transitions,
            "c_nodes": c_nodes,
            "cycle_count": len(cycles),
            "cycles": cycles,
            "branch_nodes": branch_nodes,
            "has_branch_node": len(branch_nodes) > 0,
            "is_simple_3_cycle": len(comp) == 3 and len(edges) == 3 and len(cycles) == 1 and cycles[0]["length"] == 3,
            "is_bouquet_two_3_cycles": len(comp) == 5 and len(edges) == 6 and len(cycles) == 2,
            "edge_rows": [
                {
                    "edge_role": e[2]["edge_role"],
                    "role_pair": e[2]["role_pair"],
                    "transition": [int(e[2]["from_C"]), int(e[2]["to_C"])],
                    "from_columns": pstr(e[0]),
                    "to_columns": pstr(e[1]),
                    "from_ABC": [e[2]["from_A"], e[2]["from_B"], e[2]["from_C"]],
                    "to_ABC": [e[2]["to_A"], e[2]["to_B"], e[2]["to_C"]],
                }
                for e in edges
            ],
        })

    component_size_counts = Counter(str(r["node_count"]) for r in component_rows)
    edge_size_counts = Counter(str(r["edge_count"]) for r in component_rows)

    simple_3_cycle_count = sum(1 for r in component_rows if r["is_simple_3_cycle"])
    bouquet_count = sum(1 for r in component_rows if r["is_bouquet_two_3_cycles"])

    all_c_cycles_are_XY_IW_ZT = all(c["roles_match_XY_IW_ZT_order"] for c in all_cycles) if all_cycles else False

    role_to_components = defaultdict(set)
    cnode_to_components = defaultdict(set)
    for r in component_rows:
        for role in r["role_counts"]:
            role_to_components[role].add(r["component_index"])
        for c in r["c_nodes"]:
            cnode_to_components[c].add(r["component_index"])

    result = {
        "status": "sharedB_motion_component_structure_recorded",
        "audit_id": "020",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_019": str(IN_019),
        "shared_row_count": len(shared_rows),
        "node_count": len(nodes),
        "component_count": len(component_rows),
        "component_size_counts": dict(sorted(component_size_counts.items())),
        "component_edge_size_counts": dict(sorted(edge_size_counts.items())),
        "simple_3_cycle_count": simple_3_cycle_count,
        "bouquet_two_3_cycles_count": bouquet_count,
        "c_cycle_count": len(all_cycles),
        "all_c_cycles_are_XY_IW_ZT": all_c_cycles_are_XY_IW_ZT,
        "role_to_component_indices": {k: sorted(v) for k, v in sorted(role_to_components.items())},
        "cnode_to_component_indices": {str(k): sorted(v) for k, v in sorted(cnode_to_components.items())},
        "components": component_rows,
        "prior_019_shadow_verdict": prior.get("shadow_test", {}).get("verdict"),
        "interpretation": (
            "This audit decomposes the shared_B column-motion graph from audit 019. The motion "
            "splits into two simple 3-cycles and one 5-node bouquet made from two 3-cycles sharing "
            "a column anchor. In C-transition order, each detected 3-cycle follows the role order "
            "XY -> IW -> ZT. This suggests the shared_B residual is not arbitrary column motion: it "
            "is organized by a small cycle grammar over reverse-partner anchors."
        ),
        "boundary": (
            "This is a structure audit over already selected shared_B motion. It does not derive the "
            "motion from a full dodecahedral register or close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Shared_B motion component structure 020")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- shared_row_count: `" + str(result["shared_row_count"]) + "`")
    lines.append("- node_count: `" + str(result["node_count"]) + "`")
    lines.append("- component_count: `" + str(result["component_count"]) + "`")
    lines.append("- component_size_counts: `" + str(result["component_size_counts"]) + "`")
    lines.append("- component_edge_size_counts: `" + str(result["component_edge_size_counts"]) + "`")
    lines.append("- simple_3_cycle_count: `" + str(simple_3_cycle_count) + "`")
    lines.append("- bouquet_two_3_cycles_count: `" + str(bouquet_count) + "`")
    lines.append("- c_cycle_count: `" + str(len(all_cycles)) + "`")
    lines.append("- all_c_cycles_are_XY_IW_ZT: `" + str(all_c_cycles_are_XY_IW_ZT) + "`")
    lines.append("")
    lines.append("## Components")
    lines.append("")
    for r in component_rows:
        lines.append("- component `" + str(r["component_index"]) + "`")
        lines.append("  - node_count: `" + str(r["node_count"]) + "`")
        lines.append("  - edge_count: `" + str(r["edge_count"]) + "`")
        lines.append("  - nodes: `" + str(r["nodes"]) + "`")
        lines.append("  - role_counts: `" + str(r["role_counts"]) + "`")
        lines.append("  - c_nodes: `" + str(r["c_nodes"]) + "`")
        lines.append("  - is_simple_3_cycle: `" + str(r["is_simple_3_cycle"]) + "`")
        lines.append("  - is_bouquet_two_3_cycles: `" + str(r["is_bouquet_two_3_cycles"]) + "`")
        lines.append("  - branch_nodes: `" + str(r["branch_nodes"]) + "`")
        for e in r["edge_rows"]:
            lines.append(
                "  - role=`" + str(e["edge_role"])
                + "`, transition=`" + str(tuple(e["transition"]))
                + "`, columns=`" + e["from_columns"] + " -> " + e["to_columns"] + "`"
            )
        if r["cycles"]:
            lines.append("  - C-cycles:")
            for cyc in r["cycles"]:
                lines.append(
                    "    - length=`" + str(cyc["length"])
                    + "`, roles=`" + str(cyc["roles_in_c_order"])
                    + "`, transitions=`" + str(cyc["c_transitions"])
                    + "`, XY_IW_ZT=`" + str(cyc["roles_match_XY_IW_ZT_order"]) + "`"
                )
    lines.append("")
    lines.append("## Role and C-node coverage")
    lines.append("")
    lines.append("- role_to_component_indices: `" + str(result["role_to_component_indices"]) + "`")
    lines.append("- cnode_to_component_indices: `" + str(result["cnode_to_component_indices"]) + "`")
    lines.append("")
    lines.append("## Interpretation")
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
    print("shared_row_count", result["shared_row_count"])
    print("component_count", result["component_count"])
    print("component_size_counts", result["component_size_counts"])
    print("simple_3_cycle_count", simple_3_cycle_count)
    print("bouquet_two_3_cycles_count", bouquet_count)
    print("c_cycle_count", len(all_cycles))
    print("all_c_cycles_are_XY_IW_ZT", all_c_cycles_are_XY_IW_ZT)


if __name__ == "__main__":
    main()
