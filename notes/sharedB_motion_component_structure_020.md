# Shared_B motion component structure 020

Status: sharedB_motion_component_structure_recorded

## Counts

- shared_row_count: `12`
- node_count: `11`
- component_count: `3`
- component_size_counts: `{'3': 2, '5': 1}`
- component_edge_size_counts: `{'3': 2, '6': 1}`
- simple_3_cycle_count: `2`
- bouquet_two_3_cycles_count: `1`
- c_cycle_count: `4`
- all_c_cycles_are_XY_IW_ZT: `True`

## Components

- component `0`
  - node_count: `3`
  - edge_count: `3`
  - nodes: `['[0,2]', '[28,29]', '[4,9]']`
  - role_counts: `{'IW': 1, 'XY': 1, 'ZT': 1}`
  - c_nodes: `[1, 10, 13]`
  - is_simple_3_cycle: `True`
  - is_bouquet_two_3_cycles: `False`
  - branch_nodes: `[]`
  - role=`XY`, transition=`(13, 1)`, columns=`[28,29] -> [0,2]`
  - role=`ZT`, transition=`(10, 13)`, columns=`[0,2] -> [4,9]`
  - role=`IW`, transition=`(1, 10)`, columns=`[4,9] -> [28,29]`
  - C-cycles:
    - length=`3`, roles=`['XY', 'IW', 'ZT']`, transitions=`[[13, 1], [1, 10], [10, 13]]`, XY_IW_ZT=`True`
- component `1`
  - node_count: `5`
  - edge_count: `6`
  - nodes: `['[0,4]', '[13,17]', '[2,17]', '[7,10]', '[8,18]']`
  - role_counts: `{'IW': 2, 'XY': 2, 'ZT': 2}`
  - c_nodes: `[0, 2, 4, 5]`
  - is_simple_3_cycle: `False`
  - is_bouquet_two_3_cycles: `True`
  - branch_nodes: `[{'node': '[8,18]', 'in_degree': 2, 'out_degree': 2, 'branch_like': True}]`
  - role=`XY`, transition=`(2, 5)`, columns=`[0,4] -> [2,17]`
  - role=`ZT`, transition=`(0, 2)`, columns=`[2,17] -> [8,18]`
  - role=`IW`, transition=`(5, 0)`, columns=`[8,18] -> [0,4]`
  - role=`XY`, transition=`(4, 5)`, columns=`[7,10] -> [8,18]`
  - role=`ZT`, transition=`(2, 4)`, columns=`[8,18] -> [13,17]`
  - role=`IW`, transition=`(5, 2)`, columns=`[13,17] -> [7,10]`
  - C-cycles:
    - length=`3`, roles=`['XY', 'IW', 'ZT']`, transitions=`[[2, 5], [5, 0], [0, 2]]`, XY_IW_ZT=`True`
    - length=`3`, roles=`['XY', 'IW', 'ZT']`, transitions=`[[4, 5], [5, 2], [2, 4]]`, XY_IW_ZT=`True`
- component `2`
  - node_count: `3`
  - edge_count: `3`
  - nodes: `['[23,24]', '[4,5]', '[7,12]']`
  - role_counts: `{'IW': 1, 'XY': 1, 'ZT': 1}`
  - c_nodes: `[2, 11, 14]`
  - is_simple_3_cycle: `True`
  - is_bouquet_two_3_cycles: `False`
  - branch_nodes: `[]`
  - role=`XY`, transition=`(11, 2)`, columns=`[23,24] -> [7,12]`
  - role=`ZT`, transition=`(14, 11)`, columns=`[7,12] -> [4,5]`
  - role=`IW`, transition=`(2, 14)`, columns=`[4,5] -> [23,24]`
  - C-cycles:
    - length=`3`, roles=`['XY', 'IW', 'ZT']`, transitions=`[[11, 2], [2, 14], [14, 11]]`, XY_IW_ZT=`True`

## Role and C-node coverage

- role_to_component_indices: `{'IW': [0, 1, 2], 'XY': [0, 1, 2], 'ZT': [0, 1, 2]}`
- cnode_to_component_indices: `{'0': [1], '1': [0], '2': [1, 2], '4': [1], '5': [1], '10': [0], '11': [2], '13': [0], '14': [2]}`

## Interpretation

This audit decomposes the shared_B column-motion graph from audit 019. The motion splits into two simple 3-cycles and one 5-node bouquet made from two 3-cycles sharing a column anchor. In C-transition order, each detected 3-cycle follows the role order XY -> IW -> ZT. This suggests the shared_B residual is not arbitrary column motion: it is organized by a small cycle grammar over reverse-partner anchors.

## Boundary

This is a structure audit over already selected shared_B motion. It does not derive the motion from a full dodecahedral register or close Gap A.
