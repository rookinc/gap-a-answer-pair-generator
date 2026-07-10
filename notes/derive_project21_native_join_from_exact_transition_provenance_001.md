# Derive Project 21 native join from exact transition provenance 001

## Result

- audit_pass: `True`
- verdict: `source_slot_fields_alias_on_target_rows_but_diverge_globally`
- packet fields equal: `True`
- full table fields equal: `False`
- equal pairs: `17`
- unequal pairs: `11`
- pair profile: `{'00': 9, '10': 11, '11': 8}`
- selected source axis: `None`
- target parity axis: `target_delta_parity_xor`

## Target rows

- row 5: source_slot_c_order_xor=0, source_slot_wrap=0, target_delta_parity_xor=0, equal=True
- row 6: source_slot_c_order_xor=0, source_slot_wrap=0, target_delta_parity_xor=1, equal=True
- row 14: source_slot_c_order_xor=1, source_slot_wrap=1, target_delta_parity_xor=0, equal=True
- row 15: source_slot_c_order_xor=1, source_slot_wrap=1, target_delta_parity_xor=1, equal=True

## Boundary

- Finite exact-transition provenance audit only.
- The two source fields are compared on the four target rows and across the complete transition table.
- Equality on the target rows can establish an alias on this surface, not global semantic identity unless the full table also agrees.
- Field names alone do not establish face, vertex, sheet, or cocycle meaning.
- No literal {5,3,4} honeycomb, four-chambers-per-edge theorem, physics, or Gap A closure claim.

## Next

`trace_source_slot_field_construction_order_001`
