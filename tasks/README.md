# Tasks App

The Tasks app organizes household tasks, schedules, and reminders within FamilyPlanner.

## Purpose
- Provide a central task model with due dates, recurrence, and assignment.
- Support checklists and sub-tasks for complex chores.
- Enable reminders and status tracking for each task.

## Planned Features
- Task model with title, description, due date/time, priority, and completion state.
- Optional recurrence rules and reminder notifications.
- Assignment to users or roles within a household.
- Checklist items linked to tasks with independent completion tracking.
- Attachments and notes for richer context.

## Integration Points
- Uses Accounts for assignee and creator relationships.
- Associates tasks with Locations for place-specific errands.
- Respects Visibility rules for who can view, edit, or complete tasks.

## Development Notes
- Consider background jobs for sending reminders or recalculating recurrence.
- Admin configuration should offer filters for status, priority, and household.
- Tests should cover task creation, status transitions, recurrence handling, and permissions.
