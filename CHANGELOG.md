# 变更记录

本文件记录 `vibe-coding-starter` 的版本演进，方便使用者了解每个版本新增了什么、调整了什么，以及是否需要补做升级动作。

## [Unreleased]

### Added

- 新增根级 `CLAUDE.md` 兼容入口，方便会自动读取该文件的 agent 直接按与 `AGENTS.md` 同口径的规则协作。
- 新增 `docs/governance/agent-collaboration-protocol.md`、`contracts/README.md` 与 `contracts/examples/*.json`，补齐跨 Codex / Claude / 其他 agent 的最小协作协议和可直接复用示例。
- 新增 `tools/skills/task-router/`，把“先路由任务、再决定实现路径”的入口沉淀为仓库内可复用 skill。

### Changed

- `README.md`、`QUICKSTART.md`、`EXPORTING.md`、`docs/index.md`、`docs/onboarding.md`、`docs/README.md`、`docs/governance/*.md` 与 `scripts/check_all.py` 同步补齐 `CLAUDE.md` 入口和一致性检查说明。
- `README.md`、`QUICKSTART.md`、`docs/index.md`、`docs/onboarding.md`、`docs/governance/*.md`、`EXPORTING.md`、`UPGRADING.md` 同步补齐多 agent 协作协议入口。
- `README.md`、`QUICKSTART.md`、`docs/governance/*.md` 与 `scripts/check_all.py` 同步补齐 `task-router` skill 入口和检查约束。

## [v0.3.1] - 2026-06-22

### Changed

- `AGENTS.md`、`docs/onboarding.md`、`docs/governance/*.md`、`prompts/*.txt`、`.github/PULL_REQUEST_TEMPLATE.md` 补充“优先复用现有实现、避免重复造轮子、控制架构漂移”的协作约束。
- `tools/skills/code-review/references/review-checklist.md` 增加对重复实现、不必要抽象和边界漂移的审查项。
- `scripts/check_all.ps1`、`scripts/doc_sync_check.ps1` 改为复用 `scripts/resolve_python_runtime.ps1` 探测真实 Python 运行时，避免命中 Windows Store alias 后静默失败。
- `tools/skills/doc-driven-implementation/SKILL.md`、`tools/skills/post-change-check/SKILL.md` 补充复用优先与防架构腐化的执行 / 收口要求。
- `README.md`、`QUICKSTART.md`、`CONTRIBUTING.md` 补充模板价值表达和维护者评审口径，明确“先找复用点，再做最小实现”。
- 新增 `prompts/task-entry.txt` 作为统一任务入口，并在 `README.md`、`QUICKSTART.md`、`docs/governance/ai-collaboration-best-practices.md` 中补齐路由入口说明。
- 新增 `docs/evolution/current-snapshot.md` 作为单点快照入口，并同步更新 `docs/index.md`、`docs/onboarding.md`、`docs/README.md`、`docs/evolution/INDEX.md`、`docs/governance/document-sync-map.md` 和 `README.md` 的接手链路说明。
- 新增 `docs/governance/project-handoff-checklist.md` 与 `contracts/*.schema.json`，补齐交接模板和结构化输入 / 输出约束。
- `scripts/check_all.py` 增加 starter 关键资产和 schema 形态检查，并在统一入口 / 治理规则变更时提示回查 snapshot、handoff 与 contracts。

## [v0.3.0] - 2026-06-22

### Added

- 增加 `scripts/check_all.ps1`、`scripts/check_all.sh`、`scripts/doc_sync_check.ps1`、`scripts/doc_sync_check.sh`，提供跨平台检查脚本入口。
- 扩展示例 `examples/spring-boot-device-center/`，补齐 `docs/sql`、`docs/upgrade` 与 `src/main/resources/db/migration/` 资产，覆盖更贴近真实团队的 schema / upgrade 场景。

### Changed

- `README.md`、`QUICKSTART.md`、`DEMO.md` 收紧首次采用路径，明确 `README -> QUICKSTART -> DEMO` 的入口链路。
- `.github/PULL_REQUEST_TEMPLATE.md`、`tools/skills/code-review/`、`prompts/standard-03-findings-first-review.txt`、治理文档统一为“先文档状态、再 diff、再测试”的 review 顺序。
- `scripts/check_all.py` 改为更清晰的分组式收口输出，并支持 `--base / --head`，可同时服务本地与 CI。
- `.github/workflows/doc-sync.yml` 收口为统一检查入口，在 CI 中通过 `check_all` 覆盖 `doc-sync`、链接检查与示例自检。
- 根级 `.gitignore` 补充 `.idea/`、`__pycache__/`、`target/`，减少常见本地产物噪音。

## [v0.2.0] - 2026-06-18

### Added

- 增加 `scripts/init_starter.py`，用于批量替换模板占位符，并支持关闭 `docs/ui` 可选模块。
- 增加 `examples/spring-boot-device-center/`，提供 `Java 17 + Spring Boot 3.3.4` 的后端示例项目。
- 增加 `scripts/check_all.py`，统一执行 `doc-sync`、Markdown 相对链接检查和示例自检。
- 增加 `UPGRADING.md`，说明模板升级时的覆盖策略与检查步骤。

### Changed

- `README.md`、`QUICKSTART.md` 补充初始化脚本与统一检查入口说明。
- `examples/README.md`、`DEMO.md` 增加 Spring Boot 示例入口。

## [v0.1.0] - 2026-06-18

### Added

- `AGENTS.md` 与 `AGENTS.template.md`
- `docs/` 文档优先目录骨架
- 文档状态闸门与 `document-sync-map`
- `.doc-sync.json` 与 `scripts/doc_sync_check.py`
- `.github/workflows/doc-sync.yml`
- `prompts/` 标准会话提示词
- `tools/skills/` 通用 skills
- `examples/minimal-task-board/` 最小示例项目
- `QUICKSTART.md`、`DEMO.md`
- `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`PUBLISHING.md`、`EXPORTING.md`

## 说明

- `Unreleased` 表示尚未打 tag 的工作内容。
- 正式发布时，应把 `Unreleased` 中已经完成的内容归档到对应版本号。
