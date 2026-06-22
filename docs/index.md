# docs 总入口（管文档导航与读取顺序，任何人或 AI 接手项目时先查）

## 文档元数据

- 文档类型：documentation-hub
- 当前状态：已生效
- 适用阶段：需求分析、技术设计、实现演进、交接接手
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本文件用于让人和 AI 在缺少会话上下文时，仍能快速判断：

- 当前项目正在演进什么
- 当前哪份文档最值得先看
- 新技术方案应该写到哪里
- 已接受的关键决策在哪里追溯

## 2. 推荐读取顺序

1. 先看 [docs/evolution/INDEX.md](evolution/INDEX.md)
2. 再看 [docs/architecture/current-architecture.md](architecture/current-architecture.md)
3. 再看 [docs/onboarding.md](onboarding.md) 和 [docs/governance/document-sync-map.md](governance/document-sync-map.md)
4. 若需要确认协作方式和会话节奏，再看 [docs/governance/ai-collaboration-best-practices.md](governance/ai-collaboration-best-practices.md)
5. 若涉及页面或交互，再看 [docs/ui/README.md](ui/README.md)
6. 再按业务域跳到 `requirements/`、`design/`、`tasks/`

## 3. 文档分层

| 目录 | 回答的问题 | 什么时候新增 |
|---|---|---|
| `requirements/` | 业务要什么 | 新版本需求、需求变更 |
| `design/` | 业务或模块怎么做 | 已收敛的实现设计 |
| `tasks/` | 做到哪了、还有什么没做 | 任务拆分、阶段推进 |
| `rfcs/` | 准备怎么改、为什么改 | 方案尚未最终拍板 |
| `explanation/adr/` | 为什么最终这么选 | 关键方案已接受 |
| `architecture/` | 当前系统整体长什么样 | 跨域基线变化 |
| `upgrade/` | 上线或升级需要做什么 | 配置、DDL、脚本变化 |
| `api/` / `sql/` | 稳定事实是什么 | 契约和结构事实 |
| `ui/` | 页面、弹窗和交互规则是什么 | 项目存在前端 / 管理端界面时 |
| `governance/` | 文档规则、同步矩阵、状态闸门是什么 | 需要治理和同步时 |
| `governance/ai-collaboration-best-practices.md` | 人类 + AI 协作节奏怎么走 | 需要统一会话与 review 方式时 |
| `evolution/` | 当前演进主线是什么 | 需要维护阶段总览时 |

## 4. 统一状态口径

| 状态 | 含义 |
|---|---|
| `草案` | 已创建，仍在补充 |
| `评审中` | 正在讨论，还未定稿 |
| `已接受` | 方案已拍板，可以作为落代码依据 |
| `已生效` | 治理规则、目录入口、流程规范已正式启用 |
| `已落地` | 方案已实现并同步到相关文档 |
| `已废弃` | 不再作为当前有效方案 |

状态使用约束：

- `草案`、`评审中`：只能用于讨论、评审、补充，不得直接作为落代码依据。
- `已接受`：可以作为设计落代码依据，但仍需继续同步实现结果。
- `已生效`：用于治理入口、目录说明、流程规则类文档。
- `已落地`：表示代码和相关文档已经完成同步。

## 5. AI 协作约束

- AI 在改代码前，优先读取本文件和 [AGENTS.md](../AGENTS.md)
- AI 在恢复上下文或准备改代码前，优先读取 [docs/onboarding.md](onboarding.md) 和 [docs/governance/document-sync-map.md](governance/document-sync-map.md)
- AI 在实现前，先确认现有模块、组件、脚本和文档里是否已有可复用路径，再决定是否新增抽象
- AI 在落代码前，必须先确认相关文档状态已达到 `已接受`、`已生效` 或 `已落地`
- AI 不得把 `草案`、`评审中` 文档当成已实现事实

## 关联代码

- 无直接业务代码；治理规则入口见 [AGENTS.md](../AGENTS.md)
