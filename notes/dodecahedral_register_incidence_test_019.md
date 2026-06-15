# Dodecahedral register incidence test 019

Status: dodecahedral_register_incidence_test_recorded

## Strict full-register test

- verdict: `full_dodecahedral_register_not_proven_from_observed_overlay_window`
- observed_column_count: `16`
- observed_missing_column_count: `14`
- observed_missing_columns: `[1, 3, 6, 11, 14, 15, 16, 19, 20, 21, 22, 25, 26, 27]`
- observed_distinct_column_pair_count: `11`
- observed_column_adjacency_edge_count: `11`
- observed_column_degree_counts: `{'1': 11, '2': 4, '3': 1}`
- observed_column_max_degree: `3`
- full_30_column_register_covered: `False`
- full_line_graph_edge_count_covered: `False`
- partial_degree_bound_pass: `True`

## Shadow test

- verdict: `strong_dodecahedral_register_shadow_signal`
- pass_count: `9 / 9`

- columns_inside_0_29: `True`
- column_pairs_are_two_distinct_columns: `True`
- partial_column_adjacency_degree_bound_pass: `True`
- reverse_partner_preserves_column_pair: `True`
- shared_B_changes_column_pair: `True`
- shared_B_from_to_are_reverse_anchors: `True`
- shared_motion_edge_count_matches_answer_pair_count: `True`
- shared_motion_has_three_weak_components: `True`
- shared_motion_closes_into_nontrivial_sccs: `True`

## Reverse anchors

- reverse_row_count: `12`
- reverse_anchor_count: `12`
- reverse_distinct_anchor_count: `11`
- reverse_columns_preserved_exact: `True`

## Shared_B column motion

- shared_row_count: `12`
- shared_motion_count: `12`
- shared_columns_changed_exact: `True`
- shared_from_subset_of_reverse_anchors: `True`
- shared_to_subset_of_reverse_anchors: `True`

- role=`XY`, transition=`(11, 2)`, columns=`[23,24] -> [7,12]`
- role=`ZT`, transition=`(14, 11)`, columns=`[7,12] -> [4,5]`
- role=`IW`, transition=`(2, 14)`, columns=`[4,5] -> [23,24]`
- role=`XY`, transition=`(13, 1)`, columns=`[28,29] -> [0,2]`
- role=`ZT`, transition=`(10, 13)`, columns=`[0,2] -> [4,9]`
- role=`IW`, transition=`(1, 10)`, columns=`[4,9] -> [28,29]`
- role=`XY`, transition=`(2, 5)`, columns=`[0,4] -> [2,17]`
- role=`ZT`, transition=`(0, 2)`, columns=`[2,17] -> [8,18]`
- role=`IW`, transition=`(5, 0)`, columns=`[8,18] -> [0,4]`
- role=`XY`, transition=`(4, 5)`, columns=`[7,10] -> [8,18]`
- role=`ZT`, transition=`(2, 4)`, columns=`[8,18] -> [13,17]`
- role=`IW`, transition=`(5, 2)`, columns=`[13,17] -> [7,10]`

## Shared_B motion graph

- node_count: `11`
- directed_edge_count: `12`
- weak_component_count: `3`
- scc_count: `3`
- all_nodes_in_nontrivial_scc: `True`
- weak_components: `[['[0,2]', '[28,29]', '[4,9]'], ['[0,4]', '[13,17]', '[2,17]', '[7,10]', '[8,18]'], ['[23,24]', '[4,5]', '[7,12]']]`
- sccs: `[['[0,2]', '[28,29]', '[4,9]'], ['[23,24]', '[4,5]', '[7,12]'], ['[0,4]', '[13,17]', '[2,17]', '[7,10]', '[8,18]']]`

## Interpretation

This audit distinguishes a full dodecahedral edge-register proof from a local register-shadow signal. The observed overlay does not cover all 30 columns or the full dodecahedral line graph. However, reverse_partner rows preserve column-pair anchors, shared_B rows move between those anchors, and shared_B column motion closes as a directed graph over the reverse anchors. This supports a dodecahedral-register shadow hypothesis while leaving the full cell/register incidence derivation open.

## Next needed

- Locate or construct the full 30-column dodecahedral edge register.
- Account for the 14 unseen columns in the current overlay window.
- Determine whether the 11 observed column-pair anchors are a quotient/subwindow of a 30-edge register.
- Derive shared_B column motion from full register incidence rather than from selected rows.
- Explain how this register shadow relates to the strong {5,3,4}-type signal in audit 018.

## Boundary

This is an incidence-shadow test over observed overlay rows. It is not a full dodecahedral cell decomposition, not a literal {5,3,4} proof, and not Gap A closure.
