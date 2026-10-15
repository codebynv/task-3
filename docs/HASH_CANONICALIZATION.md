# Hash Canonicalization

A reproducible integrity check requires the same canonical representation before hashing.

- Define the exact fields included.
- Use a deterministic field order and serialization.
- Specify text encoding.
- Handle missing and null values consistently.
- Keep the hash algorithm consistent.
- Test equivalent records and changed records.

If canonicalization changes, document the compatibility impact for previously stored hashes.
