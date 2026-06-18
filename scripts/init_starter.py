#!/usr/bin/env python3
"""初始化 starter 模板中的占位信息。"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".py",
    ".ps1",
    ".sh",
}

SKIP_PARTS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "examples",
}

PLACEHOLDER_KEYS = {
    "<PROJECT_NAME>",
    "<TECH_STACK>",
    "<BUILD_COMMAND>",
    "<TEST_COMMAND>",
    "<MAIN_MODULES>",
    "<BUSINESS_DOMAINS>",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="初始化模板仓库中的占位信息，并可选关闭 docs/ui 模块。"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="仓库根目录，默认取脚本所在仓库根目录。",
    )
    parser.add_argument("--project-name", required=True, help="项目名称。")
    parser.add_argument("--tech-stack", help="技术栈描述。")
    parser.add_argument("--build-command", help="构建命令。")
    parser.add_argument("--test-command", help="测试命令。")
    parser.add_argument("--main-modules", help="主模块列表或说明。")
    parser.add_argument("--business-domains", help="主要业务域列表或说明。")
    parser.add_argument(
        "--disable-ui",
        action="store_true",
        help="关闭可选的 docs/ui 模块，并移除关键入口中的直接链接。",
    )
    return parser.parse_args()


def build_replacements(args: argparse.Namespace) -> dict[str, str]:
    replacements = {
        "<PROJECT_NAME>": args.project_name,
        "<TECH_STACK>": args.tech_stack,
        "<BUILD_COMMAND>": args.build_command,
        "<TEST_COMMAND>": args.test_command,
        "<MAIN_MODULES>": args.main_modules,
        "<BUSINESS_DOMAINS>": args.business_domains,
    }
    return {key: value for key, value in replacements.items() if value}


def should_skip(path: Path, repo_root: Path) -> bool:
    relative_parts = path.relative_to(repo_root).parts
    return any(part in SKIP_PARTS for part in relative_parts)


def iter_text_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    self_script = repo_root / "scripts" / "init_starter.py"
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path, repo_root):
            continue
        if path.resolve() == self_script.resolve():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        files.append(path)
    return files


def update_readme_title(text: str, project_name: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "# vibe-coding-starter":
        lines[0] = f"# {project_name}"
        text = "\n".join(lines)
        if not text.endswith("\n"):
            text += "\n"
    template_notice = (
        "如果你是通过模板创建了一个新项目，请先把本文件标题、首段简介和仓库描述替换成你自己的项目信息；"
        "`vibe-coding-starter` 只是上游模板名。"
    )
    initialized_notice = "本仓库已基于模板完成初始化；仍需根据项目实际情况继续补全文档事实。"
    return text.replace(template_notice, initialized_notice)


def replace_placeholders(repo_root: Path, replacements: dict[str, str]) -> list[Path]:
    changed_files: list[Path] = []
    for path in iter_text_files(repo_root):
        original = path.read_text(encoding="utf-8")
        updated = original
        for source, target in replacements.items():
            updated = updated.replace(source, target)
        if path == repo_root / "README.md":
            updated = update_readme_title(updated, replacements["<PROJECT_NAME>"])
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files.append(path)
    return changed_files


def disable_ui_module(repo_root: Path) -> list[Path]:
    changed_files: list[Path] = []
    ui_dir = repo_root / "docs" / "ui"
    if ui_dir.exists():
        shutil.rmtree(ui_dir)

    line_changes = {
        repo_root / "README.md": (
            "│   └── ui/",
            None,
        ),
        repo_root / "docs" / "index.md": (
            "[docs/ui/README.md](ui/README.md)",
            "7. 若后续涉及页面或交互，再补启用 `docs/ui/`。",
        ),
        repo_root / "docs" / "evolution" / "INDEX.md": (
            "| UI 交互入口 |",
            "| UI 交互入口 | `docs/ui/` 未启用 | 如后续涉及页面 / 弹窗 / 上传交互，再补启用 |",
        ),
    }

    for path, (marker, replacement_line) in line_changes.items():
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        lines = original.splitlines()
        new_lines: list[str] = []
        changed = False
        for line in lines:
            if marker not in line:
                new_lines.append(line)
                continue
            changed = True
            if replacement_line is not None:
                new_lines.append(replacement_line)
        if not changed:
            continue
        updated = "\n".join(new_lines)
        if original.endswith("\n"):
            updated += "\n"
        path.write_text(updated, encoding="utf-8")
        changed_files.append(path)

    return changed_files


def find_remaining_placeholders(repo_root: Path) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in iter_text_files(repo_root):
        text = path.read_text(encoding="utf-8")
        matches = [token for token in PLACEHOLDER_KEYS if token in text]
        if matches:
            findings[str(path.relative_to(repo_root))] = matches
    return findings


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    replacements = build_replacements(args)

    if "<PROJECT_NAME>" not in replacements:
        print("缺少必须参数：--project-name", file=sys.stderr)
        return 1
    if not repo_root.exists():
        print(f"仓库目录不存在：{repo_root}", file=sys.stderr)
        return 1

    changed_files = replace_placeholders(repo_root, replacements)

    if args.disable_ui:
        changed_files.extend(disable_ui_module(repo_root))

    remaining = find_remaining_placeholders(repo_root)

    print(f"repo-root: {repo_root}")
    print(f"changed-files: {len({path.resolve() for path in changed_files})}")
    if args.disable_ui:
        print("ui-module: disabled")
    else:
        print("ui-module: kept")

    if remaining:
        print("remaining-placeholders:")
        for path, tokens in sorted(remaining.items()):
            print(f"- {path}: {', '.join(sorted(tokens))}")
    else:
        print("remaining-placeholders: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
