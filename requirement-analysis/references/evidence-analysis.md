# Evidence anchoring and requirement analysis

## Input handling

Inventory files before analysis. Record successful, failed, and partially parsed files. For each input, capture name, type, size, modified time, hash when possible, version, and sensitivity.

Use precise locations:

- Excel: sheet and cell/range; inspect merged cells, formulas, comments, hidden rows/columns, links, and images.
- PDF: page and section/table position.
- Word/Markdown/text: heading path and paragraph or line.
- Prototype/image: page, component, state, or visible region.
- Code/schema: file and symbol/line.
- Meeting record: date, topic, and confirmed statement.

## IDs

Use stable prefixes: `DOC`, `SRC`, `FUNC`, `PERM`, `PROTO`, `RULE`, `CLR`, `RISK`, `REQ`, `ENT`, `TBL`, `TASK`, `AC`, `TC`, `CHG`, `EXT`, and `OPEN`.

Never reuse an ID. Preserve retired IDs with status and reason.

## Summary dimensions

Extract material type and boundaries, goals, systems/clients, roles, business domains, core data, candidate cross-client flows, current permission expressions, dependencies, constraints, and uncovered areas. Label multi-source synthesis as synthesis, not as a quoted project goal.

## Risk dimensions

Check:

- new build versus modification, in-scope versus later/out;
- organization and terminology;
- identity, role, operation, data, and field permissions;
- sensitive data, encryption, masking, export, retention, and audit;
- entity keys, relationships, source of truth, import, synchronization, and deletion;
- normal states, rejection, cancellation, timeout, close, recovery, and concurrency;
- cross-client producer/processor/consumer completeness;
- interfaces, messages, files, maps, video, and failure compensation;
- metric definitions, history, recalculation, and permissions;
- performance, capacity, availability, compatibility, backup, and observability;
- acceptance measurability;
- duplicates, misplaced features, contradictions, and terminology errors.

Prioritize P0 when a missing answer changes scope, identity/authorization, sensitive data, a core workflow, architecture, or legal validity. Prioritize P1 when it blocks task/schema/acceptance design. Use P2 for consistency and documentation quality.

For every risk include evidence, potential impact, smallest decision needed, confirming role, and human status. Deduplicate by root cause.
