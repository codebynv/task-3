# Integrity Check Design

For data-integrity checks, document:

- the exact canonical representation being hashed,
- the hash algorithm and encoding,
- where the expected digest is stored,
- how changed or missing data is reported,
- how failures differ from mismatches,
- who is authorized to replace reference data.

A digest detects changes relative to a trusted reference; it does not independently establish authenticity.