# Native chain schema inspection 011

Status: native_chain_schema_inspection_recorded

## Source

- file_count: `17`
- global_needle_counts: `{'C_delta': 49, 'fiber': 130, 'from_A': 13, 'from_B': 24, 'from_C': 194, 'lift_q': 51, 'native': 3, 'q0': 71, 'q3': 84, 'role_class': 10, 'role_pair': 38, 'rule': 90, 'slot': 50, 'source': 10, 'station_role': 14, 'support': 57, 'to_A': 13, 'to_B': 15, 'to_C': 130, 'transition': 137, 'vertex': 35}`

## Top ranked files

- `c_transition_overlay_delta_generator_001.v1.json`
  - score: `112`
  - top_keys: `['boundary', 'checks', 'predictions', 'purpose', 'rule_members', 'schema', 'status', 'summary', 'timestamp_utc']`
  - needle_counts: `{'fiber': 39, 'from_A': 12, 'from_B': 12, 'from_C': 36, 'rule': 86, 'slot': 36, 'to_A': 12, 'to_B': 12, 'to_C': 36, 'transition': 43}`
  - records: `rule_members.(0, 2)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
  - records: `rule_members.(1, 10)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
  - records: `rule_members.(2, 4)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
  - records: `rule_members.(2, 5)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
  - records: `rule_members.(2, 14)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
  - records: `rule_members.(4, 5)` count `2`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_slot']`
- `from_c_lift_q_overlay_delta_formula_001.v1.json`
  - score: `56`
  - top_keys: `['boundary', 'checks', 'members_by_from_c', 'predictions', 'purpose', 'schema', 'status', 'summary', 'timestamp_utc']`
  - needle_counts: `{'fiber': 3, 'from_C': 123, 'rule': 3, 'to_C': 1}`
  - records: `members_by_from_c.0` count `2`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
  - records: `members_by_from_c.1` count `2`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
  - records: `members_by_from_c.2` count `6`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
  - records: `members_by_from_c.4` count `2`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
  - records: `members_by_from_c.5` count `4`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
  - records: `members_by_from_c.10` count `2`
    - sample_keys: `['c_delta_mod15', 'edge_role', 'from_C', 'from_fiber', 'label', 'lift_q_mod4', 'predicted_delta', 'to_C', 'to_fiber']`
- `c_transition_role_channel_grammar_audit_004.v1.json`
  - score: `33`
  - top_keys: `['boundary', 'complement', 'complement_equals_unobserved', 'from_deterministic_q', 'from_rows', 'input', 'interpretation', 'role_pair_count', 'role_pair_from_rows', 'role_pair_plus_from_determines_delta', 'role_pair_plus_from_determines_to', 'role_pair_rows', 'status', 'support', 'support_equals_observed', 'transition_count']`
  - needle_counts: `{'fiber': 8, 'from_C': 8, 'lift_q': 5, 'role_pair': 32, 'support': 3, 'to_C': 5, 'transition': 2}`
  - records: `from_rows` count `9`
    - sample_keys: `['from_C', 'from_class', 'lift_q_values', 'role_pairs', 'to_values', 'transition_count']`
  - records: `role_pair_from_rows` count `11`
    - sample_keys: `['fiber_delta_values', 'from_C', 'lift_q_values', 'role_pair', 'row_count', 'to_values']`
  - records: `role_pair_rows` count `3`
    - sample_keys: `['base_delta_counts', 'fiber_delta_counts', 'from_class_counts', 'from_values', 'q_counts', 'role_pair', 'to_class_counts', 'to_values', 'transition_count', 'transitions']`
  - records: `role_pair_rows[0].transitions` count `4`
    - sample_keys: `['base_delta_mod15', 'fiber_delta', 'from_C', 'from_class', 'lift_q', 'role_pair', 'station_roles', 'to_C', 'to_class']`
  - records: `role_pair_rows[1].transitions` count `4`
    - sample_keys: `['base_delta_mod15', 'fiber_delta', 'from_C', 'from_class', 'lift_q', 'role_pair', 'station_roles', 'to_C', 'to_class']`
  - records: `role_pair_rows[2].transitions` count `4`
    - sample_keys: `['base_delta_mod15', 'fiber_delta', 'from_C', 'from_class', 'lift_q', 'role_pair', 'station_roles', 'to_C', 'to_class']`
- `g60_native_overlay_generator_family_search_001.v1.json`
  - score: `24`
  - top_keys: `['boundary', 'candidate_results', 'checks', 'edge_records', 'missing_endpoint', 'purpose', 'schema', 'status', 'summary', 'timestamp_utc', 'two_map_exact_hits']`
  - needle_counts: `{'fiber': 24, 'from_A': 1, 'from_B': 1, 'from_C': 3, 'native': 1, 'slot': 14, 'to_A': 1, 'to_B': 1, 'to_C': 3}`
  - records: `candidate_results` count `10`
    - sample_keys: `['candidate', 'exact_all', 'exact_reverse_partner', 'exact_shared_B', 'is_permutation', 'matched_by_label', 'matched_edges', 'missed_by_label']`
  - records: `edge_records` count `24`
    - sample_keys: `['edge_index', 'edge_role', 'fiber_delta_mod60', 'form_index', 'from_A', 'from_B', 'from_C', 'from_columns', 'from_fiber', 'from_key', 'from_slot', 'label', 'slot_delta_mod15', 'to_A', 'to_B', 'to_C', 'to_columns', 'to_fiber', 'to_key', 'to_slot']`
  - records: `checks` count `8`
    - sample_keys: `['detail', 'id', 'status']`
- `c_transition_support_canonical_audit_002.v1.json`
  - score: `15`
  - top_keys: `['boundary', 'canonical_complement', 'canonical_support', 'canonical_transition_count', 'canonical_transition_rows', 'complement_equals_unobserved', 'interpretation', 'node_rows', 'q0_subset_of_support', 'q3_subset_of_support', 'q_counts', 'source', 'status', 'support_equals_observed', 'unobserved_disjoint_from_support']`
  - needle_counts: `{'fiber': 1, 'from_C': 1, 'lift_q': 1, 'q0': 1, 'q3': 1, 'source': 1, 'support': 7, 'to_C': 1, 'transition': 8}`
  - records: `canonical_transition_rows` count `12`
    - sample_keys: `['base_delta_mod15', 'fiber_delta', 'from_C', 'from_in_q0', 'from_in_q3', 'lift_q', 'to_C', 'to_in_q0', 'to_in_q3']`
  - records: `node_rows` count `15`
    - sample_keys: `['C', 'in_degree', 'in_observed_locked', 'in_q0', 'in_q3', 'in_transition_support', 'in_unobserved_locked', 'out_degree', 'total_degree']`
- `c_transition_support_partition_audit_001.v1.json`
  - score: `15`
  - top_keys: `['boundary', 'input_sources', 'interpretation', 'observed_locked', 'q0', 'q0_cut_to_transition_complement', 'q0_cut_to_transition_support', 'q0_subset_of_transition_support', 'q3', 'q3_cut_to_transition_complement', 'q3_cut_to_transition_support', 'q3_subset_of_transition_support', 'status', 'support_summary', 'transition_count', 'transition_pairs', 'transition_role_rows', 'unobserved_disjoint_from_transition_support', 'unobserved_locked']`
  - needle_counts: `{'fiber': 1, 'from_C': 1, 'lift_q': 1, 'q0': 2, 'q3': 2, 'source': 2, 'support': 45, 'to_C': 1, 'transition': 22}`
  - records: `support_summary.node_rows` count `15`
    - sample_keys: `['C', 'deltas_when_source', 'in_degree', 'in_observed_locked', 'in_q0', 'in_q3', 'in_support', 'out_degree', 'total_transition_degree']`
  - records: `transition_role_rows` count `34`
    - sample_keys: `['base_delta_mod15', 'fiber_delta', 'from_C', 'from_in_q0', 'from_in_q3', 'lift_q', 'signed_g15_edge_sign_between_endpoints', 'to_C', 'to_in_q0', 'to_in_q3']`
- `c_transition_station_role_cover_audit_003b.v1.json`
  - score: `13`
  - top_keys: `['all_pairs_have_expected_delta_somewhere', 'all_pairs_have_one_diad_one_coupler', 'all_pairs_have_two_station_roles', 'boundary', 'canonical_transition_count', 'interpretation', 'pair_rows', 'q_counts_by_transition_type', 'raw_station_role_row_count', 'role_class_counts', 'role_class_rule', 'scanned_files', 'semantic_station_role_row_count', 'station_role_counts', 'station_role_cover_confirmed', 'status']`
  - needle_counts: `{'fiber': 1, 'from_C': 1, 'lift_q': 1, 'role_class': 10, 'station_role': 14, 'to_C': 1, 'transition': 4}`
  - records: `pair_rows` count `12`
    - sample_keys: `['exact_delta_role_count', 'expected_fiber_delta', 'from_C', 'has_expected_delta_somewhere', 'lift_q', 'role_classes', 'semantic_station_role_count', 'station_roles', 'to_C']`
- `c_transition_role_block_circulation_audit_005.v1.json`
  - score: `10`
  - top_keys: `['all_circulation_matches', 'block_complement', 'block_complement_equals_unobserved', 'block_rows', 'block_union', 'block_union_equals_observed', 'boundary', 'circulation_checks', 'input', 'interpretation', 'pairwise_from_block_intersections', 'role_pair_order', 'shared_junction_is_2', 'status', 'triple_from_block_intersection', 'triple_intersection_size']`
  - needle_counts: `{'from_B': 11, 'role_pair': 5, 'to_B': 2, 'transition': 1}`
  - records: `block_rows` count `3`
    - sample_keys: `['from_block', 'q_counts', 'role_pair', 'to_block', 'transition_count']`
  - records: `circulation_checks` count `3`
    - sample_keys: `['from_role_pair', 'matches', 'next_from', 'this_to', 'to_role_pair']`
  - records: `pairwise_from_block_intersections` count `3`
    - sample_keys: `['a', 'b', 'intersection', 'size']`
- `lift_q_context_rules_001.v1.json`
  - score: `10`
  - top_keys: `['boundary', 'checks', 'purpose', 'schema', 'status', 'summary', 'timestamp_utc']`
  - needle_counts: `{'C_delta': 17, 'from_C': 19, 'lift_q': 1, 'to_C': 20, 'transition': 25}`
  - records: `summary.least_exact_feature_sets` count `20`
    - sample_keys: `['ambiguous_group_count', 'ambiguous_groups_sample', 'exact', 'features', 'group_count']`
  - records: `summary.best_near_miss_feature_sets` count `20`
    - sample_keys: `['ambiguous_group_count', 'ambiguous_groups_sample', 'exact', 'features', 'group_count']`
  - records: `checks` count `5`
    - sample_keys: `['detail', 'id', 'status']`
- `c_transition_delta_lift_decomposition_001.v1.json`
  - score: `8`
  - top_keys: `['boundary', 'checks', 'purpose', 'rows', 'schema', 'status', 'summary', 'timestamp_utc']`
  - needle_counts: `{'C_delta': 32, 'fiber': 15, 'lift_q': 42, 'transition': 16}`
  - records: `rows` count `24`
    - sample_keys: `['actual_to_fiber', 'c_delta_mod15', 'c_transition', 'delta_matches_c_delta_mod15', 'delta_mod15', 'edge_index', 'edge_role', 'form_index', 'from_fiber', 'label', 'lift_q_mod4', 'match', 'predicted_delta', 'predicted_to_fiber']`
  - records: `checks` count `6`
    - sample_keys: `['detail', 'id', 'status']`

## Reading

This schema inspection ranks imported native-chain artifacts by whether they expose transition, support, role, and A/B/C fields. The goal is to identify the best next source for reconstructing the missing A/B assignment law.

## Boundary

This is schema inspection only. It does not assert a native generator and does not close Gap A.
