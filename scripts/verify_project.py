#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "paper/main.tex",
    "paper/refs.bib",
    "paper/sections/00_abstract.tex",
    "paper/sections/01_introduction.tex",
    "paper/sections/02_project18_seed_result.tex",
    "paper/sections/03_gap_a_problem.tex",
    "paper/sections/04_reciprocal_pair_grammar.tex",
    "paper/sections/05_native_generator_criteria.tex",
    "paper/sections/06_work_plan.tex",
    "paper/sections/07_boundaries.tex",
    "paper/sections/08_conclusion.tex",
    "artifacts/json/project_manifest.v1.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("missing required files: " + ", ".join(missing))

main = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
for p in required:
    if p.startswith("paper/sections/"):
        stem = p.replace("paper/", "").replace(".tex", "")
        if stem not in main:
            raise SystemExit("main.tex does not reference " + stem)

for path in sorted((ROOT / "artifacts/json").glob("*.json")):
    json.loads(path.read_text(encoding="utf-8"))

print("OK: project verifies")
