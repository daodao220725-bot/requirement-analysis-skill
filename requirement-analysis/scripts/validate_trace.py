#!/usr/bin/env python3
"""Validate requirement-analysis IDs and trace links across case artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PREFIXES = ("REQ", "ENT", "TBL", "TASK", "AC", "TC")


def ids(text: str, prefix: str) -> set[str]:
    return set(re.findall(rf"\b{prefix}-\d{{3,}}\b", text))


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--baseline", type=Path, help="Override the requirement baseline file")
    parser.add_argument("--data", type=Path, help="Override the optional data-design file")
    parser.add_argument("--tasks", type=Path, help="Override the task file")
    parser.add_argument("--acceptance", type=Path, help="Override the acceptance/test file")
    parser.add_argument("--trace", type=Path, help="Override the traceability file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    case_dir = args.case_dir.resolve()
    paths = {
        "baseline": args.baseline.resolve() if args.baseline else case_dir / "05_requirement-baseline.md",
        "data": args.data.resolve() if args.data else case_dir / "06_data-design.md",
        "tasks": args.tasks.resolve() if args.tasks else case_dir / "07_tasks.md",
        "acceptance": args.acceptance.resolve() if args.acceptance else case_dir / "08_acceptance-tests.md",
        "trace": args.trace.resolve() if args.trace else case_dir / "09_traceability.md",
    }
    missing_required = [str(paths[name]) for name in ("baseline", "tasks", "acceptance", "trace") if not paths[name].is_file()]
    if missing_required:
        result = {"ok": False, "errors": [{"type": "missing_file", "path": path} for path in missing_required]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else "\n".join(f"ERROR missing {p}" for p in missing_required))
        return 1

    text = {name: read_optional(path) for name, path in paths.items()}
    defined = {
        "REQ": ids(text["baseline"], "REQ"),
        "ENT": ids(text["data"], "ENT"),
        "TBL": ids(text["data"], "TBL"),
        "TASK": ids(text["tasks"], "TASK"),
        "AC": ids(text["acceptance"], "AC"),
        "TC": ids(text["acceptance"], "TC"),
    }

    errors: list[dict] = []
    checks = {
        "data": ("REQ",),
        "tasks": ("REQ", "ENT", "TBL"),
        "acceptance": ("REQ", "TASK", "AC", "TC"),
        "trace": PREFIXES,
    }
    for artifact, prefixes in checks.items():
        for prefix in prefixes:
            for ref in sorted(ids(text[artifact], prefix) - defined[prefix]):
                errors.append({"type": "unknown_reference", "artifact": artifact, "id": ref})

    trace_ids = {prefix: ids(text["trace"], prefix) for prefix in PREFIXES}
    missing_trace = {
        prefix: sorted(defined[prefix] - trace_ids[prefix])
        for prefix in PREFIXES
        if defined[prefix] - trace_ids[prefix]
    }

    result = {
        "ok": not errors and not missing_trace,
        "case_dir": str(case_dir),
        "defined_counts": {prefix: len(values) for prefix, values in defined.items()},
        "errors": errors,
        "missing_from_trace": missing_trace,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Trace validation: {'PASS' if result['ok'] else 'FAIL'}")
        for prefix, count in result["defined_counts"].items():
            print(f"  {prefix}: {count}")
        for error in errors:
            print(f"ERROR {error['artifact']} references undefined {error['id']}")
        for prefix, values in missing_trace.items():
            print(f"ERROR {prefix} missing from trace: {', '.join(values)}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
