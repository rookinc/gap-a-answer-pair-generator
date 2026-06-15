#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_004 = ROOT / "source/project18_native_chain/json/c_transition_role_channel_grammar_audit_004.v1.json"
IN_020 = ROOT / "artifacts/json/sharedB_motion_component_structure_020.v1.json"

OUT_JSON = ROOT / "artifacts/json/c_transition_block_order_derivation_021.v1.json"
OUT_NOTE = ROOT / "notes/c_transition_block_order_derivation_021.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

# Canonical block circulation recorded in the imported 004 native-chain audit:
# WX/ZT sends A -> B, TI/XY sends B -> C, IW/YZ sends C -> A.
CHANNEL_MAP_004 = {
    "WX/ZT": {
        "from_block": "A",
        "to_block": "B",
        "from_values": [0, 2, 10, 14],
        "to_values": [2, 4, 11, 13],
    },
    "TI/XY": {
        "from_block": "B",
        "to_block": "C",
        "from_values": [2, 4, 11, 13],
        "to_values": [1, 2, 5],
    },
    "IW/YZ": {
        "from_block": "C",
        "to_block": "A",
        "from_values": [1, 2, 5],
        "to_values": [0, 2, 10, 14],
    },
}

EXPECTED_CHANNEL_CIRCULATION = ["WX/ZT", "TI/XY", "IW/YZ"]
EXPECTED_SHARED_B_ROLE_ORDER = ["XY", "IW", "ZT"]
EXPECTED_SHARED_B_CHANNEL_ORDER = ["TI/XY", "IW/YZ", "WX/ZT"]
EXPECTED_SHARED_B_BLOCK_ORDER = [["B", "C"], ["C", "A"], ["A", "B"]]


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


def is_cyclic_rotation(xs, base):
    if len(xs) != len(base):
        return False
    doubled = base + base
    for i in range(len(base)):
        if doubled[i:i + len(xs)] == xs:
            return True
    return False


def weak_components(nodes, edges):
    und = {n: set() for n in nodes}
    for u, v, _r in edges:
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


def rotate_to_xy(cyc):
    for i, e in enumerate(cyc):
        if e[2]["edge_role"] == "XY":
            return cyc[i:] + cyc[:i]
    return cyc


def simple_c_cycles(edges):
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

                cyc = rotate_to_xy([e1, e2, e3])
                key = tuple((int(e[2]["from_C"]), int(e[2]["to_C"]), str(e[2]["edge_role"])) for e in cyc)
                if key in seen:
                    continue
                seen.add(key)
                out.append(cyc)

    out.sort(key=lambda cyc: [(int(e[2]["from_C"]), int(e[2]["to_C"]), str(e[2]["edge_role"])) for e in cyc])
    return out


def channel_for_row(r):
    return ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))


def block_edge_for_row(r):
    ch = channel_for_row(r)
    spec = CHANNEL_MAP_004[ch]
    return [spec["from_block"], spec["to_block"]]


def row_matches_channel_map(r):
    ch = channel_for_row(r)
    spec = CHANNEL_MAP_004[ch]
    return int(r["from_C"]) in spec["from_values"] and int(r["to_C"]) in spec["to_values"]


def main():
    overlay = load_json(IN_G60_OVERLAY)
    prior_020 = load_json(IN_020) if IN_020.exists() else {}
    prior_004 = load_json(IN_004) if IN_004.exists() else {}

    shared_rows = []
    for r in overlay.get("edge_records", []):
        if r.get("label") != "shared_B":
            continue
        rr = dict(r)
        rr["role_pair"] = channel_for_row(rr)
        rr["from_col_pair"] = col_pair(r.get("from_columns"))
        rr["to_col_pair"] = col_pair(r.get("to_columns"))
        shared_rows.append(rr)

    edges = [(r["from_col_pair"], r["to_col_pair"], r) for r in shared_rows]
    nodes = sorted(set(x for e in edges for x in e[:2]), key=pstr)
    comps = weak_components(nodes, edges)

    comp_index_by_node = {}
    for i, comp in enumerate(comps):
        for n in comp:
            comp_index_by_node[n] = i

    row_tests = []
    for r in sorted(shared_rows, key=lambda x: (x["edge_role"], int(x["from_C"]), int(x["to_C"]))):
        ch = channel_for_row(r)
        spec = CHANNEL_MAP_004[ch]
        row_tests.append({
            "edge_role": r["edge_role"],
            "role_pair": ch,
            "transition": [int(r["from_C"]), int(r["to_C"])],
            "expected_block_edge": [spec["from_block"], spec["to_block"]],
            "from_C_in_expected_block": int(r["from_C"]) in spec["from_values"],
            "to_C_in_expected_block": int(r["to_C"]) in spec["to_values"],
            "matches_channel_map": row_matches_channel_map(r),
            "from_columns": pstr(r["from_col_pair"]),
            "to_columns": pstr(r["to_col_pair"]),
            "component_index": comp_index_by_node.get(r["from_col_pair"]),
        })

    cycles = simple_c_cycles(edges)
    cycle_rows = []

    for cyc in cycles:
        roles = [e[2]["edge_role"] for e in cyc]
        channels = [channel_for_row(e[2]) for e in cyc]
        block_edges = [block_edge_for_row(e[2]) for e in cyc]
        transitions = [[int(e[2]["from_C"]), int(e[2]["to_C"])] for e in cyc]
        c_path = [transitions[0][0], transitions[0][1], transitions[1][1], transitions[2][1]]

        cycle_rows.append({
            "roles": roles,
            "channels": channels,
            "block_edges": block_edges,
            "transitions": transitions,
            "c_path": c_path,
            "column_edges": [[pstr(e[0]), pstr(e[1])] for e in cyc],
            "component_index": comp_index_by_node.get(cyc[0][0]),
            "roles_match_expected_shared_B_order": roles == EXPECTED_SHARED_B_ROLE_ORDER,
            "channels_match_expected_shared_B_order": channels == EXPECTED_SHARED_B_CHANNEL_ORDER,
            "channels_are_cyclic_rotation_of_004_circulation": is_cyclic_rotation(channels, EXPECTED_CHANNEL_CIRCULATION),
            "block_edges_match_BCA_order": block_edges == EXPECTED_SHARED_B_BLOCK_ORDER,
            "closes_C_cycle": c_path[0] == c_path[-1],
        })

    role_counts = Counter(r["edge_role"] for r in shared_rows)
    channel_counts = Counter(channel_for_row(r) for r in shared_rows)
    block_edge_counts = Counter(tuple(block_edge_for_row(r)) for r in shared_rows)

    all_rows_match_channel_map = all(x["matches_channel_map"] for x in row_tests)
    all_cycles_match_role_order = all(x["roles_match_expected_shared_B_order"] for x in cycle_rows)
    all_cycles_match_channel_order = all(x["channels_match_expected_shared_B_order"] for x in cycle_rows)
    all_cycles_are_rotation_of_004 = all(x["channels_are_cyclic_rotation_of_004_circulation"] for x in cycle_rows)
    all_cycles_match_block_order = all(x["block_edges_match_BCA_order"] for x in cycle_rows)
    all_cycles_close_C = all(x["closes_C_cycle"] for x in cycle_rows)

    # Conditional derivation: if the 004 channel block map is accepted, then
    # the C-cycle closure order B->C->A->B forces shared_B role order XY->IW->ZT.
    conditional_derivation_pass = (
        all_rows_match_channel_map
        and all_cycles_match_channel_order
        and all_cycles_are_rotation_of_004
        and all_cycles_match_block_order
        and all_cycles_close_C
    )

    result = {
        "status": "c_transition_block_order_derivation_recorded",
        "audit_id": "021",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_004": str(IN_004),
        "input_020": str(IN_020),
        "shared_row_count": len(shared_rows),
        "component_count": len(comps),
        "cycle_count": len(cycle_rows),
        "role_counts": dict(sorted(role_counts.items())),
        "channel_counts": dict(sorted(channel_counts.items())),
        "block_edge_counts": {str(k): v for k, v in sorted(block_edge_counts.items())},
        "channel_map_004_used": CHANNEL_MAP_004,
        "expected_channel_circulation_004": EXPECTED_CHANNEL_CIRCULATION,
        "expected_shared_B_role_order": EXPECTED_SHARED_B_ROLE_ORDER,
        "expected_shared_B_channel_order": EXPECTED_SHARED_B_CHANNEL_ORDER,
        "expected_shared_B_block_order": EXPECTED_SHARED_B_BLOCK_ORDER,
        "all_rows_match_channel_map": all_rows_match_channel_map,
        "all_cycles_match_role_order": all_cycles_match_role_order,
        "all_cycles_match_channel_order": all_cycles_match_channel_order,
        "all_cycles_are_rotation_of_004_circulation": all_cycles_are_rotation_of_004,
        "all_cycles_match_block_order": all_cycles_match_block_order,
        "all_cycles_close_C": all_cycles_close_C,
        "conditional_derivation_pass": conditional_derivation_pass,
        "row_tests": row_tests,
        "cycles": cycle_rows,
        "prior_020_counts": {
            "c_cycle_count": prior_020.get("c_cycle_count"),
            "all_c_cycles_are_XY_IW_ZT": prior_020.get("all_c_cycles_are_XY_IW_ZT"),
            "component_size_counts": prior_020.get("component_size_counts"),
        },
        "prior_004_status": prior_004.get("status"),
        "interpretation": (
            "This audit checks whether the shared_B role order XY -> IW -> ZT is just an observed "
            "column-cycle fact or whether it is forced by the earlier C-transition block circulation. "
            "Using the 004 block map, XY belongs to TI/XY and sends B -> C; IW belongs to IW/YZ "
            "and sends C -> A; ZT belongs to WX/ZT and sends A -> B. Therefore every closed "
            "shared_B C-cycle follows B -> C -> A -> B, which is a cyclic rotation of the 004 "
            "channel circulation A -> B -> C -> A. This conditionally derives the observed "
            "XY -> IW -> ZT order from the native C-transition block grammar."
        ),
        "boundary": (
            "This derives the shared_B cycle order only conditional on the imported 004 block circulation "
            "and the already selected shared_B rows. It does not derive the shared_B rows from a full "
            "candidate universe, does not construct the full dodecahedral register, and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# C-transition block order derivation 021")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Does the shared_B role order `XY -> IW -> ZT` come from the earlier C-transition block circulation?")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- shared_row_count: `" + str(result["shared_row_count"]) + "`")
    lines.append("- component_count: `" + str(result["component_count"]) + "`")
    lines.append("- cycle_count: `" + str(result["cycle_count"]) + "`")
    lines.append("- role_counts: `" + str(result["role_counts"]) + "`")
    lines.append("- channel_counts: `" + str(result["channel_counts"]) + "`")
    lines.append("- block_edge_counts: `" + str(result["block_edge_counts"]) + "`")
    lines.append("")
    lines.append("## Expected circulation")
    lines.append("")
    lines.append("- 004 channel circulation: `" + str(EXPECTED_CHANNEL_CIRCULATION) + "`")
    lines.append("- shared_B role order: `" + str(EXPECTED_SHARED_B_ROLE_ORDER) + "`")
    lines.append("- shared_B channel order: `" + str(EXPECTED_SHARED_B_CHANNEL_ORDER) + "`")
    lines.append("- shared_B block order: `" + str(EXPECTED_SHARED_B_BLOCK_ORDER) + "`")
    lines.append("")
    lines.append("## Tests")
    lines.append("")
    lines.append("- all_rows_match_channel_map: `" + str(all_rows_match_channel_map) + "`")
    lines.append("- all_cycles_match_role_order: `" + str(all_cycles_match_role_order) + "`")
    lines.append("- all_cycles_match_channel_order: `" + str(all_cycles_match_channel_order) + "`")
    lines.append("- all_cycles_are_rotation_of_004_circulation: `" + str(all_cycles_are_rotation_of_004) + "`")
    lines.append("- all_cycles_match_block_order: `" + str(all_cycles_match_block_order) + "`")
    lines.append("- all_cycles_close_C: `" + str(all_cycles_close_C) + "`")
    lines.append("- conditional_derivation_pass: `" + str(conditional_derivation_pass) + "`")
    lines.append("")
    lines.append("## Cycles")
    lines.append("")
    for c in cycle_rows:
        lines.append(
            "- component=`" + str(c["component_index"])
            + "`, roles=`" + str(c["roles"])
            + "`, channels=`" + str(c["channels"])
            + "`, blocks=`" + str(c["block_edges"])
            + "`, transitions=`" + str(c["transitions"])
            + "`, c_path=`" + str(c["c_path"]) + "`"
        )
    lines.append("")
    lines.append("## Row tests")
    lines.append("")
    for r in row_tests:
        lines.append(
            "- role=`" + str(r["edge_role"])
            + "`, channel=`" + str(r["role_pair"])
            + "`, transition=`" + str(tuple(r["transition"]))
            + "`, block=`" + str(r["expected_block_edge"])
            + "`, matches=`" + str(r["matches_channel_map"])
            + "`, columns=`" + r["from_columns"] + " -> " + r["to_columns"] + "`"
        )
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
    print("shared_row_count", len(shared_rows))
    print("cycle_count", len(cycle_rows))
    print("all_rows_match_channel_map", all_rows_match_channel_map)
    print("all_cycles_match_role_order", all_cycles_match_role_order)
    print("all_cycles_match_channel_order", all_cycles_match_channel_order)
    print("all_cycles_are_rotation_of_004_circulation", all_cycles_are_rotation_of_004)
    print("all_cycles_match_block_order", all_cycles_match_block_order)
    print("all_cycles_close_C", all_cycles_close_C)
    print("conditional_derivation_pass", conditional_derivation_pass)


if __name__ == "__main__":
    main()
