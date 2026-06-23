from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_ALL_PATH = REPO_ROOT / "scripts" / "check_all.py"
SPEC = importlib.util.spec_from_file_location("check_all_under_test", CHECK_ALL_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load scripts/check_all.py")
CHECK_ALL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK_ALL
SPEC.loader.exec_module(CHECK_ALL)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class CheckAllTests(unittest.TestCase):
    def test_validate_starter_assets_checks_cross_platform_entrypoints(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_file(repo_root / "scripts" / "check_all.py", "print('ok')\n")

            with patch.object(CHECK_ALL, "REQUIRED_STARTER_FILES", {}), patch.object(
                CHECK_ALL,
                "PUBLIC_SCRIPT_ENTRYPOINTS",
                {"scripts/check_all.py": ("scripts/check_all.ps1", "scripts/check_all.sh")},
            ):
                results = CHECK_ALL.validate_starter_assets(repo_root, changed_files=[])

            target = next(
                result
                for result in results
                if result.title == "cross-platform script entrypoints"
            )
            self.assertEqual(target.status, "failed")
            self.assertIn("scripts/check_all.ps1", target.detail or "")
            self.assertIn("scripts/check_all.sh", target.detail or "")

    def test_collect_example_workflow_assets_requires_matching_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_file(
                repo_root / "contracts" / "task-entry.schema.json",
                json.dumps(
                    {
                        "type": "object",
                        "required": ["task_type", "goal"],
                        "properties": {
                            "task_type": {"type": "string"},
                            "goal": {"type": "string"},
                        },
                    },
                    ensure_ascii=False,
                ),
            )
            write_file(repo_root / "examples" / "demo" / "README.md", "# demo\n")
            write_file(
                repo_root
                / "examples"
                / "demo"
                / "docs"
                / "tasks"
                / "V1-demo-task-entry.json",
                json.dumps(
                    {"task_type": "code_change", "goal": "demo"},
                    ensure_ascii=False,
                ),
            )

            results = CHECK_ALL.collect_example_workflow_assets(repo_root)
            target = next(
                result for result in results if result.title == "example workflow assets"
            )

            self.assertEqual(target.status, "failed")
            self.assertIn("docs/tasks/<task-name>-task-entry.json", target.detail or "")
            self.assertIn("missing matching handoff", target.detail or "")

    def test_collect_example_workflow_assets_accepts_valid_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_file(
                repo_root / "contracts" / "task-entry.schema.json",
                json.dumps(
                    {
                        "type": "object",
                        "required": ["task_type", "goal"],
                        "properties": {
                            "task_type": {"type": "string"},
                            "goal": {"type": "string"},
                        },
                    },
                    ensure_ascii=False,
                ),
            )
            write_file(repo_root / "examples" / "demo" / "README.md", "# demo\n")
            write_file(
                repo_root
                / "examples"
                / "demo"
                / "docs"
                / "tasks"
                / "V1-demo-task-entry.json",
                json.dumps(
                    {"task_type": "code_change", "goal": "demo"},
                    ensure_ascii=False,
                ),
            )
            write_file(
                repo_root
                / "examples"
                / "demo"
                / "docs"
                / "tasks"
                / "V1-demo-handoff.md",
                "# handoff\n",
            )

            results = CHECK_ALL.collect_example_workflow_assets(repo_root)
            workflow = next(
                result for result in results if result.title == "example workflow assets"
            )
            task_entry_shape = next(
                result for result in results if result.title == "example task-entry shape"
            )

            self.assertEqual(workflow.status, "passed")
            self.assertEqual(task_entry_shape.status, "passed")


if __name__ == "__main__":
    unittest.main()
