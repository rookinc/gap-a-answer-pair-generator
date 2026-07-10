# Formalize Eidronic source-daughter chamber contract 001

## Keeper

Time separates the daughter from her mother. Provenance keeps them related. The chamber makes the daughter thinkable.

## Core definitions

### Eidron

A bounded distinction that persists sufficiently for the claim that it is to become thinkable and receiptable.

### Source and daughter

A daughter Eidron is not identical to its mother or source, but retains that source as provenance.

### Quotient chamber

A bounded comparison surface that exposes an admissible description of a larger carrier without exhausting it.

### CIK classification

`eidron_scott in [CIK] = true`

This is a bounded admissible description, not a claim that CIK exhausts Scott's identity.

## Socket orientation

- `t` is the user-declared quartz input socket.
- `I` is the user-declared receipted output socket.
- Quartz scales measurement occasions but does not admit events.

## Source-daughter contract

```text
c_next = T_t(c_source, transition)
I_next = M(c_next, chamber)
I_next != I_source
source(I_next) = I_source
```

## Finite proof obligations

### PO1_distinction

The daughter output is distinguishable from its source.

`I_next != I_source`

### PO2_provenance

The daughter retains a receiptable source relation.

`source(I_next) = I_source`

### PO3_carrier_update

A declared transition law determines the next lower-carrier state.

`c_next = T_t(c_source, transition)`

### PO4_projection

The output is a bounded quotient projection of the updated lower carrier.

`I_next = M(c_next, chamber)`

### PO5_seed_independence

Closed-path comparison is independent of the arbitrary held initial seed.

`closure_residue(seed_a) = closure_residue(seed_b)`

### PO6_native_row_admission

Any claimed native realization must replay an exact x_sigma row under the derived carrier law.

`M(c_next, chamber) in x_sigma`

## Current boundary

- Definition and proof-obligation contract only.
- The t and I orientation is user-declared for this fork.
- Choice of sockets does not itself prove a native path law.
- CIK is a bounded classification chamber, not a total identity.
- Quartz supplies scaled timing and measurement address only.
- No lower-carrier update or projection law is derived here.
- No Eidron theorem, native generator, physics, force, or Gap A closure claim.

## Next target

`search_eidronic_source_daughter_carrier_law_001`
