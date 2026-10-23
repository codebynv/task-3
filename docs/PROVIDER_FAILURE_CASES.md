# Provider Failure Cases

Test verification when an external provider:

- times out,
- returns an invalid response,
- returns a not-found result,
- rate-limits requests,
- returns an authentication error,
- is temporarily unavailable.

Keep provider failure distinct from a valid negative verification result. Do not leak provider credentials in errors or logs.