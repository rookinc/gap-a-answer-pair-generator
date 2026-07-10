# Define G15 centroid for local-I register 001

Status: `G15_CENTROID_FOR_LOCAL_I_REGISTER_001_DEFINED`

## Keeper

The centroid does not replace I. It lets every I tell the truth about its drift.

## Definition candidate

Given a finite local-I register embedded in G15-coordinate space, the G15 centroid is the arithmetic mean of the embedded local-I coordinate vectors over the selected normalization domain.

- formula_candidate: `C_G15 = (1/N) sum_i v_i`
- normalized_local_i_formula_candidate: `I_i_norm = v_i - C_G15`

## Summary

- definition_pass: `True`
- candidate_key_count: `6561`
- observed_receipted: `24`
- proxy_invalid: `1365`
- hard_absence_gate_absent: `5172`
- theorem_admitted: `False`
- proof_claim: `False`
- gap_a_closure: `False`
- recommended_next: `embed_slot_c_local_i_points_in_g15_coordinates_001`

## Boundary

- Definition artifact only.
- No theorem admitted.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No source law admission.
- No physics claim.
- No force claim.
