# Verification Trust Boundaries

Document which components are trusted and which are not.

- Treat uploaded evidence and client metadata as untrusted.
- Validate inputs on the server.
- Check authorization independently of verification results.
- Protect reference digests and audit records from unauthorized changes.
- Distinguish integrity checks from identity or ownership claims.
- Report provider outages as unavailable, not as verified or mismatched.

Use synthetic records for test scenarios and avoid publishing sensitive identity data.