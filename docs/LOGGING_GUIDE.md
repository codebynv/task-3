# Logging Guide

Logs should help diagnose failures without exposing sensitive information.

## Log

Useful operational events include:

- pipeline phase started,
- phase completed,
- external search failure,
- transaction submission status,
- verification result.

## Avoid

Do not log:

- private keys,
- API credentials,
- raw face embeddings,
- unnecessary personal data.

Use concise structured messages that make failures traceable.
