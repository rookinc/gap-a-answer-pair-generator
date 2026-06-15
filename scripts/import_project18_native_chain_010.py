#!/usr/bin/env python3
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P18 = ROOT.parent / "18-g900-kernel-admission"

JSON_SRC = P18 / "artifacts/json"
NOTE_SRC = P18 / "notes"

JSON_DST = ROOT / "source/project18_native_chain/json"
NOTE_DST = ROOT / "source/project18_native_chain/notes"

OUT_JSON = ROOT / "artifacts/json/import_project18_native_chain_010.v1.json"
OUT_NOTE = ROOT / "notes/import_project18_native_chain_010.md"

NAMES = [
    "g60_native_generator_input_bundle_001",
    "g60_native_overlay_generator_family_search_001",
    "context_dependent_overlay_delta_rules_001",
    "c_transition_overlay_delta_generator_001",
    "c_transition_delta_lift_decomposition_001",
    "lift_q_context_rules_001",
    "from_c_lift_q_overlay_delta_formula_001",
    "from_c_lift_partition_native_context_001",
    "q3_selector_sanity_audit_001",
    "c_transition_support_partition_audit_001",
    "c_transition_support_canonical_audit_002",
    "c_transition_schema_inspection_003a",
    "c_transition_station_role_cover_audit_003b",
    "c_transition_role_channel_grammar_audit_004",
    "c_transition_role_block_circulation_audit_005",
    "role_block_directed_transition_selector_006c",
    "gap_a_wxyzti_role_block_selector_checkpoint_006c",
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_one(src, dst_dir):
    if not src.exists():
        return None
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return {
        "source": str(src),
        "dest": str(dst),
        "bytes": dst.stat().st_size,
        "sha256": sha256(dst),
    }


def main():
    copied_json = []
    copied_notes = []
    missing_json = []
    missing_notes = []

    for name in NAMES:
        j = JSON_SRC / (name + ".v1.json")
        m = NOTE_SRC / (name + ".md")

        cj = copy_one(j, JSON_DST)
        if cj:
            copied_json.append(cj)
        else:
            missing_json.append(str(j))

        cm = copy_one(m, NOTE_DST)
        if cm:
            copied_notes.append(cm)
        else:
            missing_notes.append(str(m))

    result = {
        "status": "project18_native_chain_import_recorded",
        "audit_id": "010",
        "source_project": str(P18),
        "json_dest": str(JSON_DST),
        "notes_dest": str(NOTE_DST),
        "requested_name_count": len(NAMES),
        "copied_json_count": len(copied_json),
        "copied_note_count": len(copied_notes),
        "missing_json_count": len(missing_json),
        "missing_note_count": len(missing_notes),
        "copied_json": copied_json,
        "copied_notes": copied_notes,
        "missing_json": missing_json,
        "missing_notes": missing_notes,
        "interpretation": (
            "Project 21 imported the earlier Project 18 native-chain artifacts, before the later "
            "WXYZTI row-pair audits. These artifacts are candidates for recovering the missing "
            "transition-support and A/B assignment provenance."
        ),
        "boundary": (
            "This is an import manifest only. It does not test a generator and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Import Project 18 native chain 010")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Import")
    lines.append("")
    lines.append("- requested_name_count: `" + str(result["requested_name_count"]) + "`")
    lines.append("- copied_json_count: `" + str(result["copied_json_count"]) + "`")
    lines.append("- copied_note_count: `" + str(result["copied_note_count"]) + "`")
    lines.append("- missing_json_count: `" + str(result["missing_json_count"]) + "`")
    lines.append("- missing_note_count: `" + str(result["missing_note_count"]) + "`")
    lines.append("")
    lines.append("## Copied JSON")
    lines.append("")
    for item in copied_json:
        lines.append("- `" + Path(item["dest"]).name + "`")
        lines.append("  - sha256: `" + item["sha256"] + "`")
    lines.append("")
    lines.append("## Missing JSON")
    lines.append("")
    if missing_json:
        for item in missing_json:
            lines.append("- `" + item + "`")
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
    print("copied_json_count", result["copied_json_count"])
    print("copied_note_count", result["copied_note_count"])
    print("missing_json_count", result["missing_json_count"])
    print("missing_note_count", result["missing_note_count"])


if __name__ == "__main__":
    main()
