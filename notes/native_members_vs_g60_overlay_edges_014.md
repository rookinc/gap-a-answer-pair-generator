# Native members vs G60 overlay edges 014

Status: native_members_vs_g60_overlay_edges_recorded

## Inputs

- target members: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/artifacts/csv/native_rule_members_013.v1.csv`
- G60 overlay: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/21-gap-a-answer-pair-generator/source/project18_native_chain/json/g60_native_overlay_generator_family_search_001.v1.json`

## Result

- target_member_count: `24`
- g60_edge_record_count: `24`
- intersection_count: `24`
- target_only_count: `0`
- g60_only_count: `0`
- exact_signature_match: `True`
- target_edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- g60_edge_role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- target_label_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- g60_label_counts: `{'reverse_partner': 12, 'shared_B': 12}`

## Matched rows first 24

- transition=(2, 14), role=IW, label=shared_B, C=(2,14), keys=11|1|2|4,5 -> 11|7|14|23,24
- transition=(1, 10), role=IW, label=shared_B, C=(1,10), keys=13|2|1|4,9 -> 13|9|10|28,29
- transition=(5, 0), role=IW, label=shared_B, C=(5,0), keys=2|12|5|8,18 -> 2|1|0|0,4
- transition=(5, 2), role=IW, label=shared_B, C=(5,2), keys=4|10|5|13,17 -> 4|3|2|7,10
- transition=(11, 2), role=TI, label=reverse_partner, C=(11,2), keys=2|1|11|4,5 -> 11|1|2|4,5
- transition=(13, 1), role=TI, label=reverse_partner, C=(13,1), keys=1|2|13|4,9 -> 13|2|1|4,9
- transition=(2, 5), role=TI, label=reverse_partner, C=(2,5), keys=5|12|2|8,18 -> 2|12|5|8,18
- transition=(4, 5), role=TI, label=reverse_partner, C=(4,5), keys=5|10|4|13,17 -> 4|10|5|13,17
- transition=(14, 11), role=WX, label=reverse_partner, C=(14,11), keys=11|7|14|23,24 -> 14|7|11|23,24
- transition=(10, 13), role=WX, label=reverse_partner, C=(10,13), keys=13|9|10|28,29 -> 10|9|13|28,29
- transition=(0, 2), role=WX, label=reverse_partner, C=(0,2), keys=2|1|0|0,4 -> 0|1|2|0,4
- transition=(2, 4), role=WX, label=reverse_partner, C=(2,4), keys=4|3|2|7,10 -> 2|3|4|7,10
- transition=(11, 2), role=XY, label=shared_B, C=(11,2), keys=14|7|11|23,24 -> 14|3|2|7,12
- transition=(13, 1), role=XY, label=shared_B, C=(13,1), keys=10|9|13|28,29 -> 10|0|1|0,2
- transition=(2, 5), role=XY, label=shared_B, C=(2,5), keys=0|1|2|0,4 -> 0|10|5|2,17
- transition=(4, 5), role=XY, label=shared_B, C=(4,5), keys=2|3|4|7,10 -> 2|12|5|8,18
- transition=(2, 14), role=YZ, label=reverse_partner, C=(2,14), keys=14|3|2|7,12 -> 2|3|14|7,12
- transition=(1, 10), role=YZ, label=reverse_partner, C=(1,10), keys=10|0|1|0,2 -> 1|0|10|0,2
- transition=(5, 0), role=YZ, label=reverse_partner, C=(5,0), keys=0|10|5|2,17 -> 5|10|0|2,17
- transition=(5, 2), role=YZ, label=reverse_partner, C=(5,2), keys=2|12|5|8,18 -> 5|12|2|8,18
- transition=(14, 11), role=ZT, label=shared_B, C=(14,11), keys=2|3|14|7,12 -> 2|1|11|4,5
- transition=(10, 13), role=ZT, label=shared_B, C=(10,13), keys=1|0|10|0,2 -> 1|2|13|4,9
- transition=(0, 2), role=ZT, label=shared_B, C=(0,2), keys=5|10|0|2,17 -> 5|12|2|8,18
- transition=(2, 4), role=ZT, label=shared_B, C=(2,4), keys=5|12|2|8,18 -> 5|10|4|13,17

## Reading

This audit compares the Project 21 native rule-member target table against the earlier G60 native overlay edge_records. An exact signature match means the 24 rule members are the same 24 native overlay edge records, so the remaining problem shifts from deriving late answer-pair rows to deriving the native overlay edge-record construction.

## Boundary

This is a comparison audit. It does not derive the G60 overlay edge records and does not close Gap A.
