# Inspect role-pair channel-axis forbidden hits 001

## Keeper

Order spoke first. Channel may speak cleaner.

## Summary

- inspection_pass: True
- prior_reported_hit_count: 180
- classified_hit_count: 48
- direct_dependency_candidate_count: 48
- proven_forbidden_payload_dependency: False
- leakage_status: no_proven_leakage_hits_are_cooccurrence_or_name_collisions

## Classification

- candidate_path_forbidden_scalar: 48

## Candidates

### role_hooks

- classified_hit_count: 0
- direct_dependency_candidate_count: 0
- direct_dependency_candidate_found: False

### support_sources

- classified_hit_count: 48
- direct_dependency_candidate_count: 48
- direct_dependency_candidate_found: True

### native

- classified_hit_count: 0
- direct_dependency_candidate_count: 0
- direct_dependency_candidate_found: False

## Interpretation

The previous audit used broad nested-object cooccurrence and therefore overcounted possible leakage. This inspection does not treat boundary language, status language, or large-container cooccurrence as proof of downstream payload dependence.

No channel-axis rule, source law, native generator, theorem, proof, or Gap A closure is admitted.
