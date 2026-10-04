# Data Lifecycle

The project handles several categories of data.

## Flow

    Input image
        ↓
    Face processing
        ↓
    Temporary derived data
        ↓
    Search result
        ↓
    Canonical record
        ↓
    Integrity hash

Keep temporary and sensitive data out of source control and remove it when it is no longer required.

## Principle

Store only the minimum information needed for the demonstration and verification workflow.
