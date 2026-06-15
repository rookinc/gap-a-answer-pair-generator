# Native rule member target table 013

Status: native_rule_member_target_table_recorded

## Outputs

- member_csv: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/csv/native_rule_members_013.v1.csv`
- pair_csv: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/csv/native_answer_pairs_013.v1.csv`

## Counts

- native_transition_count: `12`
- native_member_count: `24`
- native_pair_count: `12`
- selected_transition_count: `12`
- member_class_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- member_edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- pair_role_pair_counts: `{'IW/YZ': 4, 'TI/XY': 4, 'WX/ZT': 4}`
- all_pairs_have_two_members: `True`
- all_pair_roles_match_002: `True`

## Synthetic comparison

- synthetic_candidate_count_per_key: `50625`
- total_synthetic_candidate_count: `607500`
- native_pair_target_count: `12`
- reduction_factor_synthetic_to_native_pairs: `50625.0`

## Native answer-pair target rows

- transition=(0, 2), role_pair=WX/ZT, roles=ZT/WX, free_vars=(S.from_A=10, S.B=5, S.to_A=12, R.A=1)
- transition=(1, 10), role_pair=IW/YZ, roles=IW/YZ, free_vars=(S.from_A=2, S.B=13, S.to_A=9, R.A=0)
- transition=(2, 4), role_pair=WX/ZT, roles=ZT/WX, free_vars=(S.from_A=12, S.B=5, S.to_A=10, R.A=3)
- transition=(2, 5), role_pair=TI/XY, roles=XY/TI, free_vars=(S.from_A=1, S.B=0, S.to_A=10, R.A=12)
- transition=(2, 14), role_pair=IW/YZ, roles=IW/YZ, free_vars=(S.from_A=1, S.B=11, S.to_A=7, R.A=3)
- transition=(4, 5), role_pair=TI/XY, roles=XY/TI, free_vars=(S.from_A=3, S.B=2, S.to_A=12, R.A=10)
- transition=(5, 0), role_pair=IW/YZ, roles=IW/YZ, free_vars=(S.from_A=12, S.B=2, S.to_A=1, R.A=10)
- transition=(5, 2), role_pair=IW/YZ, roles=IW/YZ, free_vars=(S.from_A=10, S.B=4, S.to_A=3, R.A=12)
- transition=(10, 13), role_pair=WX/ZT, roles=ZT/WX, free_vars=(S.from_A=0, S.B=1, S.to_A=2, R.A=9)
- transition=(11, 2), role_pair=TI/XY, roles=XY/TI, free_vars=(S.from_A=7, S.B=14, S.to_A=3, R.A=1)
- transition=(13, 1), role_pair=TI/XY, roles=XY/TI, free_vars=(S.from_A=9, S.B=10, S.to_A=0, R.A=2)
- transition=(14, 11), role_pair=WX/ZT, roles=ZT/WX, free_vars=(S.from_A=3, S.B=2, S.to_A=1, R.A=7)

## Reading

This audit promotes the native rule_members layer to an explicit Project 21 target table. The A/B assignments are present as native transition members: two members per selected C-transition, one shared_B and one reverse_partner. The remaining generator problem is therefore to derive these 24 native member rows, not to infer A/B assignments from the late row-pair table.

## Boundary

This is a target-table extraction and comparison audit. It does not derive the native rule_members from G60, and therefore does not close Gap A.
