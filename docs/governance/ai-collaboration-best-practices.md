# AI 使用最佳实践（管人类 + AI 协作的推荐节奏，开始实际需求前先查）

## 文档元数据

- 文档类型：ai-collaboration-guide
- 当前状态：已生效
- 适用阶段：需求分析、实现推进、代码评审、人工复核
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

本文件用于把一套高信号的 AI 协作经验沉淀成可复用方法，回答：

- 一次需求应该怎么开场，才不容易让 AI 直接跑偏
- 什么时候先让 AI 解释现状，什么时候才让它开始实现
- 改完以后，应该怎样让 AI 自审和暴露风险
- 人工 reviewer 最后应该重点看什么

## 2. 总原则

推荐固定采用下面这条闭环：

```text
先用文档恢复上下文
  ↓
再让 AI 解释当前实现与风险
  ↓
再要求最小改动实现
  ↓
再执行 doc-sync / 测试 / 收口检查
  ↓
最后做 findings-first review
  ↓
再告诉人工最值得检查的 3 个地方
```

## 3. 应该保留的好习惯

### 3.1 先解释现状，再改代码

不要一上来就让 AI “直接实现”。先让它说清：

- 当前实现路径
- 影响范围
- 风险点
- 最小改动方案

在本模板里，还要先恢复仓库文档上下文，而不是只读代码。

### 3.2 永远强调最小改动

要求 AI：

- 不顺手重构无关代码
- 保持现有风格
- 优先兼容旧逻辑
- 把改动范围压到当前需求内

### 3.3 先找复用点，再决定怎么实现

要求 AI 在真正动手前，至少先回答：

- 当前仓库里有没有现成模块、组件、脚本、配置或文档可以直接复用
- 这次改动是应该扩展现有边界，还是不得不新增抽象
- 如果要新增公共能力，是否已经有两个以上明确复用点支撑

目标不是“代码写得像新项目”，而是让改动继续贴着当前仓库演进，减少架构腐化、重复实现和边界漂移。

### 3.4 改完后必须 findings-first review

AI 自审时，不要先让它总结优点，优先让它列：

- bug
- 行为回归
- 边界遗漏
- 缺失测试
- 重复实现或不必要抽象

推荐固定顺序：

1. 先查文档状态和实现依据
2. 再看是否优先复用了现有实现、是否引入架构漂移
3. 再看 diff 和高风险路径
4. 最后看测试、验证方式和未覆盖项

### 3.5 再追“证据”而不是只听它说完成

至少追问：

- 哪些测试覆盖了这次改动
- 哪些场景还没覆盖
- 哪些地方它不确定
- 哪几个文件最值得人工 review
- 它复用了哪些现有实现，或者为什么没有复用

### 3.6 结束前补一份可交接摘要

如果这轮工作不会在当前会话里完全结束，建议在收口时固定补一份 handoff 摘要，至少写清：

- 已完成
- 未完成
- 下一步
- 风险与未验证项
- 本轮改了哪些代码和文档

推荐直接参考：

- [project-handoff-checklist.md](project-handoff-checklist.md)
- [agent-collaboration-protocol.md](agent-collaboration-protocol.md)

## 4. 在 docs-first 仓库里的额外要求

如果仓库采用本 starter，不要照搬“只读代码”的流程，还要加上：

- 先读 `AGENTS.md`
- 若当前 agent 会自动读取 `CLAUDE.md`，同步确认它与 `AGENTS.md` 一致
- 先读 `docs/index.md`
- 先读 `docs/evolution/INDEX.md`
- 先读 `docs/governance/document-sync-map.md`
- 先确认相关文档状态是否为 `已接受 / 已生效 / 已落地`
- 先确认这次实现是否能复用已有模块、组件、脚本或约束

如果仓库启用了 `.doc-sync.json` 和 `scripts/doc_sync_check.py`，收尾时还要跑一轮 `doc-sync`。

如果这轮改动命中了公开脚本入口，也要同步回查：

- 对应的 `scripts/*.ps1`
- 对应的 `scripts/*.sh`
- 文档中的命令示例是否仍然可用

如果仓库已经维护了 `docs/evolution/current-snapshot.md` 和 `docs/governance/project-handoff-checklist.md`，收尾时还应确认：

- 当前阶段快照是否仍然准确
- 本轮是否需要补一份 handoff 摘要

如果是在 PR 或提交前做 review，建议同时在 PR 模板里写清：

- 本次改动依据了哪些文档
- 这些文档当前状态
- 哪些文档已同步更新
- 哪些验证已经跑过

## 5. 推荐的统一入口和标准会话提示词

对应文件见：

1. [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
2. [prompt-workflow-playbook.md](prompt-workflow-playbook.md)
3. [agent-collaboration-protocol.md](agent-collaboration-protocol.md)
4. [../../prompts/standard-01-understand-current-state.txt](../../prompts/standard-01-understand-current-state.txt)
5. [../../prompts/standard-02-minimal-implementation.txt](../../prompts/standard-02-minimal-implementation.txt)
6. [../../prompts/standard-03-findings-first-review.txt](../../prompts/standard-03-findings-first-review.txt)
7. [../../prompts/standard-04-human-review-focus.txt](../../prompts/standard-04-human-review-focus.txt)

推荐使用顺序：

1. 先用 `task-entry` 判断任务类型和后续路径
2. 若仓库已提供 `task-router` skill，也可以先用它做同样的路由动作
3. 若信息还不够，先理解现状
4. 再最小改动实现或进入设计流程
5. 再 findings-first review
6. 最后聚焦人工检查点

如果你想降低第一次使用门槛，推荐直接让用户先给这 2 行：

```text
任务目标：
要求：
```

只要先把这 2 行说清楚，`task-entry` / `task-router` 就应该先去补查范围、限制和相关文档，不必要求用户一开始就写完整任务单。

如果你更关心“新需求、小改动、bug 修复、联调、新会话接手分别该怎么串 prompt”，再看：

- [prompt-workflow-playbook.md](prompt-workflow-playbook.md)

## 6. 前端 / UI 场景补充

如果需求涉及页面、管理端或控制台：

- 先补查 `docs/ui/`
- 明确让 AI 关注 `loading / empty / error / success`
- 必要时结合浏览器验证页面行为

## 关联代码

- [../../prompts/new-session.txt](../../prompts/new-session.txt)
- [../../prompts/design-task.txt](../../prompts/design-task.txt)
- [../../prompts/code-change.txt](../../prompts/code-change.txt)
- [../../prompts/small-change.txt](../../prompts/small-change.txt)
- [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
- [../../prompts/standard-01-understand-current-state.txt](../../prompts/standard-01-understand-current-state.txt)
- [../../prompts/standard-02-minimal-implementation.txt](../../prompts/standard-02-minimal-implementation.txt)
- [../../prompts/standard-03-findings-first-review.txt](../../prompts/standard-03-findings-first-review.txt)
- [../../prompts/standard-04-human-review-focus.txt](../../prompts/standard-04-human-review-focus.txt)
