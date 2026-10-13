# Blockchain Failure Handling

For testnet transactions, account for:

- missing RPC configuration,
- unavailable RPC endpoint,
- rejected transaction,
- insufficient testnet funds,
- pending transaction,
- reverted transaction,
- confirmation timeout.

Display the actual transaction status when known. Do not report success before the chain confirms the expected result.
