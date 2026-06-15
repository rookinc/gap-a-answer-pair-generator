#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

IN_G60 = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"

OUT_JSON = ROOT / "artifacts/json/g60_overlay_generator_family_reading_015.v1.json"
OUT_NOTE = ROOT / "notes/g60_overlay_generator_family_reading_015.md"


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def scalar(x):
    return x is None or isinstance(x, (str, int, float, bool))


def count_like(x):
    if x is None:
        return 0
    if isinstance(x, bool):
        return int(x)
    if isinstance(x, int):
        return x
    if isinstance(x, (list, tuple, set)):
        return len(x)
    if isinstance(x, dict):
        total = 0
        for v in x.values():
            total += count_like(v)
        return total
    return 0


def compact_candidate(c):
    matched_edges = count_like(c.get("matched_edges"))
    matched_by_label = c.get("matched_by_label", {})
    missed_by_label = c.get("missed_by_label", {})

    return {
        "candidate": c.get("candidate"),
        "exact_all": bool(c.get("exact_all")),
        "exact_reverse_partner": bool(c.get("exact_reverse_partner")),
        "exact_shared_B": bool(c.get("exact_shared_B")),
        "is_permutation": bool(c.get("is_permutation")),
        "matched_edges_count": matched_edges,
        "matched_by_label": matched_by_label,
        "missed_by_label": missed_by_label,
        "missed_total": count_like(missed_by_label),
        "raw_keys": sorted(c.keys()),
    }


def main():
    data = load(IN_G60)

    edge_records = data.get("edge_records", [])
    candidate_results = data.get("candidate_results", [])
    two_map_exact_hits = data.get("two_map_exact_hits", [])
    checks = data.get("checks", [])

    compact_candidates = [compact_candidate(c) for c in candidate_results]
    ranked_candidates = sorted(
        compact_candidates,
        key=lambda c: (
            not c["exact_all"],
            -c["matched_edges_count"],
            c["missed_total"],
            str(c["candidate"]),
        ),
    )

    exact_all = [c for c in compact_candidates if c["exact_all"]]
    exact_reverse = [c for c in compact_candidates if c["exact_reverse_partner"]]
    exact_shared = [c for c in compact_candidates if c["exact_shared_B"]]
    permutations = [c for c in compact_candidates if c["is_permutation"]]

    edge_role_counts = Counter(str(e.get("edge_role")) for e in edge_records)
    label_counts = Counter(str(e.get("label")) for e in edge_records)
    form_counts = Counter(str(e.get("form_index")) for e in edge_records)

    from_key_counts = Counter(str(e.get("from_key")) for e in edge_records if "from_key" in e)
    to_key_counts = Counter(str(e.get("to_key")) for e in edge_records if "to_key" in e)

    check_status_counts = Counter(str(c.get("status")) for c in checks if isinstance(c, dict))

    result = {
        "status": "g60_overlay_generator_family_reading_recorded",
        "audit_id": "015",
        "input_g60_overlay": str(IN_G60),
        "top_keys": sorted(data.keys()) if isinstance(data, dict) else [],
        "edge_record_count": len(edge_records),
        "edge_role_counts": dict(sorted(edge_role_counts.items())),
        "label_counts": dict(sorted(label_counts.items())),
        "form_counts": dict(sorted(form_counts.items())),
        "distinct_from_key_count": len(from_key_counts),
        "distinct_to_key_count": len(to_key_counts),
        "candidate_result_count": len(candidate_results),
        "exact_all_candidate_count": len(exact_all),
        "exact_reverse_partner_candidate_count": len(exact_reverse),
        "exact_shared_B_candidate_count": len(exact_shared),
        "permutation_candidate_count": len(permutations),
        "two_map_exact_hit_count": count_like(two_map_exact_hits),
        "checks_count": len(checks),
        "check_status_counts": dict(sorted(check_status_counts.items())),
        "ranked_candidates": ranked_candidates,
        "two_map_exact_hits_first_20": two_map_exact_hits[:20] if isinstance(two_map_exact_hits, list) else two_map_exact_hits,
        "checks": checks,
        "summary": data.get("summary"),
        "schema": data.get("schema"),
        "purpose": data.get("purpose"),
        "boundary_from_source": data.get("boundary"),
        "interpretation": (
            "This audit reads the earlier G60 native overlay generator-family search. It records "
            "which candidate families were tested, which partial matches were found, whether any "
            "candidate already gave an exact all-edge generator, and what remains open. This is meant "
            "to prevent Project 21 from repeating a generator family that Project 18 already tested."
        ),
        "boundary": (
            "This is a reading and triage audit over an imported search artifact. It does not derive "
            "the G60 overlay edge records and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# G60 overlay generator family reading 015")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Input")
    lines.append("")
    lines.append("- G60 overlay artifact: `" + str(IN_G60) + "`")
    lines.append("")
    lines.append("## Edge records")
    lines.append("")
    lines.append("- edge_record_count: `" + str(result["edge_record_count"]) + "`")
    lines.append("- edge_role_counts: `" + str(result["edge_role_counts"]) + "`")
    lines.append("- label_counts: `" + str(result["label_counts"]) + "`")
    lines.append("- form_counts: `" + str(result["form_counts"]) + "`")
    lines.append("- distinct_from_key_count: `" + str(result["distinct_from_key_count"]) + "`")
    lines.append("- distinct_to_key_count: `" + str(result["distinct_to_key_count"]) + "`")
    lines.append("")
    lines.append("## Candidate-family search")
    lines.append("")
    lines.append("- candidate_result_count: `" + str(result["candidate_result_count"]) + "`")
    lines.append("- exact_all_candidate_count: `" + str(result["exact_all_candidate_count"]) + "`")
    lines.append("- exact_reverse_partner_candidate_count: `" + str(result["exact_reverse_partner_candidate_count"]) + "`")
    lines.append("- exact_shared_B_candidate_count: `" + str(result["exact_shared_B_candidate_count"]) + "`")
    lines.append("- permutation_candidate_count: `" + str(result["permutation_candidate_count"]) + "`")
    lines.append("- two_map_exact_hit_count: `" + str(result["two_map_exact_hit_count"]) + "`")
    lines.append("- checks_count: `" + str(result["checks_count"]) + "`")
    lines.append("- check_status_counts: `" + str(result["check_status_counts"]) + "`")
    lines.append("")
    lines.append("## Ranked candidates")
    lines.append("")
    if ranked_candidates:
        for c in ranked_candidates[:20]:
            lines.append("- candidate: `" + str(c["candidate"]) + "`")
            lines.append("  - exact_all: `" + str(c["exact_all"]) + "`")
            lines.append("  - exact_reverse_partner: `" + str(c["exact_reverse_partner"]) + "`")
            lines.append("  - exact_shared_B: `" + str(c["exact_shared_B"]) + "`")
            lines.append("  - is_permutation: `" + str(c["is_permutation"]) + "`")
            lines.append("  - matched_edges_count: `" + str(c["matched_edges_count"]) + "`")
            lines.append("  - missed_total: `" + str(c["missed_total"]) + "`")
            lines.append("  - matched_by_label: `" + str(c["matched_by_label"]) + "`")
            lines.append("  - missed_by_label: `" + str(c["missed_by_label"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Source summary")
    lines.append("")
    lines.append("```text")
    lines.append(str(result["summary"]))
    lines.append("```")
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
    print("edge_record_count", result["edge_record_count"])
    print("candidate_result_count", result["candidate_result_count"])
    print("exact_all_candidate_count", result["exact_all_candidate_count"])
    print("exact_reverse_partner_candidate_count", result["exact_reverse_partner_candidate_count"])
    print("exact_shared_B_candidate_count", result["exact_shared_B_candidate_count"])
    print("two_map_exact_hit_count", result["two_map_exact_hit_count"])


if __name__ == "__main__":
    main()
