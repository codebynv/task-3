# Verification Result Semantics

Use distinct outcomes for distinct conditions:

- **Verified:** evidence matches the trusted reference.
- **Mismatch:** evidence was checked and did not match.
- **Not found:** no corresponding record exists.
- **Unavailable:** the provider or required service could not be reached.
- **Invalid input:** the request could not be evaluated.

Do not map timeouts or provider failures to a successful verification or a definitive mismatch. Align labels with actual implementation behavior.