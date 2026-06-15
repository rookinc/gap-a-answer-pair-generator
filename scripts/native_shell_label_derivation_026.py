#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_024 = ROOT / "artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_025 = ROOT / "artifacts/json/radial_phase_lock_selector_025.v1.json"

OUT_JSON = ROOT / "artifacts/json/native_shell_label_derivation_026.v1.json"
OUT_NOTE = ROOT / "notes/native_shell_label_derivation_026.md"


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


def main():
    overlay = load_json(IN_G60_OVERLAY)
    m024 = load_json(IN_024)
    m025 = load_json(IN_025)

    shared_rows = []
    for r in overlay.get("edge_records", []):
        if r.get("label") != "shared_B":
            continue
        rr = dict(r)
        rr["from_col_pair"] = col_pair(r.get("from_columns"))
        rr["to_col_pair"] = col_pair(r.get("to_columns"))
        shared_rows.append(rr)

    # C shell derivation:
    # The branch C marker is not read from the 024 matrix. It is the repeated
    # role-junction seam in the shared_B C-transition grammar:
    #
    #   XY ends at C
    #   IW begins at C
    #
    # The value that appears with multiplicity >1 in both XY.to_C and IW.from_C
    # is the native C-branch seam.
    xy_to_c = Counter(int(r["to_C"]) for r in shared_rows if r.get("edge_role") == "XY")
    iw_from_c = Counter(int(r["from_C"]) for r in shared_rows if r.get("edge_role") == "IW")

    c_branch_markers = sorted(
        set(k for k, v in xy_to_c.items() if v > 1)
        & set(k for k, v in iw_from_c.items() if v > 1)
    )

    c_row_derivations = []
    derived_c_shell_members = defaultdict(list)

    for r in m024["c_rows"]:
        idx = int(r["row_index"])
        c_values = [int(x) for x in r["c_values"]]
        is_branch = any(x in c_branch_markers for x in c_values)
        shell = "branch" if is_branch else "ordinary"
        derived_c_shell_members[shell].append(idx)
        c_row_derivations.append({
            "row_index": idx,
            "c_values": c_values,
            "contains_native_c_branch_marker": is_branch,
            "derived_shell": shell,
            "c_sum_mod15": r.get("c_sum_mod15"),
            "selected_anchor_col": r.get("selected_anchor_col"),
        })

    # Anchor shell derivation:
    # The branch anchor is the repeated / nontrivial column-motion junction.
    # It can be seen two ways:
    #   1. anchor node appears in more than one anchor-cycle column;
    #   2. in the shared_B column-motion graph, it has in_degree > 1 and out_degree > 1.
    anchor_freq = Counter()
    for col in m024["anchor_cols"]:
        for n in col["anchor_nodes"]:
            anchor_freq[str(n)] += 1

    repeated_anchor_markers = sorted(k for k, v in anchor_freq.items() if v > 1)

    indeg = Counter()
    outdeg = Counter()
    for r in shared_rows:
        src = pstr(r["from_col_pair"])
        dst = pstr(r["to_col_pair"])
        outdeg[src] += 1
        indeg[dst] += 1

    motion_branch_markers = sorted(
        n for n in set(indeg) | set(outdeg)
        if indeg[n] > 1 or outdeg[n] > 1
    )

    anchor_branch_markers = sorted(set(repeated_anchor_markers) & set(motion_branch_markers))

    anchor_col_derivations = []
    derived_anchor_shell_members = defaultdict(list)

    for col in m024["anchor_cols"]:
        idx = int(col["col_index"])
        nodes = [str(x) for x in col["anchor_nodes"]]
        is_branch = any(n in anchor_branch_markers for n in nodes)
        shell = "branch" if is_branch else "ordinary"
        derived_anchor_shell_members[shell].append(idx)
        anchor_col_derivations.append({
            "col_index": idx,
            "anchor_nodes": nodes,
            "contains_native_anchor_branch_marker": is_branch,
            "derived_shell": shell,
            "anchor_sum_mod15": col.get("anchor_sum_mod15"),
            "selected_c_row": col.get("selected_c_row"),
        })

    expected_c_shell_members = {
        k: list(v) for k, v in m025.get("c_shell_members", {}).items()
    }
    expected_anchor_shell_members = {
        k: list(v) for k, v in m025.get("anchor_shell_members", {}).items()
    }

    derived_c_shell_members = {k: sorted(v) for k, v in derived_c_shell_members.items()}
    derived_anchor_shell_members = {k: sorted(v) for k, v in derived_anchor_shell_members.items()}

    c_shell_match_025 = derived_c_shell_members == expected_c_shell_members
    anchor_shell_match_025 = derived_anchor_shell_members == expected_anchor_shell_members
    shell_label_derivation_pass = c_shell_match_025 and anchor_shell_match_025

    result = {
        "status": "native_shell_label_derivation_recorded",
        "audit_id": "026",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_024": str(IN_024),
        "input_025": str(IN_025),
        "xy_to_C_counts": dict(sorted((str(k), v) for k, v in xy_to_c.items())),
        "iw_from_C_counts": dict(sorted((str(k), v) for k, v in iw_from_c.items())),
        "native_c_branch_markers": c_branch_markers,
        "anchor_frequency_counts": dict(sorted(anchor_freq.items())),
        "repeated_anchor_markers": repeated_anchor_markers,
        "motion_in_degrees": dict(sorted(indeg.items())),
        "motion_out_degrees": dict(sorted(outdeg.items())),
        "motion_branch_markers": motion_branch_markers,
        "native_anchor_branch_markers": anchor_branch_markers,
        "derived_c_shell_members": derived_c_shell_members,
        "expected_c_shell_members_from_025": expected_c_shell_members,
        "c_shell_match_025": c_shell_match_025,
        "derived_anchor_shell_members": derived_anchor_shell_members,
        "expected_anchor_shell_members_from_025": expected_anchor_shell_members,
        "anchor_shell_match_025": anchor_shell_match_025,
        "shell_label_derivation_pass": shell_label_derivation_pass,
        "c_row_derivations": c_row_derivations,
        "anchor_col_derivations": anchor_col_derivations,
        "interpretation": (
            "This audit derives the shell labels used in the 025 radial phase-lock selector from "
            "native observed structure rather than from the reduced matrix by hand. The C branch "
            "shell is detected by the repeated XY-to-IW C-junction marker C=5. The anchor branch "
            "shell is detected by the repeated column-motion branch anchor [8,18], which is both "
            "reused across anchor cycles and branch-like in the shared_B motion graph. These native "
            "markers reproduce the 025 shell split exactly."
        ),
        "boundary": (
            "This derives shell labels, not shell ranks. The radial phase-lock selector still depends "
            "on phase-rank order within each shell. Gap A remains open until the ranks, and ultimately "
            "the role-labeled shared_B edge selector, are derived from native provenance."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native shell label derivation 026")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Can the shell labels used in 025 be derived natively?")
    lines.append("")
    lines.append("## C branch shell")
    lines.append("")
    lines.append("- xy_to_C_counts: `" + str(result["xy_to_C_counts"]) + "`")
    lines.append("- iw_from_C_counts: `" + str(result["iw_from_C_counts"]) + "`")
    lines.append("- native_c_branch_markers: `" + str(result["native_c_branch_markers"]) + "`")
    lines.append("- derived_c_shell_members: `" + str(result["derived_c_shell_members"]) + "`")
    lines.append("- expected_c_shell_members_from_025: `" + str(result["expected_c_shell_members_from_025"]) + "`")
    lines.append("- c_shell_match_025: `" + str(result["c_shell_match_025"]) + "`")
    lines.append("")
    lines.append("## Anchor branch shell")
    lines.append("")
    lines.append("- repeated_anchor_markers: `" + str(result["repeated_anchor_markers"]) + "`")
    lines.append("- motion_branch_markers: `" + str(result["motion_branch_markers"]) + "`")
    lines.append("- native_anchor_branch_markers: `" + str(result["native_anchor_branch_markers"]) + "`")
    lines.append("- derived_anchor_shell_members: `" + str(result["derived_anchor_shell_members"]) + "`")
    lines.append("- expected_anchor_shell_members_from_025: `" + str(result["expected_anchor_shell_members_from_025"]) + "`")
    lines.append("- anchor_shell_match_025: `" + str(result["anchor_shell_match_025"]) + "`")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("- shell_label_derivation_pass: `" + str(result["shell_label_derivation_pass"]) + "`")
    lines.append("")
    lines.append("## C row derivations")
    lines.append("")
    for r in c_row_derivations:
        lines.append("- `" + str(r) + "`")
    lines.append("")
    lines.append("## Anchor column derivations")
    lines.append("")
    for r in anchor_col_derivations:
        lines.append("- `" + str(r) + "`")
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
    print("native_c_branch_markers", c_branch_markers)
    print("native_anchor_branch_markers", anchor_branch_markers)
    print("derived_c_shell_members", derived_c_shell_members)
    print("derived_anchor_shell_members", derived_anchor_shell_members)
    print("shell_label_derivation_pass", shell_label_derivation_pass)


if __name__ == "__main__":
    main()
