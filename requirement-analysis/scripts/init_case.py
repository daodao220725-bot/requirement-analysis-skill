#!/usr/bin/env python3
"""Initialize a portable requirement-analysis case from bundled templates."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


COMMON = [
    "01_evidence-index.md",
    "02_requirement-summary.md",
    "03_risks.md",
    "04_clarifications.md",
]
FULL = [
    "05_requirement-baseline.md",
    "07_tasks.md",
    "08_acceptance-tests.md",
    "09_traceability.md",
    "10_change-impact.md",
    "12_effectiveness.md",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def input_manifest(inputs: list[Path]) -> list[dict]:
    result = []
    for item in inputs:
        resolved = item.resolve()
        if not resolved.is_file():
            raise ValueError(f"Input is not a file: {item}")
        stat = resolved.stat()
        result.append({
            "path": str(resolved),
            "name": resolved.name,
            "size_bytes": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "sha256": digest(resolved),
        })
    return result


def write_once(source: Path, target: Path) -> bool:
    if target.exists():
        return False
    shutil.copy2(source, target)
    return True


def customize_state(
    path: Path,
    case_id: str,
    case_name: str,
    mode: str,
    research_policy: str,
    manifest: list[dict],
) -> None:
    text = path.read_text(encoding="utf-8")
    fingerprints = ", ".join(f"{item['name']}:{item['sha256'][:12]}" for item in manifest) or "none"
    replacements = {
        "| 案例编号 |  |": f"| 案例编号 | {case_id} |",
        "| 案例名称 |  |": f"| 案例名称 | {case_name} |",
        "| 执行模式 | scan/full/change/resume |": f"| 执行模式 | {mode} |",
        "| 外部研究策略 | off/standards/market/sanitized |": f"| 外部研究策略 | {research_policy} |",
        "| 当前状态 | 未开始/进行中/已完成/阻塞 |": "| 当前状态 | 进行中 |",
        "| 输入材料及指纹 |  |": f"| 输入材料及指纹 | {fingerprints} |",
        "| 最后更新时间 |  |": f"| 最后更新时间 | {datetime.now().astimezone().isoformat(timespec='seconds')} |",
    }
    for old, new in replacements.items():
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", required=True, type=Path)
    parser.add_argument("--case-name", required=True)
    parser.add_argument("--case-id")
    parser.add_argument("--mode", choices=("scan", "full", "change", "resume"), default="scan")
    parser.add_argument(
        "--research-policy",
        choices=("off", "standards", "market", "sanitized"),
        default="off",
    )
    parser.add_argument("--input", action="append", type=Path, default=[])
    parser.add_argument("--with-data-design", action="store_true")
    parser.add_argument("--with-external-benchmark", action="store_true")
    parser.add_argument("--copy-inputs", action="store_true")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    templates = skill_root / "assets" / "templates"
    case_dir = args.case_dir.resolve()

    if args.mode == "resume":
        state = case_dir / "workflow-state.md"
        if not state.is_file():
            raise SystemExit("resume requires an existing workflow-state.md")
        print(json.dumps({"case_dir": str(case_dir), "mode": "resume", "created": [], "skipped": [str(state)]}, ensure_ascii=False, indent=2))
        return 0

    case_dir.mkdir(parents=True, exist_ok=True)
    input_dir = case_dir / "00_inputs"
    logs_dir = case_dir / "run-logs"
    input_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    manifest = input_manifest(args.input)
    manifest_path = case_dir / "input-manifest.json"
    manifest_document = {"files": manifest}
    if manifest_path.exists():
        existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing_manifest != manifest_document:
            raise SystemExit(
                "Existing input-manifest.json differs from current inputs; "
                "start a new case version or run change analysis."
            )
    else:
        manifest_path.write_text(
            json.dumps(manifest_document, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.copy_inputs:
        for source in args.input:
            target = input_dir / source.name
            if target.exists():
                if digest(target) == digest(source):
                    continue
                raise SystemExit(f"Refusing to overwrite copied input with different content: {target}")
            shutil.copy2(source, target)

    names = list(COMMON)
    if args.mode == "full":
        names.extend(FULL)
    if args.mode == "change":
        names = ["10_change-impact.md"]
    if args.with_data_design:
        names.append("06_data-design.md")
    if args.with_external_benchmark:
        names.append("11_external-benchmark.md")

    created: list[str] = []
    skipped: list[str] = []
    for name in dict.fromkeys(names):
        target = case_dir / name
        (created if write_once(templates / name, target) else skipped).append(str(target))

    state_target = case_dir / "workflow-state.md"
    if write_once(templates / "workflow-state.md", state_target):
        case_id = args.case_id or datetime.now().astimezone().strftime("CASE-%Y%m%d-%H%M%S")
        customize_state(
            state_target,
            case_id,
            args.case_name,
            args.mode,
            args.research_policy,
            manifest,
        )
        created.append(str(state_target))
    else:
        skipped.append(str(state_target))

    gate_target = case_dir / "gate-check.md"
    (created if write_once(templates / "gate-check.md", gate_target) else skipped).append(str(gate_target))

    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    log_target = logs_dir / f"RUN-{stamp}.md"
    if write_once(templates / "run-log.md", log_target):
        created.append(str(log_target))

    print(json.dumps({
        "case_dir": str(case_dir),
        "case_name": args.case_name,
        "mode": args.mode,
        "manifest": str(manifest_path),
        "created": created,
        "skipped_existing": skipped,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
