# Search full law-key affine sheet rule 001

## Keeper

The sheet is not local to an endpoint. It may belong to the relation between endpoints.

## Summary

- search_pass: true
- verdict: `partial_full_law_key_affine_sheet_rule_candidate_found`
- endpoint_rule_count_per_orientation: 1024
- exact_sheet_rule_pair_count: 0
- exact_sheet_rule_found: False
- best_orientation: direct
- best_matched_node_count: 3
- best_unique_row_node_count: 3
- best_mapped_transition_count: 0

## Best candidate

```json
{
  "orientation": "direct",
  "from_coefficients": [
    0,
    0,
    1,
    2,
    1
  ],
  "to_coefficients": [
    1,
    0,
    0,
    0,
    1
  ],
  "from_endpoint_compatible_count": 23,
  "to_endpoint_compatible_count": 23,
  "matched_node_count": 3,
  "unique_row_node_count": 3,
  "external_column_count": 0,
  "mapped_transition_count": 0,
  "direct_hit_nodes_matched": 0,
  "full_node_replay": false,
  "full_transition_replay": false
}
```

## Boundary

- Full-law-key affine sheet-rule search only.
- Direct and reverse endpoint orientations tested.
- Role-hook-change bits excluded.
- Cocycle values remain sealed.
- No sheet rule admission.
- No feedback unit admission.
- No native signed-lift identification.
- No cocycle or Gap A closure claim.

Recommended next: `inspect_best_full_law_key_sheet_rule_residual_001`
