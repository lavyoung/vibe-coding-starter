# 项目演进总览（管当前主线、有效方案和下一步入口，恢复项目上下文时先查）

## 文档元数据

- 文档类型：evolution-index
- 当前状态：已生效
- 适用阶段：持续维护
- 最近更新：YYYY-MM-DD

## 1. 当前主线入口

| 主题 | 当前优先文档 | 说明 |
|---|---|---|
| 全局导航 | [docs/index.md](../index.md) | 文档读取顺序与分层规则 |
| 接手入口 | [docs/onboarding.md](../onboarding.md) | 新人和 AI 新会话恢复上下文 |
| 文档治理 | [docs/governance/document-sync-map.md](../governance/document-sync-map.md) | 查状态闸门、同步矩阵和反向索引 |
| 当前架构基线 | [docs/architecture/current-architecture.md](../architecture/current-architecture.md) | 当前系统分层和边界 |
| UI 交互入口 | [docs/ui/README.md](../ui/README.md) | 项目存在页面 / 弹窗 / 上传交互时启用 |
| 当前需求主线 | `<docs/requirements/...>` | 当前最新需求入口 |
| 当前设计主线 | `<docs/design/...>` | 当前已接受方案入口 |
| 当前任务主线 | `<docs/tasks/...>` | 当前实施拆分入口 |
| 技术提案入口 | [docs/rfcs/README.md](../rfcs/README.md) | 新技术或架构方案先写 RFC |
| 决策沉淀入口 | [docs/explanation/adr/README.md](../explanation/adr/README.md) | 关键决策接受后写 ADR |

## 2. 当前约束口径

- 需求真相：`requirements/`
- 设计真相：已接受且未废弃的 `design/`、`RFC`、`ADR`
- 实现真相：代码
- 升级真相：`upgrade/`、`api/`、`sql/`

## 3. 待持续补齐项

- `docs/rfcs/`
- `docs/explanation/adr/`
- `docs/architecture/current-architecture.md`
- 各业务域的设计和任务入口

## 关联代码

- 无单一业务代码入口；关联系统基线与治理规则见 [docs/architecture/current-architecture.md](../architecture/current-architecture.md)
