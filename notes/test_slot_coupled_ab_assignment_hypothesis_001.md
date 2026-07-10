# Test slot-coupled A/B assignment hypothesis 001

Status: `SLOT_COUPLED_AB_ASSIGNMENT_HYPOTHESIS_001_TEST_RECORDED`

## Keeper

Slot coupling may name the surface, but leakage audit decides whether it is law or residue.

## Summary

- test_pass: `True`
- candidate_row_count: `156`
- loaded_source_count: `3`
- analysis_count: `39`
- exact_hit_count: `6`
- hypothesis_result: `exact_mapping_found_on_observed_rows_not_admitted`
- best_features: `from_slot, to_slot, from_C, to_C`
- best_target: `ab_delta_pair`
- best_exact: `True`
- best_purity: `1.0`
- best_conflict_group_count: `0`
- allowed_input_used_only: `True`
- gap_a_closure: `False`
- native_generator_admitted: `False`
- ab_assignment_law_admitted: `False`
- answer_label_leakage_closed: `False`
- source_law_admitted: `False`
- recommended_next: `audit_slot_coupled_ab_assignment_for_answer_label_leakage_001`

## Best analysis

{
  "conflict_group_count": 0,
  "exact": true,
  "exact_group_count": 24,
  "example_conflicts": [],
  "features": [
    "from_slot",
    "to_slot",
    "from_C",
    "to_C"
  ],
  "group_count": 24,
  "max_group_target_count": 1,
  "purity": 1.0,
  "target": "ab_delta_pair",
  "usable_row_count": 156
}

## Boundary

- Hypothesis test only.
- No theorem.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No A/B assignment law admission.
- No full role-labeled shared_B derivation.
- No answer-label leakage closure.
- No source law admission.
- No physics claim.
- No force claim.
