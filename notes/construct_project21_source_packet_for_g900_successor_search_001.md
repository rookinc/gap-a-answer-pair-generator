# Construct Project 21 source packet for G900 successor search 001

## Keeper

The bridge plug is cut from Project 21 closure provenance, not from the socket it is meant to enter.

## Result

- construction_pass: true
- verdict: `canonical_project21_provenance_source_packet_constructed`
- restricted_edge_pool_count: 15
- enumerated_candidate_count: 16383
- canonical_packet_found: True
- source_packet_size: 3

## Source packet

```json
[
  {
    "packet_row": 0,
    "edge_id": 5,
    "source": 5,
    "target": 6,
    "role_hook_change": 1,
    "is_seed_closure_defect_edge": true,
    "is_reciprocal_pair_edge": false,
    "nontrivial_basis_membership": [
      1
    ]
  },
  {
    "packet_row": 1,
    "edge_id": 6,
    "source": 5,
    "target": 8,
    "role_hook_change": 1,
    "is_seed_closure_defect_edge": true,
    "is_reciprocal_pair_edge": false,
    "nontrivial_basis_membership": []
  },
  {
    "packet_row": 2,
    "edge_id": 10,
    "source": 8,
    "target": 15,
    "role_hook_change": 1,
    "is_seed_closure_defect_edge": true,
    "is_reciprocal_pair_edge": false,
    "nontrivial_basis_membership": [
      0
    ]
  }
]
```

## Selection order

- hit every nontrivial residue basis cycle
- contain every seed-invariant closure-defect edge
- form one connected undirected packet
- minimize packet size
- maximize residue and defect support
- lexicographic edge-id tie break

## Boundary

- Project 21 provenance-only source-packet construction.
- Candidate edges come only from nontrivial cycle support, seed-invariant closure defects, and directed reciprocal support.
- No G900 successor target, G60 target, G15 signing, or answer label is used in packet selection.
- Canonical means canonical under the declared bounded scoring order only.
- No packet admission, coupling law, channel, transport, theorem, GR, physics, force, body mutation, or Gap A closure claim.

## Next target

`search_g900_carrier_incidence_successor_for_project21_packet_001`
