# Threat Model

## Sensitive assets

- Uploaded images
- Face embeddings
- API credentials
- Wallet private keys
- Search-provider credentials
- Blockchain transaction configuration

## Main risks

### Credential exposure

Mitigation: environment variables, secret management, and repository ignore rules.

### Sensitive data leakage

Mitigation: avoid unnecessary logs and avoid committing real personal images or embeddings.

### Untrusted search results

Mitigation: treat external results as untrusted discovery data and validate the selected canonical fields.

### Transaction misuse

Mitigation: use a testnet wallet for demos and keep transaction inputs constrained.

## Security principle

Minimize the amount of sensitive information collected, logged, stored, and transmitted.
