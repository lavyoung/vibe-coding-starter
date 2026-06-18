#!/usr/bin/env python3
"""Validate docs-first sync rules for the current change set."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Iterable


DEFAULT_DOC_GLOBS = ("docs/*.md", "docs/**/*.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate doc-sync rules.")
    parser.add_argument(
        "--config",
        default=".doc-sync.json",
        help="Path to the doc-sync JSON config file.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used for git diff and relative path resolution.",
    )
    parser.add_argument("--base", help="Base git revision to compare.")
    parser.add_argument("--head", help="Head git revision to compare.")
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Explicit changed file path. Repeat to bypass git diff and test locally.",
    )
    return parser.parse_args()


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def match_any(path: str, patterns: Iterable[str]) -> bool:
    posix_path = PurePosixPath(path)
    return any(posix_path.match(pattern) for pattern in patterns)


def run_git_diff(repo_root: Path, base: str | None, head: str | None) -> list[str]:
    if base and head:
        revision_range = f"{base}...{head}"
    elif not base and head:
        revision_range = f"HEAD~1...{head}"
    elif not base and not head:
        revision_range = "HEAD~1...HEAD"
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


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data.get("rules", []), list):
        raise ValueError("config.rules must be a list")
    return data


def classify_docs(changed_files: list[str], config: dict) -> list[str]:
    doc_globs = config.get("docGlobs") or list(DEFAULT_DOC_GLOBS)
    return [path for path in changed_files if match_any(path, doc_globs)]


def validate_doc_file(repo_root: Path, doc_path: str) -> list[str]:
    content = (repo_root / doc_path).read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    issues: list[str] = []

    if not lines or not lines[0].startswith("# "):
        issues.append(f"{doc_path}: 第一行必须是一级标题。")
    if "## 文档元数据" not in content:
        issues.append(f"{doc_path}: 缺少“## 文档元数据”章节。")
    if "- 当前状态：" not in content:
        issues.append(f"{doc_path}: 缺少“当前状态”元数据。")
    if "## 关联代码" not in content:
        issues.append(f"{doc_path}: 缺少“## 关联代码”章节。")

    return issues


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config_path = (repo_root / args.config).resolve()
    config = load_config(config_path)

    if args.changed_file:
        changed_files = [normalize_path(path) for path in args.changed_file]
    else:
        changed_files = run_git_diff(repo_root, args.base, args.head)

    ignore_patterns = config.get("ignore", [])
    changed_files = [
        path for path in changed_files if not match_any(path, ignore_patterns)
    ]

    print("doc-sync check")
    print(f"- repo: {repo_root}")
    print(f"- config: {config_path}")
    print(f"- changed files: {len(changed_files)}")

    if not changed_files:
        print("No relevant changed files. Nothing to validate.")
        return 0

    changed_docs = classify_docs(changed_files, config)
    changed_code = [path for path in changed_files if path not in changed_docs]

    issues: list[str] = []

    for rule in config.get("rules", []):
        code_matches = [
            path for path in changed_code if match_any(path, rule.get("code", []))
        ]
        if not code_matches:
            continue

        doc_matches = [
            path for path in changed_docs if match_any(path, rule.get("docs", []))
        ]
        if not doc_matches:
            issues.append(
                "规则命中但没有同步文档："
                f" {rule.get('name', '<unnamed>')} -> 代码 {code_matches}，"
                f"期望至少命中 {rule.get('docs', [])}"
            )

    for doc_path in changed_docs:
        issues.extend(validate_doc_file(repo_root, doc_path))

    if issues:
        print("\nFAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\nPASSED")
    if changed_code:
        print(f"- changed code: {changed_code}")
    if changed_docs:
        print(f"- changed docs: {changed_docs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
