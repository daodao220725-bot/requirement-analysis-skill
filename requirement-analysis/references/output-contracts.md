# Output contracts

## Case layout

```text
case-name/
├── 00_inputs/
├── workflow-state.md
├── 01_evidence-index.md
├── 02_requirement-summary.md
├── 03_risks.md
├── 04_clarifications.md
├── 05_requirement-baseline.md
├── 06_data-design.md
├── 07_tasks.md
├── 08_acceptance-tests.md
├── 09_traceability.md
├── 10_change-impact.md
├── 11_external-benchmark.md
└── run-logs/
```

Create only applicable outputs, but keep numbering stable.

List every ID explicitly in trace tables. Do not use ranges such as `TC-001～TC-005`; deterministic validation must be able to see each referenced object.

## Evidence labels

- `INTERNAL`: user-provided internal evidence.
- `CLARIFIED`: human-confirmed decision.
- `EXTERNAL`: public research; reference only.
- `INFERENCE`: AI hypothesis; confirmation required.

## Minimum fields

- Evidence: ID, source, version, location, summary, sensitivity.
- Risk: ID, priority, type, question, evidence, impact, smallest decision, confirming role, status.
- Requirement: ID, role, trigger, conditions, flow, exceptions, data, permissions, result, scope, evidence, status.
- Data object: `ENT/TBL`, linked `REQ`, ownership, relationships, fields, constraints, lifecycle, sensitivity, query/index rationale.
- Task: ID, linked `REQ/TBL`, type, module, implementation, dependency, risk, done definition, review status.
- Acceptance/test: IDs and links, concrete input/state/action/result.
- Change: ID, before/after, direct/indirect impacts, path, action, confidence, human result, misses.

## Versioning

Use semantic or dated versions consistently. Do not reuse IDs after retirement. Keep approved baselines and schema versions immutable; create a new version for updates.

## Final quality checks

- All current requirements have evidence.
- All confirmed current requirements have tasks, acceptance, and tests.
- Persistent data has requirement-linked entities/tables.
- No task, table, acceptance, or test is orphaned.
- P0 blockers are visible.
- External findings are not internal facts.
- Human and AI versions remain distinguishable.
