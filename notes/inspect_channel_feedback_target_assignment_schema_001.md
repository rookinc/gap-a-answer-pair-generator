# Inspect channel feedback target-assignment schema 001

## Keeper

The feedback search refused a label that was not present. Now recover the actual assignment.

## Summary

- inspection_pass: True
- primary_packet_row_path: $.source_packet_index
- primary_packet_row_count: 48
- target_assignment_directly_in_packet_rows: False
- assignment_status: target_assignment_likely_external_to_packet_rows
- exact_48_row_list_count: 1
- exact_24_row_list_count: 0
- likely_assignment_path_count: 8

## Packet row keys

- law_key: 48
- source_packet_id: 48
- source_payload: 48
- support_count: 48
- support_paths_first_12: 48
- support_sources: 48

## Likely assignment paths

```json
[
  {
    "path": "$.summary.unique_native_g15_embedding_proven",
    "value": false,
    "value_type": "bool"
  },
  {
    "path": "$.summary.non_native_row_count",
    "value": 24,
    "value_type": "int"
  },
  {
    "path": "$.summary.native_row_count",
    "value": 24,
    "value_type": "int"
  },
  {
    "path": "$.summary.native_generator_admitted",
    "value": false,
    "value_type": "bool"
  },
  {
    "path": "$.result.channel_profiles.native.exact_bucket_count",
    "value": 2,
    "value_type": "int"
  },
  {
    "path": "$.result.channel_profiles.native.bucket_count",
    "value": 2,
    "value_type": "int"
  },
  {
    "path": "$.boundary.unique_native_g15_embedding_proven",
    "value": false,
    "value_type": "bool"
  },
  {
    "path": "$.boundary.native_generator_admitted",
    "value": false,
    "value_type": "bool"
  }
]
```

## Boundary

- Target-assignment schema inspection only.
- No feedback unit admitted.
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

Recommended next: `reconstruct_channel_feedback_target_assignment_001`
