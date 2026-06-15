#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_024_JSON = ROOT / "artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_024_CSV = ROOT / "artifacts/csv/sharedB_selection_matrix_024.v1.csv"
IN_026 = ROOT / "artifacts/json/native_shell_label_derivation_026.v1.json"
IN_027 = ROOT / "artifacts/json/native_shell_rank_derivation_027.v1.json"

OUT_JSON = ROOT / "artifacts/json/reduced_universe_shell_rank_theorem_028.v1.json"
OUT_CSV = ROOT / "artifacts/csv/reduced_universe_shell_rank_theorem_028.v1.csv"
OUT_NOTE = ROOT / "notes/reduced_universe_shell_rank_theorem_028.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def make_rank_map(items, shell_key, sort_key):
    rank = {}
    details = {}
    unambiguous = True

    shells = sorted(set(item[shell_key] for item in items))
    for shell in shells:
        xs = [item for item in items if item[shell_key] == shell]
        pairs = [(sort_key(item), item) for item in xs]
        keys = [k for k, _item in pairs]
        if len(keys) != len(set(keys)):
            unambiguous = False

        pairs.sort(key=lambda kv: kv[0])
        details[shell] = []
        for i, (key, item) in enumerate(pairs):
            idx = int(item["index"])
            rank[idx] = i
            details[shell].append({
                "index": idx,
                "rank": i,
                "key": key,
            })

    return unambiguous, rank, details


def main():
    m024 = load_json(IN_024_JSON)
    m026 = load_json(IN_026)
    m027 = load_json(IN_027)
    candidate_rows = load_csv(IN_024_CSV)

    c_shell = {}
    for r in m026["c_row_derivations"]:
        c_shell[int(r["row_index"])] = str(r["derived_shell"])

    a_shell = {}
    for r in m026["anchor_col_derivations"]:
        a_shell[int(r["col_index"])] = str(r["derived_shell"])

    c_items = []
    for r in m024["c_rows"]:
        idx = int(r["row_index"])
        c_path = [int(x) for x in r["c_path"]]
        c_items.append({
            "index": idx,
            "shell": c_shell[idx],
            "c_path": c_path,
            "c_entry": c_path[0],
            "c_values": [int(x) for x in r["c_values"]],
            "c_sum_mod15": int(r["c_sum_mod15"]),
        })

    a_items = []
    for r in m024["anchor_cols"]:
        idx = int(r["col_index"])
        a_items.append({
            "index": idx,
            "shell": a_shell[idx],
            "anchor_nodes": list(r["anchor_nodes"]),
            "anchor_sum_mod15": int(r["anchor_sum_mod15"]),
            "residues": [int(x) for x in r["residues"]],
        })

    c_rank_ok, c_rank, c_rank_details = make_rank_map(
        c_items,
        "shell",
        lambda item: item["c_entry"],
    )
    a_rank_ok, a_rank, a_rank_details = make_rank_map(
        a_items,
        "shell",
        lambda item: item["anchor_sum_mod15"],
    )

    proof_rows = []
    actual_selected = []
    predicted_selected = []
    false_positives = []
    misses = []

    for r in candidate_rows:
        c_row = int(r["c_row"])
        a_col = int(r["a_col"])
        candidate_index = int(r["candidate_index"])
        actual = str(r["selected"]) == "1"

        predicted = (
            c_shell[c_row] == a_shell[a_col]
            and c_rank[c_row] == a_rank[a_col]
        )

        if actual:
            actual_selected.append(candidate_index)
        if predicted:
            predicted_selected.append(candidate_index)
        if predicted and not actual:
            false_positives.append(candidate_index)
        if actual and not predicted:
            misses.append(candidate_index)

        proof_rows.append({
            "candidate_index": candidate_index,
            "c_row": c_row,
            "a_col": a_col,
            "actual_selected": actual,
            "predicted_selected": predicted,
            "c_shell": c_shell[c_row],
            "anchor_shell": a_shell[a_col],
            "c_rank": c_rank[c_row],
            "anchor_rank": a_rank[a_col],
            "shell_match": c_shell[c_row] == a_shell[a_col],
            "rank_match": c_rank[c_row] == a_rank[a_col],
            "cycle": r["cycle"],
        })

    actual_selected = sorted(actual_selected)
    predicted_selected = sorted(predicted_selected)
    false_positives = sorted(false_positives)
    misses = sorted(misses)

    hypotheses = {
        "H1_reduced_universe_is_4_by_4": (
            int(m024.get("candidate_count", 0)) == 16
            and int(m024.get("c_row_count", 0)) == 4
            and int(m024.get("anchor_col_count", 0)) == 4
        ),
        "H2_native_shell_labels_derived": bool(m026.get("shell_label_derivation_pass")),
        "H3_c_rank_unambiguous": c_rank_ok,
        "H4_anchor_rank_unambiguous": a_rank_ok,
        "H5_027_target_rank_selector_exact": bool(m027.get("native_rank_derivation_pass")),
    }

    conclusion = {
        "actual_selected": actual_selected,
        "predicted_selected": predicted_selected,
        "false_positives": false_positives,
        "misses": misses,
        "predicted_equals_actual": predicted_selected == actual_selected,
        "false_positive_count": len(false_positives),
        "miss_count": len(misses),
    }

    theorem_pass = all(hypotheses.values()) and conclusion["predicted_equals_actual"]

    result = {
        "status": "reduced_universe_shell_rank_theorem_recorded",
        "audit_id": "028",
        "input_024_json": str(IN_024_JSON),
        "input_024_csv": str(IN_024_CSV),
        "input_026": str(IN_026),
        "input_027": str(IN_027),
        "theorem_name": "Reduced-universe native shell-rank selector theorem",
        "theorem_statement": (
            "In the 16-candidate shared_B reduced universe formed by crossing the four observed "
            "C-cycles with the four twisted anchor-cycles, define the C shell by the native C-branch "
            "marker C=5 and the anchor shell by the native branch anchor [8,18]. Rank C-cycles inside "
            "each shell by ascending C entry / XY.from_C. Rank anchor-cycles inside each shell by "
            "ascending anchor_sum_mod15. Then the selector 'same shell and same rank' accepts exactly "
            "the four observed shared_B cycles."
        ),
        "candidate_count": len(candidate_rows),
        "c_row_count": int(m024.get("c_row_count", 0)),
        "anchor_col_count": int(m024.get("anchor_col_count", 0)),
        "actual_selected_count": len(actual_selected),
        "predicted_selected_count": len(predicted_selected),
        "hypotheses": hypotheses,
        "conclusion": conclusion,
        "theorem_pass": theorem_pass,
        "native_c_branch_markers": m026.get("native_c_branch_markers"),
        "native_anchor_branch_markers": m026.get("native_anchor_branch_markers"),
        "c_rank_rule": "ascending c_entry / XY.from_C within derived shell",
        "anchor_rank_rule": "ascending anchor_sum_mod15 within derived shell",
        "c_rank_details": c_rank_details,
        "anchor_rank_details": a_rank_details,
        "proof_rows": proof_rows,
        "interpretation": (
            "This checkpoint packages 026 and 027 as a reduced-universe theorem. The result is no "
            "longer merely a visual radial phase-lock model: within the 16-candidate universe, native "
            "shell labels and native shell ranks determine the four selected shared_B cycles exactly."
        ),
        "boundary": (
            "This theorem is conditional on the reduced 16-candidate universe. It does not derive the "
            "full role-labeled shared_B edge universe from first principles, and it does not close Gap A. "
            "It proves the selector inside the reduced universe."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "candidate_index",
            "c_row",
            "a_col",
            "actual_selected",
            "predicted_selected",
            "c_shell",
            "anchor_shell",
            "c_rank",
            "anchor_rank",
            "shell_match",
            "rank_match",
        ])
        for r in proof_rows:
            w.writerow([
                r["candidate_index"],
                r["c_row"],
                r["a_col"],
                "1" if r["actual_selected"] else "0",
                "1" if r["predicted_selected"] else "0",
                r["c_shell"],
                r["anchor_shell"],
                r["c_rank"],
                r["anchor_rank"],
                "1" if r["shell_match"] else "0",
                "1" if r["rank_match"] else "0",
            ])

    lines = []
    lines.append("# Reduced-universe shell-rank theorem 028")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Theorem")
    lines.append("")
    lines.append(result["theorem_statement"])
    lines.append("")
    lines.append("## Hypotheses")
    lines.append("")
    for k, v in hypotheses.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    lines.append("- actual_selected: `" + str(actual_selected) + "`")
    lines.append("- predicted_selected: `" + str(predicted_selected) + "`")
    lines.append("- false_positives: `" + str(false_positives) + "`")
    lines.append("- misses: `" + str(misses) + "`")
    lines.append("- theorem_pass: `" + str(theorem_pass) + "`")
    lines.append("")
    lines.append("## Native ingredients")
    lines.append("")
    lines.append("- native_c_branch_markers: `" + str(result["native_c_branch_markers"]) + "`")
    lines.append("- native_anchor_branch_markers: `" + str(result["native_anchor_branch_markers"]) + "`")
    lines.append("- c_rank_rule: `" + result["c_rank_rule"] + "`")
    lines.append("- anchor_rank_rule: `" + result["anchor_rank_rule"] + "`")
    lines.append("")
    lines.append("## Rank details")
    lines.append("")
    lines.append("- c_rank_details: `" + str(c_rank_details) + "`")
    lines.append("- anchor_rank_details: `" + str(a_rank_details) + "`")
    lines.append("")
    lines.append("## Proof table")
    lines.append("")
    lines.append("| candidate | c_row | a_col | actual | predicted | c_shell | a_shell | c_rank | a_rank |")
    lines.append("|---|---:|---:|---:|---:|---|---|---:|---:|")
    for r in proof_rows:
        lines.append(
            "| "
            + str(r["candidate_index"]) + " | "
            + str(r["c_row"]) + " | "
            + str(r["a_col"]) + " | "
            + ("1" if r["actual_selected"] else "0") + " | "
            + ("1" if r["predicted_selected"] else "0") + " | "
            + r["c_shell"] + " | "
            + r["anchor_shell"] + " | "
            + str(r["c_rank"]) + " | "
            + str(r["anchor_rank"]) + " |"
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
    print("wrote", OUT_CSV)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("theorem_pass", theorem_pass)
    print("actual_selected", actual_selected)
    print("predicted_selected", predicted_selected)
    print("false_positives", false_positives)
    print("misses", misses)


if __name__ == "__main__":
    main()
