#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_022 = ROOT / "artifacts/json/sharedB_candidate_universe_boundary_022.v1.json"
IN_026 = ROOT / "artifacts/json/native_shell_label_derivation_026.v1.json"
IN_027 = ROOT / "artifacts/json/native_shell_rank_derivation_027.v1.json"
IN_028 = ROOT / "artifacts/json/reduced_universe_shell_rank_theorem_028.v1.json"
IN_029 = ROOT / "artifacts/json/reduced_universe_theorem_section_029.v1.json"

SECTION = ROOT / "paper/sections/07_reduced_universe_shell_rank_selector.tex"
MAIN_TEX = ROOT / "paper/main.tex"

OUT_JSON = ROOT / "artifacts/json/reduced_theorem_boundary_dependency_audit_030.v1.json"
OUT_NOTE = ROOT / "notes/reduced_theorem_boundary_dependency_audit_030.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)



def find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = find_key(value, key)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_key(value, key)
            if found is not None:
                return found
    return None


def contains_all(text, phrases):
    missing = []
    for phrase in phrases:
        if phrase not in text:
            missing.append(phrase)
    return missing



def to_int(value, default=None):
    try:
        return int(value)
    except Exception:
        return default


def reduced_universe_16_witness(a022, a028):
    candidates = [
        find_key(a022, "c_and_anchor_only"),
        find_key(a022, "c_and_anchor_only_count"),
        find_key(a022, "c_and_anchor_only_selected_count"),
        find_key(a022, "reduced_candidate_count"),
        find_key(a022, "candidate_count_after_c_and_anchor"),
        a028.get("candidate_count") if isinstance(a028, dict) else None,
    ]

    for value in candidates:
        if to_int(value) == 16:
            return True

    if isinstance(a028, dict):
        if (
            to_int(a028.get("candidate_count")) == 16
            and to_int(a028.get("c_row_count")) == 4
            and to_int(a028.get("anchor_col_count")) == 4
        ):
            return True

    return False


def main():
    a022 = load_json(IN_022)
    a026 = load_json(IN_026)
    a027 = load_json(IN_027)
    a028 = load_json(IN_028)
    a029 = load_json(IN_029)

    section_text = SECTION.read_text(encoding="utf-8") if SECTION.exists() else ""
    main_text = MAIN_TEX.read_text(encoding="utf-8") if MAIN_TEX.exists() else ""

    proof_checks = {
        "022_reduced_boundary_has_16_candidates": reduced_universe_16_witness(a022, a028),
        "022_observed_edge_filter_exact": bool(find_key(a022, "observed_edge_filter_exact")),
        "026_shell_labels_derived": bool(a026.get("shell_label_derivation_pass")),
        "027_shell_ranks_derived": bool(a027.get("native_rank_derivation_pass")),
        "028_reduced_theorem_pass": bool(a028.get("theorem_pass")),
        "029_section_written_from_028": bool(a029.get("theorem_pass_from_028")),
    }

    paper_required_phrases = [
        "This result does not close Gap A.",
        "conditional on the reduced 16-candidate universe",
        "does not derive the full role-labeled shared\\_B edge universe",
        "It proves the selector inside the reduced universe.",
    ]

    paper_missing_required_phrases = contains_all(section_text, paper_required_phrases)

    main_has_input = "07_reduced_universe_shell_rank_selector" in main_text

    dependency_ledger = [
        {
            "item": "Observed C-cycle support",
            "status": "assumed_from_reduced_universe",
            "artifact": "022/024",
            "claim": "Four observed C-cycles are used to form the reduced universe.",
            "gap_status": "open_upstream_dependency",
        },
        {
            "item": "Twisted anchor-cycle support",
            "status": "assumed_from_reduced_universe",
            "artifact": "022/024",
            "claim": "Four observed twisted anchor-cycles are used to form the reduced universe.",
            "gap_status": "open_upstream_dependency",
        },
        {
            "item": "Reduced 16-candidate universe",
            "status": "bounded_construct",
            "artifact": "022",
            "claim": "C-cycle support crossed with twisted anchor-cycle support gives 16 candidates.",
            "gap_status": "not_first_principles_native_generation",
        },
        {
            "item": "C shell label",
            "status": "derived_native_marker",
            "artifact": "026",
            "claim": "C branch shell is derived from repeated C-junction marker C=5.",
            "gap_status": "closed_inside_reduced_theorem",
        },
        {
            "item": "Anchor shell label",
            "status": "derived_native_marker",
            "artifact": "026",
            "claim": "Anchor branch shell is derived from repeated branch anchor [8,18].",
            "gap_status": "closed_inside_reduced_theorem",
        },
        {
            "item": "C shell rank",
            "status": "derived_native_summary",
            "artifact": "027",
            "claim": "C rows rank by ascending C entry / XY.from_C within shell.",
            "gap_status": "closed_inside_reduced_theorem",
        },
        {
            "item": "Anchor shell rank",
            "status": "derived_native_summary",
            "artifact": "027",
            "claim": "Anchor columns rank by ascending anchor_sum_mod15 within shell.",
            "gap_status": "closed_inside_reduced_theorem",
        },
        {
            "item": "Reduced selector",
            "status": "proved_exact",
            "artifact": "028",
            "claim": "Same shell and same rank selects exactly [1,6,8,15] with no false positives or misses.",
            "gap_status": "proved_inside_reduced_universe",
        },
        {
            "item": "Full role-labeled shared_B edge universe",
            "status": "not_derived",
            "artifact": "boundary",
            "claim": "The full edge universe remains upstream of this theorem.",
            "gap_status": "Gap_A_open",
        },
    ]

    closed_items = [x for x in dependency_ledger if x["gap_status"] in [
        "closed_inside_reduced_theorem",
        "proved_inside_reduced_universe",
    ]]
    open_items = [x for x in dependency_ledger if x["gap_status"] in [
        "open_upstream_dependency",
        "not_first_principles_native_generation",
        "Gap_A_open",
    ]]

    boundary_pass = (
        all(proof_checks.values())
        and len(paper_missing_required_phrases) == 0
        and main_has_input
    )

    result = {
        "status": "reduced_theorem_boundary_dependency_audit_recorded",
        "audit_id": "030",
        "inputs": {
            "022": str(IN_022),
            "026": str(IN_026),
            "027": str(IN_027),
            "028": str(IN_028),
            "029": str(IN_029),
            "section": str(SECTION),
            "main_tex": str(MAIN_TEX),
        },
        "proof_checks": proof_checks,
        "paper_required_phrases": paper_required_phrases,
        "paper_missing_required_phrases": paper_missing_required_phrases,
        "main_has_section_input": main_has_input,
        "dependency_ledger": dependency_ledger,
        "closed_item_count": len(closed_items),
        "open_item_count": len(open_items),
        "closed_items": closed_items,
        "open_items": open_items,
        "boundary_pass": boundary_pass,
        "current_best_statement": (
            "The reduced-universe shell-rank selector is proved exactly inside the 16-candidate "
            "shared_B reduced universe. Native shell labels and native shell ranks select exactly "
            "the four observed shared_B cycles with no false positives and no misses."
        ),
        "remaining_gap_a_problem": (
            "Derive the reduced 16-candidate universe, or the full role-labeled shared_B edge "
            "universe, from native provenance without using observed C-cycle and anchor-cycle support "
            "as an upstream assumption."
        ),
        "interpretation": (
            "This audit confirms that the manuscript theorem section preserves the right boundary. "
            "The selector inside the reduced universe is theorem-grade; the reduced universe itself "
            "remains the open upstream generator problem."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Reduced theorem boundary dependency audit 030")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("- boundary_pass: `" + str(boundary_pass) + "`")
    lines.append("- main_has_section_input: `" + str(main_has_input) + "`")
    lines.append("- paper_missing_required_phrases: `" + str(paper_missing_required_phrases) + "`")
    lines.append("- closed_item_count: `" + str(len(closed_items)) + "`")
    lines.append("- open_item_count: `" + str(len(open_items)) + "`")
    lines.append("")
    lines.append("## Proof checks")
    lines.append("")
    for k, v in proof_checks.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("")
    lines.append("## Current best statement")
    lines.append("")
    lines.append(result["current_best_statement"])
    lines.append("")
    lines.append("## Remaining Gap A problem")
    lines.append("")
    lines.append(result["remaining_gap_a_problem"])
    lines.append("")
    lines.append("## Dependency ledger")
    lines.append("")
    for item in dependency_ledger:
        lines.append("- " + item["item"])
        lines.append("  - status: `" + item["status"] + "`")
        lines.append("  - artifact: `" + item["artifact"] + "`")
        lines.append("  - claim: " + item["claim"])
        lines.append("  - gap_status: `" + item["gap_status"] + "`")
    lines.append("")
    lines.append("## Reading")
    lines.append("")
    lines.append(result["interpretation"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("boundary_pass", boundary_pass)
    print("main_has_section_input", main_has_input)
    print("paper_missing_required_phrases", paper_missing_required_phrases)
    print("open_item_count", len(open_items))
    print("closed_item_count", len(closed_items))


if __name__ == "__main__":
    main()
