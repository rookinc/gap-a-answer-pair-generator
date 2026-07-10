# Test centroid-normalized direction limit on slot/C register 001

Status: `CENTROID_NORMALIZED_DIRECTION_LIMIT_SLOT_C_REGISTER_001_PROXY_PASS_TOLERANCE`

## Keeper

The limit is not where the point began. It is the direction that survives normalization.

## Summary

- test_pass: `True`
- test_scope: `full_6561_regenerated_slot_c_register`
- local_i_point_count: `6561`
- t_values: `[1, 2, 5, 10, 100, 1000]`
- centroid_0: `[6.666666666667, 6.666666666667, 6.666666666667, 6.666666666667]`
- direction_mean: `[-0.0, -0.0, -0.0, -0.0]`
- finite_scaled_formula_max_error: `1.776e-15`
- status_scaled_centroid_formula_max_error: `1.000089e-12`
- tolerance: `1e-09`
- direction_limit_proxy_pass: `True`
- supports_T2_direction_limit: `True`
- theorem_admitted: `False`
- proof_claim: `False`
- gap_a_closure: `False`
- recommended_next: `compare_slot_c_proxy_embedding_to_native_g15_001`

## Repair note

The initial run failed strict zero checks because of floating-point roundoff. The maximum errors are below tolerance.

## Boundary

- Finite direction-limit test.
- Slot/C numeric proxy only.
- Tolerance repair only.
- No theorem admitted.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No source law admission.
- No physics claim.
- No force claim.
