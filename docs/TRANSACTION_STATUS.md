# Transaction Status Handling

Represent blockchain transaction states accurately.

- **Not submitted:** no transaction was sent.
- **Pending:** submitted but not yet confirmed.
- **Confirmed:** expected confirmation was observed.
- **Failed:** submission or execution failed.
- **Unknown:** status could not be determined.

Do not label a transaction successful based only on receiving a transaction hash. Keep the hash available for troubleshooting when appropriate.
