# Audit role-pair channel-axis candidate for leakage 001

## Keeper

Order spoke first. Channel may speak cleaner.

## Result

- audit_pass: True
- channel_candidate_count: 3
- channel_axis_candidates: role_hooks, support_sources, native
- leakage_clear: False
- forbidden_downstream_payload_hit_count: 180
- all_candidates_source_side_visible: False
- channel_axis_cleaner_than_order_axis: False
- channel_axis_status: channel_candidates_have_forbidden_or_downstream_hits

## Candidate audit

### role_hooks

- source_packet_hit_count: 0
- source_side_present: False
- leakage_free: True
- forbidden_hit_count: 0
- provenance_status: search_visible_clean_but_source_side_unproven

### support_sources

- source_packet_hit_count: 194
- source_side_present: True
- leakage_free: False
- forbidden_hit_count: 162
- provenance_status: source_packet_visible_with_forbidden_hits

### native

- source_packet_hit_count: 158
- source_side_present: True
- leakage_free: False
- forbidden_hit_count: 18
- provenance_status: source_packet_visible_with_forbidden_hits

## Admission boundary

- channel_axis_rule_admitted: false
- source_law_admitted: false
- native_generator_admitted: false
- unique_native_g15_embedding_proven: false
- full_theorem_admitted: false
- proof_claim: false
- gap_a_closure: false
- geometry_claim: false
- physics_claim: false
- force_claim: false

This audit tests cleanliness and source visibility only. A clean channel candidate is not yet a source law, native generator, unique embedding, theorem, or Gap A closure.
