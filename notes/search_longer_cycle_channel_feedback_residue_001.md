# Search longer-cycle channel feedback residue 001

## Keeper

No triangle closed. The bit may need a longer sentence.

## Summary

- search_pass: True
- verdict: `longer_cycle_residue_candidate_found`
- node_count: 24
- transition_count: 28
- scc_count: 3
- cyclic_scc_count: 3
- simple_cycle_count: 7
- cycle_length_counts: {6: 4, 10: 1, 12: 2}
- tested_bit_count: 14
- feedback_candidate_count: 11
- feedback_candidate_found: True

## Leading candidate

```json
{
  "feature": "role_hook_change",
  "cycle_parity_counts": {
    "0": 5,
    "1": 2
  },
  "length_parity_counts": {
    "6": {
      "0": 4
    },
    "10": {
      "1": 1
    },
    "12": {
      "0": 1,
      "1": 1
    }
  },
  "both_cycle_residues_seen": true,
  "rotation_invariant": true,
  "reversal_pair_count": 0,
  "reversal_residue_match_count": 0,
  "reversal_residue_mismatch_count": 0,
  "reversal_consistent_where_tested": true,
  "longer_cycle_feedback_candidate": true
}
```

## Boundary

- Longer directed-cycle residue search only.
- Native provenance receipt bit excluded.
- Support-source filenames excluded from feedback features.
- No feedback unit admission.
- No transport-feedback rule admission.
- No cocycle admission.
- No holonomy-class admission.
- No upstairs/downstairs identification.
- No channel-axis rule admission.
- No source law admission.
- No native generator admission.
- No unique native G15 embedding proof.
- No full theorem admitted.
- No proof claim.
- No Gap A closure.
- No geometry claim.
- No physics claim.
- No force claim.

Recommended next: `audit_longer_cycle_feedback_candidate_for_switching_invariance_001`
