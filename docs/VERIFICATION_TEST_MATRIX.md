# Verification Test Matrix

| Scenario | Expected result |
|---|---|
| Unchanged canonical record | Fingerprint matches stored value |
| Modified field | Fingerprint differs |
| Missing source data | Verification reports insufficient data |
| Search provider failure | Controlled error is shown |
| RPC or transaction failure | Failure is visible and traceable |
| Sensitive configuration missing | No secret is fabricated or exposed |

A successful hash comparison verifies data integrity only; it does not prove a person's identity.
