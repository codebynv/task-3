# Security and Privacy Notes

Task #3 combines face processing, external search, and blockchain verification. These boundaries should remain explicit during development and demos.

## Face data

- Treat uploaded face images and generated embeddings as sensitive data.
- Do not commit sample images containing real people unless you have permission to use them.
- Keep temporary image files outside version control.
- Avoid logging raw embeddings or unnecessary personal information.

## Reverse-image search

A reverse-image result is discovery evidence, not proof of a person's real-world identity.

The application should clearly distinguish:

1. face detection and representation,
2. external search results,
3. the selected canonical source,
4. the blockchain integrity record.

## Blockchain data

Only the minimum canonical record needed for verification should be anchored on-chain.

The project should not place raw face images or face embeddings on the public testnet.

## Secrets

Keep API keys, wallet private keys, RPC credentials, and environment-specific configuration in local environment variables.

Never commit:

- .env files,
- private keys,
- API keys,
- wallet seed phrases.

## Demo hygiene

Before a public demo:

- [ ] Remove real personal data from test fixtures.
- [ ] Confirm secrets are excluded by .gitignore.
- [ ] Use a testnet wallet with no unnecessary funds.
- [ ] Verify the displayed source is clearly labelled as a search result.
