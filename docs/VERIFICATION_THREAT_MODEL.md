# Verification Threat Model

Consider these failure and abuse cases:
- a user submits altered metadata,
- an image or payload is too large,
- an external provider times out,
- a stored fingerprint is replaced,
- a caller accesses another user's record,
- a replayed request creates duplicate evidence.

Define trust boundaries, authorization checks, input limits, and safe failure behavior before extending the verification flow.
