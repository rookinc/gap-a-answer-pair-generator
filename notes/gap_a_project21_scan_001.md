# Gap A Project 21 scan 001

Boundary: scan only. No theorem, proof claim, admission, physics claim, or force claim.

## Summary

- scanned_file_count: `168`
- hit_file_count: `168`

## Top dirs

- `source`: `66`
- `artifacts`: `36`
- `scripts`: `33`
- `notes`: `32`
- `.`: `1`

## Top hits

### `artifacts/json/native_shell_rank_derivation_027.v1.json`

- score: `342`
- reasons: `Gap A=1, gap a=1, gap-a=3, shared_B=1, role-labeled shared_B=1, selector=7, candidate=318, path_gap`

```
81: "audit_id": "027",
82: "best_selector_tests_first_80": [
83: {
```

```
83: {
84: "accepted_candidate_indices": [
85: 1,
```

### `artifacts/json/source_artifact_schema_inventory_009.v1.json`

- score: `333`
- reasons: `Gap A=15, gap a=15, gap-a=1, shared_B=217, native generator=1, realized rows=5, reciprocal pair=2, selector=30, candidate=37, path_gap`

```
2: "audit_id": "009",
3: "boundary": "This is a schema inventory only. It does not test a generator and does not close Gap A.",
4: "file_count": 16,
```

```
27: "needle": "A",
28: "path": "boundary.candidate_universe_generated",
29: "sample": false,
```

### `artifacts/json/native_chain_schema_inspection_011.v1.json`

- score: `148`
- reasons: `Gap A=1, gap a=1, gap-a=1, shared_B=65, native generator=1, A/B assignment=1, selector=6, candidate=62, path_gap`

```
2: "audit_id": "011",
3: "boundary": "This is schema inspection only. It does not assert a native generator and does not close Gap A.",
4: "file_count": 17,
```

```
27: },
28: "interpretation": "This schema inspection ranks imported native-chain artifacts by whether they expose transition, support, role, and A/B/C fields. The goal is to identify the best next source for reconstructing the miss...
29: "ranked_files": [
```

### `artifacts/json/radial_phase_lock_selector_025.v1.json`

- score: `132`
- reasons: `Gap A=1, gap a=1, gap-a=2, selector=5, candidate=108, path_gap, path_selector`

```
12: "audit_id": "025",
13: "boundary": "This does not close Gap A. It derives an exact selector only after accepting the shell markers and matrix-order phase ranks from the reduced 024 representation. The next step is to derive those shell/rank la...
14: "c_shell_members": {
```

```
23: },
24: "candidate_count": 16,
25: "candidate_rows": [
```

### `source/project18_artifacts/json/wxyzti_answer_pair_candidate_universe_audit_022.v1.json`

- score: `131`
- reasons: `Gap A=1, gap a=1, shared_B=86, reciprocal pair=1, selector=14, candidate=18, path_gap`

```
63: "role_pair": "IW/YZ",
64: "shared_B_row": {
65: "C_delta": 9,
```

```
72: "lift_q": 0,
73: "role_class": "shared_B",
74: "role_pair": "IW/YZ",
```

### `artifacts/json/synthetic_pair_skeleton_universe_003.v1.json`

- score: `104`
- reasons: `Gap A=1, gap a=1, gap-a=2, shared_B=48, A/B assignment=2, realized rows=2, synthetic=16, transition keys=1, selector=2, candidate=14, path_gap, path_synthetic`

```
2: "audit_id": "003",
3: "boundary": "This is not Gap A closure. It uses selected transition keys from 002, and it uses realized rows only for evaluation. It does not yet generate the transition support or the A/B assignments natively.",
4: "free_variable_count_per_key": 4,
```

```
4: "free_variable_count_per_key": 4,
5: "input_realized_rows_for_evaluation_only": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1...
6: "input_selector_002": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/json/admission_blind_row_pair_selector_002.v1.json",
```

### `artifacts/json/g60_overlay_generator_family_reading_015.v1.json`

- score: `92`
- reasons: `Gap A=2, gap a=2, gap-a=1, shared_B=41, candidate=36, path_gap`

```
2: "audit_id": "015",
3: "boundary": "This is a reading and triage audit over an imported search artifact. It does not derive the G60 overlay edge records and does not close Gap A.",
4: "boundary_from_source": [
```

```
6: "Failure refutes only this tested family.",
7: "Success would identify a candidate generator family, not full Gap A closure.",
8: "This does not prove full G900."
```

### `artifacts/json/native_rule_member_alignment_012.v1.json`

- score: `92`
- reasons: `Gap A=1, gap a=1, gap-a=3, shared_B=74, A/B assignment=1, selector=2, path_gap`

```
25: "from_slot": 13,
26: "label": "shared_B",
27: "slot_delta_mod15": 0,
```

```
57: "reverse_partner": 1,
58: "shared_B": 1
59: },
```

### `scripts/radial_phase_lock_selector_025.py`

- score: `77`
- reasons: `Gap A=1, gap a=1, selector=41, candidate=19, path_gap, path_selector`

```
11:
12: OUT_JSON = ROOT / "artifacts/json/radial_phase_lock_selector_025.v1.json"
13: OUT_NOTE = ROOT / "notes/radial_phase_lock_selector_025.md"
```

```
12: OUT_JSON = ROOT / "artifacts/json/radial_phase_lock_selector_025.v1.json"
13: OUT_NOTE = ROOT / "notes/radial_phase_lock_selector_025.md"
14:
```

### `scripts/g60_overlay_generator_family_reading_015.py`

- score: `71`
- reasons: `Gap A=1, gap a=1, shared_B=10, candidate=49, path_gap`

```
39:
40: def compact_candidate(c):
41: matched_edges = count_like(c.get("matched_edges"))
```

```
45: return {
46: "candidate": c.get("candidate"),
47: "exact_all": bool(c.get("exact_all")),
```

### `source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`

- score: `71`
- reasons: `Gap A=1, gap a=1, shared_B=41, candidate=18, path_gap`

```
4: "timestamp_utc": "2026-06-15T14:00:56.601438+00:00",
5: "purpose": "Test a bounded family of simple native G60 maps as candidate generators for WXYZTI overlay edges.",
6: "summary": {
```

```
11: "reverse_partner": 12,
12: "shared_B": 12
13: },
```

### `artifacts/json/triangle_frame_assignment_audit_006.v1.json`

- score: `68`
- reasons: `Gap A=1, gap a=1, gap-a=1, shared_B=50, A/B assignment=1, selector=1, candidate=3, path_gap`

```
2: "audit_id": "006",
3: "boundary": "This is an exploratory frame audit over realized WXYZTI rows. It does not generate the C-transition support or the A/B assignments natively. It is not Gap A closure.",
4: "candidate_count": 48,
```

```
3: "boundary": "This is an exploratory frame audit over realized WXYZTI rows. It does not generate the C-transition support or the A/B assignments natively. It is not Gap A closure.",
4: "candidate_count": 48,
5: "candidate_universe": "All shared_B rows crossed with all reverse_partner rows having the same role_pair.",
```

### `notes/g60_overlay_generator_family_reading_015.md`

- score: `66`
- reasons: `Gap A=1, gap a=1, gap-a=1, shared_B=30, candidate=23, path_gap`

```
6:
7: - G60 overlay artifact: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`
8:
```

```
12: - edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
13: - label_counts: `{'reverse_partner': 12, 'shared_B': 12}`
14: - form_counts: `{'0': 6, '1': 6, '2': 6, '3': 6}`
```

### `artifacts/json/import_project18_native_chain_010.v1.json`

- score: `62`
- reasons: `Gap A=1, gap a=1, gap-a=36, A/B assignment=1, selector=12, candidate=1, path_gap`

```
2: "audit_id": "010",
3: "boundary": "This is an import manifest only. It does not test a generator and does not close Gap A.",
4: "copied_json": [
```

```
6: "bytes": 31101,
7: "dest": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_generator_input_bundle_001.v1.json",
8: "sha256": "d9ad376911b03cad2aa0f9214b5372de78135ca6fa3b72e56da5f3478f9771ee",
```

### `scripts/sharedB_16_candidate_selector_search_023.py`

- score: `60`
- reasons: `shared_B=2, selector=6, candidate=37, path_gap, path_selector`

```
9: IN_G60_OVERLAY = ROOT / "source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json"
10: IN_022 = ROOT / "artifacts/json/sharedB_candidate_universe_boundary_022.v1.json"
11:
```

```
11:
12: OUT_JSON = ROOT / "artifacts/json/sharedB_16_candidate_selector_search_023.v1.json"
13: OUT_NOTE = ROOT / "notes/sharedB_16_candidate_selector_search_023.md"
```

### `scripts/synthetic_pair_skeleton_universe_003.py`

- score: `59`
- reasons: `Gap A=1, gap a=1, shared_B=4, A/B assignment=2, realized rows=2, synthetic=17, transition keys=1, selector=2, candidate=14, path_gap, path_synthetic`

```
7:
8: IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
9: IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
```

```
10:
11: OUT_JSON = ROOT / "artifacts/json/synthetic_pair_skeleton_universe_003.v1.json"
12: OUT_NOTE = ROOT / "notes/synthetic_pair_skeleton_universe_003.md"
```

### `scripts/native_shell_rank_derivation_027.py`

- score: `58`
- reasons: `Gap A=1, gap a=1, shared_B=1, role-labeled shared_B=1, selector=27, candidate=17, path_gap`

```
52: if got:
53: accepted.append(r["candidate_index"])
54: if got and actual:
```

```
57: fp += 1
58: false_pos.append(r["candidate_index"])
59: elif not got and actual:
```

### `artifacts/json/triangle_frame_synthetic_reduction_audit_007.v1.json`

- score: `57`
- reasons: `Gap A=1, gap a=1, gap-a=2, A/B assignment=2, realized rows=1, synthetic=18, transition keys=1, selector=2, candidate=14, path_gap, path_synthetic`

```
2: "audit_id": "007",
3: "boundary": "This is not Gap A closure. It uses selected transition keys from 002 and realized rows only for evaluation. It shows that triangle-frame closure alone does not solve the synthetic overgeneration problem.",
4: "input_realized_rows_for_evaluation_only": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1...
```

```
3: "boundary": "This is not Gap A closure. It uses selected transition keys from 002 and realized rows only for evaluation. It shows that triangle-frame closure alone does not solve the synthetic overgeneration problem.",
4: "input_realized_rows_for_evaluation_only": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1...
5: "input_selector_002": "/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/json/admission_blind_row_pair_selector_002.v1.json",
```

### `notes/source_artifact_schema_inventory_009.md`

- score: `57`
- reasons: `Gap A=1, gap a=1, shared_B=24, selector=12, candidate=9, path_gap`

```
51: - needle_hit_count: `189`
52: - top_keys: `['boundary', 'input', 'interpretation', 'name', 'reverse_partner_matches', 'reverse_partner_misses', 'reverse_partner_row_count', 'reverse_partner_swap_BC_exact', 'reverse_partner_swap_BC_match_count', 'reve...
53: - records: `reverse_partner_matches` count `12`
```

```
54: - sample_keys: `['from_ABC', 'matches', 'predicted_to_ABC', 'station_role', 'to_ABC']`
55: - records: `shared_B_by_role.IW.items` count `4`
56: - sample_keys: `['B_preserved', 'delta_ABC_mod15', 'from_ABC', 'role_pair', 'rows', 'slot_preserved', 'station_role', 'to_ABC']`
```

### `scripts/triangle_frame_synthetic_reduction_audit_007.py`

- score: `56`
- reasons: `Gap A=1, gap a=1, shared_B=5, A/B assignment=2, realized rows=1, synthetic=20, transition keys=1, selector=2, candidate=8, path_gap, path_synthetic`

```
7:
8: IN_002 = ROOT / "artifacts/json/admission_blind_row_pair_selector_002.v1.json"
9: IN_ROWS = ROOT / "source/project18_artifacts/json/wxyzti_same_sheet_wrap_carry_audit_012.v1.json"
```

```
10:
11: OUT_JSON = ROOT / "artifacts/json/triangle_frame_synthetic_reduction_audit_007.v1.json"
12: OUT_NOTE = ROOT / "notes/triangle_frame_synthetic_reduction_audit_007.md"
```
