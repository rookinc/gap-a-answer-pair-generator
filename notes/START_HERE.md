# Start here

## Current state

Project 18 admitted the bounded G900 kernel package.

The later WXYZTI audit found a local reciprocal pair grammar:

    reverse_partner:
        (A, B, C) -> (A, C, B)

    shared_B:
        preserves B / slot

    pair grammar:
        shared_B.to_C = reverse_partner.from_B = reverse_partner.from_slot
        reverse_partner.to_B = shared_B.from_C

The pair grammar selected exactly 12 realized answer-pairs from 48 realized row-pair candidates.

## This project

This project asks whether the row-pair universe can be generated natively.

## Win condition

Gap A closure requires a native generator that produces a candidate universe without using realized/admitted pair labels, followed by an exact reciprocal selector:

    accepted = 12
    false positives = 0
    misses = 0

## Boundary

Until that generator is found, this is a generator search, not a closure theorem.
