# Audit longer-cycle feedback candidate for switching invariance 001

## Keeper

A point distinguishes. An edge relates. A path carries. A cycle answers.

## Summary

- audit_pass: True
- verdict: `cycle_residue_candidates_are_switching_invariant_and_collapse_to_cohomology_signatures`
- node_count: 24
- edge_count: 28
- component_count: 3
- simple_cycle_count: 7
- cycle_rank_expected: 7
- cycle_matrix_rank: 7
- cycle_basis_complete: True
- audited_feedback_candidate_count: 11
- cohomology_signature_count: 5
- nontrivial_candidate_class_count: 4
- all_candidate_rotation_invariant: True
- all_candidate_tested_switching_invariant: True

## Leading candidate

```json
{
  "feature": "role_hook_change",
  "edge_one_count": 27,
  "cycle_residue_vector": [
    0,
    0,
    0,
    0,
    1,
    0,
    1
  ],
  "cycle_residue_bitstring": "0000101",
  "nontrivial_cycle_residue": true,
  "both_cycle_residues_seen": true,
  "rotation_invariant": true,
  "tested_switching_invariant": true,
  "tested_gauge_count": 4
}
```

## Signature groups

- `0000000`: source_cross_equal_xor, source_delta_equal, target_delta_equal
- `0000100`: source_c_wrap, target_c_wrap, transition_c_wrap
- `0000101`: role_hook_change
- `0001000`: source_delta_parity_xor, source_slot_c_order_xor, target_delta_parity_xor, transition_wrap_xor
- `0001100`: source_slot_wrap, target_slot_wrap, transition_slot_wrap

## Boundary

- Switching and cycle-space invariance audit only.
- Observed transition graph only.
- Tested feature family only.
- No feedback unit admission.
- No transport-feedback rule admission.
- No native cocycle admission.
- No holonomy-class admission.
- No upstairs/downstairs identification.
- No channel-axis rule admission.
- No source law admission.
- No native generator admission.
- No unique native G15 embedding proof.
- No full theorem admitted.
- No proof claim.
- No Gap A closure.
- No geometry claim.
- No physics claim.
- No force claim.

Recommended next: `audit_role_hook_change_feedback_candidate_native_provenance_001`
