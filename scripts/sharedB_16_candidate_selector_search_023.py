#!/usr/bin/env python3
import itertools
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
IN_022 = ROOT / "artifacts/json/sharedB_candidate_universe_boundary_022.v1.json"

OUT_JSON = ROOT / "artifacts/json/sharedB_16_candidate_selector_search_023.v1.json"
OUT_NOTE = ROOT / "notes/sharedB_16_candidate_selector_search_023.md"

ROLE_PAIR_BY_EDGE_ROLE = {
    "IW": "IW/YZ",
    "YZ": "IW/YZ",
    "TI": "TI/XY",
    "XY": "TI/XY",
    "WX": "WX/ZT",
    "ZT": "WX/ZT",
}

BLOCKS = {
    "A": [0, 2, 10, 14],
    "B": [2, 4, 11, 13],
    "C": [1, 2, 5],
}

ROLE_ORDER = ["XY", "IW", "ZT"]

ROLE_TO_REVERSE_ROLE = {
    "XY": "TI",
    "IW": "YZ",
    "ZT": "WX",
}


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


def residues(p):
    return tuple(sorted(x % 15 for x in p))


def cycle_key(cyc):
    return tuple((role, c0, c1, pstr(src), pstr(dst)) for role, c0, c1, src, dst in cyc)


def c_key(cyc):
    return tuple((role, c0, c1) for role, c0, c1 in cyc)


def a_key(cyc):
    return tuple((role, pstr(src), pstr(dst)) for role, src, dst in cyc)


def parse_observed_cycles_from_022(data):
    out = []
    for item in data.get("observed_cycles", []):
        exact = item.get("exact_cycle", [])
        cyc = []
        for role, c0, c1, src, dst in exact:
            cyc.append((role, int(c0), int(c1), col_pair(src), col_pair(dst)))
        out.append(tuple(cyc))
    return sorted(out, key=cycle_key)


def anchor_cycle_from_observed(cyc):
    return tuple((role, src, dst) for role, _c0, _c1, src, dst in cyc)


def c_cycle_from_observed(cyc):
    return tuple((role, c0, c1) for role, c0, c1, _src, _dst in cyc)


def build_reverse_anchor_info(reverse_rows):
    info = defaultdict(list)
    for r in reverse_rows:
        fp = col_pair(r.get("from_columns"))
        tp = col_pair(r.get("to_columns"))
        info[fp].append({
            "edge_role": r.get("edge_role"),
            "role_pair": ROLE_PAIR_BY_EDGE_ROLE.get(str(r.get("edge_role"))),
            "from_C": int(r.get("from_C")),
            "to_C": int(r.get("to_C")),
            "transition": [int(r.get("from_C")), int(r.get("to_C"))],
            "from_A": int(r.get("from_A")),
            "from_B": int(r.get("from_B")),
            "to_A": int(r.get("to_A")),
            "to_B": int(r.get("to_B")),
            "to_columns_same": fp == tp,
        })
    return info


def anchor_summary(anchor, reverse_info):
    infos = reverse_info.get(anchor, [])
    roles = sorted(set(str(x["edge_role"]) for x in infos))
    from_cs = sorted(set(int(x["from_C"]) for x in infos))
    to_cs = sorted(set(int(x["to_C"]) for x in infos))
    trans = sorted(set((int(x["from_C"]), int(x["to_C"])) for x in infos))
    vals = list(anchor)
    return {
        "anchor": pstr(anchor),
        "cols": vals,
        "residues": list(residues(anchor)),
        "sum": sum(vals),
        "sum_mod15": sum(vals) % 15,
        "diff": abs(vals[1] - vals[0]) if len(vals) == 2 else None,
        "diff_mod15": abs(vals[1] - vals[0]) % 15 if len(vals) == 2 else None,
        "min": min(vals) if vals else None,
        "max": max(vals) if vals else None,
        "min_mod15": min(vals) % 15 if vals else None,
        "max_mod15": max(vals) % 15 if vals else None,
        "reverse_roles": roles,
        "reverse_from_Cs": from_cs,
        "reverse_to_Cs": to_cs,
        "reverse_transitions": trans,
        "reverse_info_count": len(infos),
    }


def candidate_features(cyc, reverse_info):
    # cyc is ordered as XY, IW, ZT with twisted column closure already attached.
    d = {}

    cvals = []
    anchors = []
    for role, c0, c1, src, dst in cyc:
        cvals.extend([c0, c1])
        anchors.extend([src, dst])

        ss = anchor_summary(src, reverse_info)
        ds = anchor_summary(dst, reverse_info)

        prefix = role
        d[prefix + "_c0"] = c0
        d[prefix + "_c1"] = c1
        d[prefix + "_c_delta"] = (c1 - c0) % 15

        for side, summ in [("src", ss), ("dst", ds)]:
            p = prefix + "_" + side + "_"
            d[p + "anchor"] = summ["anchor"]
            d[p + "residues"] = tuple(summ["residues"])
            d[p + "sum_mod15"] = summ["sum_mod15"]
            d[p + "diff_mod15"] = summ["diff_mod15"]
            d[p + "min_mod15"] = summ["min_mod15"]
            d[p + "max_mod15"] = summ["max_mod15"]
            d[p + "reverse_roles"] = tuple(summ["reverse_roles"])
            d[p + "reverse_from_Cs"] = tuple(summ["reverse_from_Cs"])
            d[p + "reverse_to_Cs"] = tuple(summ["reverse_to_Cs"])
            d[p + "reverse_transitions"] = tuple(summ["reverse_transitions"])
            d[p + "has_c0_residue"] = c0 in summ["residues"]
            d[p + "has_c1_residue"] = c1 in summ["residues"]
            d[p + "has_c0_column"] = c0 in src if side == "src" else c0 in dst
            d[p + "has_c1_column"] = c1 in src if side == "src" else c1 in dst
            d[p + "reverse_has_c0_from"] = c0 in summ["reverse_from_Cs"]
            d[p + "reverse_has_c1_to"] = c1 in summ["reverse_to_Cs"]
            d[p + "reverse_has_transition"] = (c0, c1) in summ["reverse_transitions"]
            d[p + "reverse_has_reciprocal_role"] = ROLE_TO_REVERSE_ROLE[prefix] in summ["reverse_roles"]

    unique_cvals = sorted(set(cvals))
    unique_anchors = sorted(set(anchors), key=pstr)
    all_cols = sorted(set(x for a in unique_anchors for x in a))
    all_res = sorted(set(x % 15 for x in all_cols))

    d["c_values"] = tuple(unique_cvals)
    d["c_sum_mod15"] = sum(unique_cvals) % 15
    d["anchor_nodes"] = tuple(pstr(x) for x in unique_anchors)
    d["anchor_col_count"] = len(all_cols)
    d["anchor_residue_count"] = len(all_res)
    d["anchor_residues"] = tuple(all_res)
    d["c_values_subset_anchor_residues"] = set(unique_cvals).issubset(set(all_res))
    d["c_values_intersection_anchor_residue_count"] = len(set(unique_cvals) & set(all_res))
    d["anchor_sum_mod15"] = sum(all_cols) % 15

    # Cross-role equality patterns.
    d["XY_c1_eq_IW_c0"] = d["XY_c1"] == d["IW_c0"]
    d["IW_c1_eq_ZT_c0"] = d["IW_c1"] == d["ZT_c0"]
    d["ZT_c1_eq_XY_c0"] = d["ZT_c1"] == d["XY_c0"]

    # Anchor twist sanity.
    d["twisted_anchor_closes"] = (
        d["XY_dst_anchor"] == d["ZT_src_anchor"]
        and d["ZT_dst_anchor"] == d["IW_src_anchor"]
        and d["IW_dst_anchor"] == d["XY_src_anchor"]
    )

    # Candidate relation score: how many role endpoints carry reciprocal reverse-role signatures.
    recips = []
    for role in ROLE_ORDER:
        for side in ["src", "dst"]:
            recips.append(bool(d[role + "_" + side + "_reverse_has_reciprocal_role"]))
    d["reciprocal_role_endpoint_count"] = sum(1 for x in recips if x)

    # Candidate relation score: how many endpoints expose matching C data in reverse metadata.
    c_meta = []
    for role in ROLE_ORDER:
        c_meta.append(bool(d[role + "_src_reverse_has_c0_from"]))
        c_meta.append(bool(d[role + "_dst_reverse_has_c1_to"]))
    d["endpoint_c_metadata_match_count"] = sum(1 for x in c_meta if x)

    return d


def truth_signature(rows, feature_names):
    sig = defaultdict(set)
    for r in rows:
        key = tuple(r["features"].get(f) for f in feature_names)
        sig[key].add(r["selected"])
    return sig


def exact_tests(rows, feature_names, max_size=3):
    tests = []
    for n in range(1, max_size + 1):
        for combo in itertools.combinations(feature_names, n):
            groups = truth_signature(rows, combo)
            exact = all(len(v) == 1 for v in groups.values())
            if not exact:
                continue

            selected_groups = 0
            rejected_groups = 0
            for vals in groups.values():
                val = next(iter(vals))
                if val:
                    selected_groups += 1
                else:
                    rejected_groups += 1

            tests.append({
                "features": list(combo),
                "group_count": len(groups),
                "selected_groups": selected_groups,
                "rejected_groups": rejected_groups,
            })

    tests.sort(key=lambda x: (len(x["features"]), x["group_count"], x["features"]))
    return tests


def single_feature_summary(rows, feature_names):
    out = []
    for f in feature_names:
        buckets = defaultdict(Counter)
        for r in rows:
            buckets[str(r["features"].get(f))][r["selected"]] += 1

        vals = []
        pure_selected = 0
        pure_rejected = 0
        mixed = 0
        for k, c in sorted(buckets.items()):
            vals.append({"value": k, "selected": c[True], "rejected": c[False]})
            if c[True] and not c[False]:
                pure_selected += 1
            elif c[False] and not c[True]:
                pure_rejected += 1
            else:
                mixed += 1

        out.append({
            "feature": f,
            "bucket_count": len(vals),
            "pure_selected_bucket_count": pure_selected,
            "pure_rejected_bucket_count": pure_rejected,
            "mixed_bucket_count": mixed,
            "buckets": vals,
        })

    out.sort(key=lambda x: (x["mixed_bucket_count"], -x["pure_selected_bucket_count"], x["bucket_count"], x["feature"]))
    return out


def main():
    overlay = load_json(IN_G60_OVERLAY)
    data022 = load_json(IN_022)

    edge_records = overlay.get("edge_records", [])
    reverse_rows = [r for r in edge_records if r.get("label") == "reverse_partner"]
    shared_rows = [r for r in edge_records if r.get("label") == "shared_B"]

    for r in reverse_rows + shared_rows:
        r["from_col_pair"] = col_pair(r.get("from_columns"))
        r["to_col_pair"] = col_pair(r.get("to_columns"))

    reverse_info = build_reverse_anchor_info(reverse_rows)

    observed_cycles = parse_observed_cycles_from_022(data022)
    c_cycles = sorted(set(c_cycle_from_observed(c) for c in observed_cycles), key=str)
    a_cycles = sorted(set(anchor_cycle_from_observed(c) for c in observed_cycles), key=str)
    observed_exact = set(cycle_key(c) for c in observed_cycles)

    candidates = []
    for ccyc in c_cycles:
        for acyc in a_cycles:
            cyc = []
            for (role1, c0, c1), (role2, src, dst) in zip(ccyc, acyc):
                assert role1 == role2
                cyc.append((role1, int(c0), int(c1), src, dst))
            cyc = tuple(cyc)
            selected = cycle_key(cyc) in observed_exact
            candidates.append({
                "cycle": cyc,
                "selected": selected,
                "features": candidate_features(cyc, reverse_info),
            })

    # Use non-observed, non-ID-ish feature names. We intentionally exclude direct
    # exact edge existence, c_cycle_id, anchor_cycle_id, and row index.
    feature_names = sorted(candidates[0]["features"].keys())

    tests = exact_tests(candidates, feature_names, max_size=3)
    singles = single_feature_summary(candidates, feature_names)

    selected_rows = []
    rejected_rows = []
    for i, c in enumerate(candidates):
        row = {
            "candidate_index": i,
            "selected": c["selected"],
            "cycle": [
                [role, c0, c1, pstr(src), pstr(dst)]
                for role, c0, c1, src, dst in c["cycle"]
            ],
            "features": c["features"],
        }
        if c["selected"]:
            selected_rows.append(row)
        else:
            rejected_rows.append(row)

    # Flag exact tests that may be promising because they do not use raw anchors directly.
    suspicious_tokens = ["anchor", "src", "dst"]
    promising = []
    for t in tests:
        joined = " ".join(t["features"])
        if not any(tok in joined for tok in suspicious_tokens):
            promising.append(t)

    result = {
        "status": "sharedB_16_candidate_selector_search_recorded",
        "audit_id": "023",
        "input_g60_overlay": str(IN_G60_OVERLAY),
        "input_022": str(IN_022),
        "candidate_count": len(candidates),
        "selected_count": sum(1 for c in candidates if c["selected"]),
        "rejected_count": sum(1 for c in candidates if not c["selected"]),
        "feature_count": len(feature_names),
        "exact_test_count": len(tests),
        "promising_non_anchor_exact_test_count": len(promising),
        "exact_tests_first_80": tests[:80],
        "promising_non_anchor_exact_tests_first_80": promising[:80],
        "single_feature_summary_first_80": singles[:80],
        "selected_candidates": selected_rows,
        "rejected_candidates": rejected_rows,
        "interpretation": (
            "This audit reduces the corrected 022 boundary to the 16 candidates admitted by both "
            "observed C-cycle support and observed twisted anchor-cycle support. It compares the 4 "
            "selected candidates against the 12 rejected candidates using non-circular relational "
            "features derived from C values, column-anchor summaries, and reverse_partner anchor "
            "metadata. Exact tests over anchor-specific features may still be too close to row identity; "
            "the important question is whether any compact non-anchor feature separates the 4 from 12."
        ),
        "boundary": (
            "This is a selector search over the already reduced 16-candidate universe. It does not "
            "derive a native selector unless a compact, non-row-identifying feature is found and then "
            "validated against a larger candidate universe."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Shared_B 16-candidate selector search 023")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("- candidate_count: `" + str(result["candidate_count"]) + "`")
    lines.append("- selected_count: `" + str(result["selected_count"]) + "`")
    lines.append("- rejected_count: `" + str(result["rejected_count"]) + "`")
    lines.append("- feature_count: `" + str(result["feature_count"]) + "`")
    lines.append("- exact_test_count: `" + str(result["exact_test_count"]) + "`")
    lines.append("- promising_non_anchor_exact_test_count: `" + str(result["promising_non_anchor_exact_test_count"]) + "`")
    lines.append("")
    lines.append("## Best exact tests first 40")
    lines.append("")
    if tests:
        for t in tests[:40]:
            lines.append("- features=`" + str(t["features"]) + "`, groups=`" + str(t["group_count"]) + "`, selected_groups=`" + str(t["selected_groups"]) + "`, rejected_groups=`" + str(t["rejected_groups"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Promising non-anchor exact tests first 40")
    lines.append("")
    if promising:
        for t in promising[:40]:
            lines.append("- features=`" + str(t["features"]) + "`, groups=`" + str(t["group_count"]) + "`, selected_groups=`" + str(t["selected_groups"]) + "`, rejected_groups=`" + str(t["rejected_groups"]) + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Best single-feature summaries first 30")
    lines.append("")
    for s in singles[:30]:
        lines.append("- feature=`" + s["feature"] + "`, buckets=`" + str(s["bucket_count"]) + "`, pure_selected=`" + str(s["pure_selected_bucket_count"]) + "`, pure_rejected=`" + str(s["pure_rejected_bucket_count"]) + "`, mixed=`" + str(s["mixed_bucket_count"]) + "`")
    lines.append("")
    lines.append("## Selected candidates")
    lines.append("")
    for r in selected_rows:
        lines.append("- candidate `" + str(r["candidate_index"]) + "`: `" + str(r["cycle"]) + "`")
    lines.append("")
    lines.append("## Rejected candidates")
    lines.append("")
    for r in rejected_rows:
        lines.append("- candidate `" + str(r["candidate_index"]) + "`: `" + str(r["cycle"]) + "`")
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
    print("rejected_count", result["rejected_count"])
    print("feature_count", result["feature_count"])
    print("exact_test_count", result["exact_test_count"])
    print("promising_non_anchor_exact_test_count", result["promising_non_anchor_exact_test_count"])


if __name__ == "__main__":
    main()
