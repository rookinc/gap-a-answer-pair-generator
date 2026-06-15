#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source/project18_native_chain/json"

OUT_JSON = ROOT / "artifacts/json/native_chain_schema_inspection_011.v1.json"
OUT_NOTE = ROOT / "notes/native_chain_schema_inspection_011.md"

NEEDLES = [
    "from_C", "to_C", "C_delta", "lift_q",
    "from_A", "from_B", "to_A", "to_B",
    "slot", "fiber", "local", "vertex",
    "role_pair", "station_role", "role_class",
    "support", "transition", "q3", "q0",
    "source", "native", "generator", "rule",
]


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def scalar(x):
    return x is None or isinstance(x, (str, int, float, bool))


def walk(obj, prefix="", depth=0, max_depth=7, out=None):
    if out is None:
        out = []
    if depth > max_depth:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append((p, type(v).__name__, v if scalar(v) else None))
            walk(v, p, depth + 1, max_depth, out)
    elif isinstance(obj, list):
        out.append((prefix + "[]", "list", "len=" + str(len(obj))))
        if obj:
            walk(obj[0], prefix + "[]", depth + 1, max_depth, out)
    return out


def record_lists(obj, prefix=""):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, list) and v and all(isinstance(x, dict) for x in v[: min(5, len(v))]):
                found.append({
                    "path": p,
                    "count": len(v),
                    "sample_keys": sorted(v[0].keys()),
                })
            found.extend(record_lists(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:3]):
            found.extend(record_lists(v, f"{prefix}[{i}]"))
    return found


def needle_counts(paths):
    c = Counter()
    hits = []
    for p, typ, sample in paths:
        low = p.lower()
        for n in NEEDLES:
            if n.lower() in low:
                c[n] += 1
                if len(hits) < 120:
                    hits.append({"path": p, "needle": n, "type": typ, "sample": sample})
                break
    return c, hits


def score_file(name, counts, rlists):
    score = 0
    low = name.lower()

    for word in ["native", "generator", "transition", "support", "schema", "role_block", "lift", "q3"]:
        if word in low:
            score += 2

    for n in ["from_C", "to_C", "C_delta", "lift_q", "from_A", "from_B", "to_A", "to_B"]:
        if counts.get(n, 0):
            score += 2

    for rl in rlists:
        keys = set(rl["sample_keys"])
        if {"from_C", "to_C"}.issubset(keys):
            score += 5
        if {"from_A", "from_B", "to_A", "to_B"}.intersection(keys):
            score += 3
        if {"role_pair", "station_role"}.intersection(keys):
            score += 2
        if {"support", "transition"}.intersection(keys):
            score += 2

    return score


def main():
    files = sorted(SRC.glob("*.json"))
    inventory = []
    global_counts = Counter()

    for path in files:
        data = load(path)
        paths = walk(data)
        counts, hits = needle_counts(paths)
        rlists = record_lists(data)

        global_counts.update(counts)

        item = {
            "file": path.name,
            "top_keys": sorted(data.keys()) if isinstance(data, dict) else [],
            "path_count": len(paths),
            "record_lists": rlists,
            "needle_counts": dict(sorted(counts.items())),
            "needle_hits_first_120": hits,
        }
        item["score"] = score_file(path.name, counts, rlists)
        inventory.append(item)

    ranked = sorted(inventory, key=lambda x: (-x["score"], x["file"]))

    result = {
        "status": "native_chain_schema_inspection_recorded",
        "audit_id": "011",
        "source_dir": str(SRC),
        "file_count": len(files),
        "global_needle_counts": dict(sorted(global_counts.items())),
        "ranked_files": ranked,
        "top_files": ranked[:8],
        "interpretation": (
            "This schema inspection ranks imported native-chain artifacts by whether they expose "
            "transition, support, role, and A/B/C fields. The goal is to identify the best next "
            "source for reconstructing the missing A/B assignment law."
        ),
        "boundary": (
            "This is schema inspection only. It does not assert a native generator and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Native chain schema inspection 011")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append("- file_count: `" + str(result["file_count"]) + "`")
    lines.append("- global_needle_counts: `" + str(result["global_needle_counts"]) + "`")
    lines.append("")
    lines.append("## Top ranked files")
    lines.append("")
    for item in ranked[:10]:
        lines.append("- `" + item["file"] + "`")
        lines.append("  - score: `" + str(item["score"]) + "`")
        lines.append("  - top_keys: `" + str(item["top_keys"]) + "`")
        lines.append("  - needle_counts: `" + str(item["needle_counts"]) + "`")
        if item["record_lists"]:
            for rl in item["record_lists"][:6]:
                lines.append("  - records: `" + rl["path"] + "` count `" + str(rl["count"]) + "`")
                lines.append("    - sample_keys: `" + str(rl["sample_keys"][:50]) + "`")
        else:
            lines.append("  - records: none detected")
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
    print("file_count", result["file_count"])
    print("top_files", [x["file"] for x in ranked[:8]])


if __name__ == "__main__":
    main()
