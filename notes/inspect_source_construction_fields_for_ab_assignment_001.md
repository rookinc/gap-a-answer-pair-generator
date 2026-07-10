# Inspect source construction fields for A/B assignment 001

Status: `SOURCE_CONSTRUCTION_FIELDS_FOR_AB_ASSIGNMENT_001_INSPECTED`

## Keeper

Gap A is asking for the machine that makes the answer lawful.

## Repair note

The original F1 checker was too strict. It required bundled `from_ABC` / `to_ABC` fields. The inspected sources expose the native A/B/C surfaces directly as split fields.

- split_ab_fields_present: `True`
- c_support_fields_present: `True`
- core_source_field_families_present: `True`
- inspection_pass_after_repair: `True`

## Summary

- inspection_pass: `True`
- loaded_input_count: `9`
- missing_input_count: `0`
- matching_file_count: `9`
- top_record_count: `72`
- distinct_field_hit_count: `338`
- frontier_status: `source_construction_fields_inspectable_not_admitted`
- gap_a_closure: `False`
- native_generator_admitted: `False`
- ab_assignment_law_admitted: `False`
- full_role_labeled_shared_b_derived: `False`
- answer_label_leakage_closed: `False`
- source_law_admitted: `False`
- recommended_next: `derive_ab_assignment_candidate_field_hypotheses_001`

## Source field families

- `F1_abc_transition_fields` status=`present`: Split A/B/C transition fields are present directly as from_A, to_A, from_B, to_B, from_C, to_C, and C_delta/integer_C_delta. The apparatus exposes A/B assignment surfaces without requiring a bundled from_ABC field.
- `F2_slot_fields` status=`present`: Slot fields may bind tuple motion to source construction positions.
- `F3_role_fields` status=`present`: Role fields identify whether A/B assignment is tied to WXYZTI station role or role class.
- `F4_shared_b_reverse_partner_fields` status=`present`: shared_B and reverse_partner fields are the immediate role-labeled universe frontier.
- `F5_selector_rank_fields` status=`present`: Selector/rank fields record residue of source law but are not source law by themselves.

## Requirement map

- `native_source_construction_law` status=`inspectable_not_admitted`, candidate_field_families=`F1_abc_transition_fields, F2_slot_fields, F3_role_fields`
- `native_ab_assignment_law` status=`inspectable_not_admitted`, candidate_field_families=`F1_abc_transition_fields, F2_slot_fields, F4_shared_b_reverse_partner_fields`
- `full_role_labeled_shared_b_universe` status=`inspectable_not_admitted`, candidate_field_families=`F3_role_fields, F4_shared_b_reverse_partner_fields`
- `answer_label_leakage_closure` status=`requires_negative_audit`, candidate_field_families=`F5_selector_rank_fields`

## Top field hits

- `path`: `3127`
- `sample`: `2657`
- `count`: `453`
- `sample_keys`: `444`
- `C_delta`: `444`
- `integer_C_delta`: `432`
- `from_B`: `422`
- `to_B`: `422`
- `from_A`: `418`
- `to_A`: `418`
- `from_slot`: `408`
- `to_slot`: `408`
- `role_pair`: `366`
- `role_class`: `333`
- `anchor_rank_method`: `315`
- `label`: `240`
- `station_role`: `234`
- `accepted_count`: `234`
- `exact`: `234`
- `record_path`: `226`
- `to_C`: `222`
- `from_C`: `221`
- `slot_delta_mod15`: `216`
- `fiber_delta`: `216`
- `accepted_candidate_indices`: `210`
- `c_rank_method`: `210`
- `false_positive_candidate_indices`: `210`
- `miss_candidate_indices`: `210`
- `answer_R_from_B_to_S_to_C`: `168`
- `answer_R_from_slot_to_S_to_C`: `168`
- `same_C_delta`: `168`
- `same_integer_C_delta`: `168`
- `fiber_delta_mod60`: `144`
- `shared_B_row`: `126`
- `R_swaps_BC`: `126`
- `return_R_to_B_to_S_from_C`: `126`
- `return_R_to_slot_to_S_from_C`: `126`
- `fiber_mod15_delta_equals_C_delta`: `120`
- `value`: `105`
- `false_positive`: `105`

## Boundary

- Inspection/ledger only.
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
