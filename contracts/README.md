# contracts 说明（可选：管任务入口和交接摘要的固定格式，需要稳定接手时先查）

## 文档元数据

- 文档类型：contracts-guide
- 当前状态：已生效
- 适用阶段：任务开始、阶段交接、新会话接手、自动化校验
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本目录放的是两种固定格式：

- 任务刚开始时，怎样把目标、范围、约束和验证方式写清楚
- 一轮工作结束时，怎样把已完成、未完成、下一步和风险交代清楚

它的作用很简单：减少接手时的信息丢失，让不同人或不同会话看到的任务口径尽量一致。

如果你的项目暂时不需要这类固定格式，可以不启用整个 `contracts/` 目录。

## 2. 当前包含什么

- [task-entry.schema.json](task-entry.schema.json)
  任务入口的字段约束
- [handoff-summary.schema.json](handoff-summary.schema.json)
  交接摘要的字段约束
- [examples/task-entry.example.json](examples/task-entry.example.json)
  `task-entry` 的示例
- [examples/handoff-summary.example.json](examples/handoff-summary.example.json)
  `handoff-summary` 的示例

## 3. 推荐使用方式

1. 新任务开始时，先用自然语言把事情讲清楚。
2. 如果希望后续更容易接手，再按 [task-entry.schema.json](task-entry.schema.json) 补成结构化入口。
3. 一轮工作结束前，先按 [../docs/governance/project-handoff-checklist.md](../docs/governance/project-handoff-checklist.md) 整理收口信息。
4. 如果需要继续交给别人或新会话，再按 [handoff-summary.schema.json](handoff-summary.schema.json) 补成结构化交接摘要。

不想自己从头组织格式时，直接参考：

- [examples/task-entry.example.json](examples/task-entry.example.json)
- [examples/handoff-summary.example.json](examples/handoff-summary.example.json)

## 4. 使用约束

- schema 和 example 只保留通用字段，不要写某个团队私有流程。
- 不要把临时任务单、内部背景、隐私信息或本机绝对路径写进 example。
- 若修改 schema，必须同步检查 example、README、治理文档和统一检查脚本。

## 关联代码

- [task-entry.schema.json](task-entry.schema.json)
- [handoff-summary.schema.json](handoff-summary.schema.json)
- [examples/task-entry.example.json](examples/task-entry.example.json)
- [examples/handoff-summary.example.json](examples/handoff-summary.example.json)
