# Repair Project 21 AC36 membership schema replay 001

## Keeper

A carrier enters AC36 through the whole gate, not through one matching field.

## Repair

Commit `11ccf80` admitted the Project 21 knot after replaying only one recovered field:

    carrier_family

That admission is superseded.

The valid earlier result remains:

    ac36_membership_candidate_pass = true

Formal membership now fails closed unless all ten expected schema fields are recovered from Project 36 sources and replay successfully.

## Result

- repair_pass: True
- verdict: `project21_knot_remains_ac36_membership_candidate_after_fail_closed_repair`
- expected schema fields: 10
- recovered schema fields: 8
- passed schema fields: 8
- complete schema recovered: False
- complete replay pass: False
- AC36 membership admitted: False
- U_AC36 invoked on Project 21: False

## Field replay

- declared_boundary_receipt_role: candidate=True, structural=True, project36_evidence=True, replay=True
- declared_diad_closure_role: candidate=True, structural=True, project36_evidence=True, replay=True
- declared_same_boundary_closure_test: candidate=True, structural=True, project36_evidence=True, replay=True
- declared_triad_action_role: candidate=True, structural=True, project36_evidence=True, replay=True
- scanable_preservation_relation: candidate=True, structural=True, project36_evidence=True, replay=True
- morphism_or_translation_boundary: candidate=True, structural=True, project36_evidence=True, replay=True
- declared_source_output_orientation: candidate=True, structural=True, project36_evidence=False, replay=False
- non_claim_boundary: candidate=True, structural=True, project36_evidence=True, replay=True
- carrier_id: candidate=True, structural=True, project36_evidence=False, replay=False
- carrier_family: candidate=True, structural=True, project36_evidence=True, replay=True

## Boundary

- Repair and fail-closed schema replay only.
- The one-field admission in commit 11ccf80 is explicitly superseded.
- The prior 10-field AC36 membership-candidate result remains valid.
- Formal AC36 membership requires complete Project 36 evidence for all expected fields.
- U_AC36 is invoked only if complete replay passes.
- No fork selection, G900 slot, limit, anchor, target, coupling, channel, transport, theorem extension, geometry, GR, physics, force, body mutation, or Gap A closure claim.

## Next target

`inspect_missing_project36_ac36_schema_evidence_001`
