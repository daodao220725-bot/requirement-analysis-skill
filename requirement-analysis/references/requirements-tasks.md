# Requirement baseline and R&D task decomposition

## Baseline

Create one `REQ` per independently confirmable capability. Include role, goal, trigger, preconditions, main flow, exceptions/boundaries, business rules, data, permissions, outcome, priority, scope status, evidence, and confirmation status.

Only `INTERNAL` and `CLARIFIED` facts enter the formal text. Put unresolved items in `OPEN`; do not hide them in assumptions.

Use scope states `current`, `later`, `out`, and `pending`. Generate formal tasks only for confirmed `current` requirements.

Merge duplicates and split multi-capability statements while preserving source mapping.

## Tasks

Decompose by independently implementable and verifiable capability, not by copying paragraphs. Check:

- product or interaction clarification;
- frontend/client;
- backend/service and state machine;
- data model, migrations, and initialization;
- internal/external interfaces;
- identity, authorization, masking, encryption, and audit;
- messages, retry, idempotency, and compensation;
- test automation and test data;
- configuration, deployment, monitoring, rollback, and documentation.

Every `TASK` needs linked `REQ`, type, client/module, implementation scope, input/output or data change, dependencies, risks, definition of done, responsible role type, and review status.

Do not estimate effort or select final architecture unless the user explicitly asks and supplies sufficient constraints. Even then, label estimates and architecture as proposals requiring review.

At Gate B, record `accepted`, `adjusted`, or `deleted` and the reason. Use these records to evaluate and improve the skill.
