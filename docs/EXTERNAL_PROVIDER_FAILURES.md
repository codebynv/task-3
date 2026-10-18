# External Provider Failure Handling

When a search or RPC provider fails:

- Distinguish provider failure from a negative result.
- Apply a bounded timeout.
- Show a retry path when safe.
- Avoid exposing API credentials in errors.
- Preserve diagnostic identifiers without sensitive payloads.
- Never fabricate a successful verification result.

A failed lookup means the result is unknown.