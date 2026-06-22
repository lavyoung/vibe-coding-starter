# 当前项目快照（管当前阶段、主线入口和下一步优先级，恢复项目主线时先查）

## 文档元数据

- 文档类型：project-snapshot
- 当前状态：已生效
- 适用阶段：新人接手、AI 新会话、阶段交接、版本推进
- 最近更新：YYYY-MM-DD

> 这是一个“单点快照”模板，用于帮助接手者先用一页文档恢复当前项目主线。
> 将 starter 用于新项目后，优先替换下列占位信息：
> `<PROJECT_NAME>`、`<CURRENT_STAGE>`、`<CURRENT_GOAL>`、`<CORE_CAPABILITIES>`、`<CURRENT_FACTS>`、`<OPEN_ITEMS>`、`<NEXT_STEPS>`。

## 1. 这份文档解决什么问题

本文件用于给人和 AI 一个“单点快照”，尽量先用一页回答这些问题：

- 当前项目现在处于什么阶段
- 当前最重要的入口文档有哪些
- 最近已经做到了什么
- 下一步最应该继续推进什么
- 哪些内容是当前事实，哪些只是待推进事项

## 2. 当前阶段

- 当前项目：`<PROJECT_NAME>`
- 当前阶段：`<CURRENT_STAGE>`
- 当前目标：`<CURRENT_GOAL>`

当前已具备的主能力：

- `<CORE_CAPABILITIES>`

可选示例：

- 已有统一登录与权限体系
- 已有订单主流程接口与任务拆分
- 已有升级脚本和发布检查入口

## 3. 当前优先入口

看完本页后，推荐按这个顺序继续恢复当前主线：

1. [docs/evolution/INDEX.md](INDEX.md)
2. [docs/index.md](../index.md)
3. [docs/onboarding.md](../onboarding.md)
4. [docs/governance/document-sync-map.md](../governance/document-sync-map.md)
5. [docs/governance/ai-collaboration-best-practices.md](../governance/ai-collaboration-best-practices.md)

如果要开始一个新任务，优先再看：

- [prompts/task-entry.txt](../../prompts/task-entry.txt)

如果当前项目已有更具体的领域入口，也补在这里，例如：

- `<docs/requirements/...>`
- `<docs/design/...>`
- `<docs/tasks/...>`

## 4. 当前事实与待推进事项

### 4.1 当前事实

- `<CURRENT_FACTS>`

可选示例：

- 当前版本已完成用户注册、登录和基础资料维护
- 当前接口契约以 `docs/api/` 为准
- 当前升级脚本以 `docs/upgrade/` 和 `docs/sql/` 为准

### 4.2 待推进事项

- `<OPEN_ITEMS>`

可选示例：

1. 待补订单取消设计文档
2. 待补管理员操作审计 upgrade 说明
3. 待收敛支付回调异常路径

## 5. 当前推荐下一步

- `<NEXT_STEPS>`

可选示例：

1. 先补当前版本 requirements / design
2. 再推进对应代码改动
3. 最后补 tasks、upgrade、api 和收口验证

## 6. 维护规则

- 本文件只写“当前高层快照”，不要把细节设计、完整任务拆分或未来规划全堆进来
- 本文件记录的是“当前项目事实与短期主线”，不是 starter 维护计划，也不是长期路线图
- 若当前主线、版本目标、统一入口或维护优先级变化，应同步更新本文件
- 本文件不能替代 `INDEX`、治理文档、requirements、design、tasks；它只负责缩短恢复上下文的第一跳

## 关联代码

- 无单一业务代码；统一任务入口见 [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
