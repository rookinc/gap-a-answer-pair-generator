# Derive AC36-oriented Project 21 fork roles 001

## Keeper

AC36 does not choose the fork from nowhere. Given t as input and I as output, the packet topology distinguishes continuation from the terminal alternative.

## Result

- derivation_pass: True
- verdict: `ac36_oriented_project21_fork_roles_derived_under_declared_t_to_I_convention`
- AC36 membership admitted: true
- declared input socket: `t`
- declared output socket: `I`
- native direction theorem: false

## Oriented packet

    alternate terminal: 5 -> 6
    continuation entry: 5 -> 8
    continuation output: 8 -> 15

    t = node 5
    I = node 15

The oriented continuation path is:

    5 -> 8 -> 15

The alternate terminal path is:

    5 -> 6

## Role basis

- node 5 is the unique packet node with out-degree two
- node 8 is the unique node with one incoming and one outgoing packet edge
- node 15 is the terminal reached through the continuation
- node 6 is the terminal reached directly from the fork

## Boundary

- Post-membership AC36 fork-orientation derivation only.
- The t-to-I convention is user-declared and not independently derived.
- Topology uniquely distinguishes the continuing branch from the terminal alternative under that convention.
- Role assignment applies only to the three-edge Project 21 packet.
- No G900 segment role, slot, limit, anchor, target, coupling, channel, or transport is derived.
- No native source-direction theorem, geometry, GR, physics, force, body mutation, theorem extension, or Gap A closure claim.

## Next target

`construct_ac36_oriented_project21_g900_demand_candidate_001`
