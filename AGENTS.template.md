# <PROJECT_NAME> 项目专属约束模板

## 0. Skill 扫描规则

### 0.1 执行顺序

在处理本项目任何实现、修改、测试、评审类任务前，先扫描 [`tools/skills`](tools/skills/)。

### 0.2 约束

- 若存在与当前任务匹配的 skill，优先读取对应 `SKILL.md`，并按其中约束执行。
- 若多个 skill 同时匹配，按“最小覆盖原则”选择必要 skill 组合。
- 若当前任务与已有 skill 均不匹配，再回退到本 `AGENTS.md` 与全局规则继续执行。

## 1. 项目事实

- 项目名称：`<PROJECT_NAME>`
- 技术栈：`<TECH_STACK>`
- 主模块：`<MAIN_MODULES>`
- 主要业务域：`<BUSINESS_DOMAINS>`
- 构建命令：`<BUILD_COMMAND>`
- 测试命令：`<TEST_COMMAND>`
- 编码约定：统一使用 UTF-8

## 2. 代码实现约束

- 优先最小改动，不做顺手重构。
- 先匹配当前代码风格，再补能力。
- 若需求不明确，先显式说明假设。
- 不要把“待讨论方案”直接写进实现。
- 涉及跨模块边界、接口契约、表结构、配置、异步模型时，先回查文档。

## 3. 文档状态闸门

- 只有 `已接受`、`已生效`、`已落地` 的文档，才能作为落代码依据。
- `草案`、`评审中`、`已废弃` 文档只能用于讨论、补充上下文、辅助评审。
- 若当前依赖文档状态不足，先推进文档收敛，再推进实现。

## 4. 文档入口

改代码或写文档前，优先读取：

1. [docs/index.md](docs/index.md)
2. [docs/onboarding.md](docs/onboarding.md)
3. [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
4. [docs/governance/document-sync-map.md](docs/governance/document-sync-map.md)

## 5. 代码 -> 文档同步要求

- 改代码前，必须先查 `docs/governance/document-sync-map.md` 的“代码 -> 文档同步矩阵”。
- 若本次改动命中矩阵中的模块，必须同步对应文档。
- 若本次改动虽然未命中矩阵，但显然改变了需求、设计、接口、表结构、配置、任务状态，也必须主动补文档。

## 6. 文档 -> 代码校验要求

- 写文档前，必须先查 `docs/governance/document-sync-map.md` 的“文档 -> 代码反向索引”。
- 禁止把草案写成已实现事实。
- 禁止把不存在的代码、接口、配置、线程模型、表字段写成现状。

## 7. 推荐关闭动作

结束一次实现前，至少补一轮：

1. 文档同步检查
2. 状态闸门检查
3. 编译 / 测试 / 构建验证
4. 未验证项说明
