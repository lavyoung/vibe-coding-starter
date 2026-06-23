#!/usr/bin/env python3
"""Run a unified local verification pass for the starter template."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".idea", ".vscode", "node_modules", "__pycache__", "target"}
REQUIRED_STARTER_FILES = {
    "prompts/task-entry.txt": "统一任务入口 prompt",
    "tools/skills/task-router/SKILL.md": "任务路由 skill",
    "tools/skills/task-router/agents/openai.yaml": "任务路由 skill UI 元数据",
    "docs/evolution/current-snapshot.md": "单点快照模板",
    "docs/governance/project-handoff-checklist.md": "交接清单模板",
    "docs/governance/agent-collaboration-protocol.md": "多 agent 协作协议",
    "scripts/init_starter.ps1": "初始化脚本 PowerShell 入口",
    "scripts/init_starter.sh": "初始化脚本 shell 入口",
}
PUBLIC_SCRIPT_ENTRYPOINTS = {
    "scripts/check_all.py": (
        "scripts/check_all.ps1",
        "scripts/check_all.sh",
    ),
    "scripts/doc_sync_check.py": (
        "scripts/doc_sync_check.ps1",
        "scripts/doc_sync_check.sh",
    ),
    "scripts/init_starter.py": (
        "scripts/init_starter.ps1",
        "scripts/init_starter.sh",
    ),
}
SCHEMA_TOP_LEVEL_KEYS = ("$schema", "title", "type", "properties")
SCHEMA_EXAMPLE_MAP = {
    "contracts/task-entry.schema.json": "contracts/examples/task-entry.example.json",
    "contracts/handoff-summary.schema.json": "contracts/examples/handoff-summary.example.json",
}
EXAMPLE_TASK_ENTRY_SUFFIX = "-task-entry.json"
EXAMPLE_HANDOFF_SUFFIX = "-handoff.md"
SYNC_REVIEW_TRIGGER_PREFIXES = (
    "prompts/",
    "tools/skills/",
    "docs/governance/",
)
SYNC_REVIEW_COMPANION_FILES = {
    "docs/evolution/current-snapshot.md",
    "docs/governance/project-handoff-checklist.md",
    "docs/governance/agent-collaboration-protocol.md",
    "contracts/README.md",
    "contracts/task-entry.schema.json",
    "contracts/handoff-summary.schema.json",
    "contracts/examples/task-entry.example.json",
    "contracts/examples/handoff-summary.example.json",
    "tools/skills/task-router/SKILL.md",
    "tools/skills/task-router/agents/openai.yaml",
}


@dataclass(frozen=True)
class CheckResult:
    group: str
    title: str
    status: str
    detail: str | None = None

    def render(self) -> str:
        prefix = {
            "passed": "[PASSED]",
            "failed": "[FAILED]",
            "skipped": "[SKIPPED]",
        }[self.status]
        if self.detail:
            return f"{prefix} {self.title}\n{self.detail}".rstrip()
        return f"{prefix} {self.title}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="运行本地统一检查：doc-sync、Markdown 链接和示例自检。"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="仓库根目录，默认取脚本所在仓库根目录。",
    )
    parser.add_argument(
        "--skip-doc-sync",
        action="store_true",
        help="跳过 doc-sync 检查。",
    )
    parser.add_argument(
        "--skip-links",
        action="store_true",
        help="跳过 Markdown 相对链接检查。",
    )
    parser.add_argument(
        "--skip-examples",
        action="store_true",
        help="跳过示例项目自检。",
    )
    parser.add_argument(
        "--base",
        help="用于 git diff 的 base revision，常用于 CI。",
    )
    parser.add_argument(
        "--head",
        help="用于 git diff 的 head revision，常用于 CI。",
    )
    return parser.parse_args()


def run_command(command: list[str], cwd: Path, group: str, title: str) -> CheckResult:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        return CheckResult(group=group, title=title, status="failed", detail=output)
    return CheckResult(group=group, title=title, status="passed")


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def load_json_file(path: Path) -> tuple[dict[str, object] | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON ({exc.msg})"

    if not isinstance(payload, dict):
        return None, "top-level payload should be an object"
    return payload, None


def validate_payload_against_schema(
    schema_payload: dict[str, object],
    candidate_payload: dict[str, object],
    candidate_path: str,
) -> list[str]:
    issues: list[str] = []
    schema_properties = schema_payload.get("properties", {})
    if not isinstance(schema_properties, dict):
        return [f"- {candidate_path}: schema properties should be an object"]

    required_keys = set(schema_payload.get("required", []))
    candidate_keys = set(candidate_payload.keys())

    missing_keys = sorted(required_keys - candidate_keys)
    extra_keys = sorted(candidate_keys - set(schema_properties.keys()))
    if missing_keys:
        issues.append(
            f"- {candidate_path}: missing required keys {', '.join(missing_keys)}"
        )
    if extra_keys:
        issues.append(
            f"- {candidate_path}: unknown keys {', '.join(extra_keys)}"
        )

    for key in sorted(required_keys & candidate_keys):
        property_schema = schema_properties.get(key, {})
        if not isinstance(property_schema, dict):
            continue

        expected_type = property_schema.get("type")
        value = candidate_payload[key]

        if expected_type == "array" and not isinstance(value, list):
            issues.append(f"- {candidate_path}: key {key} should be an array")
        elif expected_type == "string" and not isinstance(value, str):
            issues.append(f"- {candidate_path}: key {key} should be a string")

        allowed_values = property_schema.get("enum")
        if isinstance(allowed_values, list) and value not in allowed_values:
            issues.append(
                f"- {candidate_path}: key {key} should be one of {', '.join(allowed_values)}"
            )

    return issues


def format_detail_with_hints(
    hint_lines: Sequence[str],
    issue_lines: Sequence[str],
) -> str:
    lines = [*hint_lines]
    if hint_lines and issue_lines:
        lines.append("")
    lines.extend(issue_lines)
    return "\n".join(lines)


def run_git_status(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "."],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git status failed")

    changed_files: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        path = line[3:]
        if "->" in path:
            path = path.split("->", 1)[1].strip()
        normalized = normalize_path(path)
        if normalized:
            changed_files.append(normalized)
    return changed_files


def run_git_diff(repo_root: Path, base: str | None, head: str | None) -> list[str]:
    if base and head:
        revision_range = f"{base}...{head}"
    elif not base and head:
        revision_range = f"HEAD~1...{head}"
    elif not base and not head:
        raise ValueError("run_git_diff requires at least --head or both --base/--head.")
    else:
        raise ValueError("--base and --head must be provided together.")

    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            revision_range,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")

    return [
        normalize_path(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def list_changed_files(
    repo_root: Path,
    base: str | None,
    head: str | None,
) -> tuple[list[str], str]:
    if base or head:
        changed_files = run_git_diff(repo_root, base, head)
        if base and head:
            return changed_files, f"git diff {base}...{head}"
        return changed_files, f"git diff HEAD~1...{head}"
    return run_git_status(repo_root), "git status --porcelain"


def run_doc_sync(
    repo_root: Path,
    changed_files: Sequence[str],
    base: str | None,
    head: str | None,
) -> CheckResult:
    if not changed_files:
        return CheckResult(
            group="doc-sync",
            title="doc-sync",
            status="skipped",
            detail="no changed files detected",
        )

    command = [
        sys.executable,
        "scripts/doc_sync_check.py",
        "--repo-root",
        ".",
        "--config",
        ".doc-sync.json",
    ]
    if base or head:
        if base:
            command.extend(["--base", base])
        if head:
            command.extend(["--head", head])
    else:
        for path in changed_files:
            command.extend(["--changed-file", path])
    return run_command(command, repo_root, "doc-sync", "doc-sync")


def iter_markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(repo_root).parts):
            continue
        files.append(path)
    return files


def should_skip_link(target: str) -> bool:
    return (
        not target
        or target.startswith("#")
        or "://" in target
        or target.startswith("mailto:")
    )


def validate_links(repo_root: Path) -> CheckResult:
    issues: list[str] = []
    for markdown_file in iter_markdown_files(repo_root):
        content = markdown_file.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(content):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if should_skip_link(target):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            candidate = (markdown_file.parent / clean_target).resolve()
            if not candidate.exists():
                issues.append(
                    f"{markdown_file.relative_to(repo_root)} -> {target}"
                )

    if issues:
        detail = "\n".join(f"- {issue}" for issue in issues)
        return CheckResult(
            group="markdown-links",
            title="markdown-links",
            status="failed",
            detail=detail,
        )
    return CheckResult(group="markdown-links", title="markdown-links", status="passed")


def validate_starter_assets(
    repo_root: Path,
    changed_files: Sequence[str],
) -> list[CheckResult]:
    results: list[CheckResult] = []
    missing_assets: list[str] = []

    for relative_path, label in REQUIRED_STARTER_FILES.items():
        if not (repo_root / relative_path).exists():
            missing_assets.append(f"- {relative_path} ({label})")

    if missing_assets:
        results.append(
            CheckResult(
                group="starter-assets",
                title="required starter assets",
                status="failed",
                detail="\n".join(missing_assets),
            )
        )
    else:
        results.append(
            CheckResult(
                group="starter-assets",
                title="required starter assets",
                status="passed",
            )
        )

    contract_schema_files = (
        "contracts/task-entry.schema.json",
        "contracts/handoff-summary.schema.json",
    )
    contracts_enabled = any((repo_root / path).exists() for path in contract_schema_files)

    if not contracts_enabled:
        results.append(
            CheckResult(
                group="starter-assets",
                title="starter schema shape",
                status="skipped",
                detail="contracts/ not enabled",
            )
        )
        results.append(
            CheckResult(
                group="starter-assets",
                title="contract examples",
                status="skipped",
                detail="contracts/ not enabled",
            )
        )
    else:
        schema_issues: list[str] = []
        for schema_path in contract_schema_files:
            absolute_path = repo_root / schema_path
            if not absolute_path.exists():
                continue
            try:
                payload = json.loads(absolute_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                schema_issues.append(f"- {schema_path}: invalid JSON ({exc.msg})")
                continue

            missing_keys = [key for key in SCHEMA_TOP_LEVEL_KEYS if key not in payload]
            if missing_keys:
                schema_issues.append(
                    f"- {schema_path}: missing top-level keys {', '.join(missing_keys)}"
                )

        if schema_issues:
            results.append(
                CheckResult(
                    group="starter-assets",
                    title="starter schema shape",
                    status="failed",
                    detail="\n".join(schema_issues),
                )
            )
        else:
            results.append(
                CheckResult(
                    group="starter-assets",
                    title="starter schema shape",
                    status="passed",
                )
            )

        example_issues: list[str] = []
        for schema_path, example_path in SCHEMA_EXAMPLE_MAP.items():
            schema_file = repo_root / schema_path
            example_file = repo_root / example_path
            if not schema_file.exists() or not example_file.exists():
                continue

            schema_payload, schema_error = load_json_file(schema_file)
            if schema_error:
                example_issues.append(f"- {schema_path}: {schema_error}")
                continue
            if schema_payload is None:
                continue

            example_payload, example_error = load_json_file(example_file)
            if example_error:
                example_issues.append(f"- {example_path}: {example_error}")
                continue
            if example_payload is None:
                continue

            example_issues.extend(
                validate_payload_against_schema(
                    schema_payload,
                    example_payload,
                    example_path,
                )
            )

        if example_issues:
            results.append(
                CheckResult(
                    group="starter-assets",
                    title="contract examples",
                    status="failed",
                    detail="\n".join(example_issues),
                )
            )
        else:
            results.append(
                CheckResult(
                    group="starter-assets",
                    title="contract examples",
                    status="passed",
                )
            )

    script_entrypoint_issues: list[str] = []
    for python_path, wrapper_paths in PUBLIC_SCRIPT_ENTRYPOINTS.items():
        python_file = repo_root / python_path
        if not python_file.exists():
            continue
        for wrapper_path in wrapper_paths:
            if not (repo_root / wrapper_path).exists():
                script_entrypoint_issues.append(
                    f"- {python_path}: missing {wrapper_path}"
                )

    if script_entrypoint_issues:
        results.append(
            CheckResult(
                group="starter-assets",
                title="cross-platform script entrypoints",
                status="failed",
                detail="\n".join(script_entrypoint_issues),
            )
        )
    else:
        results.append(
            CheckResult(
                group="starter-assets",
                title="cross-platform script entrypoints",
                status="passed",
            )
        )

    trigger_hit = any(
        path in {"AGENTS.md", "CLAUDE.md"}
        or any(path.startswith(prefix) for prefix in SYNC_REVIEW_TRIGGER_PREFIXES)
        for path in changed_files
    )
    companion_changed = any(
        path in SYNC_REVIEW_COMPANION_FILES for path in changed_files
    )

    if trigger_hit and not companion_changed:
        results.append(
            CheckResult(
                group="starter-assets",
                title="snapshot / handoff / contracts review",
                status="skipped",
                detail=(
                    "changed prompts / governance / skills / AGENTS / CLAUDE without touching "
                    "current-snapshot, project-handoff-checklist, agent-collaboration-protocol, or contracts; "
                    "manually confirm these assets still match the new rules"
                ),
            )
        )

    return results


def collect_example_workflow_assets(repo_root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    examples_root = repo_root / "examples"
    workflow_issues: list[str] = []
    task_entry_shape_issues: list[str] = []

    task_entry_schema_file = repo_root / "contracts/task-entry.schema.json"
    task_entry_schema: dict[str, object] | None = None
    if task_entry_schema_file.exists():
        task_entry_schema, schema_error = load_json_file(task_entry_schema_file)
        if schema_error:
            task_entry_shape_issues.append(
                f"- contracts/task-entry.schema.json: {schema_error}"
            )
            task_entry_schema = None

    for example_dir in sorted(examples_root.iterdir()):
        if not example_dir.is_dir():
            continue
        if not (example_dir / "README.md").exists():
            continue

        tasks_dir = example_dir / "docs" / "tasks"
        example_label = normalize_path(str(example_dir.relative_to(repo_root)))

        if not tasks_dir.exists():
            workflow_issues.append(f"- {example_label}: missing docs/tasks/")
            continue

        task_entry_files = sorted(tasks_dir.glob(f"*{EXAMPLE_TASK_ENTRY_SUFFIX}"))
        handoff_files = sorted(tasks_dir.glob(f"*{EXAMPLE_HANDOFF_SUFFIX}"))

        if not task_entry_files:
            workflow_issues.append(
                f"- {example_label}: missing docs/tasks/*{EXAMPLE_TASK_ENTRY_SUFFIX}"
            )
        if not handoff_files:
            workflow_issues.append(
                f"- {example_label}: missing docs/tasks/*{EXAMPLE_HANDOFF_SUFFIX}"
            )

        task_entry_bases = {
            path.name[: -len(EXAMPLE_TASK_ENTRY_SUFFIX)] for path in task_entry_files
        }
        handoff_bases = {
            path.name[: -len(EXAMPLE_HANDOFF_SUFFIX)] for path in handoff_files
        }

        for base_name in sorted(task_entry_bases - handoff_bases):
            workflow_issues.append(
                f"- {example_label}: missing matching handoff for {base_name}{EXAMPLE_TASK_ENTRY_SUFFIX}"
            )
        for base_name in sorted(handoff_bases - task_entry_bases):
            workflow_issues.append(
                f"- {example_label}: missing matching task-entry for {base_name}{EXAMPLE_HANDOFF_SUFFIX}"
            )

        if task_entry_schema is None:
            continue

        for task_entry_file in task_entry_files:
            relative_path = normalize_path(str(task_entry_file.relative_to(repo_root)))
            payload, payload_error = load_json_file(task_entry_file)
            if payload_error:
                task_entry_shape_issues.append(f"- {relative_path}: {payload_error}")
                continue
            if payload is None:
                continue

            task_entry_shape_issues.extend(
                validate_payload_against_schema(
                    task_entry_schema,
                    payload,
                    relative_path,
                )
            )

    if workflow_issues:
        results.append(
            CheckResult(
                group="examples",
                title="example workflow assets",
                status="failed",
                detail=format_detail_with_hints(
                    (
                        "each example should keep at least one complete workflow pair:",
                        f"- docs/tasks/<task-name>{EXAMPLE_TASK_ENTRY_SUFFIX}",
                        f"- docs/tasks/<task-name>{EXAMPLE_HANDOFF_SUFFIX}",
                        "- keep the <task-name> base consistent so the pair is easy to trace",
                    ),
                    workflow_issues,
                ),
            )
        )
    else:
        results.append(
            CheckResult(
                group="examples",
                title="example workflow assets",
                status="passed",
            )
        )

    if not task_entry_schema_file.exists():
        results.append(
            CheckResult(
                group="examples",
                title="example task-entry shape",
                status="skipped",
                detail="contracts/ not enabled",
            )
        )
    elif task_entry_shape_issues:
        results.append(
            CheckResult(
                group="examples",
                title="example task-entry shape",
                status="failed",
                detail=format_detail_with_hints(
                    (
                        "align example task-entry files with:",
                        "- contracts/task-entry.schema.json",
                        "- contracts/examples/task-entry.example.json",
                    ),
                    task_entry_shape_issues,
                ),
            )
        )
    else:
        results.append(
            CheckResult(
                group="examples",
                title="example task-entry shape",
                status="passed",
            )
        )

    return results


def run_example_checks(repo_root: Path) -> list[CheckResult]:
    checks = collect_example_workflow_assets(repo_root)

    node = shutil.which("node")
    if node:
        checks.append(
            run_command(
                [node, "--check", "examples/minimal-task-board/src/server.js"],
                repo_root,
                "examples",
                "minimal-task-board server.js syntax",
            )
        )
        checks.append(
            run_command(
                [node, "--check", "examples/minimal-task-board/src/task-store.js"],
                repo_root,
                "examples",
                "minimal-task-board task-store.js syntax",
            )
        )
    else:
        checks.append(
            CheckResult(
                group="examples",
                title="minimal-task-board syntax checks",
                status="skipped",
                detail="node not found",
            )
        )

    mvn = shutil.which("mvn")
    if mvn:
        checks.append(
            run_command(
                [
                    mvn,
                    "-q",
                    "-f",
                    "examples/spring-boot-device-center/pom.xml",
                    "test",
                ],
                repo_root,
                "examples",
                "spring-boot-device-center mvn test",
            )
        )
    else:
        checks.append(
            CheckResult(
                group="examples",
                title="spring-boot-device-center mvn test",
                status="skipped",
                detail="maven not found",
            )
        )

    return checks


def render_group(name: str, results: list[CheckResult]) -> list[str]:
    lines = [f"\n[{name}]"]
    for result in results:
        lines.append(result.render())
    return lines


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    results: list[CheckResult] = []
    requested_skips: list[str] = []

    changed_files, changed_source = list_changed_files(repo_root, args.base, args.head)

    if args.skip_doc_sync:
        requested_skips.append("doc-sync")
        results.append(
            CheckResult(
                group="doc-sync",
                title="doc-sync",
                status="skipped",
                detail="disabled by --skip-doc-sync",
            )
        )
    else:
        results.append(run_doc_sync(repo_root, changed_files, args.base, args.head))

    if args.skip_links:
        requested_skips.append("markdown-links")
        results.append(
            CheckResult(
                group="markdown-links",
                title="markdown-links",
                status="skipped",
                detail="disabled by --skip-links",
            )
        )
    else:
        results.append(validate_links(repo_root))

    results.extend(validate_starter_assets(repo_root, changed_files))

    if args.skip_examples:
        requested_skips.append("examples")
        results.append(
            CheckResult(
                group="examples",
                title="example checks",
                status="skipped",
                detail="disabled by --skip-examples",
            )
        )
    else:
        results.extend(run_example_checks(repo_root))

    print("starter local checks")
    print(f"- repo: {repo_root}")
    print(f"- changed source: {changed_source}")
    print(f"- changed files: {len(changed_files)}")
    if requested_skips:
        print(f"- requested skips: {', '.join(requested_skips)}")

    failed = False
    grouped_names = ["doc-sync", "markdown-links", "starter-assets", "examples"]
    for group_name in grouped_names:
        group_results = [result for result in results if result.group == group_name]
        if not group_results:
            continue
        for line in render_group(group_name, group_results):
            print(line)
        if any(result.status == "failed" for result in group_results):
            failed = True

    passed_count = sum(1 for result in results if result.status == "passed")
    failed_count = sum(1 for result in results if result.status == "failed")
    skipped_count = sum(1 for result in results if result.status == "skipped")

    print("\nsummary")
    print(f"- passed: {passed_count}")
    print(f"- failed: {failed_count}")
    print(f"- skipped: {skipped_count}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
