# 变更记录

本文件记录 `vibe-coding-starter` 的版本演进，方便使用者了解每个版本新增了什么、调整了什么，以及是否需要补做升级动作。

## [Unreleased]

### Added

- 新增 `tools/skills/java-coding-standards/`、`tools/skills/java-interface-javadoc/`、`tools/skills/java-spring-openapi-doc-generator/`、`tools/skills/java-unit-test-designer/`、`tools/skills/java-mybatis-query/` 与 `tools/skills/java-distributed-lock/` 六个通用 Java skill（从 `shared_car_wash_saas` 移植并去项目化），覆盖编码规范、接口 Javadoc、OpenAPI 定义层、单元测试设计、MyBatis 查询与分布式锁。
- 新增 `tools/skills/java-async-thread-pool/`、`tools/skills/java-client-adapter/`、`tools/skills/java-controller-contract/` 与 `tools/skills/java-error-code-i18n/` 四个通用 Java skill（从 `shared_car_wash_saas` 移植并去项目化），覆盖异步线程池、第三方防腐层、Controller 接口契约与错误码国际化。
- `docs/project-profile.md` 的“专项 skills 启用条件”同步登记上述 skill 的启用场景。

### Changed

- `tools/skills/java-service-structure/`、`tools/skills/java-transaction-boundary/`（含两份 references）与 `tools/skills/safe-code-change/` 吸收 `shared_car_wash_saas` 同源 skill 的深度内容：包职责矩阵、规则静态化决策、伪提取判别四问、事务一致性集合与代理路径、改前基线证据门禁、批量与资金流保护、带证据合并与强制交接检查。
- `docs/api/` 职责调整：对外接口契约默认产出**可导入的 OpenAPI YAML**（随设计文档生成），Markdown 不再作为默认契约输出（仅允许 `*-notes.md` 作补充说明）；同步更新 `docs/api/README.md`、`docs/governance/document-sync-map.md`、`docs/index.md`、`docs/README.md`、`docs/design/DESIGN_TEMPLATE.md`、`docs/evolution/current-snapshot.md`、`docs/governance/prompt-workflow-playbook.md` 与 `tools/skills/java-spring-openapi-doc-generator/`；并新增可直接导入的完整示例契约 `docs/api/task-api.yaml`。
- `.doc-sync.json` 将 `docs/api/**/*.yaml` 纳入文档校验范围，`scripts/doc_sync_check.py` 对 OpenAPI YAML 走结构校验（顶层 `openapi` / `info` / `paths`），不再套用 Markdown 文档模板要求。
- 新增**版本演进约束**：交付物型目录（`requirements/`、`design/`、`tasks/`、`upgrade/`、`api/`、`sql/`）必须按版本子目录 `vX.Y.Z/` 组织，版本目录之下才是真正的文件；目录根只保留 README 与跨版本模板；事实源型目录（`architecture/`、`governance/`、`rfcs/`、`explanation/adr/`、`evolution/`、`ui/`）持续根级演进。同步更新 `docs/README.md`、`docs/index.md`、`docs/governance/document-sync-map.md`、六个交付物目录 README、`docs/design/DESIGN_TEMPLATE.md`、`docs/evolution/current-snapshot.md`、`docs/governance/prompt-workflow-playbook.md` 与 `QUICKSTART.md`；示例契约移至 `docs/api/v1.0.0/task-api.yaml`。
- skill 体系优化：清除 `java-spring-openapi-doc-generator` 与 `java-error-code-i18n` 中的项目特定符号残留；`AGENTS.md` 新增 0.3 专项 skill 强制门禁（分布式锁、MyBatis、Controller / OpenAPI、错误码 / i18n、异步、防腐层、测试、编码规范等 9 个区域）；为 `java-service-structure`、`java-transaction-boundary`、`safe-code-change` 补齐 `agents/openai.yaml`；`task-router` 与 `post-change-check` 衔接 `java-*` skill 路由与收口复核。
- skill 语言统一：`java-coding-standards`、`java-interface-javadoc`、`java-spring-openapi-doc-generator`、`java-unit-test-designer`、`java-mybatis-query`、`java-distributed-lock` 六个 skill 正文由英文统一为中文；frontmatter `description` 保留英文供工具链语义匹配，代码符号与示例保持原文。
- 示例资产同步新规则：`minimal-task-board` 与 `spring-boot-device-center` 的交付物文档迁移到 `v1.2.0/` 版本目录（requirements / design / tasks / upgrade / sql），API 契约由 Markdown 改写为可导入 OpenAPI YAML（`docs/api/v1.2.0/*.yaml`，与实际代码行为对齐）；`check_all.py` 示例 task-entry / handoff 查找改为递归以支持版本目录；根仓库与两个示例的 `.doc-sync.json` `docGlobs` 加深一层覆盖版本目录三层路径；同步更新示例 README / index / INDEX / document-sync-map / handoff / task-entry 与根 `DEMO.md` 的全部引用。
- 强化价值主张：`README.md` 新增“为什么值得用（对比裸 AGENTS.md）”小节（失效场景表、机制对比表、可数资产清单、“这套体系的代价”小节），并修正 skill 清单事实（四个通用 Codex skill → 17 个 skill 全量清单）；`QUICKSTART.md` 开头新增“为什么值得花这 5 分钟”，先说服再操作。

## [v0.4.1] - 2026-06-23

### Added

- 新增 `tools/skills/README.md`（技能库结构、非 Java 项目 3 步裁剪法、新增 skill 规范）与 `tools/skills/_template/`（空白 skill 模板），非 Java 项目可一键裁剪栈绑定技能并照模板补位。

### Changed

- 处理技能库技术栈偏斜：`AGENTS.md` 0.3 专项门禁改为条件式（仅项目技术栈为 Java 系时生效，依据 `docs/project-profile.md` 技术栈字段）；`task-router`、`post-change-check`、`safe-code-change` 的 `java-*` 引用同步增加技术栈前置条件；`docs/project-profile.md` §4 与 README 技能清单补充裁剪说明。
- `README.md`、`QUICKSTART.md`、`contracts/README.md`、`CLAUDE.md` 与 `scripts/check_all.py` 收口为“`CLAUDE.md` 与 `contracts/` 按需启用”的口径，不再把它们当成默认必带能力。
- `tests/test_check_all.py` 补充“缺少 `CLAUDE.md` 或 `contracts/` 仍可通过基础检查”的回归用例，避免后续把可选能力重新写回强依赖。

## [v0.4.0] - 2026-06-23

### Added

- 新增根级 `CLAUDE.md` 兼容入口，方便会自动读取该文件的 agent 直接按与 `AGENTS.md` 同口径的规则协作。
- 新增 `docs/governance/agent-collaboration-protocol.md`、`contracts/README.md` 与 `contracts/examples/*.json`，补齐跨 Codex / Claude / 其他 agent 的最小协作协议和可直接复用示例。
- 新增 `tools/skills/task-router/`，把“先路由任务、再决定实现路径”的入口沉淀为仓库内可复用 skill。
- 新增 `scripts/init_starter.ps1`、`scripts/init_starter.sh`，补齐初始化脚本的 PowerShell / shell 入口。
- 新增 `.gitattributes` 统一文本文件行尾策略，并补充 `tests/test_check_all.py` 轻量自测，固定关键治理检查行为。

### Changed

- `README.md`、`QUICKSTART.md`、`EXPORTING.md`、`docs/index.md`、`docs/onboarding.md`、`docs/README.md`、`docs/governance/*.md` 与 `scripts/check_all.py` 同步补齐 `CLAUDE.md` 入口和一致性检查说明。
- `README.md`、`QUICKSTART.md`、`docs/index.md`、`docs/onboarding.md`、`docs/governance/*.md`、`EXPORTING.md`、`UPGRADING.md` 同步补齐多 agent 协作协议入口。
- `README.md`、`QUICKSTART.md`、`docs/governance/*.md` 与 `scripts/check_all.py` 同步补齐 `task-router` skill 入口和检查约束。
- `DEMO.md` 与 `examples/README.md` 同步补齐 `task-entry`、`task-router`、handoff 与 contracts example 在完整演示链路中的位置。
- 两个示例项目各自新增 `docs/tasks/*-task-entry.json` 与 `docs/tasks/*-handoff.md` 实物，并同步更新示例 README、演进总览和 DEMO 链路。
- `scripts/check_all.py`、`README.md` 与 `QUICKSTART.md` 补齐示例闭环资产检查，确保每个示例至少保留一份 `task-entry`、一份 `handoff`，且 `task-entry` 顶层结构仍符合根目录 contract。
- `AGENTS.md`、治理文档、prompt、skill、`README.md`、`QUICKSTART.md` 与 `scripts/check_all.py` 补齐“公开脚本入口需同步维护 `.py / .ps1 / .sh`”的约束，并让 `check_all` 自动检查这些入口是否齐全。
- `README.md` 与 `QUICKSTART.md` 补充 shell 入口的环境前提说明，并明确 `check_all.sh --skip-examples` 可用于只验证统一入口与治理检查。

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
