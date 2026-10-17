# External Provider Failure Handling

When an external search or RPC provider fails:

- Distinguish provider failure from a negative result.
- Apply a bounded timeout.
- Show a clear retry path when safe.
- Avoid exposing API credentials in errors.
- Preserve diagnostic identifiers without logging sensitive payloads.
- Never fabricate a successful verification result.

A failed lookup means the result is unknown, not that a match was or was not found.
