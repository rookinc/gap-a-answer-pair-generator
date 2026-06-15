#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "source/project18_artifacts/json"

OUT_JSON = ROOT / "artifacts/json/source_artifact_schema_inventory_009.v1.json"
OUT_NOTE = ROOT / "notes/source_artifact_schema_inventory_009.md"

NEEDLES = [
    "address_pair_source",
    "columns",
    "key",
    "fiber",
    "slot",
    "handedness",
    "handedness_word",
    "A",
    "B",
    "C",
    "C_plus_1",
    "station",
    "station_role",
    "role",
    "path",
    "provenance",
    "source_native",
    "from_BAC",
    "to_BAC",
    "from_columns",
    "to_columns",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def scalar(x):
    return x is None or isinstance(x, (str, int, float, bool))


def walk(obj, prefix="", depth=0, max_depth=5, out=None):
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


def find_record_lists(obj, prefix=""):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, list) and v and all(isinstance(x, dict) for x in v[: min(5, len(v))]):
                found.append((p, len(v), sorted(v[0].keys())))
            found.extend(find_record_lists(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:3]):
            found.extend(find_record_lists(v, f"{prefix}[{i}]"))
    return found


def needle_hits(paths):
    hits = []
    for p, typ, val in paths:
        low = p.lower()
        for n in NEEDLES:
            if n.lower() in low:
                hits.append({"path": p, "type": typ, "needle": n, "sample": val})
                break
    return hits


def main():
    files = sorted(SRC.glob("*.json"))
    inventory = []
    global_needles = Counter()
    all_record_lists = []

    for path in files:
        data = load_json(path)
        paths = walk(data, max_depth=6)
        hits = needle_hits(paths)
        record_lists = find_record_lists(data)

        for h in hits:
            global_needles[h["needle"]] += 1

        for p, n, keys in record_lists:
            all_record_lists.append({
                "file": path.name,
                "record_path": p,
                "count": n,
                "sample_keys": keys,
            })

        top_keys = sorted(data.keys()) if isinstance(data, dict) else []
        inventory.append({
            "file": path.name,
            "top_type": type(data).__name__,
            "top_keys": top_keys,
            "path_count_depth6": len(paths),
            "needle_hit_count": len(hits),
            "needle_hits_first_80": hits[:80],
            "record_lists": [
                {"path": p, "count": n, "sample_keys": keys}
                for p, n, keys in record_lists
            ],
        })

    promising = []
    for item in inventory:
        score = 0
        name = item["file"].lower()
        if "provenance" in name or "station_transition_feature" in name or "station_provenance" in name:
            score += 5
        if "station" in name:
            score += 3
        if item["needle_hit_count"] > 30:
            score += 2
        if any("address_pair_source" in str(h).lower() for h in item["needle_hits_first_80"]):
            score += 5
        if any("columns" in str(h).lower() for h in item["needle_hits_first_80"]):
            score += 3
        if score:
            promising.append({
                "file": item["file"],
                "score": score,
                "needle_hit_count": item["needle_hit_count"],
                "record_lists": item["record_lists"],
                "top_keys": item["top_keys"],
            })

    promising = sorted(promising, key=lambda x: (-x["score"], x["file"]))

    result = {
        "status": "source_artifact_schema_inventory_recorded",
        "audit_id": "009",
        "source_dir": str(SRC),
        "file_count": len(files),
        "global_needle_counts": dict(sorted(global_needles.items())),
        "record_list_count": len(all_record_lists),
        "record_lists": all_record_lists,
        "promising_files": promising,
        "inventory": inventory,
        "interpretation": (
            "This inventory checks whether the copied Project 18 source cache contains richer "
            "station provenance fields such as address_pair_source, columns, station keys, "
            "or BAC/column endpoint records. If promising files are thin or derived, the next "
            "step is to import the upstream raw WXYZTI station artifact from Project 18 or the "
            "source lab rather than continuing relation searches on thin audits."
        ),
        "boundary": (
            "This is a schema inventory only. It does not test a generator and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Source artifact schema inventory 009")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Source cache")
    lines.append("")
    lines.append("- file_count: `" + str(result["file_count"]) + "`")
    lines.append("- record_list_count: `" + str(result["record_list_count"]) + "`")
    lines.append("- global_needle_counts: `" + str(result["global_needle_counts"]) + "`")
    lines.append("")
    lines.append("## Promising files")
    lines.append("")
    if promising:
        for item in promising:
            lines.append("- `" + item["file"] + "`")
            lines.append("  - score: `" + str(item["score"]) + "`")
            lines.append("  - needle_hit_count: `" + str(item["needle_hit_count"]) + "`")
            lines.append("  - top_keys: `" + str(item["top_keys"]) + "`")
            if item["record_lists"]:
                for rl in item["record_lists"][:5]:
                    lines.append("  - records: `" + rl["path"] + "` count `" + str(rl["count"]) + "`")
                    lines.append("    - sample_keys: `" + str(rl["sample_keys"][:30]) + "`")
            else:
                lines.append("  - records: none detected")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Record lists")
    lines.append("")
    for rl in all_record_lists[:60]:
        lines.append(
            "- file=`" + rl["file"] + "`, path=`" + rl["record_path"] + "`, count=`" + str(rl["count"]) + "`"
        )
        lines.append("  - sample_keys: `" + str(rl["sample_keys"][:40]) + "`")
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
    print("record_list_count", result["record_list_count"])
    print("promising_files", [p["file"] for p in promising[:10]])
    print("global_needle_counts", result["global_needle_counts"])


if __name__ == "__main__":
    main()
