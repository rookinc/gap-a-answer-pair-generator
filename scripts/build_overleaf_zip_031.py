#!/usr/bin/env python3
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAPER = ROOT / "paper"
DIST = ROOT / "dist"
OUT_ZIP = DIST / "gap_a_answer_pair_generator_overleaf.zip"

OUT_JSON = ROOT / "artifacts/json/overleaf_zip_build_031.v1.json"
OUT_NOTE = ROOT / "notes/overleaf_zip_build_031.md"

REQUIRED = [
    PAPER / "main.tex",
    PAPER / "sections/07_reduced_universe_shell_rank_selector.tex",
]

INCLUDE_SUFFIXES = {
    ".tex",
    ".bib",
    ".bst",
    ".cls",
    ".sty",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".svg",
}

EXCLUDE_NAMES = {
    ".DS_Store",
}

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def collect_files():
    files = []
    for path in PAPER.rglob("*"):
        if not path.is_file():
            continue
        if path.name in EXCLUDE_NAMES:
            continue
        if path.suffix.lower() not in INCLUDE_SUFFIXES:
            continue
        files.append(path)
    return sorted(files)

def main():
    missing_required = [str(p) for p in REQUIRED if not p.exists()]
    if missing_required:
        raise SystemExit("missing required files: " + repr(missing_required))

    main_text = (PAPER / "main.tex").read_text(encoding="utf-8")
    section_input_present = "07_reduced_universe_shell_rank_selector" in main_text

    files = collect_files()

    DIST.mkdir(parents=True, exist_ok=True)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    if OUT_ZIP.exists():
        OUT_ZIP.unlink()

    zip_entries = []
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files:
            arcname = path.relative_to(PAPER).as_posix()
            z.write(path, arcname)
            zip_entries.append(arcname)

    zip_sha256 = sha256_file(OUT_ZIP)
    zip_size_bytes = OUT_ZIP.stat().st_size

    result = {
        "status": "overleaf_zip_build_recorded",
        "audit_id": "031",
        "paper_dir": str(PAPER),
        "zip_path": str(OUT_ZIP),
        "zip_size_bytes": zip_size_bytes,
        "zip_sha256": zip_sha256,
        "file_count": len(zip_entries),
        "zip_entries": zip_entries,
        "required_files_present": len(missing_required) == 0,
        "missing_required": missing_required,
        "section_input_present": section_input_present,
        "contains_main_tex": "main.tex" in zip_entries,
        "contains_reduced_theorem_section": "sections/07_reduced_universe_shell_rank_selector.tex" in zip_entries,
        "interpretation": (
            "Built an Overleaf-ready ZIP from the paper directory. Archive paths are rooted at "
            "the paper directory, so main.tex appears at the ZIP root and section inputs resolve "
            "as sections/*.tex."
        ),
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Overleaf ZIP build 031")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## ZIP")
    lines.append("")
    lines.append("- zip_path: `" + str(OUT_ZIP) + "`")
    lines.append("- zip_size_bytes: `" + str(zip_size_bytes) + "`")
    lines.append("- zip_sha256: `" + zip_sha256 + "`")
    lines.append("- file_count: `" + str(len(zip_entries)) + "`")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    lines.append("- required_files_present: `" + str(result["required_files_present"]) + "`")
    lines.append("- section_input_present: `" + str(section_input_present) + "`")
    lines.append("- contains_main_tex: `" + str(result["contains_main_tex"]) + "`")
    lines.append("- contains_reduced_theorem_section: `" + str(result["contains_reduced_theorem_section"]) + "`")
    lines.append("")
    lines.append("## Entries")
    lines.append("")
    for entry in zip_entries:
        lines.append("- `" + entry + "`")
    lines.append("")
    lines.append("## Reading")
    lines.append("")
    lines.append(result["interpretation"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_ZIP)
    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("zip_size_bytes", zip_size_bytes)
    print("zip_sha256", zip_sha256)
    print("file_count", len(zip_entries))
    print("section_input_present", section_input_present)
    print("contains_main_tex", result["contains_main_tex"])
    print("contains_reduced_theorem_section", result["contains_reduced_theorem_section"])

if __name__ == "__main__":
    main()
