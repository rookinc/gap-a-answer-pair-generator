# Search role-hook transition to G15 edge map 001

## Keeper

The native ruler is in the room. Place the candidate against it without looking at the marks.

## Summary

- search_pass: True
- verdict: `no_exact_low_complexity_transition_to_g15_edge_map_found`
- node_count: 24
- transition_count: 28
- native_edge_count: 30
- tested_projection_count: 612
- exact_structural_map_count: 0
- exact_structural_map_found: False

## Best candidate

```json
{
  "name": "affine_0_1_0_-1_plus_9",
  "kind": "low_complexity_affine_mod15",
  "formula": {
    "coefficients": [
      0,
      1,
      0,
      -1
    ],
    "offset": 9,
    "modulus": 15
  },
  "valid_native_edge_count": 14,
  "invalid_edge_count": 14,
  "loop_count": 0,
  "unique_vertex_count": 10,
  "unique_mapped_edge_count": 13,
  "exact_structural_map": false
}
```

## Boundary

- Blind structural edge-map search only.
- Role-hook-change bits excluded from map construction.
- Native cocycle bits excluded from map construction.
- Crossed/parallel labels excluded from map construction.
- Cycle residues excluded from map construction.
- No bit comparison completed.
- No feedback unit admission.
- No transport-feedback rule admission.
- No native signed-lift identification.
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

Recommended next: `search_upstream_transition_to_g15_edge_provenance_001`
