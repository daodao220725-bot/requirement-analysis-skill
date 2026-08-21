#!/usr/bin/env python3
"""Create a deterministic, content-safe inventory of requirement input files."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", "__pycache__"}
DIRECT = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".sql", ".xml", ".html"}
PARSER = {".xlsx", ".xls", ".docx", ".doc", ".pdf", ".pptx", ".ppt"}
VISUAL = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def support_hint(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in DIRECT:
        return "direct_text"
    if suffix in PARSER:
        return "needs_document_parser"
    if suffix in VISUAL:
        return "needs_visual_inspection"
    return "unknown_or_binary"


def collect(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    files: list[Path] = []
    errors: list[dict] = []
    for item in paths:
        if not item.exists():
            errors.append({"path": str(item), "error": "not_found"})
            continue
        if item.is_file():
            files.append(item)
            continue
        for child in sorted(item.rglob("*")):
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file():
                files.append(child)

    records: list[dict] = []
    for path in sorted(set(p.resolve() for p in files), key=str):
        try:
            stat = path.stat()
            records.append({
                "path": str(path),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "sha256": sha256(path),
                "support_hint": support_hint(path),
            })
        except OSError as exc:
            errors.append({"path": str(path), "error": str(exc)})
    return records, errors


def to_markdown(records: list[dict], errors: list[dict]) -> str:
    lines = [
        "# Input Inventory",
        "",
        "| File | Extension | Size | Modified UTC | SHA-256 | Handling |",
        "|---|---|---:|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| `{record['path']}` | `{record['extension'] or '-'}` | {record['size_bytes']} | "
            f"{record['modified_utc']} | `{record['sha256']}` | {record['support_hint']} |"
        )
    if errors:
        lines.extend(["", "## Errors", "", "| Path | Error |", "|---|---|"])
        lines.extend(f"| `{item['path']}` | {item['error']} |" for item in errors)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    records, errors = collect(args.paths)
    if args.format == "json":
        output = json.dumps({"files": records, "errors": errors}, ensure_ascii=False, indent=2) + "\n"
    else:
        output = to_markdown(records, errors)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 1 if not records else 0


if __name__ == "__main__":
    raise SystemExit(main())
