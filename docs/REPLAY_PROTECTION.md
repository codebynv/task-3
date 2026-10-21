# Replay Protection

For operations that submit evidence or trigger verification:
- Define when a request is considered a duplicate.
- Use server-side identifiers or idempotency keys where appropriate.
- Check authorization on every request.
- Make retries safe and bounded.
- Distinguish a repeated request from a new verification attempt.
- Do not rely on client timestamps as the sole protection.

Test repeated submissions and delayed responses.