#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_024_JSON = ROOT / "artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_024_CSV = ROOT / "artifacts/csv/sharedB_selection_matrix_024.v1.csv"

OUT_JSON = ROOT / "artifacts/json/radial_phase_lock_selector_025.v1.json"
OUT_NOTE = ROOT / "notes/radial_phase_lock_selector_025.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def score_selector(rows, name, pred):
    tp = fp = tn = fn = 0
    selected_indices = []
    false_positive_indices = []
    miss_indices = []

    for r in rows:
        actual = bool(r["selected"])
        predicted = bool(pred(r))

        if predicted:
            selected_indices.append(int(r["candidate_index"]))

        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
            false_positive_indices.append(int(r["candidate_index"]))
        elif not predicted and actual:
            fn += 1
            miss_indices.append(int(r["candidate_index"]))
        else:
            tn += 1

    return {
        "name": name,
        "accepted_count": tp + fp,
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "miss": fn,
        "exact": fp == 0 and fn == 0,
        "accepted_candidate_indices": selected_indices,
        "false_positive_candidate_indices": false_positive_indices,
        "miss_candidate_indices": miss_indices,
    }


def best_affine_mod4(rows):
    tests = []
    for a in range(4):
        for b in range(4):
            def pred(r, a=a, b=b):
                return r["a_col"] == ((a * r["c_row"] + b) % 4)
            sc = score_selector(rows, "affine_mod4_col_eq_" + str(a) + "_row_plus_" + str(b), pred)
            sc["a"] = a
            sc["b"] = b
            tests.append(sc)
    tests.sort(key=lambda x: (x["false_positive"] + x["miss"], x["false_positive"], x["miss"], -x["true_positive"], x["name"]))
    return tests


def main():
    data = load_json(IN_024_JSON)
    raw_rows = load_csv(IN_024_CSV)

    c_rows = {int(r["row_index"]): r for r in data["c_rows"]}
    a_cols = {int(r["col_index"]): r for r in data["anchor_cols"]}

    # Shell hypothesis from the sketch:
    # C-shell branch marker: the C-cycle contains 5.
    # Anchor-shell branch marker: the anchor-cycle uses branch anchor [8,18].
    for r in c_rows.values():
        r["contains_C5"] = 5 in r["c_values"]
        r["shell"] = "branch" if r["contains_C5"] else "ordinary"

    for r in a_cols.values():
        r["shell"] = "branch" if r["has_branch_anchor_8_18"] else "ordinary"

    # Rank within each shell by the matrix order already recovered in 024.
    c_shell_members = {}
    a_shell_members = {}
    for i in sorted(c_rows):
        c_shell_members.setdefault(c_rows[i]["shell"], []).append(i)
    for j in sorted(a_cols):
        a_shell_members.setdefault(a_cols[j]["shell"], []).append(j)

    c_shell_rank = {}
    a_shell_rank = {}
    for shell, members in c_shell_members.items():
        for rank, idx in enumerate(members):
            c_shell_rank[idx] = rank
    for shell, members in a_shell_members.items():
        for rank, idx in enumerate(members):
            a_shell_rank[idx] = rank

    rows = []
    for rr in raw_rows:
        i = int(rr["c_row"])
        j = int(rr["a_col"])
        cr = c_rows[i]
        ac = a_cols[j]

        row = {
            "candidate_index": int(rr["candidate_index"]),
            "c_row": i,
            "a_col": j,
            "selected": rr["selected"] == "1",
            "c_contains_C5": cr["contains_C5"],
            "anchor_has_branch_8_18": ac["has_branch_anchor_8_18"],
            "c_shell": cr["shell"],
            "anchor_shell": ac["shell"],
            "shell_match": cr["shell"] == ac["shell"],
            "c_shell_rank": c_shell_rank[i],
            "anchor_shell_rank": a_shell_rank[j],
            "shell_rank_match": c_shell_rank[i] == a_shell_rank[j],
            "radial_phase_lock": cr["shell"] == ac["shell"] and c_shell_rank[i] == a_shell_rank[j],
            "permutation_024": j == data["selected_col_by_row"].get(str(i)),
            "order3_plus_fixed": j == ((i + 1) % 3 if i < 3 else 3),
            "c_sum_mod15": cr["c_sum_mod15"],
            "anchor_sum_mod15": ac["anchor_sum_mod15"],
            "sum_delta_mod15": (ac["anchor_sum_mod15"] - cr["c_sum_mod15"]) % 15,
            "intersection_size": len(set(cr["c_values"]) & set(ac["residues"])),
            "c_values": cr["c_values"],
            "anchor_residues": ac["residues"],
        }
        rows.append(row)

    selector_scores = []
    selector_scores.append(score_selector(rows, "branch_gate_only_shell_match", lambda r: r["shell_match"]))
    selector_scores.append(score_selector(rows, "shell_rank_match_only", lambda r: r["shell_rank_match"]))
    selector_scores.append(score_selector(rows, "radial_phase_lock_shell_and_rank", lambda r: r["radial_phase_lock"]))
    selector_scores.append(score_selector(rows, "order3_plus_fixed_from_024_permutation_shape", lambda r: r["order3_plus_fixed"]))
    selector_scores.append(score_selector(rows, "literal_024_permutation_lookup", lambda r: r["permutation_024"]))

    affine_tests = best_affine_mod4(rows)
    selector_scores.extend(affine_tests[:8])

    # Basic scalar tests from 024 summaries, intentionally weak.
    for k in sorted(set(r["sum_delta_mod15"] for r in rows)):
        selector_scores.append(score_selector(rows, "sum_delta_mod15_eq_" + str(k), lambda r, k=k: r["sum_delta_mod15"] == k))
    for k in sorted(set(r["intersection_size"] for r in rows)):
        selector_scores.append(score_selector(rows, "intersection_size_eq_" + str(k), lambda r, k=k: r["intersection_size"] == k))

    selector_scores.sort(key=lambda x: (not x["exact"], x["false_positive"] + x["miss"], x["false_positive"], x["miss"], x["accepted_count"], x["name"]))

    exact_selectors = [x for x in selector_scores if x["exact"]]

    shell_table = []
    for i in sorted(c_rows):
        shell_table.append({
            "kind": "c_row",
            "index": i,
            "shell": c_rows[i]["shell"],
            "shell_rank": c_shell_rank[i],
            "contains_C5": c_rows[i]["contains_C5"],
            "c_values": c_rows[i]["c_values"],
            "c_sum_mod15": c_rows[i]["c_sum_mod15"],
        })
    for j in sorted(a_cols):
        shell_table.append({
            "kind": "anchor_col",
            "index": j,
            "shell": a_cols[j]["shell"],
            "shell_rank": a_shell_rank[j],
            "has_branch_anchor_8_18": a_cols[j]["has_branch_anchor_8_18"],
            "anchor_nodes": a_cols[j]["anchor_nodes"],
            "residues": a_cols[j]["residues"],
            "anchor_sum_mod15": a_cols[j]["anchor_sum_mod15"],
        })

    result = {
        "status": "radial_phase_lock_selector_recorded",
        "audit_id": "025",
        "input_024_json": str(IN_024_JSON),
        "input_024_csv": str(IN_024_CSV),
        "candidate_count": len(rows),
        "selected_count": sum(1 for r in rows if r["selected"]),
        "selected_permutation": data["selected_col_by_row"],
        "permutation_cycles": data["permutation_cycles"],
        "permutation_order": data["permutation_order"],
        "c_shell_members": c_shell_members,
        "anchor_shell_members": a_shell_members,
        "selector_scores": selector_scores,
        "exact_selectors": exact_selectors,
        "shell_table": shell_table,
        "candidate_rows": rows,
        "interpretation": (
            "This audit tests the radial phase-lock reading suggested by the hand sketch. "
            "The 024 permutation is modeled as a shell gate plus a phase-rank lock: C-cycles "
            "containing C=5 pair with anchor-cycles containing the branch anchor [8,18], while "
            "ordinary C-cycles pair with ordinary anchor-cycles. Within each shell, the recovered "
            "matrix order supplies a phase rank. The radial phase-lock selector accepts exactly "
            "the four observed cells. This is a compact model of the 4-of-16 selection, but it is "
            "still conditional because the shell order/rank must be derived from native register "
            "provenance rather than read from the reduced matrix."
        ),
        "boundary": (
            "This does not close Gap A. It derives an exact selector only after accepting the shell "
            "markers and matrix-order phase ranks from the reduced 024 representation. The next step "
            "is to derive those shell/rank labels natively."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Radial phase-lock selector 025")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- selected_permutation: `" + str(result["selected_permutation"]) + "`")
    lines.append("- permutation_cycles: `" + str(result["permutation_cycles"]) + "`")
    lines.append("- permutation_order: `" + str(result["permutation_order"]) + "`")
    lines.append("")
    lines.append("## Shells")
    lines.append("")
    lines.append("- c_shell_members: `" + str(c_shell_members) + "`")
    lines.append("- anchor_shell_members: `" + str(a_shell_members) + "`")
    lines.append("")
    lines.append("## Selector scores")
    lines.append("")
    for s in selector_scores[:40]:
        lines.append(
            "- " + s["name"]
            + ": exact=`" + str(s["exact"])
            + "`, accepted=`" + str(s["accepted_count"])
            + "`, fp=`" + str(s["false_positive"])
            + "`, miss=`" + str(s["miss"])
            + "`, accepted_indices=`" + str(s["accepted_candidate_indices"]) + "`"
        )
    lines.append("")
    lines.append("## Exact selectors")
    lines.append("")
    if exact_selectors:
        for s in exact_selectors:
            lines.append("- " + s["name"] + ": accepted_indices=`" + str(s["accepted_candidate_indices"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Shell table")
    lines.append("")
    for r in shell_table:
        lines.append("- `" + str(r) + "`")
    lines.append("")
    lines.append("## Candidate rows")
    lines.append("")
    for r in rows:
        lines.append(
            "- candidate=`" + str(r["candidate_index"])
            + "`, selected=`" + str(r["selected"])
            + "`, c_row=`" + str(r["c_row"])
            + "`, a_col=`" + str(r["a_col"])
            + "`, c_shell=`" + r["c_shell"]
            + "`, anchor_shell=`" + r["anchor_shell"]
            + "`, c_rank=`" + str(r["c_shell_rank"])
            + "`, a_rank=`" + str(r["anchor_shell_rank"])
            + "`, radial_phase_lock=`" + str(r["radial_phase_lock"]) + "`"
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
    print("candidate_count", result["candidate_count"])
    print("selected_count", result["selected_count"])
    print("exact_selectors", [x["name"] for x in exact_selectors])
    print("best_selector", selector_scores[0]["name"], "exact", selector_scores[0]["exact"])
    print("c_shell_members", c_shell_members)
    print("anchor_shell_members", a_shell_members)


if __name__ == "__main__":
    main()
