# Agent 协作协议（管 Codex / Claude / 其他 agent 之间怎样稳定交接任务，做多 agent 协作前先查）

## 文档元数据

- 文档类型：agent-collaboration-protocol
- 当前状态：已生效
- 适用阶段：任务入口、跨 agent 交接、新会话恢复、阶段收口
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本文件用于补齐“同一个仓库会被不同 agent 接力”时的最低协作协议，尽量回答：

- 一个任务怎样从自然语言描述收敛成稳定输入
- 一个回合怎样从会话内容收敛成稳定交接
- 换 agent、换人、换电脑后，哪些内容必须仍然能直接继续

## 2. 最小协作协议

### 2.1 任务入口

- 自然语言入口优先使用 [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
- 若仓库已提供 `tools/skills/task-router/`，也可以先用它完成同样的任务路由与文档状态检查
- 若需要把任务稳定交给其他 agent，优先补成 [../../contracts/task-entry.schema.json](../../contracts/task-entry.schema.json) 对应结构
- 可直接参考 [../../contracts/examples/task-entry.example.json](../../contracts/examples/task-entry.example.json)

### 2.2 执行依据

- 权威规则源优先看 [../../AGENTS.md](../../AGENTS.md)
- 若当前 agent 会自动读取 [../../CLAUDE.md](../../CLAUDE.md)，它只作为兼容入口，规则必须与 `AGENTS.md` 一致
- 实现前继续按仓库要求读取 `docs/index.md`、`docs/onboarding.md`、`docs/evolution/INDEX.md` 和 `docs/governance/document-sync-map.md`

### 2.3 回合收口

- 收口时优先按 [project-handoff-checklist.md](project-handoff-checklist.md) 整理已完成、未完成、下一步、风险和验证结果
- 若需要把结果稳定交给其他 agent，优先补成 [../../contracts/handoff-summary.schema.json](../../contracts/handoff-summary.schema.json) 对应结构
- 可直接参考 [../../contracts/examples/handoff-summary.example.json](../../contracts/examples/handoff-summary.example.json)

## 3. 事实源约束

- 协作事实源始终以仓库文档、实际代码和实际 diff 为准，不以会话记忆为准
- `草案`、`评审中`、`已废弃` 文档不能直接作为正式实现依据
- 不要把内部规划、临时任务单、私有背景信息带回公开模板
- 不要把本机绝对路径、团队黑话或只适用于单一公司的流程写进协议示例

## 4. 推荐闭环

```text
自然语言任务说明
  ↓
task-entry 路由
  ↓
文档状态检查 + 复用点检查
  ↓
最小改动实现
  ↓
doc-sync / check_all / 测试
  ↓
handoff-summary 收口
  ↓
findings-first review
```

## 5. 哪些改动需要同步检查本文件

- 修改 `AGENTS.md`、`CLAUDE.md`、`prompts/task-entry.txt` 或交接流程时
- 修改 `tools/skills/task-router/` 时
- 修改 `contracts/*.schema.json` 或 `contracts/examples/*.json` 时
- 修改 `docs/governance/project-handoff-checklist.md`、`docs/governance/ai-collaboration-best-practices.md` 时

## 关联代码

- [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
- [../../tools/skills/task-router/SKILL.md](../../tools/skills/task-router/SKILL.md)
- [../../contracts/task-entry.schema.json](../../contracts/task-entry.schema.json)
- [../../contracts/handoff-summary.schema.json](../../contracts/handoff-summary.schema.json)
- [../../contracts/examples/task-entry.example.json](../../contracts/examples/task-entry.example.json)
- [../../contracts/examples/handoff-summary.example.json](../../contracts/examples/handoff-summary.example.json)
