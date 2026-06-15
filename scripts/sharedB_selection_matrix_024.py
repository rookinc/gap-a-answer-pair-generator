#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from math import gcd
from functools import reduce

ROOT = Path(__file__).resolve().parents[1]

IN_023 = ROOT / "artifacts/json/sharedB_16_candidate_selector_search_023.v1.json"

OUT_JSON = ROOT / "artifacts/json/sharedB_selection_matrix_024.v1.json"
OUT_CSV = ROOT / "artifacts/csv/sharedB_selection_matrix_024.v1.csv"
OUT_NOTE = ROOT / "notes/sharedB_selection_matrix_024.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pcycle(cyc):
    parts = []
    for role, c0, c1, src, dst in cyc:
        parts.append(str(role) + ":" + str(c0) + "->" + str(c1) + ":" + str(src) + "->" + str(dst))
    return " | ".join(parts)


def c_key(cyc):
    return tuple((str(role), int(c0), int(c1)) for role, c0, c1, _src, _dst in cyc)


def a_key(cyc):
    return tuple((str(role), str(src), str(dst)) for role, _c0, _c1, src, dst in cyc)


def c_path(ckey):
    # Expected order: XY, IW, ZT, with C closure.
    d = {role: (c0, c1) for role, c0, c1 in ckey}
    return [d["XY"][0], d["XY"][1], d["IW"][1], d["ZT"][1]]


def c_summary(ckey):
    path = c_path(ckey)
    vals = sorted(set(path))
    return {
        "c_key": str(ckey),
        "transitions": [[role, c0, c1] for role, c0, c1 in ckey],
        "c_path": path,
        "c_values": vals,
        "c_sum_mod15": sum(vals) % 15,
        "c_min": min(vals),
        "c_max": max(vals),
        "c_span": max(vals) - min(vals),
    }


def parse_anchor_pair(s):
    # s looks like "[0,4]"
    body = str(s).strip()[1:-1]
    return tuple(int(x.strip()) for x in body.split(",") if x.strip())


def anchor_summary(akey):
    # Expected twisted order:
    # XY n0->n1, IW n2->n0, ZT n1->n2.
    d = {role: (src, dst) for role, src, dst in akey}
    n0 = d["XY"][0]
    n1 = d["XY"][1]
    n2 = d["ZT"][1]
    anchor_path = [n0, n1, n2, n0]

    pairs = [parse_anchor_pair(x) for x in [n0, n1, n2]]
    cols = sorted(set(v for p in pairs for v in p))
    residues = sorted(set(v % 15 for v in cols))

    return {
        "a_key": str(akey),
        "anchor_edges": [[role, src, dst] for role, src, dst in akey],
        "anchor_path": anchor_path,
        "anchor_nodes": [n0, n1, n2],
        "column_count": len(cols),
        "columns": cols,
        "residues": residues,
        "anchor_sum_mod15": sum(cols) % 15,
        "has_branch_anchor_8_18": "[8,18]" in [n0, n1, n2],
    }


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def permutation_cycles(mapping):
    seen = set()
    cycles = []
    for start in sorted(mapping):
        if start in seen:
            continue
        cur = start
        cyc = []
        while cur not in seen:
            seen.add(cur)
            cyc.append(cur)
            cur = mapping[cur]
        cycles.append(cyc)
    return cycles


def main():
    data = load_json(IN_023)

    rows = []
    for r in data.get("selected_candidates", []):
        rr = dict(r)
        rr["selected"] = True
        rows.append(rr)
    for r in data.get("rejected_candidates", []):
        rr = dict(r)
        rr["selected"] = False
        rows.append(rr)

    rows.sort(key=lambda r: int(r["candidate_index"]))

    for r in rows:
        cyc = r["cycle"]
        r["c_key"] = c_key(cyc)
        r["a_key"] = a_key(cyc)

    c_order = []
    a_order = []
    for r in rows:
        if r["c_key"] not in c_order:
            c_order.append(r["c_key"])
        if r["a_key"] not in a_order:
            a_order.append(r["a_key"])

    c_index = {k: i for i, k in enumerate(c_order)}
    a_index = {k: i for i, k in enumerate(a_order)}

    matrix = [["." for _ in a_order] for _ in c_order]
    matrix_candidate_indices = [["" for _ in a_order] for _ in c_order]
    selected_positions = []

    for r in rows:
        i = c_index[r["c_key"]]
        j = a_index[r["a_key"]]
        matrix_candidate_indices[i][j] = str(r["candidate_index"])
        if r["selected"]:
            matrix[i][j] = "S"
            selected_positions.append({
                "candidate_index": int(r["candidate_index"]),
                "c_row": i,
                "a_col": j,
                "cycle": r["cycle"],
            })

    selected_positions.sort(key=lambda x: x["c_row"])

    selected_col_by_row = {x["c_row"]: x["a_col"] for x in selected_positions}
    selected_row_by_col = {x["a_col"]: x["c_row"] for x in selected_positions}

    is_permutation = (
        len(selected_positions) == len(c_order) == len(a_order)
        and len(selected_col_by_row) == len(c_order)
        and len(selected_row_by_col) == len(a_order)
    )

    cycles = permutation_cycles(selected_col_by_row) if is_permutation else []
    cycle_lengths = [len(x) for x in cycles]
    permutation_order = reduce(lcm, cycle_lengths, 1) if cycle_lengths else None

    c_rows = []
    for i, ck in enumerate(c_order):
        s = c_summary(ck)
        s["row_index"] = i
        s["selected_anchor_col"] = selected_col_by_row.get(i)
        c_rows.append(s)

    a_cols = []
    for j, ak in enumerate(a_order):
        s = anchor_summary(ak)
        s["col_index"] = j
        s["selected_c_row"] = selected_row_by_col.get(j)
        a_cols.append(s)

    selected_pair_rows = []
    for pos in selected_positions:
        cr = c_rows[pos["c_row"]]
        ac = a_cols[pos["a_col"]]
        selected_pair_rows.append({
            "candidate_index": pos["candidate_index"],
            "c_row": pos["c_row"],
            "a_col": pos["a_col"],
            "c_path": cr["c_path"],
            "c_values": cr["c_values"],
            "anchor_path": ac["anchor_path"],
            "anchor_nodes": ac["anchor_nodes"],
            "anchor_residues": ac["residues"],
            "c_values_intersection_anchor_residues": sorted(set(cr["c_values"]) & set(ac["residues"])),
            "c_sum_mod15": cr["c_sum_mod15"],
            "anchor_sum_mod15": ac["anchor_sum_mod15"],
            "has_branch_anchor_8_18": ac["has_branch_anchor_8_18"],
        })

    result = {
        "status": "sharedB_selection_matrix_recorded",
        "audit_id": "024",
        "input_023": str(IN_023),
        "candidate_count": len(rows),
        "c_row_count": len(c_order),
        "anchor_col_count": len(a_order),
        "selected_count": len(selected_positions),
        "selection_matrix": matrix,
        "candidate_index_matrix": matrix_candidate_indices,
        "selected_positions": selected_positions,
        "selected_col_by_row": {str(k): v for k, v in sorted(selected_col_by_row.items())},
        "selected_row_by_col": {str(k): v for k, v in sorted(selected_row_by_col.items())},
        "is_permutation": is_permutation,
        "permutation_cycles": cycles,
        "permutation_cycle_lengths": cycle_lengths,
        "permutation_order": permutation_order,
        "c_rows": c_rows,
        "anchor_cols": a_cols,
        "selected_pair_rows": selected_pair_rows,
        "interpretation": (
            "The 16-candidate shared_B boundary is a 4 x 4 pairing problem: four C-cycles "
            "crossed with four twisted anchor-cycles. The observed selection picks one cell in "
            "each row and one cell in each column, so it is a permutation rather than a scalar "
            "threshold. In the recovered row/column order, the selected permutation is row -> col "
            + str([selected_col_by_row.get(i) for i in range(len(c_order))])
            + ". This reframes the missing selector as a coupling/permutation between C-cycle "
            "phase and anchor-cycle phase."
        ),
        "boundary": (
            "This audit does not derive the permutation. It identifies the reduced 4 x 4 selection "
            "shape that a future native generator must explain."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["c_row", "a_col", "candidate_index", "selected", "c_key", "a_key", "cycle"])
        for r in rows:
            w.writerow([
                c_index[r["c_key"]],
                a_index[r["a_key"]],
                r["candidate_index"],
                "1" if r["selected"] else "0",
                str(r["c_key"]),
                str(r["a_key"]),
                pcycle(r["cycle"]),
            ])

    lines = []
    lines.append("# Shared_B selection matrix 024")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- c_row_count: `" + str(result["c_row_count"]) + "`")
    lines.append("- anchor_col_count: `" + str(result["anchor_col_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- is_permutation: `" + str(result["is_permutation"]) + "`")
    lines.append("- selected_col_by_row: `" + str(result["selected_col_by_row"]) + "`")
    lines.append("- permutation_cycles: `" + str(result["permutation_cycles"]) + "`")
    lines.append("- permutation_cycle_lengths: `" + str(result["permutation_cycle_lengths"]) + "`")
    lines.append("- permutation_order: `" + str(result["permutation_order"]) + "`")
    lines.append("")
    lines.append("## Selection matrix")
    lines.append("")
    lines.append("Rows are C-cycles. Columns are twisted anchor-cycles.")
    lines.append("")
    header = "| c_row | " + " | ".join("a" + str(i) for i in range(len(a_order))) + " |"
    sep = "|---|" + "|".join("---" for _ in a_order) + "|"
    lines.append(header)
    lines.append(sep)
    for i, row in enumerate(matrix):
        cells = []
        for j, val in enumerate(row):
            cand = matrix_candidate_indices[i][j]
            cells.append(val + cand if val == "S" else cand)
        lines.append("| " + str(i) + " | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## C-cycle rows")
    lines.append("")
    for r in c_rows:
        lines.append("- c_row `" + str(r["row_index"]) + "`")
        lines.append("  - transitions: `" + str(r["transitions"]) + "`")
        lines.append("  - c_path: `" + str(r["c_path"]) + "`")
        lines.append("  - c_values: `" + str(r["c_values"]) + "`")
        lines.append("  - c_sum_mod15: `" + str(r["c_sum_mod15"]) + "`")
        lines.append("  - selected_anchor_col: `" + str(r["selected_anchor_col"]) + "`")
    lines.append("")
    lines.append("## Anchor-cycle columns")
    lines.append("")
    for r in a_cols:
        lines.append("- a_col `" + str(r["col_index"]) + "`")
        lines.append("  - anchor_path: `" + str(r["anchor_path"]) + "`")
        lines.append("  - anchor_nodes: `" + str(r["anchor_nodes"]) + "`")
        lines.append("  - residues: `" + str(r["residues"]) + "`")
        lines.append("  - anchor_sum_mod15: `" + str(r["anchor_sum_mod15"]) + "`")
        lines.append("  - has_branch_anchor_8_18: `" + str(r["has_branch_anchor_8_18"]) + "`")
        lines.append("  - selected_c_row: `" + str(r["selected_c_row"]) + "`")
    lines.append("")
    lines.append("## Selected pair rows")
    lines.append("")
    for r in selected_pair_rows:
        lines.append("- candidate `" + str(r["candidate_index"]) + "`: c_row=`" + str(r["c_row"]) + "`, a_col=`" + str(r["a_col"]) + "`")
        lines.append("  - c_path: `" + str(r["c_path"]) + "`")
        lines.append("  - anchor_path: `" + str(r["anchor_path"]) + "`")
        lines.append("  - intersection: `" + str(r["c_values_intersection_anchor_residues"]) + "`")
        lines.append("  - c_sum_mod15: `" + str(r["c_sum_mod15"]) + "`, anchor_sum_mod15: `" + str(r["anchor_sum_mod15"]) + "`")
        lines.append("  - has_branch_anchor_8_18: `" + str(r["has_branch_anchor_8_18"]) + "`")
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
    print("wrote", OUT_CSV)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("candidate_count", result["candidate_count"])
    print("c_row_count", result["c_row_count"])
    print("anchor_col_count", result["anchor_col_count"])
    print("selected_count", result["selected_count"])
    print("is_permutation", result["is_permutation"])
    print("selected_col_by_row", result["selected_col_by_row"])
    print("permutation_cycles", result["permutation_cycles"])
    print("permutation_order", result["permutation_order"])


if __name__ == "__main__":
    main()
