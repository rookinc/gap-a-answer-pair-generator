# Derive hard absence source rule search plan 001

Status: `HARD_ABSENCE_SOURCE_RULE_SEARCH_PLAN_001_DERIVED`

## Keeper

The hard absences are not noise. They are the next source-law question.

## Summary

- plan_pass: `True`
- search_family_count: `4`
- search_order_count: `5`
- immediate_next: `search_hard_absence_endpoint_motion_rules_001`
- observed_key_count: `24`
- hard_absence_count: `5172`
- source_invalid_proxy_count: `1365`
- answer_label_leakage_closed: `False`
- source_law_admitted: `False`
- birth_order_proven: `False`
- gap_a_closure: `False`
- recommended_next: `search_hard_absence_endpoint_motion_rules_001`

## Search order

- `search_hard_absence_endpoint_motion_rules_001`
- `search_hard_absence_source_packet_incidence_rules_001`
- `search_hard_absence_role_pair_channel_rules_001`
- `search_native_chain_hard_absence_gate_001`
- `audit_hard_absence_source_rule_candidates_001`

## Search families

### F1_endpoint_motion_filters

- goal: Search for source-side motion rules that reject hard absences by endpoint motion rather than answer labels.
- success_receipt: `hard_absence_endpoint_motion_rule_candidate`
- failure_receipt: `endpoint_motion_does_not_resolve_hard_absences`
- recommended_artifact: `search_hard_absence_endpoint_motion_rules_001`

### F2_source_packet_incidence_filters

- goal: Use source-only packet incidence to distinguish observed keys from hard absences.
- success_receipt: `hard_absence_source_packet_incidence_rule_candidate`
- failure_receipt: `source_packet_incidence_not_enough`
- recommended_artifact: `search_hard_absence_source_packet_incidence_rules_001`

### F3_role_pair_channel_filters

- goal: Test whether role_pair/channel constraints reject hard absences before A/B assignment.
- success_receipt: `hard_absence_role_pair_channel_rule_candidate`
- failure_receipt: `role_pair_channel_not_enough`
- recommended_artifact: `search_hard_absence_role_pair_channel_rules_001`

### F4_native_chain_lift_filters

- goal: Search native-chain source artifacts for a pre-answer lift or construction gate that admits observed slot/C keys and withholds hard absences.
- success_receipt: `native_chain_hard_absence_gate_candidate`
- failure_receipt: `native_chain_membership_not_enough`
- recommended_artifact: `search_native_chain_hard_absence_gate_001`

## Boundary

- Search-plan ledger only.
- No theorem.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No universal A/B assignment law admission.
- No full chirality admission.
- No full role-labeled shared_B derivation.
- No answer-label leakage closure.
- No source law admission.
- No physics claim.
- No force claim.
