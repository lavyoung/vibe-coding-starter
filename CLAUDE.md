# <PROJECT_NAME> Claude 协作入口

> 本文件可按需保留。
> 本文件提供给会自动读取 `CLAUDE.md` 的 agent 使用。
> 本项目的权威协作规则仍以同目录下的 [AGENTS.md](AGENTS.md) 为准。
> 若修改协作规则、文档入口或收尾流程，必须同步检查 `CLAUDE.md` 与 `AGENTS.md` 是否仍然一致。

## 0. 开始前先做什么

1. 先扫描 [`tools/skills`](tools/skills/)。
2. 先读 [AGENTS.md](AGENTS.md)。
3. 再按顺序读：
   - [docs/index.md](docs/index.md)
   - [docs/onboarding.md](docs/onboarding.md)
   - [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
   - [docs/governance/document-sync-map.md](docs/governance/document-sync-map.md)
4. 只有 `已接受`、`已生效`、`已落地` 的文档，才能作为实现依据。
5. 动手前先确认当前模块、相邻模块、脚本、组件和文档里是否已有可复用路径。

## 1. 项目事实

- 项目名称：`<PROJECT_NAME>`
- 技术栈：`<TECH_STACK>`
- 主模块：`<MAIN_MODULES>`
- 主要业务域：`<BUSINESS_DOMAINS>`
- 构建命令：`<BUILD_COMMAND>`
- 测试命令：`<TEST_COMMAND>`
- 编码约定：统一使用 UTF-8

## 2. 必须遵守的协作约束

- 优先最小改动，不做顺手重构。
- 先匹配当前代码风格，再补能力。
- 先复用现有实现，再决定是否新增抽象。
- 不要把草案、评审中或已废弃文档写成已实现事实。
- 涉及跨模块边界、接口契约、表结构、配置、异步模型时，先回查文档。

## 3. 收尾要求

1. 做一轮文档同步检查。
2. 做一轮状态闸门检查。
3. 若仓库存在 `.doc-sync.json` 与 `scripts/doc_sync_check.py`，先运行一轮 `doc-sync`。
4. 运行构建、测试或仓库已有统一检查脚本。
5. 明确说明未验证项、剩余风险和下一步建议。

## 4. 常用入口

- 统一任务入口：[prompts/task-entry.txt](prompts/task-entry.txt)
- 当前阶段快照：[docs/evolution/current-snapshot.md](docs/evolution/current-snapshot.md)
- 交接模板：[docs/governance/project-handoff-checklist.md](docs/governance/project-handoff-checklist.md)
- 结构化输入 / 输出约束：
  - [contracts/task-entry.schema.json](contracts/task-entry.schema.json)
  - [contracts/handoff-summary.schema.json](contracts/handoff-summary.schema.json)
