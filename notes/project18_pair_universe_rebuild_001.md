# Project 18 pair universe rebuild 001

Status: project18_pair_universe_rebuild_recorded

## Rebuild

- shared_row_count: `12`
- reverse_row_count: `12`
- candidate_count: `48`
- expected_pair_count: `12`
- candidate_role_pair_counts: `{'IW/YZ': 16, 'TI/XY': 16, 'WX/ZT': 16}`

## Selector scores

- same_from_C: accepted=14, false_positive=2, miss=0, exact=False
- same_to_C: accepted=14, false_positive=2, miss=0, exact=False
- same_C_delta: accepted=18, false_positive=6, miss=0, exact=False
- same_integer_C_delta: accepted=14, false_positive=2, miss=0, exact=False
- same_lift_q: accepted=26, false_positive=14, miss=0, exact=False
- answer_R_supplies_S_to_C: accepted=14, false_positive=2, miss=0, exact=False
- return_R_returns_S_from_C: accepted=14, false_positive=2, miss=0, exact=False
- reciprocal_answer_pair: accepted=12, false_positive=0, miss=0, exact=True
- strict_pair_grammar: accepted=12, false_positive=0, miss=0, exact=True

## Exact selectors

- reciprocal_answer_pair
- strict_pair_grammar

## Boundary

This rebuilds the Project 18 realized row-pair universe inside Project 21. It is a baseline reproduction, not a native generator and not Gap A closure.
