# Planning Documentation Index

This folder centralizes the planning references for the Family Planner project so product, engineering, and data contributors can align on scope, sequencing, and modeling decisions.

## Audience and Purpose
- **Product & Delivery:** track roadmap scope, milestones, and dependencies.
- **Engineering:** understand implementation plans and data design before building features.
- **Data & QA:** reference canonical field definitions and enrichment expectations when validating models and integrations.

## Document Map
- **[Roadmap](./roadmap.md):** phased delivery plan with milestones and expected timelines.
- **[Data Model Plan](./data-model-plan.md):** implementation guidance and task stubs for key modeling workstreams.
- **[Enrichment Strategy](./enrichment-strategy.md):** local-first approach for optional external lookups and provenance.
- **[Data Dictionary](./data-dictionary.md):** canonical field definitions across apps to keep naming and usage consistent.

## How to Use These Docs
1. Start with the **Roadmap** to understand sequencing and scope.
2. Consult the **Data Model Plan** to break roadmap items into actionable engineering tasks.
3. Apply the **Enrichment Strategy** wherever external data is involved (ingredients, barcodes, OCR).
4. Validate implementations against the **Data Dictionary** to keep schemas and terminology aligned.

## Maintenance
- Keep filenames and headings synchronized with the links above.
- Update cross-links when documents move or change names.
- Add changelog notes inside each document when making substantive planning updates.
