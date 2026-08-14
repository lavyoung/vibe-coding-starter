#!/usr/bin/env python3
"""Validate docs-first sync rules for the current change set."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Iterable


DEFAULT_DOC_GLOBS = ("docs/*.md", "docs/**/*.md")

# 文档状态闸门的合法取值（与 AGENTS.md §3、document-sync-map.md §1.2 同口径）
VALID_DOC_STATUSES = ("草案", "评审中", "已接受", "已生效", "已落地", "已废弃")
STATUS_PREFIX = "- 当前状态："
LINKED_CODE_HEADING = "## 关联代码"
BACKTICK_REF_RE = re.compile(r"`([^`\n]+)`")
# 反引号引用中属于模板占位符 / URL / 非仓库路径的特征
PLACEHOLDER_MARKERS = ("<", ">", "...", "vX.Y.Z")
# 状态推进证据链：已生效 / 已落地 必须携带真实日期（YYYY-MM-DD）
REAL_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# 交付物型目录：根级只允许 README.md 与模板，实际文件必须位于 vX.Y.Z/ 版本子目录
DELIVERY_DIR_NAMES = ("requirements", "design", "tasks", "upgrade", "api", "sql")
VERSION_DIR_RE = re.compile(r"^v\d+\.\d+\.\d+$")


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
    parser.add_argument(
        "--scan-all",
        action="store_true",
        help=(
            "全量扫描 docGlobs 下所有文档（不依赖 git diff），"
            "校验状态枚举与关联代码引用，用于存量治理。"
        ),
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


def scan_all_docs(repo_root: Path, config: dict) -> list[str]:
    """全量扫描 docGlobs 下的所有文档，供 --scan-all 存量治理使用。"""
    doc_globs = config.get("docGlobs") or list(DEFAULT_DOC_GLOBS)
    ignore_patterns = config.get("ignore", [])
    found: list[str] = []
    seen: set[str] = set()
    for pattern in doc_globs:
        for path in repo_root.glob(pattern):
            rel = normalize_path(path.relative_to(repo_root).as_posix())
            if rel in seen or match_any(rel, ignore_patterns):
                continue
            seen.add(rel)
            found.append(rel)
    return sorted(found)


def is_ignored_ref(ref: str) -> bool:
    """过滤掉模板占位符、URL、锚点、方法引用等非仓库路径的引用。"""
    lowered = ref.lower()
    if lowered.startswith(("http://", "https://", "mailto:")):
        return True
    if "/" not in ref or ref.startswith("#") or "{" in ref or "(" in ref:
        return True
    return any(marker in ref for marker in PLACEHOLDER_MARKERS)


def validate_linked_code_paths(
    repo_root: Path, doc_path: str
) -> tuple[list[str], list[str]]:
    """校验“## 关联代码”章节中反引号包裹的仓库内路径真实存在。

    同时支持两种写法：相对本文档目录（Markdown 链接语义）与相对仓库根。
    返回 (issues, 找到的代码路径)；代码路径指非 docs/ 开头的引用。
    """
    full_path = repo_root / doc_path
    content = full_path.read_text(encoding="utf-8")
    section = content.split(LINKED_CODE_HEADING, 1)[1]
    section = section.split("\n## ", 1)[0]
    issues: list[str] = []
    code_paths: list[str] = []
    checked: set[str] = set()
    for match in BACKTICK_REF_RE.finditer(section):
        ref = match.group(1).strip().split("#", 1)[0].strip()
        if ref in checked or is_ignored_ref(ref):
            continue
        checked.add(ref)
        resolved = (full_path.parent / ref).resolve()
        root_resolved = (repo_root / ref).resolve()
        if not resolved.exists() and not root_resolved.exists():
            issues.append(
                f"{doc_path}: “关联代码”引用不存在：`{ref}`"
                "（已按相对本文档与仓库根两种方式解析）。"
            )
            continue
        if not ref.startswith("docs/"):
            code_paths.append(ref)
    return issues, code_paths


def validate_doc_file(repo_root: Path, doc_path: str) -> list[str]:
    full_path = repo_root / doc_path
    content = full_path.read_text(encoding="utf-8")
    if doc_path.lower().endswith((".yaml", ".yml")):
        return validate_openapi_yaml(full_path, doc_path)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    issues: list[str] = []

    if not lines or not lines[0].startswith("# "):
        issues.append(f"{doc_path}: 第一行必须是一级标题。")
    if "## 文档元数据" not in content:
        issues.append(f"{doc_path}: 缺少“## 文档元数据”章节。")

    status_line = next(
        (line for line in lines if line.startswith(STATUS_PREFIX)), None
    )
    status: str | None = None
    if status_line is None:
        issues.append(f"{doc_path}: 缺少“当前状态”元数据。")
    else:
        status = status_line[len(STATUS_PREFIX):].strip()
        if status not in VALID_DOC_STATUSES:
            issues.append(
                f"{doc_path}: “当前状态”取值 {status!r} 非法，"
                f"必须为 {' / '.join(VALID_DOC_STATUSES)} 之一。"
            )
        elif status in ("已生效", "已落地"):
            # 状态推进证据链：已生效 / 已落地 必须有真实更新日期，不能是 YYYY-MM-DD 占位
            update_line = next(
                (line for line in lines if line.startswith("- 最近更新：")), None
            )
            if update_line is None:
                issues.append(f"{doc_path}: 状态为 {status} 但缺少“最近更新”元数据。")
            else:
                update_value = update_line[len("- 最近更新："):].strip()
                if not REAL_DATE_RE.match(update_value):
                    issues.append(
                        f"{doc_path}: 状态为 {status}，但“最近更新”不是真实日期"
                        f"（当前 {update_value!r}，应为 YYYY-MM-DD）。"
                    )

    if LINKED_CODE_HEADING not in content:
        issues.append(f"{doc_path}: 缺少“{LINKED_CODE_HEADING}”章节。")
    else:
        linked_issues, code_paths = validate_linked_code_paths(repo_root, doc_path)
        issues.extend(linked_issues)
        if status == "已落地" and not code_paths:
            issues.append(
                f"{doc_path}: 状态为“已落地”但“关联代码”没有引用任何代码路径"
                "（docs/ 之外的引用），无法证明已落地事实。"
            )

    return issues


def validate_openapi_yaml(path: Path, doc_path: str) -> list[str]:
    """OpenAPI YAML 契约按自身结构校验，不套用 Markdown 文档模板。"""
    issues: list[str] = []
    try:
        import yaml
    except ImportError:
        issues.append(
            f"{doc_path}: 缺少 PyYAML，无法校验 OpenAPI 结构"
            "（python -m pip install pyyaml 后重跑）。"
        )
        return issues

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.append(f"{doc_path}: OpenAPI YAML 解析失败：{exc}")
        return issues

    if not isinstance(data, dict):
        issues.append(f"{doc_path}: OpenAPI YAML 顶层必须是映射（openapi / info / paths）。")
        return issues
    if "openapi" not in data:
        issues.append(f"{doc_path}: OpenAPI YAML 缺少顶层 openapi 版本字段（如 openapi: 3.1.0）。")
    if not isinstance(data.get("info"), dict):
        issues.append(f"{doc_path}: OpenAPI YAML 缺少 info 节点（title / version）。")
    if not isinstance(data.get("paths"), dict):
        issues.append(f"{doc_path}: OpenAPI YAML 缺少 paths 节点。")
    return issues


def validate_versioned_layout(repo_root: Path) -> list[str]:
    """交付物型目录（requirements/design/tasks/upgrade/api/sql）根级只允许
    README.md 与 *TEMPLATE* 文件，实际文件必须位于 vX.Y.Z/ 版本子目录。"""
    issues: list[str] = []
    docs_root = repo_root / "docs"
    for dirname in DELIVERY_DIR_NAMES:
        delivery_dir = docs_root / dirname
        if not delivery_dir.is_dir():
            continue
        for entry in sorted(delivery_dir.iterdir()):
            if entry.is_dir():
                if not VERSION_DIR_RE.match(entry.name):
                    issues.append(
                        f"docs/{dirname}/{entry.name}: 交付物目录的子目录必须是 vX.Y.Z 版本目录"
                    )
                continue
            if entry.name == "README.md" or "TEMPLATE" in entry.name:
                continue
            issues.append(
                f"docs/{dirname}/{entry.name}: 交付物目录根级只允许 README.md 与模板，"
                "实际文件必须放入 vX.Y.Z/ 子目录"
            )
    return issues


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config_path = (repo_root / args.config).resolve()
    config = load_config(config_path)

    if args.scan_all:
        changed_files = scan_all_docs(repo_root, config)
    elif args.changed_file:
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
    if args.scan_all:
        print(f"- scanned docs: {len(changed_files)}")
    else:
        print(f"- changed files: {len(changed_files)}")

    if not changed_files:
        print("No relevant changed files. Nothing to validate.")
        return 0

    changed_docs = classify_docs(changed_files, config)
    changed_code = [path for path in changed_files if path not in changed_docs]

    issues: list[str] = []

    # 版本演进约束：交付物目录根级布局（与模式无关，始终校验）
    issues.extend(validate_versioned_layout(repo_root))

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
