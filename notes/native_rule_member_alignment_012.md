# Native rule member alignment 012

Status: native_rule_member_alignment_recorded

## Inputs

- native rule members: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/c_transition_overlay_delta_generator_001.v1.json`
- selector 002: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/json/admission_blind_row_pair_selector_002.v1.json`
- free-variable table 004: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/json/realized_free_variable_table_004.v1.json`

## Result

- native_transition_count: `12`
- native_flat_member_count: `24`
- selected_transition_count: `12`
- missing_transition_keys: `[]`
- selected_transitions_with_two_members: `12`
- free_variable_match_count: `12`
- ambiguous_member_count: `0`
- flat_member_class_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- flat_member_label_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- flat_member_edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`

## Alignment rows

- role_pair=IW/YZ, transition=(1, 10), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=IW/YZ, transition=(2, 14), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=IW/YZ, transition=(5, 0), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=IW/YZ, transition=(5, 2), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=TI/XY, transition=(2, 5), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=TI/XY, transition=(4, 5), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=TI/XY, transition=(11, 2), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=TI/XY, transition=(13, 1), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=WX/ZT, transition=(0, 2), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=WX/ZT, transition=(2, 4), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=WX/ZT, transition=(10, 13), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True
- role_pair=WX/ZT, transition=(14, 11), native_members=2, class_counts={'reverse_partner': 1, 'shared_B': 1}, free_match=True

## Reading

This audit aligns the native rule_members from the imported Project 18 native-chain artifact with the 12 selected C-tracks from Project 21. If the native members match the free variables in 004, then the A/B assignments are not absent; they are present in the earlier native transition member layer.

## Boundary

This is an alignment audit. It does not yet derive the rule_members natively from G60, and therefore does not close Gap A by itself.
