# Shared_B residual selector profile 017

Status: sharedB_residual_selector_profile_recorded

## Input

- G60 overlay artifact: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`
- shared_B row_count: `12`

## Search

- source_test_count: `828`
- extended_test_count: `1575`
- source_exact_count: `530`
- extended_exact_count: `928`
- strength_counts_source: `{'not_exact': 298, 'row_identity_like': 530}`
- strength_counts_extended: `{'not_exact': 647, 'row_identity_like': 926, 'weak': 2}`

## Global shared_B laws

- B_preserved_count: `12`
- slot_preserved_count: `12`
- fiber_mod15_tracks_C_count: `12`
- columns_preserved_count: `0`

## Named tests

- edge_role_from_C_to_to_C: exact=`False`, strength=`not_exact`, groups=`11`, ambiguous=`1`
- edge_role_from_B_to_to_C: exact=`False`, strength=`not_exact`, groups=`11`, ambiguous=`1`
- edge_role_from_C_from_B_to_to_C: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- role_pair_from_C_from_B_to_to_C: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_A_to_to_A: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_B_to_to_A: exact=`False`, strength=`not_exact`, groups=`11`, ambiguous=`1`
- edge_role_from_A_from_B_to_to_A: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- role_pair_from_A_from_B_to_to_A: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_columns_to_to_columns: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- role_pair_from_columns_to_to_columns: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_C_from_columns_to_to_columns: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_C_from_B_to_reduced_endpoint: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_A_from_B_to_reduced_endpoint: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`
- edge_role_from_columns_to_reduced_endpoint: exact=`True`, strength=`row_identity_like`, groups=`12`, ambiguous=`0`

## Compact source exact tests first 40

- none

## Best exact tests by target

- target: `to_A`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `to_C`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `to_columns`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `to_fiber`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `to_A_to_C`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `to_endpoint_reduced`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `A_delta_mod15`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`
- target: `C_delta_mod15`
  - features=`['edge_role', 'from_B']`, strength=`row_identity_like`, groups=`11`
  - features=`['edge_role', 'from_slot']`, strength=`row_identity_like`, groups=`11`
  - features=`['role_pair', 'from_B']`, strength=`row_identity_like`, groups=`11`
  - features=`['role_pair', 'from_slot']`, strength=`row_identity_like`, groups=`11`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
- target: `columns_change`
  - features=`['edge_role', 'from_A']`, strength=`row_identity_like`, groups=`12`
  - features=`['edge_role', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_C']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_columns']`, strength=`row_identity_like`, groups=`12`
  - features=`['from_B', 'from_fiber']`, strength=`row_identity_like`, groups=`12`

## Role rows

- role=`IW`, transitions=`[(1, 10), (2, 14), (5, 0), (5, 2)]`, A_delta_counts=`{'4': 1, '6': 1, '7': 1, '8': 1}`, C_delta_counts=`{'10': 1, '12': 2, '9': 1}`
- role=`XY`, transitions=`[(2, 5), (4, 5), (11, 2), (13, 1)]`, A_delta_counts=`{'11': 1, '6': 1, '9': 2}`, C_delta_counts=`{'1': 1, '3': 2, '6': 1}`
- role=`ZT`, transitions=`[(0, 2), (2, 4), (10, 13), (14, 11)]`, A_delta_counts=`{'13': 2, '2': 2}`, C_delta_counts=`{'12': 1, '2': 2, '3': 1}`

## Shared_B rows

- role=`IW`, transition=`(1, 10)`, from_ABC=`(2, 13, 1)`, to_ABC=`(9, 13, 10)`, columns=`[4, 9] -> [28, 29]`
- role=`IW`, transition=`(2, 14)`, from_ABC=`(1, 11, 2)`, to_ABC=`(7, 11, 14)`, columns=`[4, 5] -> [23, 24]`
- role=`IW`, transition=`(5, 0)`, from_ABC=`(12, 2, 5)`, to_ABC=`(1, 2, 0)`, columns=`[8, 18] -> [0, 4]`
- role=`IW`, transition=`(5, 2)`, from_ABC=`(10, 4, 5)`, to_ABC=`(3, 4, 2)`, columns=`[13, 17] -> [7, 10]`
- role=`XY`, transition=`(2, 5)`, from_ABC=`(1, 0, 2)`, to_ABC=`(10, 0, 5)`, columns=`[0, 4] -> [2, 17]`
- role=`XY`, transition=`(4, 5)`, from_ABC=`(3, 2, 4)`, to_ABC=`(12, 2, 5)`, columns=`[7, 10] -> [8, 18]`
- role=`XY`, transition=`(11, 2)`, from_ABC=`(7, 14, 11)`, to_ABC=`(3, 14, 2)`, columns=`[23, 24] -> [7, 12]`
- role=`XY`, transition=`(13, 1)`, from_ABC=`(9, 10, 13)`, to_ABC=`(0, 10, 1)`, columns=`[28, 29] -> [0, 2]`
- role=`ZT`, transition=`(0, 2)`, from_ABC=`(10, 5, 0)`, to_ABC=`(12, 5, 2)`, columns=`[2, 17] -> [8, 18]`
- role=`ZT`, transition=`(2, 4)`, from_ABC=`(12, 5, 2)`, to_ABC=`(10, 5, 4)`, columns=`[8, 18] -> [13, 17]`
- role=`ZT`, transition=`(10, 13)`, from_ABC=`(0, 1, 10)`, to_ABC=`(2, 1, 13)`, columns=`[0, 2] -> [4, 9]`
- role=`ZT`, transition=`(14, 11)`, from_ABC=`(3, 2, 14)`, to_ABC=`(1, 2, 11)`, columns=`[7, 12] -> [4, 5]`

## Reading

This audit isolates the shared_B residual after reverse_partner has been treated as solved. It searches for compact context-dependent selectors for to_A, to_C, to_columns, and the reduced endpoint, while excluding row-id fields such as edge_index, form_index, and from_key. Compact exact tests suggest reusable structure; row-identity-like tests suggest the remaining selector still needs a native candidate universe or additional provenance.

## Boundary

This is a residual profile over the 12 already selected shared_B rows. It does not derive shared_B from a candidate universe and does not close Gap A.
