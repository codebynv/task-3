# Incident Response

If a credential or sensitive artifact is exposed:

1. Stop further publication or processing.
2. Revoke or rotate the affected credential.
3. Remove the exposed value from active configuration.
4. Review logs and repository history for further exposure.
5. Document the cause and corrective action.
6. Verify that the replacement credential works.

Deleting a secret from the latest commit does not necessarily remove it from repository history.
