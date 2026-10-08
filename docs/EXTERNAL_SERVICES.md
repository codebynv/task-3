# External Services

Task #3 depends on external services for search and blockchain interaction.

- Treat provider responses as untrusted input.
- Handle timeouts and failed requests explicitly.
- Keep credentials outside source control.
- Avoid assuming a provider always returns a result.
- Record enough context to diagnose failures without logging secrets.

External service failures should produce a controlled application result rather than an unhandled crash.
