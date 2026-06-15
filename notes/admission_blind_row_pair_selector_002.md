# Admission-blind row-pair selector 002

Status: admission_blind_row_pair_selector_recorded

## Input discipline

- uses_project18_expected_pair_records: `False`

## Result

- shared_row_count: `12`
- reverse_row_count: `12`
- candidate_count: `48`
- selected_count: `12`
- candidate_role_pair_counts: `{'IW/YZ': 16, 'TI/XY': 16, 'WX/ZT': 16}`
- selected_role_pair_counts: `{'IW/YZ': 4, 'TI/XY': 4, 'WX/ZT': 4}`

## Selected pair keys

- `('IW/YZ', 1, 10, 'IW', 'YZ')`
- `('IW/YZ', 2, 14, 'IW', 'YZ')`
- `('IW/YZ', 5, 0, 'IW', 'YZ')`
- `('IW/YZ', 5, 2, 'IW', 'YZ')`
- `('TI/XY', 2, 5, 'XY', 'TI')`
- `('TI/XY', 4, 5, 'XY', 'TI')`
- `('TI/XY', 11, 2, 'XY', 'TI')`
- `('TI/XY', 13, 1, 'XY', 'TI')`
- `('WX/ZT', 0, 2, 'ZT', 'WX')`
- `('WX/ZT', 2, 4, 'ZT', 'WX')`
- `('WX/ZT', 10, 13, 'ZT', 'WX')`
- `('WX/ZT', 14, 11, 'ZT', 'WX')`

## Boundary

This is admission-blind relative to Project 18 expected pair records, but it still uses realized WXYZTI station rows. It is not Gap A closure.
