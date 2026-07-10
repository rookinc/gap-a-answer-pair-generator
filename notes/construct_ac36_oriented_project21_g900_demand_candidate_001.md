# Construct AC36-oriented Project 21 G900 demand candidate 001

## Keeper

AC36 names how the knot acts. Native provenance must still supply where that action enters G900.

## Result

- construction_pass: True
- verdict: `ac36_oriented_project21_g900_demand_candidate_constructed_with_open_addresses`
- demand row count: 3
- AC36 roles present: continuation entry, continuation output, alternate terminal branch
- all G900 address fields remain open

## Demand rows

### continuation_entry

- Project 21 edge: `5 -> 8`
- edge ID: `6`
- source law key: `[2, 2, 4, 5]`
- target law key: `[2, 5, 5, 2]`
- G900 segment role: open
- G900 from slot: open
- G900 to slot: open
- G900 anchor limit: open

### continuation_output

- Project 21 edge: `8 -> 15`
- edge ID: `10`
- source law key: `[2, 5, 5, 2]`
- target law key: `[5, 5, 2, 4]`
- G900 segment role: open
- G900 from slot: open
- G900 to slot: open
- G900 anchor limit: open

### alternate_terminal_branch

- Project 21 edge: `5 -> 6`
- edge ID: `5`
- source law key: `[2, 2, 4, 5]`
- target law key: `[2, 2, 5, 0]`
- G900 segment role: open
- G900 from slot: open
- G900 to slot: open
- G900 anchor limit: open

## Boundary

- AC36-oriented G900 demand-candidate construction only.
- AC36 roles are derived only for the three-edge Project 21 packet.
- The t-to-I orientation remains conditional on the user declaration.
- All G900 address fields remain explicitly open.
- No G900 segment role, slot, limit, anchor, or target is inferred from Project 21 node numbers.
- No G60 or G15 target data is used.
- No coupling, channel, transport, native generator, theorem extension, geometry, GR, physics, force, body mutation, or Gap A closure claim.

## Next target

`search_native_projection_from_project21_law_keys_to_g900_demand_addresses_001`
