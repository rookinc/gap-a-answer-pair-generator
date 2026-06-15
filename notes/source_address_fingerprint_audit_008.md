# Source address fingerprint audit 008

Status: source_address_fingerprint_audit_recorded

## Schema

- selected_record_count: `12`
- shared_common_scalar_keys: `['A_same', 'B_same', 'C_delta', 'C_wrap_flag', 'base_delta_mod15', 'fiber_delta', 'fiber_delta_from_fields', 'fiber_delta_matches_canonical', 'fiber_mod15_delta', 'fiber_mod15_delta_equals_C_delta', 'fiber_mod30_delta', 'fiber_sheet15_delta', 'fiber_sheet30_delta', 'from_A', 'from_B', 'from_C', 'from_fiber', 'from_fiber_mod15', 'from_fiber_mod15_equals_from_C', 'from_fiber_mod30', 'from_fiber_sheet15', 'from_fiber_sheet30', 'from_slot', 'integer_C_delta', 'lift_q', 'path', 'predicted_fiber_delta_matches', 'predicted_fiber_delta_same_sheet', 'predicted_lift_q_from_wrap', 'predicted_lift_q_matches', 'q3_implies_sheet30_flip', 'role_class', 'role_pair', 'same_sheet15', 'same_sheet30', 'sheet15_delta_equals_lift_q', 'slot_delta', 'slot_same', 'source', 'station_role', 'to_A', 'to_B', 'to_C', 'to_fiber', 'to_fiber_mod15', 'to_fiber_mod15_equals_to_C', 'to_fiber_mod30', 'to_fiber_sheet15', 'to_fiber_sheet30', 'to_slot']`
- reverse_common_scalar_keys: `['A_same', 'B_same', 'C_delta', 'C_wrap_flag', 'base_delta_mod15', 'fiber_delta', 'fiber_delta_from_fields', 'fiber_delta_matches_canonical', 'fiber_mod15_delta', 'fiber_mod15_delta_equals_C_delta', 'fiber_mod30_delta', 'fiber_sheet15_delta', 'fiber_sheet30_delta', 'from_A', 'from_B', 'from_C', 'from_fiber', 'from_fiber_mod15', 'from_fiber_mod15_equals_from_C', 'from_fiber_mod30', 'from_fiber_sheet15', 'from_fiber_sheet30', 'from_slot', 'integer_C_delta', 'lift_q', 'path', 'predicted_fiber_delta_matches', 'predicted_fiber_delta_same_sheet', 'predicted_lift_q_from_wrap', 'predicted_lift_q_matches', 'q3_implies_sheet30_flip', 'role_class', 'role_pair', 'same_sheet15', 'same_sheet30', 'sheet15_delta_equals_lift_q', 'slot_delta', 'slot_same', 'source', 'station_role', 'to_A', 'to_B', 'to_C', 'to_fiber', 'to_fiber_mod15', 'to_fiber_mod15_equals_to_C', 'to_fiber_mod30', 'to_fiber_sheet15', 'to_fiber_sheet30', 'to_slot']`
- available_feature_count: `109`

## Fingerprint search

- direct_identity_count: `8`
- exact_test_count: `7606`
- strength_counts: `{'row_identity_like': 7194, 'weak': 412}`

## Strong exact tests

- none

## Medium exact tests

- none

## Weak exact tests first 20

- target=R.minus_S_from_A, features=['R.C_delta', 'S.from_B'], groups=11
- target=R.minus_S_from_A, features=['R.C_delta', 'S.from_slot'], groups=11
- target=R.minus_S_from_A, features=['R.C_delta', 'S.to_B'], groups=11
- target=R.minus_S_from_A, features=['R.C_delta', 'S.to_slot'], groups=11
- target=R.minus_S_from_A, features=['R.base_delta_mod15', 'S.from_B'], groups=11
- target=R.minus_S_from_A, features=['R.base_delta_mod15', 'S.from_slot'], groups=11
- target=R.minus_S_from_A, features=['R.base_delta_mod15', 'S.to_B'], groups=11
- target=R.minus_S_from_A, features=['R.base_delta_mod15', 'S.to_slot'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'R.role_pair'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'R.station_role'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.from_B'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.from_slot'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.role_pair'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.station_role'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.to_B'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'S.to_slot'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'pair.reverse_role'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'pair.role_pair'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta', 'pair.shared_role'], groups=11
- target=R.minus_S_from_A, features=['R.fiber_delta_from_fields', 'R.role_pair'], groups=11

## Reading

This audit asks whether the available realized source-row fields contain a compact address fingerprint for the free A/B assignment variables. Strong tests would suggest a low-dimensional selector already present in the copied source row schema. Weak or row-identity-like tests indicate the current row schema is not rich enough, or that the law lives in upstream provenance not included in this artifact.

## Boundary

This is a schema/fingerprint audit over realized selected rows. It is not a native generator and not Gap A closure. It only tests the fields available in the copied Project 18 row artifact.
