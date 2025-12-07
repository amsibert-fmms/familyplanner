# Planning Data Dictionary

This document captures the full data dictionary for the Family Planner application, organized by app.

## Navigation
- [accounts](#1-app-accounts)
- [visibility](#2-app-visibility)
- [locations](#3-app-locations)
- [eldercare](#4-app-eldercare)
- [tasks](#5-app-tasks)
- [food](#6-app-food-recipes-ingredients-nutrition)
- [scanning](#7-app-scanning)
- [notifications](#8-app-notifications)
- [automation](#9-app-automation)
- [pwa](#10-app-pwa)
- [nutrition](#11-app-nutrition)

Use this reference alongside the roadmap and implementation plan to keep schemas consistent across services and APIs.

## 1. App: accounts

### 1.1 Profile
One-to-one with Django `User`.

| Field | Type | Description |
| --- | --- | --- |
| user | OneToOne → User | Links Django account |
| default_household | FK → Household | User’s primary household |
| timezone | string | User time zone |
| preferred_units | string | "metric" or "us" |
| nutrition_profile | OneToOne → UserNutritionProfile | User dietary constraints & goals |
| notification_preferences | JSON | Per-category toggles, e.g., tasks, bills, elder care |

### 1.2 Household

| Field | Type | Description |
| --- | --- | --- |
| id | UUID | Primary key |
| name | string | e.g. “Sibert Household” |
| owner | FK → User | Household admin |
| members | M2M → User | Core adults |
| extended_family_members | M2M → FamilyMember | Non-user relatives |

### 1.3 FamilyMember

| Field | Type | Description |
| --- | --- | --- |
| id | UUID |  |
| household | FK → Household |  |
| linked_user | FK → User (nullable) | When a family member has an account |
| full_name | string |  |
| relationship_to_household | string | “spouse”, “child”, “elder parent”, etc. |
| is_elder | bool | Marks whether tied to eldercare system |
| primary_location | FK → Location (nullable) | Where they live |

### 1.4 Pet

| Field | Type | Description |
| --- | --- | --- |
| id | UUID |  |
| household | FK → Household |  |
| name | string |  |
| species | string | cat/dog/etc |
| breed | string (optional) |  |
| date_of_birth | date (optional) |  |
| primary_location | FK → Location (nullable) |  |
| primary_caregiver_user | FK → User (nullable) |  |
| primary_caregiver_family_member | FK → FamilyMember (nullable) |  |

## 2. App: visibility

### 2.1 OwnedVisibleModel (abstract)

| Field | Type | Description |
| --- | --- | --- |
| owner | FK → User | Creator/owner |
| private_to_owner | bool | True → only owner sees |
| visibility_groups | M2M → VisibilityGroup | Sharing control |
| visibility_override | enum | HOUSEHOLD_DEFAULT, EXTENDED_FAMILY, CUSTOM_GROUPS_ONLY |

### 2.2 VisibilityGroup

| Field | Type | Description |
| --- | --- | --- |
| id | UUID |  |
| household | FK → Household | Groups are household-scoped |
| owner | FK → User | Person who created the group |
| name | string |  |
| members | M2M → User | Users with access |
| default_for_elder | FK → Elder (nullable) | For elder-specific visibility pools |

## 3. App: locations

### 3.1 Location (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| id | UUID |  |
| household | FK → Household |  |
| name | string | “Main house”, “Elder 1 apartment” |
| location_type | enum | PRIMARY_HOME, ELDER_HOME, OTHER |
| address_line1 | string |  |
| address_line2 | string | optional |
| city, state, postal_code, country | strings |  |
| notes | text |  |
| is_primary | bool | Marks main home |

### 3.2 PropertyNote (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| location | FK → Location |  |
| title | string |  |
| body | text |  |
| tags | string (optional) |  |
| pinned | bool |  |

### 3.3 MaintenanceSchedule (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| location | FK → Location |  |
| name | string |  |
| description | text |  |
| recurrence_type | enum | daily, weekly, monthly, custom |
| interval | int | e.g. every 2 weeks |
| day_of_week | int (nullable) |  |
| day_of_month | int (nullable) |  |
| next_due | date |  |
| last_completed | date (nullable) |  |
| auto_create_task | bool | Generate Task automatically |

## 4. App: eldercare

### 4.1 Elder (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| family_member | OneToOne → FamilyMember | Must equal an elder |
| primary_location | FK → Location |  |
| date_of_birth | date |  |
| medical_summary | text | High-level notes only |

### 4.2 Caregiver

| Field | Type | Description |
| --- | --- | --- |
| elder | FK → Elder |  |
| caregiver_family_member | FK → FamilyMember (nullable) |  |
| caregiver_user | FK → User (nullable) |  |
| external_name | string (nullable) |  |
| relationship | string | daughter, nurse, etc. |
| is_primary | bool |  |

### 4.3 ElderMedicalNeed (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| elder | FK → Elder |  |
| title | string |  |
| description | text |  |
| severity | int (optional) |  |
| notes | text |  |

### 4.4 ElderMedication (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| elder | FK → Elder |  |
| name | string |  |
| dosage | string |  |
| instructions | text |  |
| frequency_type | enum | daily, weekly, etc. |
| times_of_day | JSON | [“08:00”,”20:00”] |
| prescribing_doctor | string (optional) |  |
| pharmacy | string (optional) |  |
| active | bool |  |

### 4.5 ElderCareTaskTemplate (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| elder | FK → Elder |  |
| title | string |  |
| description | text |  |
| recurrence_type | enum |  |
| interval | int |  |
| days_of_week | JSON (optional) |  |
| linked_medication | FK → ElderMedication (nullable) |  |
| default_assignee_group | FK → VisibilityGroup (nullable) |  |

## 5. App: tasks

### 5.1 Task (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| title | string |  |
| description | text |  |
| category | enum | HOUSEHOLD, ELDER_CARE, MAINTENANCE, PET, BILL_REMINDER |
| location | FK → Location (nullable) |  |
| elder | FK → Elder (nullable) |  |
| pet | FK → Pet (nullable) |  |
| related_maintenance_schedule | FK → MaintenanceSchedule (nullable) |  |
| due_date | date (nullable) |  |
| due_datetime | datetime (nullable) |  |
| priority | int |  |
| is_completed | bool |  |
| last_completed_at | datetime (nullable) |  |
| created_from_template | FK → ElderCareTaskTemplate (nullable) |  |
| assigned_to_user | FK → User (nullable) |  |
| assigned_to_group | FK → VisibilityGroup (nullable) |  |
| recurrence_type | enum |  |
| recurrence_rule | FK → RecurrenceRule (nullable) |  |

### 5.2 RecurrenceRule

| Field | Type | Description |
| --- | --- | --- |
| frequency | enum | daily, weekly, monthly |
| interval | int |  |
| by_weekday | JSON (optional) |  |
| by_monthday | int (nullable) |  |
| start_date | date |  |
| end_date | date (nullable) |  |

### 5.3 TaskCompletion

| Field | Type | Description |
| --- | --- | --- |
| task | FK → Task |  |
| completed_by | FK → User (nullable) |  |
| completed_at | datetime |  |
| notes | text |  |
| source | string | “web”, “mobile”, “pwa-sync” |

### 5.4 BillReminderTemplate (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| name | string |  |
| description | text |  |
| day_of_month_due | int |  |
| recurrence_type | enum | = monthly |
| active | bool |  |
| last_generated | date (nullable) |  |

Creates `Task(category=BILL_REMINDER)` monthly.

## 6. App: food (recipes, ingredients, nutrition)

### 6.1 Ingredient (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| name | string |  |
| default_unit | string | g, ml, tbsp, etc. |
| category | string (e.g. “Produce”) |  |
| calories | float | per 100g |
| protein_g | float |  |
| carbs_g | float |  |
| sugars_g | float |  |
| fiber_g | float |  |
| fat_g | float |  |
| saturated_fat_g | float |  |
| sodium_mg | float |  |
| potassium_mg | float |  |
| cholesterol_mg | float |  |
| micronutrients | JSON | vitamins/minerals |
| source_system | string | USDA / OFF / Manual |
| source_url | string (nullable) |  |
| source_confidence | float (nullable) | 0–1 |

### 6.2 Recipe (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| title | string |  |
| description | text |  |
| instructions | text |  |
| servings | int |  |
| tags | string / tag model |  |
| source_url | string (optional) |  |
| total_calories | float | auto-calculated |
| total_protein_g | float |  |
| total_carbs_g | float |  |
| total_fat_g | float |  |
| total_sodium_mg | float |  |
| nutrition_json | JSON | breakdown per serving |

### 6.3 RecipeIngredient

| Field | Type | Description |
| --- | --- | --- |
| recipe | FK → Recipe |  |
| ingredient | FK → Ingredient (nullable) |  |
| ingredient_name | string | fallback |
| quantity | float |  |
| unit | string |  |
| optional | bool |  |

### 6.4 Product (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| name | string |  |
| brand | string (optional) |  |
| default_ingredient | FK → Ingredient (nullable) |  |
| unit_size | string | “1L”, “500g” |
| category | string |  |
| source_system | string | USDA/OFF/Manual |
| source_url | string |  |
| source_confidence | float |  |

### 6.5 ProductBarcode

| Field | Type | Description |
| --- | --- | --- |
| product | FK → Product |  |
| barcode_type | string | UPC-A, EAN |
| barcode_value | string | unique |

### 6.6 PantryLocation

| Field | Type | Description |
| --- | --- | --- |
| location | FK → Location |  |
| name | string |  |

### 6.7 PantryItem (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| location | FK → PantryLocation |  |
| product | FK → Product (nullable) |  |
| ingredient | FK → Ingredient (nullable) |  |
| item_name | string | fallback |
| quantity | float |  |
| unit | string |  |
| expiration_date | date (nullable) |  |
| added_at | datetime |  |
| source | string | manual, receipt, scan |

### 6.8 MealPlanDay (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| date | date |  |
| household | FK → Household |  |
| location | FK → Location (nullable) |  |
| notes | text |  |

### 6.9 MealPlanEntry

| Field | Type | Description |
| --- | --- | --- |
| meal_plan_day | FK → MealPlanDay |  |
| meal_type | enum | breakfast/lunch/dinner/snack |
| recipe | FK → Recipe (nullable) |  |
| external_description | string |  |
| servings | int |  |

### 6.10 GroceryList (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| name | string |  |
| location | FK → Location (nullable) |  |
| is_default | bool |  |

### 6.11 GroceryListItem

| Field | Type | Description |
| --- | --- | --- |
| grocery_list | FK → GroceryList |  |
| product | FK → Product (nullable) |  |
| ingredient | FK → Ingredient (nullable) |  |
| item_name | string |  |
| quantity | float (nullable) |  |
| unit | string |  |
| is_purchased | bool |  |
| pantry_item_created | FK → PantryItem (nullable) |  |
| source | string | recipe, manual, scan |

## 7. App: scanning

### 7.1 Receipt (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| location | FK → Location (nullable) |  |
| uploaded_by | FK → User |  |
| image_file | File |  |
| uploaded_at | datetime |  |
| purchase_datetime | datetime (nullable) |  |
| merchant_name | string (nullable) |  |
| raw_ocr_text | text | from Tesseract |
| ocr_status | enum | pending/completed/failed |
| processed_at | datetime (nullable) |  |

### 7.2 ReceiptLineItem

| Field | Type | Description |
| --- | --- | --- |
| receipt | FK → Receipt |  |
| raw_description | string |  |
| quantity | float |  |
| unit_price | float |  |
| total_price | float |  |
| matched_product | FK → Product (nullable) |  |
| matching_confidence | float |  |
| matched_pantry_item | FK → PantryItem (nullable) |  |
| matched_grocery_item | FK → GroceryListItem (nullable) |  |

### 7.3 ScanEvent

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| user | FK → User |  |
| location | FK → Location/PantryLocation |  |
| barcode_value | string |  |
| product | FK → Product (nullable) |  |
| scan_type | enum | add_to_list/add_to_pantry/check |
| processed | bool |  |
| processed_at | datetime (nullable) |  |

## 8. App: notifications

### 8.1 PushSubscription

| Field | Type | Description |
| --- | --- | --- |
| user | FK → User |  |
| endpoint | text (unique) |  |
| p256dh | text |  |
| auth | text |  |
| browser | string |  |
| device_label | string |  |
| is_active | bool |  |
| created_at | datetime |  |
| updated_at | datetime |  |

### 8.2 Notification

| Field | Type | Description |
| --- | --- | --- |
| id | UUID |  |
| user | FK → User |  |
| type | enum | task_overdue, bill_due, pantry_expired, etc. |
| title | string |  |
| body | string |  |
| related_task | FK → Task (nullable) |  |
| related_pantry_item | FK → PantryItem (nullable) |  |
| sent_at | datetime |  |
| delivery_status | enum | queued/sent/failed |
| response_payload | JSON |  |

## 9. App: automation

### 9.1 AutomationRule (extends OwnedVisibleModel)

| Field | Type | Description |
| --- | --- | --- |
| household | FK → Household |  |
| name | string |  |
| trigger_type | enum | task_overdue, bill_due_soon, pantry_expiring, elder_task_due, nutrition_alert |
| enabled | bool |  |
| days_before_due | int (nullable) |  |
| target_group | FK → VisibilityGroup (nullable) |  |
| target_user | FK → User (nullable) |  |

## 10. App: pwa

### 10.1 BackgroundSyncJob

| Field | Type | Description |
| --- | --- | --- |
| user | FK → User |  |
| job_type | enum | receipt_upload, barcode_scan |
| payload | JSON |  |
| status | enum | pending/in_progress/completed/failed |
| created_at | datetime |  |
| updated_at | datetime |  |

## 11. App: nutrition

(Could live in accounts or food — your choice.)

### 11.1 UserNutritionProfile

| Field | Type | Description |
| --- | --- | --- |
| user | OneToOne → User or Profile |  |
| diet_type | enum | omnivore, vegetarian, vegan, keto, dash, custom |
| calorie_goal | int |  |
| macro_ratio | JSON | {protein: 0.3, fat: 0.3, carbs: 0.4} |
| allergens | M2M → Ingredient |  |
| excluded_ingredients | M2M → Ingredient |  |
| nutrition_focus_goals | JSON | “low sodium”, “increase fiber” |
| medical_constraints | text | e.g., low-sodium for eldercare |
