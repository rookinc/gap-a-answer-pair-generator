# Audit native channel bit as provenance projection 001

## Keeper

We found the bit. It was a receipt bit, not yet a feedback bit.

## Verdict

`native_bit_is_derived_provenance_projection`

## Exact construction

```python
0039: ss=[str(v) for v in x.get("support_sources",[])]
0051: "native":any("native_chain" in s for s in ss),
0060: for mode in ["role_hooks","support_sources","native"]:
```

The generator defines the bit by testing whether any support-source path contains `native_chain`.

## Result

- audit_pass: True
- packet_row_count: 48
- native_row_count: 24
- non_native_row_count: 24
- count_match: True
- support_source_ablation_erases_native_bit: True
- support_sources_status: provenance_carrier
- native_status: derived_provenance_projection
- native_independent_channel_candidate: False
- native_transport_feedback_bit: False

## Interpretation

The `native` bit is a one-bit projection of source provenance. It receipts native-chain support, but does not yet encode transport feedback, sheet exchange, cocycle value, or cycle closure.

## Boundary

- Native-bit provenance projection audit only.
- No feedback unit admission.
- No transport-feedback interpretation.
- No upstairs/downstairs identification.
- No cocycle or holonomy claim.
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

Recommended next: `search_transition_level_channel_feedback_unit_001`
