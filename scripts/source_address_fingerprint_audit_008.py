#!/usr/bin/env python3
import json
from pathlib import Path
from itertools import combinations
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]

IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"

OUT_JSON = ROOT / "artifacts/json/source_address_fingerprint_audit_008.v1.json"
OUT_NOTE = ROOT / "notes/source_address_fingerprint_audit_008.md"

REVERSE_ROLES = {"WX", "YZ", "TI"}
SHAREDB_ROLES = {"XY", "ZT", "IW"}


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def is_scalar(x):
    return x is None or isinstance(x, (str, int, float, bool))


def role_class(role):
    if role in REVERSE_ROLES:
        return "reverse_partner"
    if role in SHAREDB_ROLES:
        return "shared_B"
    return "unknown"


def triangle_frame_closure(s, r):
    return (
        s["role_pair"] == r["role_pair"]
        and s["from_C"] == r["from_C"]
        and s["to_C"] == r["to_C"]
        and s["integer_C_delta"] == r["integer_C_delta"]
        and s["C_delta"] == r["C_delta"]
        and s["lift_q"] == r["lift_q"]
        and s["from_B"] == s["to_B"]
        and s["from_slot"] == s["to_slot"]
        and r["from_A"] == r["to_A"]
        and r["from_B"] == r["to_C"]
        and r["from_C"] == r["to_B"]
        and r["from_B"] == s["to_C"]
        and r["from_slot"] == s["to_C"]
        and r["to_B"] == s["from_C"]
        and r["to_slot"] == s["from_C"]
    )


def common_scalar_keys(rows):
    if not rows:
        return []
    keys = set(rows[0].keys())
    for r in rows[1:]:
        keys &= set(r.keys())
    out = []
    for k in sorted(keys):
        if all(is_scalar(r.get(k)) for r in rows):
            out.append(k)
    return out


def build_record(s, r):
    c0 = s["from_C"]
    c1 = s["to_C"]
    c_delta = (c1 - c0) % 15
    integer_delta = c1 - c0
    lift_q = 0 if integer_delta >= 0 else 3

    targets = {
        "S.from_A": s["from_A"],
        "S.B": s["from_B"],
        "S.to_A": s["to_A"],
        "R.A": r["from_A"],
        "S.A_delta": (s["to_A"] - s["from_A"]) % 15,
        "R.minus_S_from_A": (r["from_A"] - s["from_A"]) % 15,
        "S.B_minus_c1": (s["from_B"] - c1) % 15,
    }

    features = {
        "pair.role_pair": s["role_pair"],
        "pair.c0": c0,
        "pair.c1": c1,
        "pair.C_delta": c_delta,
        "pair.integer_C_delta": integer_delta,
        "pair.lift_q": lift_q,
        "pair.shared_role": s["station_role"],
        "pair.reverse_role": r["station_role"],
        "pair.C_track": str((c0, c1)),
    }

    for k, v in s.items():
        if is_scalar(v):
            features["S." + k] = v
    for k, v in r.items():
        if is_scalar(v):
            features["R." + k] = v

    return {
        "key": [s["role_pair"], c0, c1, s["station_role"], r["station_role"]],
        "targets": targets,
        "features": features,
    }


def deterministic_search(records):
    target_equiv = {
        "S.from_A": {"S.from_A"},
        "S.B": {"S.from_B", "S.from_slot", "S.to_B", "S.to_slot"},
        "S.to_A": {"S.to_A"},
        "R.A": {"R.from_A", "R.to_A"},
        "S.A_delta": set(),
        "R.minus_S_from_A": set(),
        "S.B_minus_c1": set(),
    }

    all_features = sorted(records[0]["features"].keys())
    targets = sorted(records[0]["targets"].keys())

    direct_identity = []
    tests = []

    for target in targets:
        for f in all_features:
            vals = [(rec["features"][f], rec["targets"][target]) for rec in records]
            if all(a == b for a, b in vals):
                direct_identity.append({"target": target, "feature": f})

        allowed = [f for f in all_features if f not in target_equiv.get(target, set())]

        for size in [1, 2]:
            for fs in combinations(allowed, size):
                groups = defaultdict(set)
                for rec in records:
                    key = tuple(rec["features"][f] for f in fs)
                    groups[key].add(rec["targets"][target])

                ambiguous = [k for k, vals in groups.items() if len(vals) > 1]
                exact = len(ambiguous) == 0
                group_count = len(groups)

                if exact:
                    if group_count <= 6:
                        strength = "strong"
                    elif group_count <= 9:
                        strength = "medium"
                    elif group_count <= 11:
                        strength = "weak"
                    else:
                        strength = "row_identity_like"

                    tests.append({
                        "target": target,
                        "features": list(fs),
                        "group_count": group_count,
                        "strength": strength,
                    })

    tests = sorted(
        tests,
        key=lambda x: (
            {"strong": 0, "medium": 1, "weak": 2, "row_identity_like": 3}[x["strength"]],
            len(x["features"]),
            x["group_count"],
            x["target"],
            ",".join(x["features"]),
        ),
    )

    return {
        "feature_count": len(all_features),
        "target_count": len(targets),
        "direct_identity_count": len(direct_identity),
        "direct_identity_first_50": direct_identity[:50],
        "exact_test_count": len(tests),
        "strength_counts": dict(sorted(Counter(t["strength"] for t in tests).items())),
        "exact_tests_first_100": tests[:100],
        "strong_tests": [t for t in tests if t["strength"] == "strong"],
        "medium_tests": [t for t in tests if t["strength"] == "medium"],
        "weak_tests_first_50": [t for t in tests if t["strength"] == "weak"][:50],
    }


def main():
    drows = load(IN_ROWS)
    d002 = load(IN_002)

    selected_keys = {tuple(k) for k in d002["selected_pair_keys"]}

    rows = []
    for row in drows.get("rows", []):
        r = dict(row)
        r["role_class"] = role_class(r["station_role"])
        rows.append(r)

    shared = [r for r in rows if r["role_class"] == "shared_B"]
    reverse = [r for r in rows if r["role_class"] == "reverse_partner"]

    selected_records = []
    for s in shared:
        for r in reverse:
            if not triangle_frame_closure(s, r):
                continue
            key = (s["role_pair"], s["from_C"], s["to_C"], s["station_role"], r["station_role"])
            if key in selected_keys:
                selected_records.append(build_record(s, r))

    search = deterministic_search(selected_records)

    shared_keys = common_scalar_keys(shared)
    reverse_keys = common_scalar_keys(reverse)

    result = {
        "status": "source_address_fingerprint_audit_recorded",
        "audit_id": "008",
        "input_rows": str(IN_ROWS),
        "input_selector_002": str(IN_002),
        "selected_record_count": len(selected_records),
        "shared_common_scalar_keys": shared_keys,
        "reverse_common_scalar_keys": reverse_keys,
        "available_feature_count": search["feature_count"],
        "target_count": search["target_count"],
        "direct_identity_count": search["direct_identity_count"],
        "exact_test_count": search["exact_test_count"],
        "strength_counts": search["strength_counts"],
        "strong_tests": search["strong_tests"],
        "medium_tests": search["medium_tests"],
        "weak_tests_first_50": search["weak_tests_first_50"],
        "direct_identity_first_50": search["direct_identity_first_50"],
        "selected_keys": [r["key"] for r in selected_records],
        "interpretation": (
            "This audit asks whether the available realized source-row fields contain a compact "
            "address fingerprint for the free A/B assignment variables. Strong tests would suggest "
            "a low-dimensional selector already present in the copied source row schema. Weak or "
            "row-identity-like tests indicate the current row schema is not rich enough, or that the "
            "law lives in upstream provenance not included in this artifact."
        ),
        "boundary": (
            "This is a schema/fingerprint audit over realized selected rows. It is not a native "
            "generator and not Gap A closure. It only tests the fields available in the copied "
            "Project 18 row artifact."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Source address fingerprint audit 008")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Schema")
    lines.append("")
    lines.append("- selected_record_count: `" + str(result["selected_record_count"]) + "`")
    lines.append("- shared_common_scalar_keys: `" + str(result["shared_common_scalar_keys"]) + "`")
    lines.append("- reverse_common_scalar_keys: `" + str(result["reverse_common_scalar_keys"]) + "`")
    lines.append("- available_feature_count: `" + str(result["available_feature_count"]) + "`")
    lines.append("")
    lines.append("## Fingerprint search")
    lines.append("")
    lines.append("- direct_identity_count: `" + str(result["direct_identity_count"]) + "`")
    lines.append("- exact_test_count: `" + str(result["exact_test_count"]) + "`")
    lines.append("- strength_counts: `" + str(result["strength_counts"]) + "`")
    lines.append("")
    lines.append("## Strong exact tests")
    lines.append("")
    if result["strong_tests"]:
        for t in result["strong_tests"][:40]:
            lines.append(
                "- target=" + t["target"]
                + ", features=" + str(t["features"])
                + ", groups=" + str(t["group_count"])
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Medium exact tests")
    lines.append("")
    if result["medium_tests"]:
        for t in result["medium_tests"][:40]:
            lines.append(
                "- target=" + t["target"]
                + ", features=" + str(t["features"])
                + ", groups=" + str(t["group_count"])
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Weak exact tests first 20")
    lines.append("")
    if result["weak_tests_first_50"]:
        for t in result["weak_tests_first_50"][:20]:
            lines.append(
                "- target=" + t["target"]
                + ", features=" + str(t["features"])
                + ", groups=" + str(t["group_count"])
            )
    else:
        lines.append("- none")
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
    print("selected_record_count", result["selected_record_count"])
    print("available_feature_count", result["available_feature_count"])
    print("exact_test_count", result["exact_test_count"])
    print("strength_counts", result["strength_counts"])
    print("strong_test_count", len(result["strong_tests"]))
    print("medium_test_count", len(result["medium_tests"]))


if __name__ == "__main__":
    main()
