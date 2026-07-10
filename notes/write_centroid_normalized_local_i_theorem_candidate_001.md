# Centroid-normalized local-I theorem candidate 001

Status: `CENTROID_NORMALIZED_LOCAL_I_THEOREM_CANDIDATE_001_WRITTEN_BOUNDED`

## Keeper

The theorem candidate can speak, but it cannot outrun its boundary.

## Informal statement

In the Project 21 slot/C register, if each local-I candidate is represented by the 4-coordinate proxy vector (from_slot, to_slot, from_C, to_C), then the full 6561-point candidate register has a stable centroid, local-t extension is centroid-accountable, and the centroid-normalized scaled direction has an exact finite proxy limit up to floating tolerance. On the observed native-chain packet layer, the proxy law-key coordinates agree with the native-chain key coordinates and share the observed centroid.

## Formal candidate statement

- Let R be the 6561-point slot/C candidate register.
- Let x in R be represented by the proxy coordinate vector p(x) = (from_slot, to_slot, from_C, to_C).
- Let C be the arithmetic centroid of all p(x) over R.
- For each x, define d(x) = p(x) - C.
- For local parameter t, define p_t(x) = p(x) + t d(x).
- Then the full-register centroid of p_t is C for tested t values.
- The centered scaled expression (p_t(x) - C) / t obeys the finite proxy direction formula recorded in the direction-limit audit.
- The native-chain observed packet layer has law-key coordinates matching the same slot/C proxy coordinate form.
- Therefore centroid normalization gives a common local-I comparison frame for the slot/C register, bounded to proxy coordinate status.

## Supported tracks

- `T1_local_t_centroid_normalization`
- `T2_direction_limit_proxy`
- `T3_g15_local_i_comparability_proxy`
- `T4_slot_c_register_partition`

## Boundary

- Slot/C numeric proxy only.
- Native-chain key-coordinate agreement recorded.
- Unique native G15 embedding not proven.
- Metric status not admitted.
- Full theorem not admitted.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No source law admission.
- No physics claim.
- No force claim.

## Recommended next

`audit_centroid_normalized_local_i_candidate_boundaries_001`
