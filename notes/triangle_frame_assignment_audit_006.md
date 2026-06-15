# Triangle frame assignment audit 006

Status: triangle_frame_assignment_audit_recorded

## Sketch reading

The hand sketch is interpreted as one ABC triangle with two complementary readings. The shared_B reading fixes B and lets A/C move. The reverse_partner reading fixes A and swaps B/C. A selected answer-pair is where both readings close on the same C-track.

## Candidate universe

All shared_B rows crossed with all reverse_partner rows having the same role_pair.

- candidate_count: `48`
- selected_count: `12`
- selected_role_pair_counts: `{'IW/YZ': 4, 'TI/XY': 4, 'WX/ZT': 4}`

## Frame rule

A candidate closes as a triangle-frame answer-pair when:

- shared_B fixes corner `B`
- reverse_partner fixes corner `A`
- reverse_partner swaps `B/C`
- both readings use the same `C` track
- forward seam holds: `S.to_C = R.from_B`
- return seam holds: `S.from_C = R.to_B`
- delta/lift registers agree

## Selected C tracks

- role_pair=IW/YZ, roles=IW/YZ, C_track=(1, 10)
- role_pair=IW/YZ, roles=IW/YZ, C_track=(2, 14)
- role_pair=IW/YZ, roles=IW/YZ, C_track=(5, 0)
- role_pair=IW/YZ, roles=IW/YZ, C_track=(5, 2)
- role_pair=TI/XY, roles=XY/TI, C_track=(2, 5)
- role_pair=TI/XY, roles=XY/TI, C_track=(4, 5)
- role_pair=TI/XY, roles=XY/TI, C_track=(11, 2)
- role_pair=TI/XY, roles=XY/TI, C_track=(13, 1)
- role_pair=WX/ZT, roles=ZT/WX, C_track=(0, 2)
- role_pair=WX/ZT, roles=ZT/WX, C_track=(2, 4)
- role_pair=WX/ZT, roles=ZT/WX, C_track=(10, 13)
- role_pair=WX/ZT, roles=ZT/WX, C_track=(14, 11)

## Reading

The triangle-frame predicate selects the same 12-style structure from the 48 row-pair candidate universe, but phrases the selector geometrically: fixed B face plus fixed A answer face, joined by forward and return C seams.

## Boundary

This is an exploratory frame audit over realized WXYZTI rows. It does not generate the C-transition support or the A/B assignments natively. It is not Gap A closure.
