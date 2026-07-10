# Derive A/B assignment candidate field hypotheses 001

Status: `AB_ASSIGNMENT_CANDIDATE_FIELD_HYPOTHESES_001_DERIVED`

## Keeper

The apparatus exposes A/B surfaces. The next question is whether they are source law or answer residue.

## Summary

- derive_pass: `True`
- loaded_source_count: `3`
- source_candidate_row_count: `156`
- hypothesis_count: `5`
- leakage_guard_count: `4`
- strongest_initial_hypothesis: `H2_slot_coupled_ab_assignment`
- highest_leakage_risk_hypothesis: `H4_shared_b_reverse_partner_split`
- gap_a_closure: `False`
- native_generator_admitted: `False`
- ab_assignment_law_admitted: `False`
- answer_label_leakage_closed: `False`
- source_law_admitted: `False`
- recommended_next: `test_slot_coupled_ab_assignment_hypothesis_001`

## Hypotheses

### H1_split_ab_transition_surface - split A/B transition surface

- statement: A/B assignment may be recoverable from split transition fields from_A, from_B, to_A, to_B together with C support fields.
- candidate_fields: `from_A, from_B, to_A, to_B, from_C, to_C, C_delta, integer_C_delta`
- support_status: `field_surface_present`
- risk: field presence is not a law; it may still be post-realized row residue
- next_test: `test whether A/B deltas are determined by non-label source fields`

### H2_slot_coupled_ab_assignment - slot-coupled A/B assignment

- statement: A/B assignment may be coupled to from_slot, to_slot, and slot_delta_mod15 rather than to answer labels.
- candidate_fields: `from_slot, to_slot, slot_delta_mod15, from_A, from_B, to_A, to_B`
- support_status: `slot_surface_present`
- risk: slot fields may encode downstream row construction unless provenance is separated
- next_test: `test slot-to-A/B transition determinism inside source rows`

### H3_role_conditioned_ab_assignment - role-conditioned A/B assignment

- statement: A/B assignment may depend on station_role or role_pair as a source orientation condition.
- candidate_fields: `station_role, role_pair, role_class, from_A, from_B, to_A, to_B`
- support_status: `role_surface_present`
- risk: role fields may leak answer labels if role_class is already shared_B/reverse_partner target class
- next_test: `separate station_role/role_pair from role_class and test non-label role conditioning`

### H4_shared_b_reverse_partner_split - shared_B / reverse_partner split law

- statement: A/B assignment may arise from a split between shared_B preservation behavior and reverse_partner return behavior.
- candidate_fields: `shared_B, reverse_partner, role_class, from_B, to_B, from_slot, to_C`
- support_status: `role_labeled_universe_surface_present`
- risk: shared_B and reverse_partner are close to answer labels and need leakage guard
- next_test: `test laws using station and transition fields before role_class labels`

### H5_source_rank_residue_not_law - source-rank residue boundary

- statement: Selector/rank features likely record residue of the source law, but should not be admitted as the A/B assignment law without independent provenance.
- candidate_fields: `candidate, selector, rank, anchor_rank_method, c_rank_method`
- support_status: `residue_surface_present`
- risk: high leakage risk because selector/rank fields may be downstream success measurements
- next_test: `use selector/rank fields only as evaluation targets, not source-law inputs`

## Leakage guards

- `L1_no_role_class_as_source_input` Do not use role_class, label, shared_B, or reverse_partner as source-law inputs in first-pass A/B derivation. Reason: These fields may already encode the answer class.
- `L2_no_accepted_candidate_indices` Do not use accepted_candidate_indices, exact flags, false_positive lists, or miss lists as source-law inputs. Reason: These fields are selector outcomes, not source construction variables.
- `L3_source_before_evaluation` Prefer from/to A/B/C, slot, station_role, role_pair, and transition fields that exist before acceptance evaluation. Reason: These are closer to apparatus fields than to downstream result labels.
- `L4_negative_audit_required` Every candidate A/B hypothesis must be followed by a negative leakage audit. Reason: Field hypotheses are not admitted laws until answer-label leakage is excluded.

## Boundary

- Hypotheses/ledger only.
- No theorem.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No A/B assignment law admission.
- No full role-labeled shared_B derivation.
- No answer-label leakage closure.
- No source law admission.
- No physics claim.
- No force claim.
