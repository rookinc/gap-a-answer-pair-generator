# Schlafli 534 shadow test 018

Status: schlafli_534_shadow_test_recorded

## Strict literal test

- verdict: `literal_g60_one_skeleton_identity_not_supported`
- G60 vertex_count: `60`
- G60 edge_count: `120`
- G60 degree_set: `[4]`
- G60 triangle_count: `40`
- literal degree-6 test pass: `False`

## Shadow test

- verdict: `strong_534_type_shadow_signal`
- pass_count: `10 / 10`

## Indicators

- four_forms: `True`
- six_roles: `True`
- twenty_four_role_incidents: `True`
- role_incidence_four_each: `True`
- form_role_grid_4_by_6: `True`
- three_reciprocal_axes: `True`
- axes_imply_octahedral_vertex_figure: `True`
- twelve_answer_pairs: `True`
- answer_pair_count_matches_octahedron_edge_count: `True`
- columns_inside_30_register: `True`

## Role/form counts

- role_counts: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- label_counts: `{'reverse_partner': 12, 'shared_B': 12}`
- form_counts: `{'0': 6, '1': 6, '2': 6, '3': 6}`
- forms_have_all_six_roles_once: `True`
- form_role_matrix: `{'0': {'IW': 1, 'TI': 1, 'WX': 1, 'XY': 1, 'YZ': 1, 'ZT': 1}, '1': {'IW': 1, 'TI': 1, 'WX': 1, 'XY': 1, 'YZ': 1, 'ZT': 1}, '2': {'IW': 1, 'TI': 1, 'WX': 1, 'XY': 1, 'YZ': 1, 'ZT': 1}, '3': {'IW': 1, 'TI': 1, 'WX': 1, 'XY': 1, 'YZ': 1, 'ZT': 1}}`

## Reciprocal axes and octahedral scaffold

- unique_reciprocal_axes: `[['IW', 'YZ'], ['TI', 'XY'], ['WX', 'ZT']]`
- axis_counts: `{"('IW', 'YZ')": 4, "('TI', 'XY')": 4, "('WX', 'ZT')": 4}`
- octahedral_vertex_figure_pass: `True`
- implied_graph_edge_count: `12`
- implied_graph_degrees_by_role: `{'IW': 4, 'TI': 4, 'WX': 4, 'XY': 4, 'YZ': 4, 'ZT': 4}`
- implied_triangle_count: `8`

## Column register

- distinct_column_count_seen: `16`
- column_min: `0`
- column_max: `29`
- columns_within_0_29_register: `True`
- distinct_column_pairs_seen: `11`
- column_pair_rows_seen: `48`
- reading: `Columns sit inside a 0..29 register in the observed overlay rows. That is compatible with a 30-column dodecahedral edge register, but it is not by itself a proof of dodecahedral cell decomposition.`

## Interpretation

The strict literal test asks whether G60 is the raw 1-skeleton of a {5,3,4} honeycomb quotient. The shadow test asks whether the native overlay has a {5,3,4}-type finite signature: four forms, six roles, 24 role incidences, three reciprocal axes, an implied octahedral vertex-figure scaffold, and 12 answer-pairs. Passing the shadow test supports a finite transport-shadow hypothesis, not literal tessellation identity.

## Next needed for stronger claim

- Construct an explicit dodecahedral cell decomposition or cell-shadow.
- Show a 30-edge dodecahedral register with accountable incidence.
- Show fourfold around-edge incidence or its finite quotient replacement.
- Explain why the observed carrier is tetravalent while the literal {5,3,4} 1-skeleton has degree 6.
- Derive shared_B column motion from the candidate cell/register incidence.

## Boundary

This does not prove that the Thalean carrier is {5,3,4}. It distinguishes literal identity from finite shadow evidence and records what remains to prove.
