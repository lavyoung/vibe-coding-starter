# contracts 说明（管跨 agent 共享的结构化输入 / 输出约束，准备做多 agent 协作时先查）

## 文档元数据

- 文档类型：contracts-guide
- 当前状态：已生效
- 适用阶段：任务入口、跨 agent 交接、新会话恢复、自动化校验
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本目录用于把不同 agent 之间最容易口径不一的输入 / 输出，收敛成一组可复用约束，尽量回答：

- 第一个 agent 应该怎样把任务描述交给下一个 agent
- 中途换人、换电脑或新开会话时，怎样减少信息丢失
- 哪些字段属于稳定协作协议，哪些只是自然语言补充

## 2. 当前包含什么

- [task-entry.schema.json](task-entry.schema.json)
  统一任务入口的结构化字段约束
- [handoff-summary.schema.json](handoff-summary.schema.json)
  阶段交接或回合收口的结构化字段约束
- [examples/task-entry.example.json](examples/task-entry.example.json)
  `task-entry` 的最小可用示例
- [examples/handoff-summary.example.json](examples/handoff-summary.example.json)
  `handoff-summary` 的最小可用示例

## 3. 推荐使用方式

1. 新任务开始时，先用 [../prompts/task-entry.txt](../prompts/task-entry.txt) 做自然语言路由。
2. 如果后续需要跨 agent、跨会话或跨人接力，再把结果收敛成 `task-entry.schema.json` 对应结构。
3. 本轮工作收口前，按 [../docs/governance/project-handoff-checklist.md](../docs/governance/project-handoff-checklist.md) 整理信息。
4. 若需要稳定交给其他 agent 继续执行，再输出 `handoff-summary.schema.json` 对应结构。

## 4. 使用约束

- schema 和 example 只描述通用协作字段，不应写入某个团队私有流程。
- 不要把临时任务单、内部背景、隐私信息或本机绝对路径写进 example。
- 若修改 schema，必须同步检查 example、README、治理文档和统一检查脚本。

## 关联代码

- [task-entry.schema.json](task-entry.schema.json)
- [handoff-summary.schema.json](handoff-summary.schema.json)
- [examples/task-entry.example.json](examples/task-entry.example.json)
- [examples/handoff-summary.example.json](examples/handoff-summary.example.json)
