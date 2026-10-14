# Chain Data Integrity

- Define the exact canonical fields included in the fingerprint.
- Use a deterministic serialization before hashing.
- Keep hash algorithm and encoding consistent.
- Test that field changes alter the fingerprint.
- Test that equivalent canonical records produce the same fingerprint.
- Handle missing fields explicitly.

A reproducible hash comparison establishes data consistency under the chosen scheme, not the truth of the underlying claims.
