# Large-input batching

Use batching for more than 100 features, multiple systems/domains, unstable parsing, or repeated context/ID failures.

## Sequence

```text
global pre-scan
→ global IDs and terminology
→ domain/client batches
→ per-batch summary and risks
→ cross-batch duplicate/conflict/dependency scan
→ global reconciliation
→ coverage validation
```

Create a global batch for goals, terminology, organization, roles, permissions, shared master data, and nonfunctional requirements. Split business features by stable domain, not arbitrary page count.

Use a single global ID namespace. Record each batch's included and excluded scope. When one requirement appears in multiple batches, designate one canonical record and link the others.

Check cross-batch role meaning, data keys/states/source of truth, duplicate client functions, upstream/downstream flows, deletion and permission propagation, duplicate risks, and globally missing P0 items.

Never form a final baseline by concatenating batch outputs without reconciliation.
