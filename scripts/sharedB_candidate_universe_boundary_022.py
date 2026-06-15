#!/usr/bin/env python3
import itertools
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_021 = ROOT / "artifacts/json/c_transition_block_order_derivation_021.v1.json"

OUT_JSON = ROOT / "artifacts/json/sharedB_candidate_universe_boundary_022.v1.json"
OUT_NOTE = ROOT / "notes/sharedB_candidate_universe_boundary_022.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

# Imported 004 block grammar, used in 021.
BLOCKS = {
    "A": [0, 2, 10, 14],
    "B": [2, 4, 11, 13],
    "C": [1, 2, 5],
}

ROLE_BLOCK_EDGE = {
    "XY": ["B", "C"],
    "IW": ["C", "A"],
    "ZT": ["A", "B"],
}

ROLE_ORDER = ["XY", "IW", "ZT"]


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


def c_cycle_key(cyc):
    return tuple((role, int(a), int(b)) for role, a, b in cyc)


def anchor_cycle_key(cyc):
    return tuple((role, pstr(a), pstr(b)) for role, a, b in cyc)


def exact_cycle_key(cyc):
    return tuple((role, int(c0), int(c1), pstr(a), pstr(b)) for role, c0, c1, a, b in cyc)


def build_observed_cycles(shared_rows):
    edge_by_from_c = defaultdict(list)
    for r in shared_rows:
        edge_by_from_c[int(r["from_C"])].append(r)

    cycles = []
    seen = set()

    for xy in [r for r in shared_rows if r["edge_role"] == "XY"]:
        for iw in edge_by_from_c.get(int(xy["to_C"]), []):
            if iw["edge_role"] != "IW":
                continue
            for zt in edge_by_from_c.get(int(iw["to_C"]), []):
                if zt["edge_role"] != "ZT":
                    continue
                if int(zt["to_C"]) != int(xy["from_C"]):
                    continue

                cyc = [
                    ("XY", int(xy["from_C"]), int(xy["to_C"]), xy["from_col_pair"], xy["to_col_pair"]),
                    ("IW", int(iw["from_C"]), int(iw["to_C"]), iw["from_col_pair"], iw["to_col_pair"]),
                    ("ZT", int(zt["from_C"]), int(zt["to_C"]), zt["from_col_pair"], zt["to_col_pair"]),
                ]
                key = exact_cycle_key(cyc)
                if key not in seen:
                    seen.add(key)
                    cycles.append(cyc)

    cycles.sort(key=lambda c: exact_cycle_key(c))
    return cycles


def main():
    overlay = load_json(IN_G60_OVERLAY)
    prior_021 = load_json(IN_021) if IN_021.exists() else {}

    edge_records = overlay.get("edge_records", [])

    reverse_rows = []
    shared_rows = []

    for r in edge_records:
        rr = dict(r)
        rr["from_col_pair"] = col_pair(r.get("from_columns"))
        rr["to_col_pair"] = col_pair(r.get("to_columns"))
        rr["role_pair"] = ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role")))

        if r.get("label") == "reverse_partner":
            reverse_rows.append(rr)
        elif r.get("label") == "shared_B":
            shared_rows.append(rr)

    reverse_anchors = sorted(set(r["from_col_pair"] for r in reverse_rows), key=pstr)

    observed_cycles = build_observed_cycles(shared_rows)

    observed_c_cycles = sorted(set(
        c_cycle_key([(role, c0, c1) for role, c0, c1, _a, _b in cyc])
        for cyc in observed_cycles
    ))

    observed_anchor_cycles = sorted(set(
        anchor_cycle_key([(role, a, b) for role, _c0, _c1, a, b in cyc])
        for cyc in observed_cycles
    ))

    observed_exact_cycles = sorted(set(exact_cycle_key(cyc) for cyc in observed_cycles))

    # 004 block-circulation C-cycle universe:
    # XY: B -> C, IW: C -> A, ZT: A -> B.
    c_cycle_universe = []
    for b in BLOCKS["B"]:
        for c in BLOCKS["C"]:
            for a in BLOCKS["A"]:
                c_cycle_universe.append((
                    ("XY", b, c),
                    ("IW", c, a),
                    ("ZT", a, b),
                ))

    c_cycle_universe_keys = sorted(c_cycle_key(c) for c in c_cycle_universe)

    # Observed anchor-cycle universe over reverse_partner anchors.
    #
    # C-role order is XY -> IW -> ZT, but the column-edge closure is twisted:
    #
    #   XY: n0 -> n1
    #   IW: n2 -> n0
    #   ZT: n1 -> n2
    #
    # Equivalently, the column traversal order is XY -> ZT -> IW.
    # The earlier version used the untwisted orientation and therefore missed
    # all observed exact cycles.
    anchor_cycle_universe = []
    for n0, n1, n2 in itertools.permutations(reverse_anchors, 3):
        anchor_cycle_universe.append((
            ("XY", n0, n1),
            ("IW", n2, n0),
            ("ZT", n1, n2),
        ))

    anchor_cycle_universe_keys = sorted(anchor_cycle_key(c) for c in anchor_cycle_universe)

    observed_shared_edge_keys = set(
        (r["edge_role"], int(r["from_C"]), int(r["to_C"]), pstr(r["from_col_pair"]), pstr(r["to_col_pair"]))
        for r in shared_rows
    )

    combined_candidate_count = len(c_cycle_universe) * len(anchor_cycle_universe)

    selected_by_c_transition_only = len(observed_c_cycles) * len(anchor_cycle_universe)
    selected_by_anchor_only = len(c_cycle_universe) * len(observed_anchor_cycles)
    selected_by_c_and_anchor = len(observed_c_cycles) * len(observed_anchor_cycles)

    # Exact observed-edge filter over the loose combined universe.
    observed_edge_filtered = []
    for ccyc in c_cycle_universe:
        ckey = c_cycle_key(ccyc)
        for acyc in anchor_cycle_universe:
            akey = anchor_cycle_key(acyc)

            exact_parts = []
            ok = True
            for (role1, c0, c1), (role2, src, dst) in zip(ccyc, acyc):
                if role1 != role2:
                    ok = False
                    break
                edge_key = (role1, int(c0), int(c1), pstr(src), pstr(dst))
                exact_parts.append((role1, int(c0), int(c1), src, dst))
                if edge_key not in observed_shared_edge_keys:
                    ok = False
                    break

            if ok:
                observed_edge_filtered.append(tuple(exact_parts))

    observed_edge_filtered_keys = sorted(set(exact_cycle_key(c) for c in observed_edge_filtered))

    false_positive_counts = {
        "c_transition_only": selected_by_c_transition_only - len(observed_exact_cycles),
        "anchor_only": selected_by_anchor_only - len(observed_exact_cycles),
        "c_and_anchor_only": selected_by_c_and_anchor - len(observed_exact_cycles),
        "observed_edge_filter": len(observed_edge_filtered_keys) - len(observed_exact_cycles),
    }

    miss_counts = {
        "c_transition_only": 0 if all(k in c_cycle_universe_keys for k in observed_c_cycles) else None,
        "anchor_only": 0 if all(k in anchor_cycle_universe_keys for k in observed_anchor_cycles) else None,
        "c_and_anchor_only": 0,
        "observed_edge_filter": len(set(observed_exact_cycles) - set(observed_edge_filtered_keys)),
    }

    exact_filter_pass = (
        set(observed_edge_filtered_keys) == set(observed_exact_cycles)
        and len(observed_edge_filtered_keys) == 4
    )

    observed_cycle_rows = []
    for cyc in observed_cycles:
        observed_cycle_rows.append({
            "c_cycle": [[role, c0, c1] for role, c0, c1, _a, _b in cyc],
            "anchor_cycle": [[role, pstr(a), pstr(b)] for role, _c0, _c1, a, b in cyc],
            "exact_cycle": [[role, c0, c1, pstr(a), pstr(b)] for role, c0, c1, a, b in cyc],
        })

    result = {
        "status": "sharedB_candidate_universe_boundary_recorded",
        "audit_id": "022",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_021": str(IN_021),
        "reverse_anchor_count": len(reverse_rows),
        "reverse_distinct_anchor_count": len(reverse_anchors),
        "shared_row_count": len(shared_rows),
        "observed_exact_cycle_count": len(observed_exact_cycles),
        "observed_c_cycle_count": len(observed_c_cycles),
        "observed_anchor_cycle_count": len(observed_anchor_cycles),
        "c_cycle_universe_count": len(c_cycle_universe),
        "anchor_cycle_universe_count": len(anchor_cycle_universe),
        "combined_cycle_candidate_count": combined_candidate_count,
        "selected_counts": {
            "c_transition_only": selected_by_c_transition_only,
            "anchor_only": selected_by_anchor_only,
            "c_and_anchor_only": selected_by_c_and_anchor,
            "observed_edge_filter": len(observed_edge_filtered_keys),
        },
        "false_positive_counts": false_positive_counts,
        "miss_counts": miss_counts,
        "observed_edge_filter_exact": exact_filter_pass,
        "reduction_factors": {
            "combined_to_observed": combined_candidate_count / max(1, len(observed_exact_cycles)),
            "c_transition_only_to_observed": selected_by_c_transition_only / max(1, len(observed_exact_cycles)),
            "anchor_only_to_observed": selected_by_anchor_only / max(1, len(observed_exact_cycles)),
            "c_and_anchor_only_to_observed": selected_by_c_and_anchor / max(1, len(observed_exact_cycles)),
        },
        "blocks": BLOCKS,
        "role_block_edge": ROLE_BLOCK_EDGE,
        "role_order": ROLE_ORDER,
        "reverse_anchors": [pstr(x) for x in reverse_anchors],
        "observed_cycles": observed_cycle_rows,
        "observed_c_cycles": [str(x) for x in observed_c_cycles],
        "observed_anchor_cycles": [str(x) for x in observed_anchor_cycles],
        "observed_edge_filtered_cycles": [str(x) for x in observed_edge_filtered_keys],
        "prior_021": {
            "conditional_derivation_pass": prior_021.get("conditional_derivation_pass"),
            "cycle_count": prior_021.get("cycle_count"),
            "all_cycles_match_block_order": prior_021.get("all_cycles_match_block_order"),
        },
        "interpretation": (
            "The 004 block circulation generates 48 possible C-cycles. The observed reverse-partner "
            "anchors generate 990 possible twisted ordered column 3-cycles. Their loose product gives "
            "47,520 candidate shared_B cycles, but only 4 are observed. C-transition selection alone, "
            "anchor selection alone, and their conjunction still overgenerate. The exact filter is the "
            "role-edge filter: each of the three role-labeled moves must exist as an observed shared_B "
            "edge. That filter recovers the 4 cycles exactly, but it is circular until the role-edge "
            "moves are derived from a native register or candidate universe. Therefore the missing "
            "generator has been narrowed to the role-labeled shared_B edge selector."
        ),
        "boundary": (
            "This is a candidate-universe boundary audit. It does not derive the observed shared_B edges; "
            "it shows where the overgeneration lives and what a future native selector must explain. "
            "It does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Shared_B candidate-universe boundary 022")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Can 004 block circulation plus reverse_partner anchors recover the observed shared_B cycles exactly?")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- reverse_anchor_count: `" + str(result["reverse_anchor_count"]) + "`")
    lines.append("- reverse_distinct_anchor_count: `" + str(result["reverse_distinct_anchor_count"]) + "`")
    lines.append("- shared_row_count: `" + str(result["shared_row_count"]) + "`")
    lines.append("- observed_exact_cycle_count: `" + str(result["observed_exact_cycle_count"]) + "`")
    lines.append("- observed_c_cycle_count: `" + str(result["observed_c_cycle_count"]) + "`")
    lines.append("- observed_anchor_cycle_count: `" + str(result["observed_anchor_cycle_count"]) + "`")
    lines.append("- c_cycle_universe_count: `" + str(result["c_cycle_universe_count"]) + "`")
    lines.append("- anchor_cycle_universe_count: `" + str(result["anchor_cycle_universe_count"]) + "`")
    lines.append("- combined_cycle_candidate_count: `" + str(result["combined_cycle_candidate_count"]) + "`")
    lines.append("")
    lines.append("## Selector counts")
    lines.append("")
    for k, v in result["selected_counts"].items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## False positives")
    lines.append("")
    for k, v in result["false_positive_counts"].items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Misses")
    lines.append("")
    for k, v in result["miss_counts"].items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Exactness")
    lines.append("")
    lines.append("- observed_edge_filter_exact: `" + str(result["observed_edge_filter_exact"]) + "`")
    lines.append("")
    lines.append("## Reduction factors")
    lines.append("")
    for k, v in result["reduction_factors"].items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Observed cycles")
    lines.append("")
    for r in observed_cycle_rows:
        lines.append("- C-cycle: `" + str(r["c_cycle"]) + "`")
        lines.append("  - anchor-cycle: `" + str(r["anchor_cycle"]) + "`")
        lines.append("  - exact-cycle: `" + str(r["exact_cycle"]) + "`")
    lines.append("")
    lines.append("## Reverse anchors")
    lines.append("")
    lines.append("`" + str(result["reverse_anchors"]) + "`")
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
    print("c_cycle_universe_count", result["c_cycle_universe_count"])
    print("anchor_cycle_universe_count", result["anchor_cycle_universe_count"])
    print("combined_cycle_candidate_count", result["combined_cycle_candidate_count"])
    print("observed_exact_cycle_count", result["observed_exact_cycle_count"])
    print("selected_counts", result["selected_counts"])
    print("false_positive_counts", result["false_positive_counts"])
    print("observed_edge_filter_exact", result["observed_edge_filter_exact"])


if __name__ == "__main__":
    main()
