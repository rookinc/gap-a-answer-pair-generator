# Test slot/C proxy embedding uniqueness against native G15 001

Status: `SLOT_C_PROXY_EMBEDDING_UNIQUENESS_AGAINST_NATIVE_G15_001_BOUNDED_NEGATIVE`

## Keeper

The labels hold the frame; the unlabeled centroid does not.

## Summary

- test_pass: `True`
- test_family: `coordinate_permutations_of_slot_c_proxy_fields`
- permutation_count: `24`
- strict_field_anchor_unique: `True`
- centroid_preserving_perm_count: `24`
- non_identity_centroid_preserving_alternative_count: `23`
- unlabeled_centroid_uniqueness_fails: `True`
- unique_native_g15_embedding_proven: `False`
- native_embedding_status: `not_unique_in_unlabeled_centroid_family_field_anchor_required`
- recommended_next: `test_slot_c_proxy_embedding_field_anchor_invariants_001`

## Interpretation

Field-anchored coordinates are unique by declared labels, but unlabeled centroid-preserving alternatives exist in the tested permutation family. Therefore native G15 uniqueness is not proven.

## Boundary

- Bounded uniqueness probe only.
- Field-anchored uniqueness is not native uniqueness.
- Unlabeled centroid uniqueness fails in the tested family.
- No full theorem admitted.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No source law admission.
- No metric geometry claim.
- No physics claim.
- No force claim.
