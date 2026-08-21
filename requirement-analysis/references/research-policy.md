# External research policy

## Default

Keep research `off`. Analyze internal materials first. Skill invocation never implies permission to browse or disclose requirement details.

## Authorized research

- `standards`: use official laws, standards, regulatory sources, and primary technical documentation.
- `market`: use public official product documentation and credible primary material to compare mature capabilities.
- `sanitized`: abstract confidential context into generic keywords before searching.

Do not place company names, customer names, internal URLs, interface names, data samples, secrets, or unreleased plans into search queries.

## Evidence separation

Store external findings as `EXT` with URL, title, publisher, access date, product/standard version when available, observed practice, applicability, and uncertainty.

Convert an external finding into a candidate question, not an internal requirement. Only a human-confirmed answer becomes `CLR` and may enter the baseline.

## Recommended order

```text
internal scan → optional external benchmark → candidate questions → Gate A → baseline
```

If research is not available, continue internal analysis and state that no current external benchmark was performed.
