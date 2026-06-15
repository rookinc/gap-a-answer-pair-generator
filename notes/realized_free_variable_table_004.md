# Realized free-variable table 004

Status: realized_free_variable_table_recorded

## Output

- record_count: `12`
- role_pair_counts: `{'IW/YZ': 4, 'TI/XY': 4, 'WX/ZT': 4}`
- S_A_delta_counts: `{2: 2, 4: 1, 6: 2, 7: 1, 8: 1, 9: 2, 11: 1, 13: 2}`
- R_minus_S_from_A_counts: `{2: 2, 4: 1, 6: 2, 7: 1, 8: 1, 9: 2, 11: 1, 13: 2}`
- S_B_minus_c1_counts: `{1: 1, 2: 2, 3: 3, 6: 1, 9: 1, 10: 1, 12: 3}`

## Free-variable table

| role_pair | c0 | c1 | shared | reverse | S_from_A | S_B | S_to_A | R_A | S_A_delta | R_minus_S_from_A | S_B_minus_c1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IW/YZ | 1 | 10 | IW | YZ | 2 | 13 | 9 | 0 | 7 | 13 | 3 |
| IW/YZ | 2 | 14 | IW | YZ | 1 | 11 | 7 | 3 | 6 | 2 | 12 |
| IW/YZ | 5 | 0 | IW | YZ | 12 | 2 | 1 | 10 | 4 | 13 | 2 |
| IW/YZ | 5 | 2 | IW | YZ | 10 | 4 | 3 | 12 | 8 | 2 | 2 |
| TI/XY | 2 | 5 | XY | TI | 1 | 0 | 10 | 12 | 9 | 11 | 10 |
| TI/XY | 4 | 5 | XY | TI | 3 | 2 | 12 | 10 | 9 | 7 | 12 |
| TI/XY | 11 | 2 | XY | TI | 7 | 14 | 3 | 1 | 11 | 9 | 12 |
| TI/XY | 13 | 1 | XY | TI | 9 | 10 | 0 | 2 | 6 | 8 | 9 |
| WX/ZT | 0 | 2 | ZT | WX | 10 | 5 | 12 | 1 | 2 | 6 | 3 |
| WX/ZT | 2 | 4 | ZT | WX | 12 | 5 | 10 | 3 | 13 | 6 | 1 |
| WX/ZT | 10 | 13 | ZT | WX | 0 | 1 | 2 | 9 | 2 | 9 | 3 |
| WX/ZT | 14 | 11 | ZT | WX | 3 | 2 | 1 | 7 | 13 | 4 | 6 |

## Reading

This table exposes the four free variables left by the synthetic skeleton: S.from_A, S.B/slot, S.to_A, and R.from_A. It is a preparation step for finding the missing A/B assignment law.

## Boundary

This table uses realized selected pairs. It is descriptive and preparatory, not a native generator and not Gap A closure.
