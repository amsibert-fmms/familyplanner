# Data Model Implementation Plan

This plan breaks down the data-model-related workstreams into actionable task stubs.

Use it alongside the [Planning Index](./README.md) and related references like the [Roadmap](./roadmap.md) (which now owns the enrichment strategy) and the [Data Dictionary](./data-dictionary.md). Enrichment sequencing lives in the roadmap; this plan adds the implementation stubs to keep that guidance actionable.

## Working Notes
- Update task stubs with status tags (e.g., _(In Progress)_, _(Ready for review)_); keep the order aligned with the Roadmap’s Now/Next/Later snapshot.
- Add short decision callouts when schemas change (what changed, why, when) so migrations remain traceable.
- Link to tickets or PRs from each stub after work begins to keep planning artifacts connected to implementation.

## Roadmap → Codex Task Breakdown
These stubs translate roadmap phases into codex-sized tickets. Use the scope tags to keep work batchable.

:::task-stub{title="Phase 0: visibility core hardening"}
- Add `OwnedVisibleModel`/`VisibilityGroup` unit tests covering owner-only, household default, and extended family scopes (see `visibility/models.py`).
- Implement DRF permission mixins that combine owner, household, and group membership (update `visibility/permissions.py`).
- Create seed fixtures for sample households and visibility groups for local/dev data (`visibility/fixtures/`).
:::

:::task-stub{title="Phase 1: household/pet CRUD polish"}
- Build CRUD serializers/views for Household, FamilyMember, Pet, and Location with visibility filters applied (`locations/views.py`, `accounts/views.py`).
- Add list/detail UI copy and filters for “my household” vs. “all members” (web/PWA layer strings).
- Write regression tests to confirm Elder 1 caregivers cannot read Elder 2 data; include household default visibility.
:::

:::task-stub{title="Phase 2: task engine MVP"}
- Implement Task recurrence logic (daily/weekly/monthly/custom) with `TaskCompletion` rollup and assignment (`tasks/models.py`, `tasks/services/recurrence.py`).
- Create Task list endpoints with overdue/due-soon filters plus My Tasks/Household/Elder-specific scopes (`tasks/views.py`).
- Add serializer validation for category-specific constraints (BILL_REMINDER forbids payment fields; ELDER_CARE requires elder link when provided).
:::

:::task-stub{title="Phase 3: nutrition data path"}
- Expand Ingredient fields for macro/micro nutrition and add validation (`food/models.py`, migrations).
- Implement nutrition aggregation for recipes (pulling RecipeIngredient quantities) and persist totals on save (`food/services/nutrition_aggregation.py`).
- Add user-facing checks for allergens/diet conflicts using `UserNutritionProfile` (views/services layered in `accounts` or `food`).
:::

:::task-stub{title="Phase 4: scan/OCR queueing"}
- Implement `ScanEvent` model and barcode lookup pipeline invoking `product_lookup_service.py` and enrichment proposal flow.
- Add Tesseract-backed receipt upload endpoint and line-parsing service with fuzzy product matching (`food/services/receipt_parser.py`).
- Queue enrichment/background sync jobs for offline scans and replays (`tasks/services/background_sync.py`), ensuring idempotent updates.
:::

## 0) Enrichment & Provenance Enablement
Apply the roadmap’s enrichment strategy in code, preserving local-first, user-controlled flows.

:::task-stub{title="Implement enrichment services and provenance"}
- Update `ingredient_enrichment_service.py`, `product_lookup_service.py`, and `nutrition_enrichment_service.py` to honor the roadmap order: Local DB → Open Food Facts → USDA FoodData Central → UPCItemDB → Edamam (paid) → retail APIs. Add per-source timeouts and feature flags so lookups never block saves.
- Normalize service outputs to a proposed payload (name, nutrition, serving size, confidence, source metadata). Persist provenance fields (`source_system`, `source_url`, `source_confidence`) on Ingredients, Products, RecipeIngredients, and any models storing nutrition/barcode data.
- Respect offline entry: queue enrichment requests in `BackgroundSyncJob`; replay them idempotently on reconnect without overwriting user edits. Present review/decline flows before accepting remote data.
- Add observability and QA coverage for source ordering, fallbacks, offline-to-online retries, and user overrides; document API fields as optional/nullable when enrichment is disabled.
:::

## 1) Consolidate Tasks into Core Bill-Reminder Usage
The finance subsystem is removed; bill reminders now use Task with category `BILL_REMINDER`.

:::task-stub{title="Implement bill reminders via Task"}
- Update `tasks` app enums/constants to add `BILL_REMINDER` category alongside HOUSEHOLD/ELDER_CARE/MAINTENANCE/PET.
- Remove or deprecate finance/billing models and references; migrate any legacy billing code to create Tasks instead.
- Add validation/helpers so bill-reminder Tasks forbid financial fields and surface due/recurrence/visibility only.
- Adjust serializers/forms and API responses to expose the new category and hide old finance objects.
- Update UI strings and filtering to treat bill reminders as a Task type (lists, dashboards, reminders).
:::

## 2) BillReminderTemplate Model & Scheduling
Create templates that auto-generate monthly bill reminder Tasks.

:::task-stub{title="Add BillReminderTemplate scheduling"}
- Add `BillReminderTemplate` model with fields (household, name, description, day_of_month_due, recurrence_type=MONTHLY, active) inheriting ownership/visibility mixins.
- Implement scheduler/cron job to instantiate Task(category=BILL_REMINDER) each month per active template; include safeguards against duplicates.
- Add admin/API endpoints to CRUD templates; ensure validation of day-of-month boundaries.
- Write unit tests for template creation, scheduling logic, and Task generation edge cases.
:::

## 3) Nutrition-Enhanced Ingredient Model
Ingredients now store full nutrition per 100g/unit.

:::task-stub{title="Expand Ingredient nutrition fields"}
- Add numeric fields: calories, protein_g, carbs_g, sugars_g, fiber_g, fat_g, saturated_fat_g, sodium_mg, potassium_mg, cholesterol_mg; add optional `micronutrients` JSON.
- Migrations to populate defaults (e.g., null/zero) and backfill if needed.
- Update serializers/forms/admin to expose new fields; enforce unit basis (per 100g or standard unit).
- Add validation/tests ensuring non-negative values and JSON shape.
:::

## 4) Recipe Nutrition Aggregation
Recipes denormalize nutrition totals for performance.

:::task-stub{title="Compute recipe nutrition aggregates"}
- Extend Recipe model with total_calories, total_protein_g, total_carbs_g, total_fat_g, total_sodium_mg, optional `nutrition_json`.
- Implement aggregation logic pulling Ingredient nutrition through RecipeIngredient quantities; store totals on save/signal/management command.
- Ensure unit conversions align with Ingredient’s unit basis; add rounding rules.
- Add tests covering aggregation accuracy and updates when ingredients or quantities change.
:::

## 5) UserNutritionProfile Model
Per-user dietary preferences, goals, and restrictions.

:::task-stub{title="Add UserNutritionProfile"}
- Create OneToOne model to Profile/User with fields: diet_type (enum), calorie_goal, macro_ratio JSON, allergens M2M → Ingredient, ingredient_dietary_restrictions M2M, excluded_ingredients M2M, nutrition_focus_goals JSON, preferred_serving_size, medical_constraints.
- Add admin/API CRUD and validation (macro ratio sums ~100%, optional fields handled).
- Wire meal-planning/grocery/recipe filters to respect profile constraints and warn on conflicts.
- Tests for profile creation, constraints enforcement, and filtering behavior.
:::

## 6) Meal Planning & Alerts Integration
Use nutrition data to power warnings and summaries.

:::task-stub{title="Integrate nutrition into meal planning and alerts"}
- Update meal plan day/entry services to aggregate daily nutrition from recipes; compare against UserNutritionProfile goals.
- Add allergen/diet conflict detection (ingredient presence vs. profile exclusions/allergens).
- Surface alerts in UI and push notifications; add Automation trigger types NUTRITION_GOAL_ALERT, ALLERGEN_WARNING, DIET_CONFLICT_DETECTED.
- Tests for aggregation accuracy and alert triggering logic.
:::

## 7) Cleanup Removed Financial Structures
Remove obsolete finance artifacts to avoid confusion.

:::task-stub{title="Deprecate/remove finance subsystem"}
- Delete/disable models for bill accounts, payments, autopay, bank fields, and financial visibilities.
- Migrate data: convert any future-due bills into BillReminderTemplates or Tasks; drop unused tables/columns.
- Update documentation and user-facing copy to reflect reminder-only flow.
- Regression tests ensuring no finance endpoints or UI paths remain.
:::

## 8) Documentation & Migration Strategy
Ensure clarity and safe rollout.

:::task-stub{title="Document and migrate"}
- Produce ERD/update docs describing new Task category, BillReminderTemplate, Ingredient/Recipe/UserNutritionProfile fields.
- Plan migrations: schema first, then data backfill for ingredients/recipes, then feature toggles for scheduling.
- Add release notes and admin/operator runbook for the monthly scheduler.
:::
