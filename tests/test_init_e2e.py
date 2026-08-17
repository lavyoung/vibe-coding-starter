from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns(
    ".git", ".idea", ".vscode", "node_modules", "__pycache__", "target"
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)


def copy_repo(dest: Path) -> None:
    shutil.copytree(REPO_ROOT, dest, ignore=IGNORE)


def init_starter(dest: Path, tech_stack: str) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            "scripts/init_starter.py",
            "--repo-root",
            ".",
            "--project-name",
            "e2e-demo",
            "--tech-stack",
            tech_stack,
            "--build-command",
            "go build",
            "--test-command",
            "go test",
            "--main-modules",
            "app",
            "--business-domains",
            "tasks",
        ],
        cwd=dest,
    )


def check_all(dest: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [sys.executable, "scripts/check_all.py", "--scan-docs", "--skip-examples"],
        cwd=dest,
    )


class InitEndToEndTests(unittest.TestCase):
    """端到端验证：复制真实仓库 → init_starter 初始化 → check_all 开箱即绿。

    非 Java 技术栈应自动裁剪 Java 技能且校验通过；Java 技术栈应保留技能且校验通过。
    需要 PyYAML（doc-sync --scan-all 校验 OpenAPI YAML），CI 已通过
    `python -m pip install pyyaml` 安装。
    """

    def test_init_non_java_stack_is_green(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dest = Path(temp_dir) / "repo"
            copy_repo(dest)

            init_result = init_starter(dest, "Go 1.22")
            self.assertEqual(
                init_result.returncode, 0, init_result.stdout + init_result.stderr
            )

            java_dirs = list((dest / "tools" / "skills").glob("java-*"))
            self.assertEqual(java_dirs, [])
            agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotIn("0.3 专项 skill 强制门禁", agents)

            check_result = check_all(dest)
            self.assertEqual(
                check_result.returncode,
                0,
                check_result.stdout + check_result.stderr,
            )

    def test_init_java_stack_keeps_skills_and_is_green(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dest = Path(temp_dir) / "repo"
            copy_repo(dest)

            init_result = init_starter(dest, "Java 17 + Spring Boot")
            self.assertEqual(
                init_result.returncode, 0, init_result.stdout + init_result.stderr
            )

            java_dirs = list((dest / "tools" / "skills").glob("java-*"))
            self.assertEqual(len(java_dirs), 12)
            agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("0.3 专项 skill 强制门禁", agents)

            check_result = check_all(dest)
            self.assertEqual(
                check_result.returncode,
                0,
                check_result.stdout + check_result.stderr,
            )


if __name__ == "__main__":
    unittest.main()
