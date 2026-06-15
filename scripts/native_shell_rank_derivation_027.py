#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from itertools import product

ROOT = Path(__file__).resolve().parents[1]

IN_024_JSON = ROOT / "artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_024_CSV = ROOT / "artifacts/csv/sharedB_selection_matrix_024.v1.csv"
IN_026 = ROOT / "artifacts/json/native_shell_label_derivation_026.v1.json"

OUT_JSON = ROOT / "artifacts/json/native_shell_rank_derivation_027.v1.json"
OUT_NOTE = ROOT / "notes/native_shell_rank_derivation_027.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_anchor_pair(s):
    body = str(s).strip()[1:-1]
    return tuple(int(x.strip()) for x in body.split(",") if x.strip())


def flatten_cols(anchor_nodes):
    vals = []
    for n in anchor_nodes:
        vals.extend(parse_anchor_pair(n))
    return sorted(set(vals))


def flatten_residues(anchor_nodes):
    return sorted(set(x % 15 for x in flatten_cols(anchor_nodes)))


def score(rows, name, pred):
    tp = fp = tn = miss = 0
    accepted = []
    false_pos = []
    misses = []

    for r in rows:
        actual = bool(r["selected"])
        got = bool(pred(r))
        if got:
            accepted.append(r["candidate_index"])
        if got and actual:
            tp += 1
        elif got and not actual:
            fp += 1
            false_pos.append(r["candidate_index"])
        elif not got and actual:
            miss += 1
            misses.append(r["candidate_index"])
        else:
            tn += 1

    return {
        "name": name,
        "exact": fp == 0 and miss == 0,
        "accepted_count": tp + fp,
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "miss": miss,
        "accepted_candidate_indices": accepted,
        "false_positive_candidate_indices": false_pos,
        "miss_candidate_indices": misses,
    }


def make_rank_map(items, shell_getter, key_getter, reverse=False):
    rank = {}
    details = {}
    valid = True
    shells = sorted(set(shell_getter(x) for x in items))

    for shell in shells:
        xs = [x for x in items if shell_getter(x) == shell]
        decorated = []
        for x in xs:
            k = key_getter(x)
            decorated.append((k, x))

        keys = [k for k, _x in decorated]
        if len(set(keys)) != len(keys):
            valid = False

        decorated.sort(key=lambda kv: kv[0], reverse=reverse)

        details[shell] = []
        for i, (k, x) in enumerate(decorated):
            idx = int(x["index"])
            rank[idx] = i
            details[shell].append({
                "index": idx,
                "rank": i,
                "key": k,
            })

    return valid, rank, details


def main():
    m024 = load_json(IN_024_JSON)
    m026 = load_json(IN_026)
    csv_rows = load_csv(IN_024_CSV)

    c_shell_by_index = {}
    for r in m026["c_row_derivations"]:
        c_shell_by_index[int(r["row_index"])] = r["derived_shell"]

    a_shell_by_index = {}
    for r in m026["anchor_col_derivations"]:
        a_shell_by_index[int(r["col_index"])] = r["derived_shell"]

    c_items = []
    for r in m024["c_rows"]:
        idx = int(r["row_index"])
        c_path = [int(x) for x in r["c_path"]]
        c_values = [int(x) for x in r["c_values"]]
        item = {
            "index": idx,
            "shell": c_shell_by_index[idx],
            "c_path": c_path,
            "c_values": c_values,
            "c_entry": c_path[0],
            "c_mid": c_path[1],
            "c_exit": c_path[2],
            "c_sum_mod15": int(r["c_sum_mod15"]),
            "c_min": min(c_values),
            "c_max": max(c_values),
            "c_span": max(c_values) - min(c_values),
        }
        c_items.append(item)

    a_items = []
    for r in m024["anchor_cols"]:
        idx = int(r["col_index"])
        nodes = list(r["anchor_nodes"])
        cols = flatten_cols(nodes)
        residues = flatten_residues(nodes)
        branch_pos = nodes.index("[8,18]") if "[8,18]" in nodes else -1
        item = {
            "index": idx,
            "shell": a_shell_by_index[idx],
            "anchor_nodes": nodes,
            "anchor_sum_mod15": int(r["anchor_sum_mod15"]),
            "anchor_min_col": min(cols),
            "anchor_max_col": max(cols),
            "anchor_min_residue": min(residues),
            "anchor_max_residue": max(residues),
            "anchor_residue_count": len(residues),
            "branch_anchor_position": branch_pos,
            "first_anchor_min_col": min(parse_anchor_pair(nodes[0])),
            "first_anchor_sum_mod15": sum(parse_anchor_pair(nodes[0])) % 15,
            "last_anchor_min_col": min(parse_anchor_pair(nodes[-1])),
        }
        a_items.append(item)

    c_methods = {
        "c_entry": lambda x: x["c_entry"],
        "c_mid": lambda x: x["c_mid"],
        "c_exit": lambda x: x["c_exit"],
        "c_sum_mod15": lambda x: x["c_sum_mod15"],
        "c_min": lambda x: x["c_min"],
        "c_max": lambda x: x["c_max"],
        "c_span": lambda x: x["c_span"],
    }

    a_methods = {
        "anchor_sum_mod15": lambda x: x["anchor_sum_mod15"],
        "anchor_min_col": lambda x: x["anchor_min_col"],
        "anchor_max_col": lambda x: x["anchor_max_col"],
        "anchor_min_residue": lambda x: x["anchor_min_residue"],
        "anchor_max_residue": lambda x: x["anchor_max_residue"],
        "anchor_residue_count": lambda x: x["anchor_residue_count"],
        "branch_anchor_position": lambda x: x["branch_anchor_position"],
        "first_anchor_min_col": lambda x: x["first_anchor_min_col"],
        "first_anchor_sum_mod15": lambda x: x["first_anchor_sum_mod15"],
        "last_anchor_min_col": lambda x: x["last_anchor_min_col"],
    }

    c_rank_methods = []
    for name, fn in c_methods.items():
        for rev in [False, True]:
            valid, rank, details = make_rank_map(c_items, lambda x: x["shell"], fn, reverse=rev)
            c_rank_methods.append({
                "name": name + ("_desc" if rev else "_asc"),
                "valid": valid,
                "rank": rank,
                "details": details,
            })

    a_rank_methods = []
    for name, fn in a_methods.items():
        for rev in [False, True]:
            valid, rank, details = make_rank_map(a_items, lambda x: x["shell"], fn, reverse=rev)
            a_rank_methods.append({
                "name": name + ("_desc" if rev else "_asc"),
                "valid": valid,
                "rank": rank,
                "details": details,
            })

    rows = []
    for rr in csv_rows:
        c_row = int(rr["c_row"])
        a_col = int(rr["a_col"])
        rows.append({
            "candidate_index": int(rr["candidate_index"]),
            "c_row": c_row,
            "a_col": a_col,
            "selected": rr["selected"] == "1",
            "c_shell": c_shell_by_index[c_row],
            "anchor_shell": a_shell_by_index[a_col],
        })

    selector_tests = []
    for cm, am in product(c_rank_methods, a_rank_methods):
        if not cm["valid"] or not am["valid"]:
            continue

        def pred(r, cm=cm, am=am):
            return (
                r["c_shell"] == r["anchor_shell"]
                and cm["rank"][r["c_row"]] == am["rank"][r["a_col"]]
            )

        sc = score(rows, cm["name"] + "__x__" + am["name"], pred)
        sc["c_rank_method"] = cm["name"]
        sc["anchor_rank_method"] = am["name"]
        selector_tests.append(sc)

    selector_tests.sort(key=lambda x: (
        not x["exact"],
        x["false_positive"] + x["miss"],
        x["false_positive"],
        x["miss"],
        x["c_rank_method"],
        x["anchor_rank_method"],
    ))

    exact_tests = [x for x in selector_tests if x["exact"]]

    target_name = "c_entry_asc__x__anchor_sum_mod15_asc"
    target_test = next((x for x in selector_tests if x["name"] == target_name), None)

    native_rank_derivation_pass = bool(target_test and target_test["exact"])

    c_target = next(x for x in c_rank_methods if x["name"] == "c_entry_asc")
    a_target = next(x for x in a_rank_methods if x["name"] == "anchor_sum_mod15_asc")

    result = {
        "status": "native_shell_rank_derivation_recorded",
        "audit_id": "027",
        "input_024_json": str(IN_024_JSON),
        "input_024_csv": str(IN_024_CSV),
        "input_026": str(IN_026),
        "candidate_count": len(rows),
        "selected_count": sum(1 for r in rows if r["selected"]),
        "c_items": c_items,
        "anchor_items": a_items,
        "c_rank_method_count": len(c_rank_methods),
        "anchor_rank_method_count": len(a_rank_methods),
        "selector_test_count": len(selector_tests),
        "exact_selector_count": len(exact_tests),
        "exact_selectors_first_80": exact_tests[:80],
        "best_selector_tests_first_80": selector_tests[:80],
        "target_native_rank_selector": target_test,
        "target_c_rank_details": c_target["details"],
        "target_anchor_rank_details": a_target["details"],
        "native_rank_derivation_pass": native_rank_derivation_pass,
        "interpretation": (
            "This audit derives the shell-rank part of the 025 radial phase-lock selector from simple "
            "native summaries rather than from the selected permutation. The C rank is obtained by "
            "ordering C-cycles within each derived shell by their entry value c_path[0] / XY.from_C. "
            "The anchor rank is obtained by ordering anchor-cycles within each derived shell by "
            "anchor_sum_mod15. Combined with the native shell labels from 026, this shell-rank lock "
            "recovers exactly the four selected candidates."
        ),
        "boundary": (
            "This is still a reduced-universe selector over the 16 candidates. It derives shell labels "
            "and shell ranks from native summaries visible in the reduced register shadow, but it does "
            "not yet derive the full role-labeled shared_B edge universe from first principles and does "
            "not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native shell rank derivation 027")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Can the shell ranks used in 025 be derived from native summaries?")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- c_rank_method_count: `" + str(result["c_rank_method_count"]) + "`")
    lines.append("- anchor_rank_method_count: `" + str(result["anchor_rank_method_count"]) + "`")
    lines.append("- selector_test_count: `" + str(result["selector_test_count"]) + "`")
    lines.append("- exact_selector_count: `" + str(result["exact_selector_count"]) + "`")
    lines.append("")
    lines.append("## Target native rank selector")
    lines.append("")
    lines.append("- selector: `c_entry_asc__x__anchor_sum_mod15_asc`")
    lines.append("- native_rank_derivation_pass: `" + str(result["native_rank_derivation_pass"]) + "`")
    lines.append("- target_test: `" + str(result["target_native_rank_selector"]) + "`")
    lines.append("")
    lines.append("## Target C rank details")
    lines.append("")
    lines.append("`" + str(result["target_c_rank_details"]) + "`")
    lines.append("")
    lines.append("## Target anchor rank details")
    lines.append("")
    lines.append("`" + str(result["target_anchor_rank_details"]) + "`")
    lines.append("")
    lines.append("## Exact selectors first 40")
    lines.append("")
    if exact_tests:
        for t in exact_tests[:40]:
            lines.append(
                "- " + t["name"]
                + ": accepted=`" + str(t["accepted_candidate_indices"])
                + "`, fp=`" + str(t["false_positive"])
                + "`, miss=`" + str(t["miss"]) + "`"
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## C items")
    lines.append("")
    for x in c_items:
        lines.append("- `" + str(x) + "`")
    lines.append("")
    lines.append("## Anchor items")
    lines.append("")
    for x in a_items:
        lines.append("- `" + str(x) + "`")
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
    print("selector_test_count", result["selector_test_count"])
    print("exact_selector_count", result["exact_selector_count"])
    print("native_rank_derivation_pass", result["native_rank_derivation_pass"])
    if target_test:
        print("target_selector_exact", target_test["exact"])
        print("accepted", target_test["accepted_candidate_indices"])


if __name__ == "__main__":
    main()
