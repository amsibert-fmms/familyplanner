# Family Planner Roadmap

This roadmap outlines phased delivery for the Family Planner project, including core milestones and estimated timelines.

See the [Planning Index](./README.md) for how this roadmap fits with the [Data Model Plan](./data-model-plan.md), [Enrichment Strategy](./enrichment-strategy.md), and [Data Dictionary](./data-dictionary.md).

## 🗾 Phase 0 — Foundation & Infrastructure (1–2 weeks)

### 0.1 Project Setup
- Create Django project and initial apps.
- Set up PostgreSQL with optional Docker Compose support.
- Add Django REST Framework for APIs.
- Install Django Allauth if needed.
- Create `accounts`, `visibility`, `locations`, `tasks`, and `food` apps.

### 0.2 Core Framework Features
- Implement an `OwnedVisibleModel` abstract base class.
- Implement `VisibilityGroup` for grouping visibility rules.
- Implement `Profile` support.
- Create household membership model and account linking.
- Add a permissions system (custom DRF permissions mixing household/group logic).

### 0.3 Continuous Integration & Deployment
- Set up dev, staging, and production deployment flows.
- Configure static media storage.
- Enable HTTPS for the PWA and push notifications.

### 0.4 PWA Essentials
- Create `manifest.json`.
- Implement a base service worker.
- Enable an offline shell.

## 🧱 Phase 1 — Core Household Structure (1–3 weeks)

### 1.1 Household, Family, Pets, Locations
- CRUD UI for household, family members, basic user profile settings, pets, and locations (home, elder’s house, apartment).
- Role-based visibility for each object.
- Migration of real family data (test set).

### 1.2 Visibility & Permissions Enforcement
- Implement global query filters.
- Test cases:
  - Owner-only private items.
  - Elder 1 caregivers cannot see Elder 2 data.
  - Extended family visibility.
  - Household default visibility.

**Milestone:** Family management and privacy model fully working.

## 🧰 Phase 2 — Tasks & Reminders (2–4 weeks)

### 2.1 Task System Foundations
- Create Task with recurrence (daily, weekly, monthly, and optional custom rules).
- Implement TaskCompletion.
- Create assignment system (to user or visibility group).

### 2.2 Elder Care Tasks
- Elder model and Caregivers model.
- `ElderCareTaskTemplate` → Task auto-generation scheduler.

### 2.3 Property Maintenance Tasks
- `MaintenanceSchedule` → Task auto-generation.

### 2.4 Bill Reminder Templates
- Create `BillReminderTemplate` (no bank/payments, purely due-date reminders).
- Monthly cron job generates tasks.

### 2.5 Task UI & Filters
- My tasks, household tasks, elder-specific task views.
- Overdue, due soon, completed filters.

**Milestone:** Unified task engine powering chores, elder care, maintenance, and bills.

## 🧴 Phase 3 — Meal Planning & Food Foundations (3–5 weeks)

### 3.1 Ingredients & Nutrition System
- Ingredient model with full nutrition fields and CRUD UI.
- External lookup service architecture (USDA / OpenFoodFacts requests).
- Manual edits before save and a nutrition calculation service.

### 3.2 Recipes
- Recipe CRUD and `RecipeIngredient` linking.
- Nutrition aggregation per recipe and per serving.
- Recipe visibility (owner, groups).

### 3.3 Pantry
- `PantryLocation` and `PantryItem` CRUD.
- Expiration handling.

### 3.4 Grocery Lists
- `GroceryList` and `GroceryListItem` with auto-add deficits:
  - Shopping list based on recipes planned.
  - Items missing from pantry.

### 3.5 Meal Planning Calendar
- `MealPlanDay` and `MealPlanEntry`.
- Nutrition per-day roll-up.

**Milestone:** A working local-first meal planner with nutrition integration and pantry automation.

## 📸 Phase 4 — Barcode Scanning & Receipt OCR (4–6 weeks)

### 4.1 Barcode Scanning
- Implement barcode scanning (PWA camera).
- Create `ScanEvent` pipeline to match or create Product → Ingredient.
- External product lookup with user-edit-review before save.
- Auto-add to grocery list and pantry.

### 4.2 Receipt OCR (Local Tesseract)
- Tesseract installation and testing.
- Receipt upload model and OCR pipeline storing raw text.
- Line parsing engine with fuzzy product matching.
- Optional external enrichment from APIs.
- UI for user correction: edit matched product, edit quantity, approve adding to pantry, mark grocery list purchased.

### 4.3 Background Sync Processing
- PWA offline scan queue.
- `BackgroundSyncJob` and server endpoint to process pending jobs.

**Milestone:** Phone scans → Products → Pantry + Grocery tracking fully automated.

## 🔔 Phase 5 — Notifications, Automation, PWA (2–4 weeks)

### 5.1 Push Notifications
- Implement push subscription model and VAPID key generation.
- Subscribe/unsubscribe UI and server-side send logic.

### 5.2 Scheduled Job System
- Daily cron job checks: overdue tasks, bills due soon, elder medications, elder care tasks, expiring pantry items, nutrition conflicts (if enabled).

### 5.3 Automation Rules
- Users can configure nutrition alerts, pantry expiring alerts, task/bill reminders, elder care requirements.

### 5.4 PWA Polishing
- Offline caching for tasks, meals, shopping list.
- Background sync for scans and receipt uploads.
- Add “Add to Home Screen” meta.

**Milestone:** A fully functional PWA with push notifications and automation.

## 🧬 Phase 6 — User Nutrition Profiles (2–3 weeks)

### 6.1 Nutrition Profiles
- Create `UserNutritionProfile` with allergens, excluded ingredients, macro goals, medical constraints.

### 6.2 Integrations
- Highlight recipes that violate constraints; grocery warning flags; meal plan nutrition roll-up vs. user goals.

### 6.3 Elder-Specific Nutrition
- Tie elder medication, medical needs, and nutrition.
- Alerts for sodium, food-clinic contraindications, fiber/constipation, hydration reminders.

**Milestone:** Personalized nutrition-aware meal planning for all users and elders.

## 🪚 Phase 7 — Hardening, QA, Performance (2–4 weeks)

### 7.1 Performance
- Add indexes and denormalized fields as needed.
- Improve OCR parsing accuracy.
- Caching strategy for recipes, nutrition, visibility filters.

### 7.2 UI Polish
- Task drag-drop, meal plan weekly grid, pantry color coding for expiring items, elder dashboards.

### 7.3 Permissions Audit
- Confirm visibility rules correct.
- Household-only objects behave correctly.
- Elder-specific caregivers limited appropriately.

## 🏁 Phase 8 — Optional Advanced Features (ongoing)

- AI-based ingredient extraction from text recipes.
- AI-based meal planning according to nutrition profile.
- Natural language task creation and voice input for groceries.
- Wearable integrations (Fitbit, Apple Health).
- Multi-household collaboration (merge visibility groups).
- Machine learning for receipt parsing and product matching.

## 📌 Grand Timeline Summary (Flexible)

| Phase | Est. Time | Core Outcome |
| --- | --- | --- |
| 0 | 1–2 weeks | Infrastructure + PWA skeleton |
| 1 | 1–3 weeks | Household, visibility, locations |
| 2 | 2–4 weeks | Task engine + elder care + maintenance + bills |
| 3 | 3–5 weeks | Food, nutrition, pantry, grocery, meal planning |
| 4 | 4–6 weeks | Barcode + OCR + enrichment pipeline |
| 5 | 2–4 weeks | Push notifications + automation |
| 6 | 2–3 weeks | Nutrition profiles & diet rules |
| 7 | 2–4 weeks | Optimization + hardening |
| 8 | ongoing | Advanced AI & integrations |

**Total MVP:** Approximately 12–20 weeks depending on depth per phase.
