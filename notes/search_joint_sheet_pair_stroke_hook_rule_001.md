# Search joint sheet-pair stroke-hook rule 001

## Keeper

Two threads do not make a stitch. The stroke hooks them into closure.

## Summary

- search_pass: true
- verdict: `partial_joint_sheet_pair_stroke_hook_candidate_found`
- tested_candidate_count: 131072
- exact_candidate_count: 0
- exact_candidate_found: False
- best_orientation: direct
- best_matched_node_count: 2
- best_unique_row_node_count: 2
- best_mapped_transition_count: 0

## Best candidate

```json
{
  "orientation": "direct",
  "stroke_coefficients": [
    0,
    0,
    0,
    0,
    0
  ],
  "top_thread_sign": 1,
  "bottom_thread_sign": 1,
  "top_thread_offset": 1,
  "bottom_thread_offset": 3,
  "matched_node_count": 2,
  "unique_row_node_count": 2,
  "external_column_count": 0,
  "mapped_transition_count": 0,
  "direct_hit_nodes_matched": 0,
  "full_node_replay": false,
  "full_transition_replay": false
}
```

## Boundary

- Joint sheet-pair and stroke-hook search only.
- Shared four-state stroke phase tested.
- Top and bottom thread sheets derived from the same stroke.
- Role-hook-change bits excluded.
- Cocycle values remain sealed.
- No stroke, sheet, feedback, cocycle, theorem, or Gap A admission.

Recommended next: `inspect_best_joint_sheet_pair_stroke_hook_residual_001`
