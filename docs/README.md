# docs 目录说明（管 `docs/` 目录组织规则，新增或重构文档目录时先查）

## 文档元数据

- 文档类型：docs-directory-guide
- 当前状态：已生效
- 适用阶段：文档维护、目录调整、AI 接手项目
- 最近更新：2026-08-14

`docs/` 目录统一按“文档类型 + 业务域”组织，避免不同类型文档混放。

## 统一入口

- 人类与 AI 的统一入口是 [docs/index.md](index.md)
- 项目差异化事实入口是 [docs/project-profile.md](project-profile.md)
- 当前阶段单点快照入口是 [docs/evolution/current-snapshot.md](evolution/current-snapshot.md)
- 当前阶段主线入口是 [docs/evolution/INDEX.md](evolution/INDEX.md)
- 若当前 agent 会自动读取根目录 `CLAUDE.md`，也要与 `AGENTS.md` 保持同口径
- 若需要按真实任务场景确定 prompts 使用顺序，再看 [governance/prompt-workflow-playbook.md](governance/prompt-workflow-playbook.md)
- 若需要跨 agent 结构化交接，再看 [governance/agent-collaboration-protocol.md](governance/agent-collaboration-protocol.md)

## 目标结构

```text
docs/
├── index.md
├── project-profile.md
├── onboarding.md
├── evolution/
├── governance/
├── architecture/
├── rfcs/
├── explanation/
│   └── adr/
├── requirements/
│   └── v1.1.1/          (版本目录，之下才是真正的文件)
├── design/
│   └── v1.1.1/
├── tasks/
│   └── v1.1.1/
├── upgrade/
│   └── v1.1.1/
├── api/
│   ├── v1.1.1/          (契约本体按版本目录存放)
│   └── README.md
├── sql/
│   └── v1.1.1/
├── ui/                (可选)
└── README.md
```

## 分类规则

- `requirements/`：业务要什么
- `design/`：准备怎么做
- `tasks/`：怎么拆、做到哪
- `rfcs/`：方案未拍板前的提案
- `explanation/adr/`：已接受的关键决策
- `architecture/`：系统整体基线
- `upgrade/`：上线和升级要同步什么
- `api/`：对外接口契约（可导入 OpenAPI YAML，随设计文档生成；md 不再作为默认契约输出）
- `sql/`：表结构和脚本
- `ui/`：页面、弹窗、上传和交互事实源；仅在项目存在稳定界面时启用
- `governance/`：文档治理规则、同步矩阵、状态闸门
- `governance/ai-collaboration-best-practices.md`：推荐的人类 + AI 协作节奏与标准会话提示词
- `governance/prompt-workflow-playbook.md`：按真实场景组织的提示词使用顺序说明
- `governance/agent-collaboration-protocol.md`：多 agent 之间共享任务入口与交接摘要时的最小协作协议
- `evolution/`：当前主线入口与单点快照

## 版本演进约束

文档元数据虽然带有"版本"字段，但目录组织也必须按版本演进：

- **交付物型目录**（`requirements/`、`design/`、`tasks/`、`upgrade/`、`api/`、`sql/`）必须先在分类目录下创建版本目录 `vX.Y.Z/`（语义化版本，如 `v1.1.1`），**版本目录之下才是真正的文件**；禁止把版本交付物直接散落在分类目录根。
- 版本目录名与文档元数据的"版本"字段保持一致；新版本开始演进时新建版本目录，同一版本内的修订原地更新，不重复建目录。
- 版本目录内再按业务域组织：如 `docs/design/v1.1.1/<domain>/`、`docs/tasks/v1.1.1/<domain>/`；单文件可直接放版本目录内。
- 分类目录根只保留目录职责说明（`README.md`）与跨版本模板（如 `DESIGN_TEMPLATE.md`、`TASK_TEMPLATE.md`），不放任何版本交付物。
- **事实源型目录**（`architecture/`、`governance/`、`rfcs/`、`explanation/adr/`、`evolution/`、`ui/` 的全局规则文件）不按版本目录组织，持续根级演进；`ui/screens/` 按页面组织。
- 改代码时以"当前有效版本目录"为准：最新版本目录是当前契约与设计的事实源，历史版本目录仅作追溯。
- `api/` 契约的版本策略：契约版本目录与设计版本一致；已发布的版本目录保持冻结（仅修复性修订可原地更新并升 patch 版本），破坏性变更必须开新版本目录，并在 `docs/upgrade/vX.Y.Z/` 补迁移说明。

## 关联代码

- 无直接业务代码；治理规则入口见 [AGENTS.md](../AGENTS.md) 与 [CLAUDE.md](../CLAUDE.md)
