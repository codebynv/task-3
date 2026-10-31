# Evidence Hash Canonicalization

A digest is only reproducible when the input representation is stable.

Document:

- which exact bytes are hashed,
- whether metadata is included or excluded,
- the encoding and serialization rules,
- the digest algorithm and version,
- how files are normalized, if at all,
- how the reference digest is protected.

Do not re-encode or normalize evidence silently. Test that identical byte sequences produce the same digest and changed bytes produce a different digest.