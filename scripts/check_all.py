#!/usr/bin/env python3
"""Run a unified local verification pass for the starter template."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".idea", ".vscode", "node_modules", "__pycache__", "target"}


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


def list_changed_files(repo_root: Path) -> list[str]:
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
        normalized = path.replace("\\", "/")
        if normalized:
            changed_files.append(normalized)
    return changed_files


def run_doc_sync(repo_root: Path, changed_files: list[str]) -> CheckResult:
    command = [
        sys.executable,
        "scripts/doc_sync_check.py",
        "--repo-root",
        ".",
        "--config",
        ".doc-sync.json",
    ]
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


def run_example_checks(repo_root: Path) -> list[CheckResult]:
    checks: list[CheckResult] = []

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

    changed_files = list_changed_files(repo_root)

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
        results.append(run_doc_sync(repo_root, changed_files))

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
    print(f"- changed files: {len(changed_files)}")
    if requested_skips:
        print(f"- requested skips: {', '.join(requested_skips)}")

    failed = False
    grouped_names = ["doc-sync", "markdown-links", "examples"]
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
