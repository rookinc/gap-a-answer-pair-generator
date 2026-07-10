# Derive lifted residue functional on directed cycle space 001

## Keeper

Position returns home. The lifted path divides the cycles into two classes.

## Result

- derivation_pass: True
- verdict: `nonzero_linear_lifted_residue_functional_derived_on_full_directed_cycle_space`
- cycle_space_dimension: 7
- cycle_space_size: 128
- basis_signature: `[0, 1, 1, 0, 0, 0, 0]`
- basis_formula: `rho(sum_i a_i gamma_i) = a_1 + a_2 mod 2`
- functional_rank: 1
- kernel_dimension: 6
- kernel_size: 64
- nontrivial_coset_size: 64
- functional_is_linear: True
- basis_change_invariant: True

## Functional

```text
rho(sum_i a_i gamma_i) = a_1 + a_2 mod 2
kernel dimension = 6
kernel size = 64
nontrivial coset size = 64
```

## Boundary

- GF(2) directed cycle-space functional derivation only.
- The role-hook edge values are treated as the previously audited candidate edge assignment.
- Linearity is exhaustively verified over all 128 represented cycle vectors.
- Basis independence is tested by invertible elementary basis changes.
- No native signed-lift identification or cocycle admission.
- No holonomy, winding, torus, metric, curvature, GR, physics, force, theorem, or Gap A closure claim.

## Next target

`audit_lifted_residue_functional_against_native_signed_lift_001`
