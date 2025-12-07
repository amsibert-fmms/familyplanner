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

## Planning Status and Cadence
- **Statuses:** Mark roadmap items as _Planned_, _In Progress_, or _Complete_; use inline dates when relevant (e.g., “Complete — 2024-06-15”).
- **Weekly review:** Reserve 15–20 minutes in the team sync to update roadmap statuses, capture scope changes, and add new risks.
- **Monthly reset:** Confirm the next month’s Now/Next/Later priorities and adjust timelines based on completed work and new dependencies.

## Decision & Risk Notes
- Capture major decisions (e.g., “bill reminders merged into Task model”) directly in the relevant document with a short rationale and date.
- Track risks with owners and mitigation steps; link to issues or tickets when a mitigation is filed.
- Prefer concise callouts over long prose so updates stay skimmable during planning meetings.

## Maintenance
- Keep filenames and headings synchronized with the links above.
- Update cross-links when documents move or change names.
- Add changelog notes inside each document when making substantive planning updates.
- Include timestamps on major roadmap or modeling changes so readers can tell what’s fresh vs. stale.
