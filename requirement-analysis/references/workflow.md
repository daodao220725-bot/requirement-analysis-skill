# Workflow, modes, gates, and state

## Pipeline

```text
0 scope and measurement design
1 evidence inventory and anchoring
2 requirement-understanding summary
3 ambiguity, gap, conflict, and risk scan
Gate A: business facts and scope
4 structured requirement baseline
5A optional domain/database design
5B R&D task decomposition
Gate B: technical and database review
6 acceptance criteria and test points
7 bidirectional traceability
8 change impact and version update
9 effectiveness and reuse evaluation
```

## Gate results

- **Pass**: all mandatory facts are confirmed.
- **Conditional pass**: nonblocking items have a role and due date; continue only unaffected scope.
- **Blocked**: unresolved facts could change scope, security, core workflow, architecture, or schema; stop affected downstream work.

Gate A requires product/business confirmation. Gate B requires engineering and, when relevant, security/data/DBA confirmation. AI output never counts as approval.

## State values

Use `not_started`, `in_progress`, `complete`, `blocked`, or `skipped`. Record a reason for `skipped`; record linked open items and responsible roles for `blocked`.

Update state at stage start and completion. Update it last after producing outputs. Do not overwrite an approved version.

## Mode boundaries

- `scan`: stop after Gate A questions.
- `full`: run the complete pipeline with both gates.
- `change`: require a baseline and before/after versions; stop for impact review.
- `resume`: verify fingerprints before continuing.

## Minimum measurement

Record one efficiency, one effectiveness, and one quality metric. Prefer analysis time, reviewed suggestion adoption, effective newly found questions, evidence trace rate, trace coverage, change-impact accuracy/misses, and independent completion rate.

Do not count unreviewed suggestions as effective. Freeze the scoring rule for “partially effective” before evaluation.
