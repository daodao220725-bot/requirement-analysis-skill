# Domain and database design branch

## Entry conditions

Enter when the user requests database, table, schema, ER, migration, or DDL design, or confirmed requirements materially require persistence. Skip when the feature is stateless or the user excludes data design.

## Inspect before designing

For an existing system, inspect current schemas, migrations, ORM entities, repositories/queries, conventions, and supported database version. Produce an incremental proposal, not a parallel idealized schema.

For a new system, request or infer only as provisional: database engine/version, naming conventions, ID strategy, organization/tenant isolation, expected scale, hot queries, deletion/retention, audit, encryption/masking, migration tool, and compatibility constraints.

## Depth levels

### Conceptual

Produce `ENT` entities, responsibilities, ownership, relationships, lifecycle, source of truth, sensitivity, and retention. Use when technical constraints are missing.

### Logical

Produce candidate `TBL` tables and columns, PK/FK, cardinality, nullability, uniqueness, status model, audit fields, logical deletion, sensitive-field treatment, query patterns, and candidate indexes. Separate business identifiers from surrogate keys.

### Physical

Produce dialect-specific types, constraints, indexes, partitioning when justified, migration order, rollback, backfill, compatibility, and candidate DDL. Generate only with sufficient engine/version and existing-schema context.

## Mandatory checks

- Map each entity/table to confirmed `REQ` evidence.
- Define organization/tenant data isolation.
- Avoid redundant stored derived values unless justified.
- Define time zone, money precision, enum evolution, and unique-key semantics.
- Align indexes to known query and sort patterns; do not add speculative indexes.
- Define optimistic locking or concurrency behavior when updates may conflict.
- Preserve history for logical deletion, relationship changes, and audit needs.
- Separate encryption at rest from field encryption; define key ownership and rotation before implementation.
- Plan import deduplication, migration, rollback, and partial failure.
- Identify PII and limit exposure in logs, exports, and lower environments.

## Outputs

- domain model and ER diagram (Mermaid when useful);
- table/column data dictionary;
- constraints and index rationale;
- migration/backfill/rollback plan;
- candidate DDL only when safe;
- database task breakdown;
- requirement→entity→table/column→task trace;
- Gate B questions and DBA review record.

Never execute DDL or connect to a production database as part of analysis. Require an explicit separate implementation request and authorization.
