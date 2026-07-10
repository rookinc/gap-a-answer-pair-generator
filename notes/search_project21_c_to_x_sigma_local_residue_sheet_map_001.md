# Search Project 21 C to x_sigma local-residue sheet map 001

## Keeper

The address grammar is known. Recover the missing sheet without looking at the sign.

## Summary

- search_pass: True
- verdict: `partial_endpoint_local_sheet_rule_candidate_found`
- tested_sheet_rule_pair_count: 4096
- exact_sheet_rule_count: 0
- exact_sheet_rule_found: False
- best_matched_node_count: 3
- best_unique_row_node_count: 3
- best_mapped_transition_count: 0
- best_external_column_count: 0

## Best candidate

```json
{
  "from_coefficients": [
    0,
    3,
    2
  ],
  "to_coefficients": [
    1,
    2,
    0
  ],
  "from_rule": "q_from = (a0 + a_slot*from_slot + a_C*from_C) mod 4",
  "to_rule": "q_to = (b0 + b_slot*to_slot + b_C*to_C) mod 4",
  "matched_node_count": 3,
  "unique_row_node_count": 3,
  "kind_correct_node_count": 3,
  "external_node_count": 12,
  "external_column_count": 0,
  "internal_node_count": 12,
  "mapped_transition_count": 0,
  "direct_hit_nodes_matched": 0,
  "full_node_replay": false,
  "full_transition_replay": false
}
```

## Boundary

- Endpoint-local affine sheet-rule search only.
- No full four-coordinate affine rule tested here.
- Role-hook-change bits excluded.
- Cocycle values remain sealed.
- No blind bit comparison completed.
- No sheet rule admission.
- No feedback unit admission.
- No transport-feedback rule admission.
- No native signed-lift identification.
- No cocycle admission.
- No holonomy-class admission.
- No source law admission.
- No native generator admission.
- No full theorem admitted.
- No proof claim.
- No Gap A closure.
- No geometry claim.
- No physics claim.
- No force claim.

Recommended next: `inspect_best_project21_sheet_rule_residual_001`
