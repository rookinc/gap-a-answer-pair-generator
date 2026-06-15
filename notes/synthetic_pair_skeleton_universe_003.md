# Synthetic pair skeleton universe 003

Status: synthetic_pair_skeleton_universe_recorded

## Input discipline

- uses_project18_expected_pair_records: `False`
- uses_realized_rows_for_generation: `False`
- uses_realized_rows_for_evaluation: `True`

## Synthetic universe

- selected_key_count: `12`
- free_variable_count_per_key: `4`
- values_per_free_variable: `15`
- synthetic_candidate_count_per_key: `50625`
- total_synthetic_candidate_count: `607500`
- realized_pair_signature_count: `12`
- total_realized_match_count: `12`
- overgeneration_factor_per_realized_pair: `50625`

## Free variables

For each selected transition key, the reciprocal skeleton leaves:

- `S.from_A`
- `S.from_B_or_slot`
- `S.to_A`
- `R.from_A`

## Per-key counts

- key=('IW/YZ', 1, 10, 'IW', 'YZ'): synthetic=50625, realized_matches=1
- key=('IW/YZ', 2, 14, 'IW', 'YZ'): synthetic=50625, realized_matches=1
- key=('IW/YZ', 5, 0, 'IW', 'YZ'): synthetic=50625, realized_matches=1
- key=('IW/YZ', 5, 2, 'IW', 'YZ'): synthetic=50625, realized_matches=1
- key=('TI/XY', 2, 5, 'XY', 'TI'): synthetic=50625, realized_matches=1
- key=('TI/XY', 4, 5, 'XY', 'TI'): synthetic=50625, realized_matches=1
- key=('TI/XY', 11, 2, 'XY', 'TI'): synthetic=50625, realized_matches=1
- key=('TI/XY', 13, 1, 'XY', 'TI'): synthetic=50625, realized_matches=1
- key=('WX/ZT', 0, 2, 'ZT', 'WX'): synthetic=50625, realized_matches=1
- key=('WX/ZT', 2, 4, 'ZT', 'WX'): synthetic=50625, realized_matches=1
- key=('WX/ZT', 10, 13, 'ZT', 'WX'): synthetic=50625, realized_matches=1
- key=('WX/ZT', 14, 11, 'ZT', 'WX'): synthetic=50625, realized_matches=1

## Reading

Given the selected transition key and reciprocal station roles, the pair grammar still leaves four mod-15 degrees of freedom: S.from_A, S.B/slot, S.to_A, and R.from_A. The synthetic skeleton universe therefore overgenerates heavily. This identifies the next native-generator problem: select the missing A/B assignments without using realized rows.

## Boundary

This is not Gap A closure. It uses selected transition keys from 002, and it uses realized rows only for evaluation. It does not yet generate the transition support or the A/B assignments natively.
