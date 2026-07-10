# Search seeded Z4 stroke memory against x_sigma 001

## Keeper

The hand chooses the first thread state. The seam decides whether that choice closes.

## Summary

- search_pass: true
- verdict: `partial_seeded_z4_stroke_memory_candidate_found`
- tested_candidate_count: 21504
- exact_candidate_count: 0
- exact_candidate_found: False
- best_matched_node_count: 2
- best_unique_row_node_count: 2
- best_mapped_transition_count: 0
- best_closure_defect_count: 0

## Best candidate

```json
{
  "orientation": "direct",
  "increment_feature": "source_cross_equal_xor",
  "increment_multiplier": 1,
  "q_to_offset": 0,
  "component_seeds": [
    0,
    2,
    2
  ],
  "matched_node_count": 2,
  "unique_row_node_count": 2,
  "external_column_count": 0,
  "mapped_transition_count": 0,
  "closure_defect_count": 0,
  "closure_defects": [],
  "full_node_replay": false,
  "full_transition_replay": false
}
```

## Boundary

- Seeded Z4 transition-memory search only.
- One held seed per observed component.
- Single audited transition bit used as increment source.
- Native cocycle values remain sealed.
- No seeded rule, feedback, cocycle, theorem, or Gap A admission.

Recommended next: `inspect_best_seeded_z4_stroke_memory_residual_001`
