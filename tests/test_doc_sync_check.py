from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_SYNC_PATH = REPO_ROOT / "scripts" / "doc_sync_check.py"
SPEC = importlib.util.spec_from_file_location("doc_sync_check_under_test", DOC_SYNC_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load scripts/doc_sync_check.py")
DOC_SYNC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DOC_SYNC
SPEC.loader.exec_module(DOC_SYNC)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _has_pyyaml() -> bool:
    try:
        import yaml  # noqa: F401

        return True
    except ImportError:
        return False


VALID_DOC = """# 测试文档

## 文档元数据

- 当前状态：已生效
- 最近更新：2026-08-17

## 关联代码

- `src/app.js`
"""


class DocSyncCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo_root = Path(self._tmp.name)
        write_file(self.repo_root / "src" / "app.js", "// app\n")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # ---- validate_doc_file ----

    def test_validate_doc_file_accepts_valid_doc(self) -> None:
        write_file(self.repo_root / "docs" / "index.md", VALID_DOC)
        issues = DOC_SYNC.validate_doc_file(self.repo_root, "docs/index.md")
        self.assertEqual(issues, [])

    def test_validate_doc_file_rejects_invalid_status(self) -> None:
        doc = VALID_DOC.replace("- 当前状态：已生效", "- 当前状态：随便")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues = DOC_SYNC.validate_doc_file(self.repo_root, "docs/index.md")
        self.assertTrue(any("非法" in issue for issue in issues))

    def test_validate_doc_file_requires_real_date_for_effective(self) -> None:
        doc = VALID_DOC.replace("- 最近更新：2026-08-17", "- 最近更新：YYYY-MM-DD")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues = DOC_SYNC.validate_doc_file(self.repo_root, "docs/index.md")
        self.assertTrue(any("最近更新" in issue and "真实日期" in issue for issue in issues))

    def test_validate_doc_file_requires_code_path_for_landed(self) -> None:
        # 已落地但关联代码只引用 docs 内文档（无代码路径）→ 必须失败
        doc = (
            VALID_DOC.replace("- 当前状态：已生效", "- 当前状态：已落地")
            .replace("- `src/app.js`", "- `docs/index.md`")
        )
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues = DOC_SYNC.validate_doc_file(self.repo_root, "docs/index.md")
        self.assertTrue(any("已落地" in issue and "代码路径" in issue for issue in issues))

    def test_validate_doc_file_accepts_landed_with_code_path(self) -> None:
        # 已落地且关联代码引用了真实代码路径 → 通过
        doc = VALID_DOC.replace("- 当前状态：已生效", "- 当前状态：已落地")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues = DOC_SYNC.validate_doc_file(self.repo_root, "docs/index.md")
        self.assertEqual(issues, [])

    # ---- validate_linked_code_paths ----

    def test_validate_linked_code_paths_supports_markdown_links(self) -> None:
        doc = VALID_DOC.replace("- `src/app.js`", "- [src/app.js](src/app.js)")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues, code_paths = DOC_SYNC.validate_linked_code_paths(
            self.repo_root, "docs/index.md"
        )
        self.assertEqual(issues, [])
        self.assertEqual(code_paths, ["src/app.js"])

    def test_validate_linked_code_paths_reports_missing_path(self) -> None:
        doc = VALID_DOC.replace("- `src/app.js`", "- `src/missing.js`")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues, _ = DOC_SYNC.validate_linked_code_paths(self.repo_root, "docs/index.md")
        self.assertTrue(any("引用不存在" in issue for issue in issues))

    def test_validate_linked_code_paths_ignores_template_placeholders(self) -> None:
        doc = VALID_DOC.replace("- `src/app.js`", "- `<path/to/code>`：说明关系")
        write_file(self.repo_root / "docs" / "index.md", doc)
        issues, code_paths = DOC_SYNC.validate_linked_code_paths(
            self.repo_root, "docs/index.md"
        )
        self.assertEqual(issues, [])
        self.assertEqual(code_paths, [])

    # ---- validate_versioned_layout ----

    def test_validate_versioned_layout_accepts_version_dirs_and_templates(self) -> None:
        write_file(self.repo_root / "docs" / "design" / "v1.2.3" / "note.md", VALID_DOC)
        write_file(self.repo_root / "docs" / "design" / "README.md", "# design\n")
        write_file(
            self.repo_root / "docs" / "design" / "DESIGN_TEMPLATE.md", "# template\n"
        )
        issues = DOC_SYNC.validate_versioned_layout(self.repo_root)
        self.assertEqual(issues, [])

    def test_validate_versioned_layout_rejects_root_files_and_bad_dirs(self) -> None:
        write_file(self.repo_root / "docs" / "design" / "loose.md", VALID_DOC)
        write_file(
            self.repo_root / "docs" / "design" / "not-a-version" / "x.md", VALID_DOC
        )
        issues = DOC_SYNC.validate_versioned_layout(self.repo_root)
        self.assertTrue(any("loose.md" in issue for issue in issues))
        self.assertTrue(any("not-a-version" in issue for issue in issues))

    # ---- validate_openapi_yaml ----

    def _write_openapi(self, payload: dict, rel: str = "docs/api/v1.0.0/test-api.yaml") -> Path:
        import yaml

        path = self.repo_root / rel
        write_file(path, yaml.safe_dump(payload, allow_unicode=True))
        return path

    @unittest.skipUnless(_has_pyyaml(), "pyyaml not installed")
    def test_validate_openapi_yaml_accepts_valid_contract(self) -> None:
        path = self._write_openapi(
            {
                "openapi": "3.1.0",
                "info": {"title": "t", "version": "v1.0.0"},
                "paths": {
                    "/tasks/{taskId}": {
                        "get": {"responses": {"200": {"description": "ok"}}},
                    },
                },
                "components": {"schemas": {"Task": {"type": "object"}}},
            }
        )
        issues = DOC_SYNC.validate_openapi_yaml(path, "docs/api/v1.0.0/test-api.yaml")
        self.assertEqual(issues, [])

    @unittest.skipUnless(_has_pyyaml(), "pyyaml not installed")
    def test_validate_openapi_yaml_rejects_empty_operation_and_dangling_ref(self) -> None:
        path = self._write_openapi(
            {
                "openapi": "3.1.0",
                "info": {"title": "t", "version": "v1.0.0"},
                "paths": {
                    "/x": {"summary": "no op"},
                    "/tasks/{taskId}": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "ok",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Missing"
                                            }
                                        }
                                    },
                                },
                            }
                        },
                    },
                },
                "components": {"schemas": {"Task": {"type": "object"}}},
            }
        )
        issues = DOC_SYNC.validate_openapi_yaml(path, "docs/api/v1.0.0/test-api.yaml")
        self.assertTrue(any("缺少任何 HTTP operation" in issue for issue in issues))
        self.assertTrue(any("$ref 指向不存在" in issue for issue in issues))

    # ---- scan_all_docs ----

    def test_scan_all_docs_collects_globs(self) -> None:
        write_file(self.repo_root / "docs" / "index.md", VALID_DOC)
        write_file(self.repo_root / "docs" / "design" / "v1.0.0" / "d.md", VALID_DOC)
        write_file(self.repo_root / "docs" / "api" / "v1.0.0" / "a.yaml", "openapi: 3.1.0\n")
        config = {
            "docGlobs": [
                "docs/*.md",
                "docs/**/*.md",
                "docs/**/**/*.md",
                "docs/api/*.yaml",
                "docs/api/**/*.yaml",
            ],
            "ignore": [],
        }
        found = DOC_SYNC.scan_all_docs(self.repo_root, config)
        self.assertIn("docs/index.md", found)
        self.assertIn("docs/design/v1.0.0/d.md", found)
        self.assertIn("docs/api/v1.0.0/a.yaml", found)


if __name__ == "__main__":
    unittest.main()
