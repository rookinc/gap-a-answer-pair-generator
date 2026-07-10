# Derive Eidronic source-daughter carrier domain 001

## Keeper

The carrier must exist before its motion can be derived.

## Result

- derivation_pass: true
- verdict: `partial_native_eidronic_carrier_domain_derived`
- best_orientation: `direct`
- supported nodes: 3/24
- supported transitions: 0/28
- transitions permitting a distinct daughter carrier: 0/28
- full_native_carrier_domain_derived: false

## Derived carrier state

```text
c = (q_t, q_I, local_t, local_I, kind, columns)
local_t = C_t + 15*q_t
local_I = C_I + 15*q_I
c is admitted only by an exact x_sigma row
```

## Proof boundary

- Exact native carrier-domain derivation only.
- The t and I socket orientation remains user-declared.
- Every carrier candidate is backed by an exact x_sigma row.
- No carrier update law is inferred from domain membership.
- No stochastic, quartz, cocycle, physics, or force law is derived.
- No Eidron theorem or Gap A closure claim.

## Next target

`inspect_eidronic_carrier_domain_obstruction_001`
