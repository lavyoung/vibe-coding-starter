#!/usr/bin/env python3
"""Run a unified local verification pass for the starter template."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".idea", ".vscode", "node_modules", "__pycache__", "target"}


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


def run_command(command: list[str], cwd: Path, title: str) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        return False, f"[FAILED] {title}\n{output}".rstrip()
    return True, f"[PASSED] {title}"


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


def run_doc_sync(repo_root: Path, changed_files: list[str]) -> tuple[bool, str]:
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
    return run_command(command, repo_root, "doc-sync")


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


def validate_links(repo_root: Path) -> tuple[bool, str]:
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
        return False, "[FAILED] markdown-links\n" + "\n".join(f"- {issue}" for issue in issues)
    return True, "[PASSED] markdown-links"


def run_example_checks(repo_root: Path) -> list[tuple[bool, str]]:
    checks: list[tuple[bool, str]] = []

    node = shutil.which("node")
    if node:
        checks.append(
            run_command(
                [node, "--check", "examples/minimal-task-board/src/server.js"],
                repo_root,
                "minimal-task-board server.js syntax",
            )
        )
        checks.append(
            run_command(
                [node, "--check", "examples/minimal-task-board/src/task-store.js"],
                repo_root,
                "minimal-task-board task-store.js syntax",
            )
        )
    else:
        checks.append((True, "[SKIPPED] minimal-task-board syntax checks (node not found)"))

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
                "spring-boot-device-center mvn test",
            )
        )
    else:
        checks.append((True, "[SKIPPED] spring-boot-device-center mvn test (maven not found)"))

    return checks


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    results: list[tuple[bool, str]] = []

    changed_files = list_changed_files(repo_root)

    if not args.skip_doc_sync:
        results.append(run_doc_sync(repo_root, changed_files))
    if not args.skip_links:
        results.append(validate_links(repo_root))
    if not args.skip_examples:
        results.extend(run_example_checks(repo_root))

    failed = False
    print("starter local checks")
    print(f"- repo: {repo_root}")
    print(f"- changed files: {len(changed_files)}")
    for success, message in results:
        print(message)
        if not success:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
