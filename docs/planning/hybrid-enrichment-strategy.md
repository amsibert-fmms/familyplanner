# Hybrid Local + Optional External Data Fetch Design

This strategy keeps enrichment local-first while allowing optional external lookups for barcodes, products, and nutrition data. It pairs with the roadmap and data model plan to ensure enrichment work is safe, reviewable, and traceable.

## Scope and Principles
- **Local-first**: the data model and user experience never depend on external services.
- **User control**: proposed data is always reviewable and editable before persistence.
- **Offline-friendly**: enrichment can be deferred to background sync when connectivity is available.
- **Traceable**: provenance metadata records source system, URL, and confidence.

## Target Objects
- Ingredients, Products, PantryItems, RecipeIngredients, and any models with nutrition or barcode data.

## External Sources (configurable)
- Open Food Facts
- USDA FoodData Central
- UPCItemDB
- Edamam (paid)
- Retail APIs (e.g., Walmart/Target) as optional harder sources

## Recommended Model Additions
Add provenance fields to models that receive enriched data:
- `source_url` (string)
- `source_system` (choices: Manual, OFF, USDA, etc.)
- `source_confidence` (decimal/float)

## Service Entry Points
Implement configurable pipelines in:
- `ingredient_enrichment_service.py`
- `product_lookup_service.py`
- `nutrition_enrichment_service.py`

Default priority: Local DB → Open Food Facts → USDA → heuristics (name parsing). Each step should be optional, timeout-tolerant, and return a common result structure (proposed name, ingredients, nutrition, serving size, confidence, source).

## User Flows
### New Product Entry or Barcode Scan
1. User scans a barcode or enters a product (creates `ScanEvent` or `Product`).
2. Backend attempts lookup using the priority above.
3. UI shows proposed name, ingredients, nutrition, serving size, and provenance **before saving**.
4. User can edit values, change units, select different matches, or decline external data entirely.
5. Final data is saved locally to Product/Ingredient/PantryItem/RecipeIngredient with optional provenance.

### New Ingredient Entry → Nutrition Fetch
1. User types an ingredient (e.g., “Black beans cooked”).
2. System queries USDA/OFF or configured sources for nutrition and micros.
3. UI displays proposed calories, macros, sodium, fiber, micronutrients with confidence.
4. User edits/accepts; warn if values conflict with user profile (e.g., high sodium).
5. Save locally with provenance.

### Receipt OCR → Line-Item Matching and Enrichment
1. OCR produces line items; parse names and match to existing Products when possible.
2. Unknown items trigger product/nutrition lookups; propose Product + Ingredient + Nutrition records.
3. User can approve/edit per line item or in batch; declining external data is allowed.
4. Persist locally; enqueue background sync jobs when offline.

## Offline and Background Sync
- Allow offline entry; queue enrichment jobs via BackgroundSyncJob.
- When online, run lookups, but never overwrite user edits; present diffs for review.
- Ensure idempotent retries and clear provenance for any externally sourced values.

## Observability and Configuration
- Environment flags enable/disable sources and set timeouts; store API keys securely.
- Collect structured logs/metrics for lookup success, latency, and user acceptance rates.

## Developer Notes
- Keep imports free of try/except wrappers.
- Extend API docs/schemas to mention optional enrichment and provenance fields.
- Add tests for source ordering, fallback behavior, offline-to-online transitions, and user override handling.
