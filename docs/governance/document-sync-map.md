# 文档清单与同步矩阵（管 docs 总索引、代码和文档的同步关系，改代码或写文档前先查）

## 文档元数据

- 文档类型：governance-map
- 当前状态：已生效
- 适用阶段：需求分析、技术设计、代码实现、文档维护、代码评审
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本文件承载三类信息：

1. `docs/` 下哪些文档是当前有效入口
2. 改某段代码时，必须同步哪些文档
3. 写某份文档时，必须先核对哪些代码

## 1.1 仓库内链接规范

- 仓库内文档指向仓库文件时，必须使用相对路径。
- 文档里引用代码位置时，优先写“仓库相对路径 + 类名 / 方法名 / 章节号”。
- 只有在描述本地环境配置时，才允许出现机器相关路径。

## 1.2 文档状态生效规则

- 设计类、RFC、ADR、治理类文档，只有在状态为 `已接受`、`已生效` 或 `已落地` 时，才属于当前有效文档。
- `草案`、`评审中` 文档只能用于讨论、评审、补充上下文，不能直接作为落代码、联调、上线、对外说明的依据。
- 改代码前，必须先核对本次依赖文档的状态；若状态未生效，先推进文档收敛，再推进实现。

## 1.3 自动化补充口径

- `docs/governance/document-sync-map.md` 仍是人工可读的主矩阵
- `.doc-sync.json` 是机器可校验的补充规则文件
- `scripts/doc_sync_check.py` 用于在本地和 CI 中检查“代码改了但文档没跟上”的问题
- 若仓库已启用 `.github/workflows/doc-sync.yml`，PR 默认应通过这条统一 CI 校验，其中包含 `doc-sync`、链接检查和示例自检
- 若修改 `AGENTS.md`、`CLAUDE.md`、`prompts/`、`tools/skills/`、PR 模板里的协作规则，需同步检查本文件和 `docs/governance/ai-collaboration-best-practices.md` 是否仍然一致
- 若仓库已启用 `docs/evolution/current-snapshot.md`、`docs/governance/project-handoff-checklist.md` 与 `contracts/*.schema.json`，修改统一入口、治理规则或交接流程时，也应回查这些资产是否仍然成立
- 若仓库已启用 `docs/governance/agent-collaboration-protocol.md` 与 `contracts/examples/*.json`，修改多 agent 协作口径时，也应同步检查协议文档和示例是否仍然成立
- 若仓库已启用 `tools/skills/task-router/`，修改统一入口、路由规则或多 agent 协作入口时，也应同步检查该 skill 是否仍然成立

## 2. 文档清单模板

| 文档路径 | 职责 | 何时查阅 |
|---|---|---|
| `docs/index.md` | 文档统一入口 | 接手项目、准备新增文档时 |
| `docs/onboarding.md` | 新人和新会话接手指南 | 新成员接手、AI 新会话 |
| `docs/evolution/current-snapshot.md` | 当前阶段单点快照 | 新人接手、AI 新会话、阶段交接 |
| `docs/evolution/INDEX.md` | 当前项目演进总览 | 恢复当前主线时 |
| `docs/architecture/current-architecture.md` | 当前系统整体架构基线 | 做跨域设计时 |
| `docs/governance/ai-collaboration-best-practices.md` | AI 协作节奏与标准提示词 | 统一会话方式和 review 节奏时 |
| `docs/governance/agent-collaboration-protocol.md` | 多 agent 输入 / 输出协作协议 | 跨 agent 接力、结构化交接、新会话续做 |
| `docs/governance/project-handoff-checklist.md` | 阶段交接和回合收口模板 | 跨人接力、AI 新会话、提交前收口时 |
| `docs/rfcs/README.md` / `RFC_TEMPLATE.md` | 提案规则与模板 | 新技术方案设计时 |
| `docs/explanation/adr/README.md` / `ADR_TEMPLATE.md` | 决策记录规则与模板 | 方案已接受时 |
| `docs/ui/README.md` / `page-map.md` / `interaction-patterns.md` / `screens/*.md` | 页面、弹窗和交互事实源 | 项目存在前端 / 管理端界面时 |
| `<docs/design/...>` | 已接受的领域设计 | 改对应领域代码时 |
| `<docs/tasks/...>` | 领域任务拆分和进度 | 实施推进和交接时 |
| `<docs/upgrade/...>` | 升级说明和脚本 | 上线和发布时 |
| `<docs/api/...>` | 对外接口契约 | 联调和对接时 |
| `<docs/sql/...>` | 表结构和 SQL 脚本 | 排查表结构和升级时 |

## 3. 代码 -> 文档同步矩阵模板

改代码前先补齐并维护下表。

| 代码模块 | 必须同步的文档 | 同步动作 |
|---|---|---|
| `<controller/...>` | `<docs/api/...>` + `<docs/design/...>` | 新增 / 修改 / 废弃端点同步契约和设计 |
| `<service/...>` | `<docs/design/...>` + `<docs/tasks/...>` | 重大逻辑变化同步设计和任务状态 |
| `<dataobject / entity / schema>` | `<docs/sql/...>` + `<docs/upgrade/...>` + `<docs/design/...>` | 字段 / 索引 / DDL / 升级说明同步 |
| `<config / properties / env>` | `<docs/upgrade/...>` + `<docs/architecture/...>` | 配置项和基线变化同步 |
| `<job / worker / scheduler>` | `<docs/upgrade/...>` + `<docs/design/...>` | 任务入口和执行约束同步 |
| `<frontend/pages / routes / views>` | `<docs/ui/screens/...>` + `<docs/ui/page-map.md>` + `<docs/design/...>` | 页面结构、交互规则、导航入口同步 |
| `<frontend/components / hooks>` | `<docs/ui/interaction-patterns.md>` + `<docs/ui/screens/...>` | 通用交互和单页特例同步 |
| 跨域架构调整 | `docs/architecture/current-architecture.md` + `docs/rfcs/*.md` / `docs/explanation/adr/*.md` | 先更新架构基线，再补提案或决策 |

## 4. 文档 -> 代码反向索引模板

| 文档 | 必须先确认的代码 | 不允许凭空写 |
|---|---|---|
| `<docs/design/...>` | 先 grep 代码现状，再写 | 禁止写“将来会做但代码没有”的内容 |
| `<docs/api/...>` | 必须基于当前接口生成 | 禁止保留无效路径 |
| `<docs/sql/...>` | 必须与实体 / DO / schema 一致 | 禁止写不存在的字段 |
| `<docs/upgrade/...>` | 必须基于当前代码和脚本生成 | 禁止把未落地能力写成已完成 |
| `<docs/ui/screens/...>` | 必须先确认当前页面、组件、接口约束 | 禁止把草图或未实现交互写成现状 |
| `<docs/ui/interaction-patterns.md>` | 必须先确认通用组件和现有交互 | 禁止把单页特例误写成全局规则 |
| `docs/architecture/current-architecture.md` | 必须基于实际模块、依赖和分层生成 | 禁止凭空描述系统边界 |

## 5. 文档同步工作流

```text
改代码
  ↓
[1] 先确认关联文档状态是否为 已接受 / 已生效 / 已落地
  ↓
[2] 查“代码 -> 文档同步矩阵”
  ↓
[3] 逐个打开对应文档，按需修改
  ↓
[4] 在提交说明或 PR 模板里写清：改了哪些代码、改了哪些文档、文档状态、哪些未验证
```

## 6. 新增文档的硬性要求

1. 第一行注明职责：`# 文档名（管什么、什么时候查）`
2. 文档元数据至少包含：文档类型、当前状态、适用阶段、最近更新
3. 末尾必须有“关联代码”章节
4. 需求、设计、升级类技术方案文档必须有版本号和状态
5. `docs/index.md`、`docs/README.md`、本文件三处入口关系必须同步更新

## 关联代码

- 无单一业务代码；本文件用于约束项目所有关键代码与文档的同步关系
