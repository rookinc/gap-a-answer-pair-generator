# Context-dependent endpoint profile 016

Status: context_dependent_endpoint_profile_recorded

## Input

- G60 overlay artifact: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`
- row_count: `24`

## Search

- source_test_count: `3278`
- extended_test_count: `5159`
- source_exact_count: `1460`
- extended_exact_count: `2615`
- endpoint_source_exact_count: `130`
- endpoint_extended_exact_count: `219`

## Best source-only endpoint tests

- features=`['edge_index', 'from_A']`, groups=`24`
- features=`['edge_index', 'from_columns']`, groups=`24`
- features=`['edge_index', 'from_key']`, groups=`24`
- features=`['edge_role', 'form_index']`, groups=`24`
- features=`['edge_role', 'from_A']`, groups=`24`
- features=`['edge_role', 'from_columns']`, groups=`24`
- features=`['edge_role', 'from_key']`, groups=`24`
- features=`['form_index', 'edge_index']`, groups=`24`
- features=`['form_index', 'from_key']`, groups=`24`
- features=`['label', 'from_key']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_B']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_C']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_columns']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_fiber']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_key']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_slot']`, groups=`24`
- features=`['edge_index', 'from_B', 'from_C']`, groups=`24`
- features=`['edge_index', 'from_B', 'from_columns']`, groups=`24`
- features=`['edge_index', 'from_B', 'from_fiber']`, groups=`24`
- features=`['edge_index', 'from_B', 'from_key']`, groups=`24`

## Best extended endpoint tests

- features=`['edge_index', 'from_A']`, groups=`24`
- features=`['edge_index', 'from_columns']`, groups=`24`
- features=`['edge_index', 'from_key']`, groups=`24`
- features=`['edge_role', 'form_index']`, groups=`24`
- features=`['edge_role', 'from_A']`, groups=`24`
- features=`['edge_role', 'from_columns']`, groups=`24`
- features=`['edge_role', 'from_key']`, groups=`24`
- features=`['form_index', 'edge_index']`, groups=`24`
- features=`['form_index', 'from_key']`, groups=`24`
- features=`['from_A', 'fiber_delta_mod60']`, groups=`24`
- features=`['from_columns', 'fiber_delta_mod60']`, groups=`24`
- features=`['from_key', 'fiber_delta_mod60']`, groups=`24`
- features=`['from_key', 'slot_delta_mod15']`, groups=`24`
- features=`['label', 'from_key']`, groups=`24`
- features=`['edge_index', 'from_A', 'fiber_delta_mod60']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_B']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_C']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_columns']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_fiber']`, groups=`24`
- features=`['edge_index', 'from_A', 'from_key']`, groups=`24`

## Best source-only component tests

- target: `to_endpoint`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
  - features=`['edge_role', 'form_index']`, groups=`24`
  - features=`['edge_role', 'from_A']`, groups=`24`
- target: `to_ABC`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
  - features=`['edge_role', 'form_index']`, groups=`24`
  - features=`['edge_role', 'from_A']`, groups=`24`
- target: `to_key`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
  - features=`['edge_role', 'form_index']`, groups=`24`
  - features=`['edge_role', 'from_A']`, groups=`24`
- target: `to_columns`
  - features=`['form_index', 'from_B']`, groups=`12`
  - features=`['form_index', 'from_slot']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
- target: `to_fiber`
  - features=`['form_index', 'from_C']`, groups=`12`
  - features=`['form_index', 'from_fiber']`, groups=`12`
  - features=`['role_pair', 'form_index']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
- target: `to_A`
  - features=`['form_index', 'from_B']`, groups=`12`
  - features=`['form_index', 'from_slot']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
- target: `to_B`
  - features=`['form_index', 'from_A']`, groups=`12`
  - features=`['form_index', 'from_columns']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
- target: `to_C`
  - features=`['form_index', 'from_C']`, groups=`12`
  - features=`['form_index', 'from_fiber']`, groups=`12`
  - features=`['role_pair', 'form_index']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
- target: `to_slot`
  - features=`['form_index', 'from_A']`, groups=`12`
  - features=`['form_index', 'from_columns']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
- target: `fiber_delta_mod60`
  - features=`['form_index', 'from_C']`, groups=`12`
  - features=`['form_index', 'from_fiber']`, groups=`12`
  - features=`['role_pair', 'form_index']`, groups=`12`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
- target: `slot_delta_mod15`
  - features=`['edge_index', 'from_A']`, groups=`24`
  - features=`['edge_index', 'from_columns']`, groups=`24`
  - features=`['edge_index', 'from_key']`, groups=`24`
  - features=`['edge_role', 'form_index']`, groups=`24`
  - features=`['edge_role', 'from_A']`, groups=`24`

## Label law checks

- label: `reverse_partner`
  - row_count: `12`
  - edge_role_counts: `{'TI': 4, 'WX': 4, 'YZ': 4}`
  - A_preserved_count: `12`
  - B_preserved_count: `0`
  - C_preserved_count: `0`
  - slot_preserved_count: `0`
  - fiber_mod15_tracks_C_count: `12`
  - reverse_swap_BC_count: `12`
  - shared_B_face_count: `0`
  - from_columns_equal_to_columns_count: `12`
- label: `shared_B`
  - row_count: `12`
  - edge_role_counts: `{'IW': 4, 'XY': 4, 'ZT': 4}`
  - A_preserved_count: `0`
  - B_preserved_count: `12`
  - C_preserved_count: `0`
  - slot_preserved_count: `12`
  - fiber_mod15_tracks_C_count: `12`
  - reverse_swap_BC_count: `0`
  - shared_B_face_count: `12`
  - from_columns_equal_to_columns_count: `0`

## Role rows

- role=`IW`, label_counts=`{'shared_B': 4}`, from_C=`[1, 2, 5]`, to_C=`[0, 2, 10, 14]`
- role=`TI`, label_counts=`{'reverse_partner': 4}`, from_C=`[2, 4, 11, 13]`, to_C=`[1, 2, 5]`
- role=`WX`, label_counts=`{'reverse_partner': 4}`, from_C=`[0, 2, 10, 14]`, to_C=`[2, 4, 11, 13]`
- role=`XY`, label_counts=`{'shared_B': 4}`, from_C=`[2, 4, 11, 13]`, to_C=`[1, 2, 5]`
- role=`YZ`, label_counts=`{'reverse_partner': 4}`, from_C=`[1, 2, 5]`, to_C=`[0, 2, 10, 14]`
- role=`ZT`, label_counts=`{'shared_B': 4}`, from_C=`[0, 2, 10, 14]`, to_C=`[2, 4, 11, 13]`

## Role-pair rows

- role_pair=`IW/YZ`, roles=`{'IW': 4, 'YZ': 4}`, transitions=`[(1, 10), (2, 14), (5, 0), (5, 2)]`
- role_pair=`TI/XY`, roles=`{'TI': 4, 'XY': 4}`, transitions=`[(2, 5), (4, 5), (11, 2), (13, 1)]`
- role_pair=`WX/ZT`, roles=`{'WX': 4, 'ZT': 4}`, transitions=`[(0, 2), (2, 4), (10, 13), (14, 11)]`

## Reading

This audit profiles the 24 G60 native overlay edge records as a context-dependent endpoint map. It does not search for one global permutation. Instead it asks which small context fields determine endpoint targets and records the exact visible laws for reverse_partner and shared_B rows.

## Boundary

This is a context profile over the already selected 24 edge records. It does not derive the 24 records from a candidate universe and does not close Gap A.
