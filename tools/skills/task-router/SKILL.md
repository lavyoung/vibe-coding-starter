---
name: task-router
description: 在 docs-first 仓库里先做任务分流与入口判断。适用于需要先判断当前请求属于新需求、设计收敛、代码改动、小修复、升级发布、文档维护还是 findings-first review，再决定该读哪些文档、优先复用哪些现有实现、后续进入哪个 prompt 或协作协议的场景。
---

# 任务路由

## 说明

当一个请求还没有明确进入“设计 / 实现 / review / 升级”哪条路径时，先用这个 skill。

目标不是直接开始写代码，而是先把任务归类、确认文档依据、识别复用点，再决定下一步入口。

## 最简用法

用户哪怕只给下面 2 行信息，也足够先进入路由：

- 任务目标
- 要求

如果信息不全，不要卡住；先按现有目标补查范围、限制和相关文档，再完成最小路由判断。

## 工作流

### 1. 先恢复仓库上下文

优先按下面顺序读取：

1. `AGENTS.md`
2. `docs/index.md`
3. `docs/onboarding.md`
4. `docs/evolution/INDEX.md`
5. `docs/governance/document-sync-map.md`
6. `docs/governance/ai-collaboration-best-practices.md`
7. 若仓库已启用多 agent 协作协议，再看 `docs/governance/agent-collaboration-protocol.md`

不要只根据会话内容做路由判断。

### 2. 先判断任务类型

至少先归到下面一类：

- 新需求 / 新能力
- 设计收敛 / 提案
- 已有功能代码改动
- 小改动 / 小修复
- 升级 / 发布 / SQL / 配置同步
- 文档维护
- findings-first review

如果无法判断，就先归为“信息不足”，转去理解现状。

优先使用最接近用户原话的分类，不要为了“分类完整”硬凑复杂结论。

### 3. 先检查文档状态

- 只有 `已接受`、`已生效`、`已落地` 的文档，才能作为正式实现依据
- `草案`、`评审中`、`已废弃` 只能用于讨论、评审和补充上下文
- 如果任务需要新设计，但当前没有有效文档，先补文档，不要直接进入实现

### 4. 先找复用点

在真正推进前，至少确认：

- 当前模块、相邻模块、脚本、prompt、skill 或文档里是否已有可直接复用路径
- 这次是扩展现有边界，还是确实需要新增抽象
- 如果要新增公共能力，是否已经有明确复用场景支撑

### 5. 再决定进入哪条后续路径

优先按下面规则路由：

- 新需求 / 新能力：`prompts/design-task.txt`
- 已有功能代码改动：`prompts/code-change.txt`
- 小改动 / 小修复：`prompts/small-change.txt`
- findings-first review：`prompts/standard-03-findings-first-review.txt`
- 人工复核重点：`prompts/standard-04-human-review-focus.txt`
- 如果当前信息仍不足：`prompts/standard-01-understand-current-state.txt`

如果仓库已经维护了统一任务入口 prompt，也可以直接对照：

- `prompts/task-entry.txt`

### 6. 若需要跨 agent 接力，再补结构化协议

如果仓库启用了 `contracts/`，且任务后续需要交给其他 agent 或新会话继续推进，再把结果收敛成：

- `contracts/task-entry.schema.json`
- `contracts/examples/task-entry.example.json`

任务收口时优先对照：

- `docs/governance/project-handoff-checklist.md`
- `contracts/handoff-summary.schema.json`
- `contracts/examples/handoff-summary.example.json`

## 输出要求

开始实施前，至少先输出下面 6 项；有更多信息时再补完整：

1. 你理解的当前任务
2. 你判断的任务类型
3. 推荐进入的后续路径，以及为什么
4. 本次应优先读取的文档
5. 当前有哪些可优先复用的代码、脚本、组件、prompt 或 skill
6. 当前缺少哪些关键信息

如果信息已经足够，再继续补：

7. 这些文档的当前状态
8. 哪些文档可以作为有效依据
9. 本次后续大概率需要同步哪些文档
10. 建议的验证方式

确认完这些信息后，再进入实现、设计、review 或升级流程。
