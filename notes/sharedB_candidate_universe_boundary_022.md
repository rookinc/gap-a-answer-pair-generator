# Shared_B candidate-universe boundary 022

Status: sharedB_candidate_universe_boundary_recorded

## Question

Can 004 block circulation plus reverse_partner anchors recover the observed shared_B cycles exactly?

## Counts

- reverse_anchor_count: `12`
- reverse_distinct_anchor_count: `11`
- shared_row_count: `12`
- observed_exact_cycle_count: `4`
- observed_c_cycle_count: `4`
- observed_anchor_cycle_count: `4`
- c_cycle_universe_count: `48`
- anchor_cycle_universe_count: `990`
- combined_cycle_candidate_count: `47520`

## Selector counts

- c_transition_only: `3960`
- anchor_only: `192`
- c_and_anchor_only: `16`
- observed_edge_filter: `4`

## False positives

- c_transition_only: `3956`
- anchor_only: `188`
- c_and_anchor_only: `12`
- observed_edge_filter: `0`

## Misses

- c_transition_only: `0`
- anchor_only: `0`
- c_and_anchor_only: `0`
- observed_edge_filter: `0`

## Exactness

- observed_edge_filter_exact: `True`

## Reduction factors

- combined_to_observed: `11880.0`
- c_transition_only_to_observed: `990.0`
- anchor_only_to_observed: `48.0`
- c_and_anchor_only_to_observed: `4.0`

## Observed cycles

- C-cycle: `[['XY', 2, 5], ['IW', 5, 0], ['ZT', 0, 2]]`
  - anchor-cycle: `[['XY', '[0,4]', '[2,17]'], ['IW', '[8,18]', '[0,4]'], ['ZT', '[2,17]', '[8,18]']]`
  - exact-cycle: `[['XY', 2, 5, '[0,4]', '[2,17]'], ['IW', 5, 0, '[8,18]', '[0,4]'], ['ZT', 0, 2, '[2,17]', '[8,18]']]`
- C-cycle: `[['XY', 4, 5], ['IW', 5, 2], ['ZT', 2, 4]]`
  - anchor-cycle: `[['XY', '[7,10]', '[8,18]'], ['IW', '[13,17]', '[7,10]'], ['ZT', '[8,18]', '[13,17]']]`
  - exact-cycle: `[['XY', 4, 5, '[7,10]', '[8,18]'], ['IW', 5, 2, '[13,17]', '[7,10]'], ['ZT', 2, 4, '[8,18]', '[13,17]']]`
- C-cycle: `[['XY', 11, 2], ['IW', 2, 14], ['ZT', 14, 11]]`
  - anchor-cycle: `[['XY', '[23,24]', '[7,12]'], ['IW', '[4,5]', '[23,24]'], ['ZT', '[7,12]', '[4,5]']]`
  - exact-cycle: `[['XY', 11, 2, '[23,24]', '[7,12]'], ['IW', 2, 14, '[4,5]', '[23,24]'], ['ZT', 14, 11, '[7,12]', '[4,5]']]`
- C-cycle: `[['XY', 13, 1], ['IW', 1, 10], ['ZT', 10, 13]]`
  - anchor-cycle: `[['XY', '[28,29]', '[0,2]'], ['IW', '[4,9]', '[28,29]'], ['ZT', '[0,2]', '[4,9]']]`
  - exact-cycle: `[['XY', 13, 1, '[28,29]', '[0,2]'], ['IW', 1, 10, '[4,9]', '[28,29]'], ['ZT', 10, 13, '[0,2]', '[4,9]']]`

## Reverse anchors

`['[0,2]', '[0,4]', '[13,17]', '[2,17]', '[23,24]', '[28,29]', '[4,5]', '[4,9]', '[7,10]', '[7,12]', '[8,18]']`

## Reading

The 004 block circulation generates 48 possible C-cycles. The observed reverse-partner anchors generate 990 possible twisted ordered column 3-cycles. Their loose product gives 47,520 candidate shared_B cycles, but only 4 are observed. C-transition selection alone, anchor selection alone, and their conjunction still overgenerate. The exact filter is the role-edge filter: each of the three role-labeled moves must exist as an observed shared_B edge. That filter recovers the 4 cycles exactly, but it is circular until the role-edge moves are derived from a native register or candidate universe. Therefore the missing generator has been narrowed to the role-labeled shared_B edge selector.

## Boundary

This is a candidate-universe boundary audit. It does not derive the observed shared_B edges; it shows where the overgeneration lives and what a future native selector must explain. It does not close Gap A.
