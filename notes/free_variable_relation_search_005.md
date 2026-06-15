# Free-variable relation search 005

Status: free_variable_relation_search_recorded

## Output

- record_count: `12`
- deterministic_test_count: `686`
- exact_deterministic_test_count: `304`
- non_identity_exact_deterministic_test_count: `38`
- global_affine_law_count: `0`
- role_coded_affine_law_count: `0`

## Non-identity exact deterministic tests

- target=S_A_delta, keys=['c1', 'reverse'], groups=11
- target=S_A_delta, keys=['c1', 'shared'], groups=11
- target=S_A_delta, keys=['role_pair', 'c1'], groups=11
- target=S_B_minus_c1, keys=['c0', 'reverse'], groups=11
- target=S_B_minus_c1, keys=['c0', 'shared'], groups=11
- target=S_B_minus_c1, keys=['role_pair', 'c0'], groups=11
- target=R_minus_S_from_A, keys=['reverse', 'C_delta', 'lift_q'], groups=11
- target=R_minus_S_from_A, keys=['role_pair', 'C_delta', 'lift_q'], groups=11
- target=R_minus_S_from_A, keys=['shared', 'C_delta', 'lift_q'], groups=11
- target=S_A_delta, keys=['c1', 'reverse', 'lift_q'], groups=11
- target=S_A_delta, keys=['c1', 'shared', 'lift_q'], groups=11
- target=S_A_delta, keys=['c1', 'shared', 'reverse'], groups=11
- target=S_A_delta, keys=['role_pair', 'c1', 'lift_q'], groups=11
- target=S_A_delta, keys=['role_pair', 'c1', 'reverse'], groups=11
- target=S_A_delta, keys=['role_pair', 'c1', 'shared'], groups=11
- target=S_B, keys=['reverse', 'C_delta', 'lift_q'], groups=11
- target=S_B, keys=['role_pair', 'C_delta', 'lift_q'], groups=11
- target=S_B, keys=['shared', 'C_delta', 'lift_q'], groups=11
- target=S_B_minus_c1, keys=['c0', 'reverse', 'lift_q'], groups=11
- target=S_B_minus_c1, keys=['c0', 'shared', 'lift_q'], groups=11
- target=S_B_minus_c1, keys=['c0', 'shared', 'reverse'], groups=11
- target=S_B_minus_c1, keys=['role_pair', 'c0', 'lift_q'], groups=11
- target=S_B_minus_c1, keys=['role_pair', 'c0', 'reverse'], groups=11
- target=S_B_minus_c1, keys=['role_pair', 'c0', 'shared'], groups=11
- target=R_minus_S_from_A, keys=['role_pair', 'reverse', 'C_delta', 'lift_q'], groups=11

## Global affine laws

- none

## Role-coded affine laws

- none

## Role-specific affine laws

- IW/YZ: laws=3
  - R_A = C_delta + 3*lift_q + 6 mod 15
  - R_A = C_delta + 8*lift_q + 6 mod 15
  - R_A = C_delta + 13*lift_q + 6 mod 15
- TI/XY: laws=3
  - S_from_A = c0 + 4*lift_q + 14 mod 15
  - S_from_A = c0 + 9*lift_q + 14 mod 15
  - S_from_A = c0 + 14*lift_q + 14 mod 15
- WX/ZT: laws=3
  - S_to_A = 14*c0 + lift_q + 12 mod 15
  - S_to_A = 14*c0 + 6*lift_q + 12 mod 15
  - S_to_A = 14*c0 + 11*lift_q + 12 mod 15

## Pairwise target relations

- S_to_A vs S_B_minus_c1: equal=2/12, constant_diff=False, constant_sum=False
- R_A vs R_minus_S_from_A: equal=1/12, constant_diff=False, constant_sum=False
- R_minus_S_from_A vs S_B_minus_c1: equal=1/12, constant_diff=False, constant_sum=False
- S_B vs R_minus_S_from_A: equal=1/12, constant_diff=False, constant_sum=False
- S_B vs S_B_minus_c1: equal=1/12, constant_diff=False, constant_sum=False
- S_from_A vs S_B_minus_c1: equal=1/12, constant_diff=False, constant_sum=False
- S_to_A vs S_A_delta: equal=1/12, constant_diff=False, constant_sum=False
- R_A vs S_A_delta: equal=0/12, constant_diff=False, constant_sum=False
- R_A vs S_B_minus_c1: equal=0/12, constant_diff=False, constant_sum=False
- S_A_delta vs R_minus_S_from_A: equal=0/12, constant_diff=False, constant_sum=False
- S_A_delta vs S_B_minus_c1: equal=0/12, constant_diff=False, constant_sum=False
- S_B vs R_A: equal=0/12, constant_diff=False, constant_sum=False
- S_B vs S_A_delta: equal=0/12, constant_diff=False, constant_sum=False
- S_B vs S_to_A: equal=0/12, constant_diff=False, constant_sum=False
- S_from_A vs R_A: equal=0/12, constant_diff=False, constant_sum=False
- S_from_A vs R_minus_S_from_A: equal=0/12, constant_diff=False, constant_sum=False
- S_from_A vs S_A_delta: equal=0/12, constant_diff=False, constant_sum=False
- S_from_A vs S_B: equal=0/12, constant_diff=False, constant_sum=False
- S_from_A vs S_to_A: equal=0/12, constant_diff=False, constant_sum=False
- S_to_A vs R_A: equal=0/12, constant_diff=False, constant_sum=False

## Reading

This searches for low-complexity relations in the realized free-variable table. It is intended to identify whether the missing A/B assignment law is already visible from c0, c1, C_delta, lift_q, and role-channel labels, or whether additional native structure is required.

## Boundary

This is a descriptive relation search over realized selected pairs. Exact relations here may be overfit. This is not a native generator and not Gap A closure.
