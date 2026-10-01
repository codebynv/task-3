# Verification Model

Task #3 separates discovery from integrity verification.

## Evidence flow

    Face input
       ↓
    Face processing
       ↓
    External search result
       ↓
    Canonical record
       ↓
    SHA-256 fingerprint
       ↓
    Sepolia record
       ↓
    Recompute + compare

## What verification proves

A matching hash demonstrates that the canonical record being checked has the same fingerprint as the anchored record.

It does not independently prove that a reverse-image search result identifies a real-world person.

## Tamper scenario

1. Load the original canonical record.
2. Recompute its hash.
3. Compare it with the stored hash.
4. Modify a field in memory.
5. Recompute the modified hash.
6. Confirm the hashes differ.
7. Leave the blockchain record unchanged.

This keeps discovery evidence and integrity evidence clearly separated.
