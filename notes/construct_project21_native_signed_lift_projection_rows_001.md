# Construct Project 21 native signed-lift projection rows 001

## Result

- audit_pass: `True`
- verdict: `four_projection_rows_constructed_native_fields_remain_unjoined`
- projection rows: `4`
- native candidate records: `36`
- explicit index hits: `0`
- mapped rows: `0`
- full native map: `False`

## Projection status

- transport 0: within=0, class=0, product=0, native_status=open
- transport 1: within=1, class=0, product=1, native_status=open
- transport 2: within=0, class=1, product=1, native_status=open
- transport 3: within=1, class=1, product=0, native_status=open

## Boundary

- Finite four-row native-facing projection construction only.
- Project 21 transport and Klein-bit fields are explicit.
- Native fields remain null unless an explicit transport index joins them.
- Candidate native records are inventory evidence, not mappings.
- No sheet, cocycle, face, vertex, literal {5,3,4}, physics, or Gap A closure claim.

## Next

`derive_project21_native_projection_join_keys_001`
