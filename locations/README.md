# Locations App

The Locations app tracks households, venues, and geospatial context used across FamilyPlanner.

## Purpose
- Store household records and shared spaces linked to user accounts.
- Manage places related to tasks (e.g., grocery stores, schools, parks).
- Provide geocoding hooks for mapping and distance calculations.

## Planned Features
- Household model with address, timezone, and default visibility settings.
- Venue/place model with optional coordinates and category tags.
- Support for tagging locations per task or checklist item.
- Search endpoints to find locations by name, category, or proximity.
- Basic validations for address and timezone fields.

## Integration Points
- Consumes membership data from Accounts to enforce who can manage a household.
- Shares location references with Tasks for scheduling and reminders.
- Works with Visibility to determine who can view or edit location details.

## Development Notes
- Consider leveraging Django GIS add-ons if geospatial queries are needed later.
- Admin pages should surface household and venue data with filters by owner or type.
- Tests should verify location creation, search filters, and permission-aware access.
