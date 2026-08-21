# Acceptance, testing, traceability, and change

## Acceptance and tests

Create `AC` entries with explicit Given/When/Then. Avoid “works normally”, “supports management”, or other non-observable results.

Create `TC` entries linked to `REQ`, `TASK`, and `AC`. Cover normal, null/boundary/invalid, duplicate, authorization, cross-organization, masking, timeout, external failure, retry, idempotency, concurrency, audit/history, multi-client synchronization, migration, and backward compatibility as applicable.

## Trace

Maintain:

```text
source ↔ requirement ↔ entity/table/column ↔ task ↔ acceptance ↔ test
```

Check missing tasks, acceptance, tests, data mappings, orphan tasks/tests, and retired requirements whose downstream objects remain active.

Trace coverage is the percentage of confirmed current requirements with task, acceptance, and test coverage. Report orphan counts separately; never delete uncovered rows to improve the metric.

## Change impact

1. Diff semantics: add, modify, retire, wording-only.
2. Map each change to evidence and `REQ`.
3. Traverse direct task/data/AC/TC links.
4. Infer indirect module, interface, permission, migration, reporting, and regression effects.
5. Record the impact path and label it evidence-based or dependency inference.
6. Recommend add, modify, retire, migrate, regress, or review.
7. Require human confirmation and record false positives and missed impacts.
8. Update all artifacts under a new version; retain the old version.

Do not report impact accuracy without independent review. Report missed-impact count alongside accuracy.
