# Disambiguate Project 21 native V4 join-key candidates 001

## Result

- audit_pass: `True`
- verdict: `native_v4_join_candidates_remain_tied_after_packet_topology_scoring`
- input candidates: `20`
- evaluated candidates: `20`
- tied best candidates: `2`
- unique join candidate: `False`
- unique transport mapping: `False`

## Boundary

- Finite V4 join-candidate disambiguation audit only.
- All bit swaps, bit complements, and four-row bijections are tested.
- Scoring uses packet edge, node, and oriented continuation topology evidence.
- Row order is never treated as provenance.
- A unique candidate does not name its bits as sheet, cocycle, face, or vertex without a separate semantic audit.
- No literal {5,3,4} honeycomb, four-chambers-per-edge theorem, physics, or Gap A closure claim.

## Next

`derive_project21_native_join_from_exact_transition_provenance_001`
