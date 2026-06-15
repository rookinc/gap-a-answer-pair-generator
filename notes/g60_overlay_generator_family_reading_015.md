# G60 overlay generator family reading 015

Status: g60_overlay_generator_family_reading_recorded

## Input

- G60 overlay artifact: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`

## Edge records

- edge_record_count: `24`
- edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- label_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- form_counts: `{'0': 6, '1': 6, '2': 6, '3': 6}`
- distinct_from_key_count: `22`
- distinct_to_key_count: `22`

## Candidate-family search

- candidate_result_count: `10`
- exact_all_candidate_count: `0`
- exact_reverse_partner_candidate_count: `0`
- exact_shared_B_candidate_count: `0`
- permutation_candidate_count: `10`
- two_map_exact_hit_count: `0`
- checks_count: `8`
- check_status_counts: `{'True': 8}`

## Ranked candidates

- candidate: `old_hyperxi_ab_relabelled`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `4`
  - missed_total: `20`
  - matched_by_label: `{'reverse_partner': 2, 'shared_B': 2}`
  - missed_by_label: `{'reverse_partner': 10, 'shared_B': 10}`
- candidate: `old_hyperxi_ba_relabelled`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `4`
  - missed_total: `20`
  - matched_by_label: `{'reverse_partner': 2, 'shared_B': 2}`
  - missed_by_label: `{'reverse_partner': 10, 'shared_B': 10}`
- candidate: `identity`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `minus_15_mod60`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `minus_30_mod60`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `old_g60_pair_involution_relabelled`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `old_hyperxi_a_relabelled`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `old_hyperxi_b_relabelled`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `plus_15_mod60`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`
- candidate: `plus_30_mod60`
  - exact_all: `False`
  - exact_reverse_partner: `False`
  - exact_shared_B: `False`
  - is_permutation: `True`
  - matched_edges_count: `0`
  - missed_total: `24`
  - matched_by_label: `{}`
  - missed_by_label: `{'reverse_partner': 12, 'shared_B': 12}`

## Source summary

```text
{'forms_key': 'wxyzti_admitted_forms', 'form_count': 4, 'edge_record_count': 24, 'label_counts': {'reverse_partner': 12, 'shared_B': 12}, 'role_counts': {'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}, 'candidate_count': 10, 'candidate_names': ['identity', 'minus_15_mod60', 'minus_30_mod60', 'old_g60_pair_involution_relabelled', 'old_hyperxi_a_relabelled', 'old_hyperxi_ab_relabelled', 'old_hyperxi_b_relabelled', 'old_hyperxi_ba_relabelled', 'plus_15_mod60', 'plus_30_mod60'], 'best_single_candidate': {'candidate': 'old_hyperxi_ab_relabelled', 'is_permutation': True, 'matched_edges': 4, 'matched_by_label': {'reverse_partner': 2, 'shared_B': 2}, 'missed_by_label': {'reverse_partner': 10, 'shared_B': 10}, 'exact_all': False, 'exact_reverse_partner': False, 'exact_shared_B': False}, 'two_map_exact_hit_count': 0, 'strict_native_two_map_generator_found': False, 'fiber_delta_by_label': {'reverse_partner': {'1': 1, '2': 2, '3': 2, '9': 1, '12': 1, '48': 1, '51': 1, '55': 1, '57': 2}, 'shared_B': {'1': 1, '2': 2, '3': 2, '9': 1, '12': 1, '48': 1, '51': 1, '55': 1, '57': 2}}, 'slot_delta_by_label': {'reverse_partner': {'3': 3, '5': 1, '6': 1, '9': 1, '12': 3, '13': 2, '14': 1}, 'shared_B': {'0': 12}}, 'gap_a_closed': False, 'full_g900_admission_found': False, 'next_step': 'expand_to_context_dependent_g60_native_generator_family'}
```

## Reading

This audit reads the earlier G60 native overlay generator-family search. It records which candidate families were tested, which partial matches were found, whether any candidate already gave an exact all-edge generator, and what remains open. This is meant to prevent Project 21 from repeating a generator family that Project 18 already tested.

## Boundary

This is a reading and triage audit over an imported search artifact. It does not derive the G60 overlay edge records and does not close Gap A.
