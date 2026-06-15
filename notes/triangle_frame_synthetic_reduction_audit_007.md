# Triangle-frame synthetic reduction audit 007

Status: triangle_frame_synthetic_reduction_recorded

## Input discipline

- uses_project18_expected_pair_records: `False`
- uses_realized_rows_for_generation: `False`
- uses_realized_rows_for_evaluation: `True`

## Result

- selected_key_count: `12`
- total_synthetic_candidate_count: `607500`
- triangle_frame_selected_count: `607500`
- realized_match_count: `12`
- triangle_frame_accepts_all_synthetic_skeletons: `True`
- triangle_frame_reduction_factor: `1.0`
- realized_reduction_factor_needed_after_frame: `50625.0`

## Per-key counts

- key=('IW/YZ', 1, 10, 'IW', 'YZ'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('IW/YZ', 2, 14, 'IW', 'YZ'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('IW/YZ', 5, 0, 'IW', 'YZ'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('IW/YZ', 5, 2, 'IW', 'YZ'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('TI/XY', 2, 5, 'XY', 'TI'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('TI/XY', 4, 5, 'XY', 'TI'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('TI/XY', 11, 2, 'XY', 'TI'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('TI/XY', 13, 1, 'XY', 'TI'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('WX/ZT', 0, 2, 'ZT', 'WX'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('WX/ZT', 2, 4, 'ZT', 'WX'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('WX/ZT', 10, 13, 'ZT', 'WX'): synthetic=50625, frame_selected=50625, realized_matches=1
- key=('WX/ZT', 14, 11, 'ZT', 'WX'): synthetic=50625, frame_selected=50625, realized_matches=1

## Reading

The triangle-frame rule is already built into the synthetic skeleton construction. It accepts the whole synthetic skeleton universe rather than selecting the realized A/B assignments. Therefore the hand-sketch frame explains the pair closure grammar, but the missing generator problem remains the native selection of A/B assignments.

## Boundary

This is not Gap A closure. It uses selected transition keys from 002 and realized rows only for evaluation. It shows that triangle-frame closure alone does not solve the synthetic overgeneration problem.
