#!/usr/bin/env python3
"""Choose requirement-analysis mode from explicit input, state, versions, and request text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FULL_PATTERNS = (
    r"研发任务", r"任务拆", r"验收", r"测试点", r"追踪矩阵",
    r"数据库", r"表结构", r"ER图", r"DDL", r"schema",
    r"完整流程", r"完整分析", r"full",
)
CHANGE_PATTERNS = (r"变更影响", r"影响分析", r"版本对比", r"change")
SCAN_PATTERNS = (r"检查", r"审查", r"评审", r"遗漏", r"风险", r"分析需求", r"scan")


def state_is_resumable(case_dir: Path | None) -> bool:
    if not case_dir:
        return False
    state = case_dir / "workflow-state.md"
    if not state.is_file():
        return False
    text = state.read_text(encoding="utf-8", errors="replace")
    return bool(re.search(r"进行中|阻塞|in_progress|blocked|未开始|not_started", text, re.I))


def matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def route(args: argparse.Namespace) -> tuple[str, str]:
    if args.explicit != "auto":
        return args.explicit, "user explicitly selected the mode"
    if state_is_resumable(args.case_dir):
        return "resume", "an unfinished or blocked workflow-state.md exists"
    if args.before and args.after:
        return "change", "before and after versions were provided"
    if matches(args.request, CHANGE_PATTERNS):
        return "change", "the request asks for change or version impact analysis"
    if matches(args.request, FULL_PATTERNS):
        return "full", "the request asks for downstream delivery or data design outputs"
    if matches(args.request, SCAN_PATTERNS):
        return "scan", "the request asks for requirement review or gap analysis"
    return "scan", "ambiguous requests default to the safest scan mode"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", default="", help="User request text")
    parser.add_argument("--explicit", choices=("auto", "scan", "full", "change", "resume"), default="auto")
    parser.add_argument("--case-dir", type=Path)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--after", type=Path)
    args = parser.parse_args()

    mode, reason = route(args)
    print(json.dumps({"mode": mode, "reason": reason}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
