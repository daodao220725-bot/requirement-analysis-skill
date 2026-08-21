---
name: requirement-analysis
description: Analyze product and software requirements from PRDs, spreadsheets, Word/PDF documents, prototypes, meeting notes, rules, schemas, or codebase context; identify ambiguity, missing rules, conflicts, permission and data risks; create evidence-linked requirement baselines, development task breakdowns, optional domain/database designs and candidate DDL, acceptance criteria, test points, traceability matrices, and change-impact reports. Use for requirement review, PRD health checks, R&D task decomposition, database/table design, ER modeling, requirement changes, impact analysis, or resuming an unfinished requirement workflow.
---

# Requirement Analysis

Turn source material into evidence-linked, human-confirmed R&D inputs. Keep business facts, external references, AI inferences, and human decisions separate.

## Start every run

1. Identify the input materials, desired outcome, existing case directory, and explicit user constraints.
2. Select a workflow mode with the routing table below. Honor an explicit mode.
3. Select a research policy. Default to `off`; never browse merely because internet access exists.
4. Create or read `workflow-state.md`. For a new case, run `scripts/init_case.py` and `scripts/inspect_inputs.py` when shell and Python are available.
5. Read only the references needed for the selected mode and branch.
6. Preserve original inputs. Create versioned outputs; never overwrite a human-confirmed baseline.

## Route the mode

| Condition | Mode |
|---|---|
| User explicitly names `scan`, `full`, `change`, or `resume` | Use it |
| A state file exists with unfinished or blocked work | `resume` |
| Before/after requirement versions are provided | `change` |
| User requests tasks, acceptance, traceability, database design, or complete delivery inputs | `full` |
| User asks to review, inspect, find omissions, or analyze a requirement | `scan` |
| Intent remains ambiguous | Default to `scan` |

Use [workflow.md](references/workflow.md) for stage gates and resume behavior.

## Select the research policy

| Policy | Behavior |
|---|---|
| `off` | Use only user-provided materials, local project context, bundled rules, and reasoning. Default. |
| `standards` | Search official laws, standards, or primary technical documentation only after explicit authorization. |
| `market` | Research mature public products or industry practices only after explicit authorization. |
| `sanitized` | Search only abstracted, non-sensitive keywords approved or safely derived from the request. |

Read [research-policy.md](references/research-policy.md) before any external research. Never copy external practices into the baseline; convert them into `EXT` evidence and candidate questions for human confirmation.

## Enforce invariants

- Label every key statement as `INTERNAL`, `CLARIFIED`, `EXTERNAL`, or `INFERENCE`.
- Require stable evidence IDs and precise source locations for key conclusions.
- Never turn an inference, common practice, or market feature into a business fact.
- Never decide scope, business rules, architecture, estimates, owners, production schema, or production DDL execution for the user.
- Stop at Gate A for unresolved business facts and at Gate B for unresolved technical/database decisions.
- Treat unanswered P0 issues as blockers for the affected scope.
- Keep raw AI output and human-final output when effectiveness is being measured.
- Do not claim reduced defects or rework unless real delivery evidence exists.

## Execute `scan`

1. Inventory and anchor inputs.
2. Produce a requirement-understanding summary.
3. Scan scope, roles, permissions, data, privacy, workflows, states, interfaces, analytics, nonfunctional requirements, and acceptance gaps.
4. Deduplicate by root cause and prioritize P0/P1/P2.
5. Produce Gate A questions with evidence, impact, minimal decision needed, and suggested confirming role.
6. Stop for human confirmation. Do not create a formal baseline or development plan.

Read [evidence-analysis.md](references/evidence-analysis.md). Use templates `01` through `04` in `assets/templates/`.

## Execute `full`

1. Run `scan` unless equivalent, current, evidence-linked outputs already exist.
2. Apply Gate A. Allow partial work only for unaffected scope when the gate is conditionally passed.
3. Build a structured requirement baseline using only `INTERNAL` and `CLARIFIED` facts.
4. Run the data-design branch when persistence is requested or materially required.
5. Break confirmed in-scope requirements into candidate R&D tasks.
6. Apply Gate B with product, engineering, security/data, and DBA roles as applicable.
7. Create acceptance criteria and test points.
8. Build the bidirectional source→requirement→data→task→acceptance→test trace.
9. Validate IDs and trace links with `scripts/validate_trace.py` when possible.

Read [requirements-tasks.md](references/requirements-tasks.md), [database-design.md](references/database-design.md) when applicable, and [acceptance-change.md](references/acceptance-change.md). Use templates `05` through `10`; include `06_data-design.md` when data design applies.

## Run the data-design branch

Run after the requirement baseline and before final task decomposition when the user asks for database/table/ER/DDL design or confirmed requirements require persistent data.

Choose the deepest safe level:

1. **Conceptual**: entities, ownership, relationships, lifecycle, sensitivity.
2. **Logical**: candidate tables, columns, keys, constraints, states, audit fields, query patterns.
3. **Physical**: dialect-specific types, indexes, partitions, migrations, rollback, and candidate DDL.

Generate physical design or DDL only when the database engine/version, existing schema or new-build status, conventions, isolation model, scale/query patterns, deletion/audit policy, and migration constraints are sufficiently known. Otherwise stop at conceptual/logical design and raise Gate B questions. Never execute DDL or modify a database without an explicit separate request and authorization.

## Execute `change`

1. Require before/after inputs, a confirmed baseline, and preferably a trace matrix.
2. Produce semantic additions, modifications, deletions, and wording-only changes.
3. Map changes to evidence and requirement IDs.
4. Trace direct effects, then infer indirect data, permission, interface, module, acceptance, and test effects.
5. Give an evidence path, confidence label, and suggested action for every impact.
6. Stop for human impact review. Record false positives and misses.
7. Update versioned artifacts only after confirmation; keep old versions.

Read [acceptance-change.md](references/acceptance-change.md). Use template `09`.

## Execute `resume`

1. Read the state and latest run log.
2. Recompute or verify input fingerprints.
3. If inputs changed, switch to change detection before reusing old conclusions.
4. Apply newly supplied human answers to clarification or technical review records.
5. Continue from the first incomplete or impacted stage only.
6. Create new run and output versions; update state last.

## Handle large inputs

Use [large-inputs.md](references/large-inputs.md) when there are more than 100 features, multiple systems/domains, unstable single-pass parsing, or repeated numbering/context failures. Perform global pre-scan, domain batches, cross-batch deduplication/conflict checks, and final coverage validation. Never concatenate batch outputs without global reconciliation.

## Use bundled resources

- `scripts/inspect_inputs.py`: produce a deterministic file inventory with sizes, times, hashes, and support hints.
- `scripts/init_case.py`: create a portable case directory from bundled templates without overwriting existing work.
- `scripts/validate_trace.py`: verify defined IDs, invalid references, missing trace coverage, and orphan tasks/tests.
- `assets/templates/`: copy into each case; never edit templates in place.
- [output-contracts.md](references/output-contracts.md): use for IDs, folders, minimum fields, and quality checks.

If a script or parser is unavailable, report the limitation, use the safest available parser, and record the degradation in the run log.

## Finish a run

1. Update `workflow-state.md` with stages, versions, gate result, blockers, and next action.
2. Save a run log containing inputs, prompt/skill version, tools, elapsed time when known, outputs, errors, and human modifications.
3. State what is confirmed, provisional, blocked, externally sourced, and intentionally not done.
4. Provide links to the case outputs.
