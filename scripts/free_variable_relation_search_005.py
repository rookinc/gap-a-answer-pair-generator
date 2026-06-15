#!/usr/bin/env python3
import json
from pathlib import Path
from itertools import combinations, product
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]

IN_004 = ROOT / "artifacts/json/realized_free_variable_table_004.v1.json"

OUT_JSON = ROOT / "artifacts/json/free_variable_relation_search_005.v1.json"
OUT_NOTE = ROOT / "notes/free_variable_relation_search_005.md"

MOD = 15

FEATURE_FIELDS = [
    "role_pair",
    "c0",
    "c1",
    "shared",
    "reverse",
    "C_delta",
    "lift_q",
]

NUMERIC_FIELDS = [
    "c0",
    "c1",
    "C_delta",
    "lift_q",
]

TARGET_FIELDS = [
    "S_from_A",
    "S_B",
    "S_to_A",
    "R_A",
    "S_A_delta",
    "R_minus_S_from_A",
    "S_B_minus_c1",
]

ROLE_PAIR_INDEX = {
    "IW/YZ": 0,
    "TI/XY": 1,
    "WX/ZT": 2,
}

SHARED_INDEX = {
    "IW": 0,
    "XY": 1,
    "ZT": 2,
}

REVERSE_INDEX = {
    "YZ": 0,
    "TI": 1,
    "WX": 2,
}


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def enrich(rec):
    r = dict(rec)
    r["C_delta"] = (int(r["c1"]) - int(r["c0"])) % MOD
    r["integer_C_delta"] = int(r["c1"]) - int(r["c0"])
    r["lift_q"] = 0 if r["integer_C_delta"] >= 0 else 3
    r["role_pair_index"] = ROLE_PAIR_INDEX[r["role_pair"]]
    r["shared_index"] = SHARED_INDEX[r["shared"]]
    r["reverse_index"] = REVERSE_INDEX[r["reverse"]]
    r["c0_plus_c1"] = (int(r["c0"]) + int(r["c1"])) % MOD
    r["c1_minus_c0"] = r["C_delta"]
    return r


def key_value(row, keys):
    return tuple(row[k] for k in keys)


def deterministic_tests(records):
    tests = []
    for target in TARGET_FIELDS:
        for size in range(1, 5):
            for keys in combinations(FEATURE_FIELDS, size):
                groups = defaultdict(set)
                for row in records:
                    groups[key_value(row, keys)].add(row[target])

                ambiguous = {str(k): sorted(v) for k, v in groups.items() if len(v) > 1}
                exact = not ambiguous

                tests.append({
                    "target": target,
                    "keys": list(keys),
                    "exact": exact,
                    "group_count": len(groups),
                    "row_count": len(records),
                    "row_identity_like": len(groups) >= len(records),
                    "ambiguous_group_count": len(ambiguous),
                    "ambiguous_examples_first_10": dict(list(ambiguous.items())[:10]),
                })

    exact = [t for t in tests if t["exact"]]
    exact_sorted = sorted(
        exact,
        key=lambda t: (
            t["row_identity_like"],
            len(t["keys"]),
            t["group_count"],
            t["target"],
            ",".join(t["keys"]),
        ),
    )
    non_identity_exact = [t for t in exact_sorted if not t["row_identity_like"]]
    return tests, exact_sorted, non_identity_exact


def expr_text(terms, coeffs, const):
    parts = []
    for term, coeff in zip(terms, coeffs):
        coeff = coeff % MOD
        if coeff == 0:
            continue
        if coeff == 1:
            parts.append(term)
        else:
            parts.append(str(coeff) + "*" + term)
    if const:
        parts.append(str(const))
    if not parts:
        return "0 mod 15"
    return " + ".join(parts) + " mod 15"


def eval_affine(row, terms, coeffs, const):
    total = const
    for term, coeff in zip(terms, coeffs):
        total += coeff * int(row[term])
    return total % MOD


def affine_search(records, features, targets, max_terms=2):
    laws = []
    for target in targets:
        for term_count in range(1, max_terms + 1):
            for terms in combinations(features, term_count):
                for coeffs in product(range(MOD), repeat=term_count):
                    if all(c == 0 for c in coeffs):
                        continue
                    for const in range(MOD):
                        ok = True
                        for row in records:
                            if eval_affine(row, terms, coeffs, const) != int(row[target]) % MOD:
                                ok = False
                                break
                        if ok:
                            laws.append({
                                "target": target,
                                "terms": list(terms),
                                "coeffs": list(coeffs),
                                "const": const,
                                "expr": target + " = " + expr_text(terms, coeffs, const),
                                "term_count": term_count,
                                "nonzero_coeff_count": sum(1 for c in coeffs if c != 0),
                            })
            # keep minimal term-count laws only per target if any found at this size
            if any(l["target"] == target and l["term_count"] == term_count for l in laws):
                break

    return sorted(
        laws,
        key=lambda x: (
            x["target"],
            x["nonzero_coeff_count"],
            x["term_count"],
            sum(x["coeffs"]),
            x["const"],
            x["expr"],
        ),
    )


def role_specific_affine(records):
    role_results = {}
    for role_pair in sorted(set(r["role_pair"] for r in records)):
        xs = [r for r in records if r["role_pair"] == role_pair]
        laws = affine_search(xs, NUMERIC_FIELDS, TARGET_FIELDS, max_terms=2)
        role_results[role_pair] = {
            "row_count": len(xs),
            "laws_first_40": laws[:40],
            "law_count": len(laws),
        }
    return role_results


def pairwise_target_relations(records):
    relations = []
    for a, b in combinations(TARGET_FIELDS, 2):
        diff_counts = Counter((int(r[a]) - int(r[b])) % MOD for r in records)
        sum_counts = Counter((int(r[a]) + int(r[b])) % MOD for r in records)
        eq_count = sum(1 for r in records if int(r[a]) % MOD == int(r[b]) % MOD)

        relations.append({
            "a": a,
            "b": b,
            "equal_count": eq_count,
            "row_count": len(records),
            "diff_counts": dict(sorted(diff_counts.items())),
            "sum_counts": dict(sorted(sum_counts.items())),
            "constant_diff": len(diff_counts) == 1,
            "constant_sum": len(sum_counts) == 1,
        })

    return sorted(
        relations,
        key=lambda x: (
            -x["equal_count"],
            not x["constant_diff"],
            not x["constant_sum"],
            x["a"],
            x["b"],
        ),
    )


def main():
    data = load(IN_004)
    records = [enrich(r) for r in data["records"]]

    tests, exact_tests, non_identity_exact = deterministic_tests(records)

    global_affine = affine_search(
        records,
        NUMERIC_FIELDS,
        TARGET_FIELDS,
        max_terms=2,
    )

    role_coded_affine = affine_search(
        records,
        NUMERIC_FIELDS + ["role_pair_index", "shared_index", "reverse_index"],
        TARGET_FIELDS,
        max_terms=2,
    )

    role_specific = role_specific_affine(records)
    pairwise = pairwise_target_relations(records)

    result = {
        "status": "free_variable_relation_search_recorded",
        "audit_id": "005",
        "input_004": str(IN_004),
        "record_count": len(records),
        "feature_fields": FEATURE_FIELDS,
        "numeric_fields": NUMERIC_FIELDS,
        "target_fields": TARGET_FIELDS,
        "deterministic_test_count": len(tests),
        "exact_deterministic_test_count": len(exact_tests),
        "non_identity_exact_deterministic_test_count": len(non_identity_exact),
        "non_identity_exact_deterministic_tests_first_50": non_identity_exact[:50],
        "global_affine_law_count": len(global_affine),
        "global_affine_laws_first_50": global_affine[:50],
        "role_coded_affine_law_count": len(role_coded_affine),
        "role_coded_affine_laws_first_50": role_coded_affine[:50],
        "role_specific_affine": role_specific,
        "pairwise_target_relations_first_50": pairwise[:50],
        "interpretation": (
            "This searches for low-complexity relations in the realized free-variable table. "
            "It is intended to identify whether the missing A/B assignment law is already visible "
            "from c0, c1, C_delta, lift_q, and role-channel labels, or whether additional native "
            "structure is required."
        ),
        "boundary": (
            "This is a descriptive relation search over realized selected pairs. Exact relations here "
            "may be overfit. This is not a native generator and not Gap A closure."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Free-variable relation search 005")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("- record_count: `" + str(result["record_count"]) + "`")
    lines.append("- deterministic_test_count: `" + str(result["deterministic_test_count"]) + "`")
    lines.append("- exact_deterministic_test_count: `" + str(result["exact_deterministic_test_count"]) + "`")
    lines.append("- non_identity_exact_deterministic_test_count: `" + str(result["non_identity_exact_deterministic_test_count"]) + "`")
    lines.append("- global_affine_law_count: `" + str(result["global_affine_law_count"]) + "`")
    lines.append("- role_coded_affine_law_count: `" + str(result["role_coded_affine_law_count"]) + "`")
    lines.append("")
    lines.append("## Non-identity exact deterministic tests")
    lines.append("")
    if non_identity_exact:
        for t in non_identity_exact[:25]:
            lines.append(
                "- target=" + t["target"]
                + ", keys=" + str(t["keys"])
                + ", groups=" + str(t["group_count"])
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Global affine laws")
    lines.append("")
    if global_affine:
        for law in global_affine[:25]:
            lines.append("- " + law["expr"])
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Role-coded affine laws")
    lines.append("")
    if role_coded_affine:
        for law in role_coded_affine[:25]:
            lines.append("- " + law["expr"])
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Role-specific affine laws")
    lines.append("")
    for role_pair, rr in role_specific.items():
        lines.append("- " + role_pair + ": laws=" + str(rr["law_count"]))
        if rr["laws_first_40"]:
            for law in rr["laws_first_40"][:10]:
                lines.append("  - " + law["expr"])
        else:
            lines.append("  - none")
    lines.append("")
    lines.append("## Pairwise target relations")
    lines.append("")
    for rel in pairwise[:20]:
        lines.append(
            "- " + rel["a"] + " vs " + rel["b"]
            + ": equal=" + str(rel["equal_count"]) + "/" + str(rel["row_count"])
            + ", constant_diff=" + str(rel["constant_diff"])
            + ", constant_sum=" + str(rel["constant_sum"])
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
    print("record_count", result["record_count"])
    print("non_identity_exact_deterministic_test_count", result["non_identity_exact_deterministic_test_count"])
    print("global_affine_law_count", result["global_affine_law_count"])
    print("role_coded_affine_law_count", result["role_coded_affine_law_count"])
    print("role_specific_law_counts", {k: v["law_count"] for k, v in role_specific.items()})


if __name__ == "__main__":
    main()
