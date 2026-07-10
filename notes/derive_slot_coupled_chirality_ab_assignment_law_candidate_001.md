# Derive slot-coupled chirality A/B assignment law candidate 001

Status: `SLOT_COUPLED_CHIRALITY_AB_ASSIGNMENT_LAW_CANDIDATE_001_DERIVED`

## Keeper

A/B is not chosen by the answer. A/B is handed by the apparatus.

## Summary

- derive_pass: `True`
- candidate_name: `slot_coupled_chirality_ab_assignment_law_candidate`
- law_surface: `from_slot, to_slot, from_C, to_C -> from_A, from_B, to_A, to_B and ab_delta_pair`
- row_count: `156`
- key_map_count: `24`
- key_conflict_count: `0`
- hand_signature_count: `19`
- ab_assignment_law_admitted: `False`
- chirality_admitted: `False`
- gap_a_closure: `False`
- native_generator_admitted: `False`
- answer_label_leakage_closed: `False`
- source_law_admitted: `False`
- recommended_next: `negative_test_slot_coupled_chirality_ab_law_candidate_001`

## Law candidate

A/B assignment is the visible side-face outcome of a slot/C chirality rule.

Slot motion plus C endpoint motion hands the A/B side-face transition.

## Interpretation

The law surface determines A/B behavior from a directed slot motion and C endpoint motion, without using answer-label fields. This has the form of a handed transition rather than a flat selector.

from_slot and to_slot provide apparatus motion, while from_C and to_C provide the orientation socket. The A/B side-face transition is handed by that apparatus surface.

No leakage was detected on observed rows, but answer-label leakage is not closed. This remains a law candidate, not an admitted A/B assignment law.

## Boundary

- Candidate law only.
- Chirality candidate only.
- No theorem.
- No proof claim.
- No Gap A closure.
- No native generator admission.
- No A/B assignment law admission.
- No chirality admission.
- No full role-labeled shared_B derivation.
- No answer-label leakage closure.
- No source law admission.
- No physics claim.
- No force claim.
