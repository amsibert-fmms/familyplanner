# Accounts App

The Accounts app manages user identities, authentication, and household membership context for the FamilyPlanner project.

## Purpose
- Provide a central user profile that can be linked to multiple households.
- Handle account lifecycle tasks such as registration, login, and credential recovery.
- Expose role-aware information (e.g., guardian vs. child access) to other apps.

## Planned Features
- Email and password-based authentication with optional social login providers.
- Profile data for each user, including contact details and avatar.
- Household membership records with roles and join/invite flows.
- Session and token issuance for the API.
- Audit fields on user-related changes to support activity history.

## Integration Points
- Shares authenticated user context with the Tasks, Locations, and Visibility apps.
- Accepts visibility rules from the Visibility app to tailor what user profile data is exposed.
- Emits signals for user creation and membership changes that other apps can subscribe to.

## Development Notes
- Models will likely extend Django's `AbstractUser` or use a OneToOne profile pattern.
- Admin configuration should group authentication, profile, and membership management.
- Tests should cover authentication flows, role enforcement, and invitation acceptance.
