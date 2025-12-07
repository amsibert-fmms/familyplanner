# Visibility App

The Visibility app centralizes access control and sharing logic across FamilyPlanner resources.

## Purpose
- Define who can view or edit specific records (tasks, locations, households).
- Offer share links or invite-based access for non-members when appropriate.
- Provide policy evaluation utilities for other apps.

## Planned Features
- Rules engine describing permissions by role, membership, and resource ownership.
- Shareable link generation with configurable expiration and scopes.
- Access logs to record when resources are viewed or modified.
- Middleware or utilities to enforce visibility rules at the API layer.
- Administrative overrides for guardians or owners.

## Integration Points
- Consumes user and membership data from Accounts.
- Applies to Tasks and Locations to determine read/write access.
- Emits audit events that can be surfaced in activity feeds.

## Development Notes
- Consider a reusable policy API (e.g., decorators or DRF permissions) to keep logic centralized.
- Admin pages should allow inspecting current rules and active share links.
- Tests should validate policy evaluation, share link lifecycles, and audit logging.
