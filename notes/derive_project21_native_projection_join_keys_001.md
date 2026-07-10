# Derive Project 21 native projection join keys 001

## Result

- audit_pass: `True`
- verdict: `native_four_row_v4_join_key_candidates_found_nonunique`
- record tables: `10`
- packet-linked rows: `28`
- four-row V4 candidates: `512`
- exact join candidates: `512`
- join key derived: `False`

## Boundary

- Finite native join-key derivation audit only.
- Packet edge, node, and law-key values are used as provenance anchors.
- A candidate requires four packet-linked native rows with two binary fields realizing all four V4 states.
- A derived join key additionally requires a nonempty shared provenance signature and a unique best candidate.
- No row-order join, sheet/cocycle naming, face/vertex naming, literal {5,3,4}, physics, or Gap A closure claim.

## Next

`disambiguate_project21_native_v4_join_key_candidates_001`
