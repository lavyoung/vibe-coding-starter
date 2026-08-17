from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_STARTER_PATH = REPO_ROOT / "scripts" / "init_starter.py"
SPEC = importlib.util.spec_from_file_location("init_starter_under_test", INIT_STARTER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load scripts/init_starter.py")
INIT_STARTER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INIT_STARTER
SPEC.loader.exec_module(INIT_STARTER)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


AGENTS_WITH_JAVA = """# Demo 项目专属约束

## 0. Skill 扫描规则

### 0.2 约束

- 若存在与当前任务匹配的 skill，优先读取对应 `SKILL.md`。
- 新增或重构 Java 服务层结构时，读取 `tools/skills/java-service-structure/SKILL.md`。
- 仅当项目技术栈为 Java 系（以 `docs/project-profile.md` 技术栈字段为准）时，`tools/skills/java-*` 技能才参与匹配与门禁。
- 若当前任务与已有 skill 均不匹配，再回退到本 `AGENTS.md`。

### 0.3 专项 skill 强制门禁

> 本节仅在项目技术栈为 Java 系时生效。

涉及以下区域时，必须同时读取对应 `SKILL.md`：

- 分布式锁：`tools/skills/java-distributed-lock/SKILL.md`
- MyBatis-Plus 查询：`tools/skills/java-mybatis-query/SKILL.md`

## 1. 项目事实

- 项目事实维护在 `docs/project-profile.md`。
"""

PROFILE_WITH_JAVA = """# 项目事实档案

## 文档元数据

- 当前状态：已生效
- 最近更新：2026-08-17

## 4. 专项 skills 启用条件

> 本节以 Java 系技能库为示例。非 Java 项目按 [`tools/skills/README.md`](../tools/skills/README.md) 裁剪技能库后，同步精简或改写本节条目。

- Java 编码规范：`tools/skills/java-coding-standards/`
- 分布式锁：`tools/skills/java-distributed-lock/`
- 修改既有行为：`tools/skills/safe-code-change/`
- 完成代码或文档变更：`tools/skills/post-change-check/`

## 关联代码

- [AGENTS.md](../AGENTS.md)
"""

SKILLS_README = """# 技能库（tools/skills）

| 类别 | 判定 | 当前清单 |
|---|---|---|
| 通用技能 | 与具体技术栈无关 | `task-router` |
| 栈绑定技能 | 规则深度依赖某技术栈 / 框架语感（如 Spring、MyBatis-Plus、Redisson） | 12 个 `java-*`：服务结构、事务边界 |

> 本模板以 Java 系为示例栈（技能库作者的主技术栈），因此 17 个 skill 中 12 个是 `java-*`。这是"电池内置"设计，不是必须保留的内容。
"""

README_WITH_JAVA = """# vibe-coding-starter

一个包含 17 个可复用 skills 的模板仓库。

| AI 行为约束 | 无 | 17 个可复用 skill，`AGENTS.md` 0.3 设强制门禁 |

- **17 个 skill**：5 个通用能力，外加 12 个 Java 专项

- `tools/skills/`
  17 个可复用 skill：
  - 通用：`task-router`
  - Java 专项（栈绑定）：`java-service-structure`、`java-distributed-lock`
  - 注：`java-*` 为栈绑定技能，非 Java 项目按 [tools/skills/README.md](tools/skills/README.md) 裁剪
"""


def build_repo(root: Path) -> None:
    write_file(root / "tools" / "skills" / "java-distributed-lock" / "SKILL.md", "---\nname: java-distributed-lock\n---\n# lock\n")
    write_file(root / "tools" / "skills" / "java-service-structure" / "SKILL.md", "---\nname: java-service-structure\n---\n# structure\n")
    write_file(root / "tools" / "skills" / "task-router" / "SKILL.md", "---\nname: task-router\n---\n# router\n")
    write_file(root / "AGENTS.md", AGENTS_WITH_JAVA)
    write_file(root / "docs" / "project-profile.md", PROFILE_WITH_JAVA)
    write_file(root / "tools" / "skills" / "README.md", SKILLS_README)
    write_file(root / "README.md", README_WITH_JAVA)


class InitStarterTrimTests(unittest.TestCase):
    def test_is_java_stack(self) -> None:
        self.assertFalse(INIT_STARTER.is_java_stack(None))
        self.assertFalse(INIT_STARTER.is_java_stack("Node.js 20"))
        self.assertFalse(INIT_STARTER.is_java_stack("Python 3.12"))
        self.assertTrue(INIT_STARTER.is_java_stack("Java 17"))
        self.assertTrue(INIT_STARTER.is_java_stack("Spring Boot 3.3"))

    def test_trim_java_skills_removes_java_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build_repo(root)

            changed = INIT_STARTER.trim_java_skills(root)

            self.assertFalse((root / "tools" / "skills" / "java-distributed-lock").exists())
            self.assertFalse((root / "tools" / "skills" / "java-service-structure").exists())
            self.assertTrue((root / "tools" / "skills" / "task-router").exists())
            self.assertIn(root / "AGENTS.md", changed)
            self.assertIn(root / "docs" / "project-profile.md", changed)
            self.assertIn(root / "tools" / "skills" / "README.md", changed)
            self.assertIn(root / "README.md", changed)

            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotIn("0.3 专项 skill 强制门禁", agents)
            self.assertNotIn("java-service-structure", agents)
            self.assertNotIn("仅当项目技术栈为 Java 系", agents)
            self.assertIn("## 1. 项目事实", agents)

            profile = (root / "docs" / "project-profile.md").read_text(encoding="utf-8")
            self.assertNotIn("tools/skills/java-", profile)
            self.assertNotIn("本节以 Java 系技能库为示例", profile)
            self.assertIn("本节按项目技术栈维护专项 skill 启用条件", profile)
            self.assertIn("tools/skills/safe-code-change/", profile)

            skills_readme = (root / "tools" / "skills" / "README.md").read_text(encoding="utf-8")
            self.assertNotIn("12 个 `java-*`", skills_readme)
            self.assertNotIn("本模板以 Java 系为示例栈", skills_readme)

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertNotIn("Java 专项（栈绑定）", readme)
            self.assertNotIn("17 个可复用", readme)
            self.assertNotIn("**17 个 skill**", readme)
            self.assertIn("通用：`task-router`", readme)

    def test_trim_java_skills_noop_without_java_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "README.md", "# x\n")
            changed = INIT_STARTER.trim_java_skills(root)
            self.assertEqual(changed, [])


if __name__ == "__main__":
    unittest.main()
