# Planning Package

This folder consolidates the Family Planner planning artifacts into a single, easy-to-navigate location.
Use this package to understand what we plan to build, how we intend to build it, and the models that support the work.

## Document Map
- [`roadmap.md`](./roadmap.md): Program-level phases, milestones, and timeline expectations.
- [`data-model-implementation-plan.md`](./data-model-implementation-plan.md): Task stubs and sequencing for delivering the updated data model.
- [`data-dictionary.md`](./data-dictionary.md): Canonical reference for fields across apps.
- [`hybrid-enrichment-strategy.md`](./hybrid-enrichment-strategy.md): Local-first enrichment approach for barcodes, products, and nutrition data.

## How to Use This Package
1. Start with the **roadmap** to understand release sequencing and scope.
2. Review the **data model implementation plan** for actionable task stubs and dependencies.
3. Consult the **data dictionary** when designing schemas, serializers, or API payloads.
4. Follow the **hybrid enrichment strategy** when implementing external lookups or background sync.

## Conventions
- Documents are organized for cross-linking; headings mirror app names and workstreams.
- Task stubs are intentionally specific so they can be scheduled or ticketed directly.
- Keep imports free of `try/except` wrappers when implementing referenced modules.
