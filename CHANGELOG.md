# 变更记录

本文件记录 `vibe-coding-starter` 的版本演进，方便使用者了解每个版本新增了什么、调整了什么，以及是否需要补做升级动作。

## [Unreleased]

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
