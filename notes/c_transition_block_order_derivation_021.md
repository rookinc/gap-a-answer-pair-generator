# C-transition block order derivation 021

Status: c_transition_block_order_derivation_recorded

## Question

Does the shared_B role order `XY -> IW -> ZT` come from the earlier C-transition block circulation?

## Counts

- shared_row_count: `12`
- component_count: `3`
- cycle_count: `4`
- role_counts: `{'IW': 4, 'XY': 4, 'ZT': 4}`
- channel_counts: `{'IW/YZ': 4, 'TI/XY': 4, 'WX/ZT': 4}`
- block_edge_counts: `{"('A', 'B')": 4, "('B', 'C')": 4, "('C', 'A')": 4}`

## Expected circulation

- 004 channel circulation: `['WX/ZT', 'TI/XY', 'IW/YZ']`
- shared_B role order: `['XY', 'IW', 'ZT']`
- shared_B channel order: `['TI/XY', 'IW/YZ', 'WX/ZT']`
- shared_B block order: `[['B', 'C'], ['C', 'A'], ['A', 'B']]`

## Tests

- all_rows_match_channel_map: `True`
- all_cycles_match_role_order: `True`
- all_cycles_match_channel_order: `True`
- all_cycles_are_rotation_of_004_circulation: `True`
- all_cycles_match_block_order: `True`
- all_cycles_close_C: `True`
- conditional_derivation_pass: `True`

## Cycles

- component=`1`, roles=`['XY', 'IW', 'ZT']`, channels=`['TI/XY', 'IW/YZ', 'WX/ZT']`, blocks=`[['B', 'C'], ['C', 'A'], ['A', 'B']]`, transitions=`[[2, 5], [5, 0], [0, 2]]`, c_path=`[2, 5, 0, 2]`
- component=`1`, roles=`['XY', 'IW', 'ZT']`, channels=`['TI/XY', 'IW/YZ', 'WX/ZT']`, blocks=`[['B', 'C'], ['C', 'A'], ['A', 'B']]`, transitions=`[[4, 5], [5, 2], [2, 4]]`, c_path=`[4, 5, 2, 4]`
- component=`2`, roles=`['XY', 'IW', 'ZT']`, channels=`['TI/XY', 'IW/YZ', 'WX/ZT']`, blocks=`[['B', 'C'], ['C', 'A'], ['A', 'B']]`, transitions=`[[11, 2], [2, 14], [14, 11]]`, c_path=`[11, 2, 14, 11]`
- component=`0`, roles=`['XY', 'IW', 'ZT']`, channels=`['TI/XY', 'IW/YZ', 'WX/ZT']`, blocks=`[['B', 'C'], ['C', 'A'], ['A', 'B']]`, transitions=`[[13, 1], [1, 10], [10, 13]]`, c_path=`[13, 1, 10, 13]`

## Row tests

- role=`IW`, channel=`IW/YZ`, transition=`(1, 10)`, block=`['C', 'A']`, matches=`True`, columns=`[4,9] -> [28,29]`
- role=`IW`, channel=`IW/YZ`, transition=`(2, 14)`, block=`['C', 'A']`, matches=`True`, columns=`[4,5] -> [23,24]`
- role=`IW`, channel=`IW/YZ`, transition=`(5, 0)`, block=`['C', 'A']`, matches=`True`, columns=`[8,18] -> [0,4]`
- role=`IW`, channel=`IW/YZ`, transition=`(5, 2)`, block=`['C', 'A']`, matches=`True`, columns=`[13,17] -> [7,10]`
- role=`XY`, channel=`TI/XY`, transition=`(2, 5)`, block=`['B', 'C']`, matches=`True`, columns=`[0,4] -> [2,17]`
- role=`XY`, channel=`TI/XY`, transition=`(4, 5)`, block=`['B', 'C']`, matches=`True`, columns=`[7,10] -> [8,18]`
- role=`XY`, channel=`TI/XY`, transition=`(11, 2)`, block=`['B', 'C']`, matches=`True`, columns=`[23,24] -> [7,12]`
- role=`XY`, channel=`TI/XY`, transition=`(13, 1)`, block=`['B', 'C']`, matches=`True`, columns=`[28,29] -> [0,2]`
- role=`ZT`, channel=`WX/ZT`, transition=`(0, 2)`, block=`['A', 'B']`, matches=`True`, columns=`[2,17] -> [8,18]`
- role=`ZT`, channel=`WX/ZT`, transition=`(2, 4)`, block=`['A', 'B']`, matches=`True`, columns=`[8,18] -> [13,17]`
- role=`ZT`, channel=`WX/ZT`, transition=`(10, 13)`, block=`['A', 'B']`, matches=`True`, columns=`[0,2] -> [4,9]`
- role=`ZT`, channel=`WX/ZT`, transition=`(14, 11)`, block=`['A', 'B']`, matches=`True`, columns=`[7,12] -> [4,5]`

## Interpretation

This audit checks whether the shared_B role order XY -> IW -> ZT is just an observed column-cycle fact or whether it is forced by the earlier C-transition block circulation. Using the 004 block map, XY belongs to TI/XY and sends B -> C; IW belongs to IW/YZ and sends C -> A; ZT belongs to WX/ZT and sends A -> B. Therefore every closed shared_B C-cycle follows B -> C -> A -> B, which is a cyclic rotation of the 004 channel circulation A -> B -> C -> A. This conditionally derives the observed XY -> IW -> ZT order from the native C-transition block grammar.

## Boundary

This derives the shared_B cycle order only conditional on the imported 004 block circulation and the already selected shared_B rows. It does not derive the shared_B rows from a full candidate universe, does not construct the full dodecahedral register, and does not close Gap A.
