# 提示词使用顺序说明（管常见协作场景里 prompts / skills 怎么串，第一次按模板推进任务时先查）

## 文档元数据

- 文档类型：prompt-workflow-guide
- 当前状态：已生效
- 适用阶段：需求分析、设计收敛、实现推进、联调修正、问题修复、交接接手
- 最近更新：YYYY-MM-DD

## 1. 这份文档解决什么问题

这份文档不重复解释每个 prompt 的细节，而是回答另外一类问题：

- 一个任务刚进来，第一句该怎么说
- 新需求、小改动、bug 修复、联调修正分别该走哪条路径
- 上一步的输出，下一步应该怎么接
- 什么时候先补文档，什么时候可以直接落代码

如果你只想知道“有哪些 prompt”，先看 [ai-collaboration-best-practices.md](ai-collaboration-best-practices.md)。
如果你想知道“一个真实任务应该怎么按顺序用”，优先看这份文档。

## 2. 统一入口

默认先从这 2 行开始：

```text
任务目标：
要求：
```

然后先让 agent 按以下任一入口工作：

- [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
- [../../tools/skills/task-router/SKILL.md](../../tools/skills/task-router/SKILL.md)

用户不必先自己判断涉及范围、限制、相关文档和后续路径。
在这套模板里，这部分应由 agent 先补查并明确。

## 3. 统一规则

无论走哪条路径，前 4 步都尽量固定：

1. 先用 `task-entry` 或 `task-router` 判断任务类型
2. 先恢复文档上下文，确认有效文档状态
3. 先找现有可复用实现，再决定是否新增抽象
4. 再进入设计、实现、联调或 review

统一收口也尽量固定：

1. 同步相关文档
2. 运行 `doc-sync` / `check_all` / 必要测试
3. 做 findings-first review
4. 给人工 reviewer 留下重点检查项

## 4. 通用闭环

```text
任务目标 + 要求
  -> task-entry / task-router
  -> 判断任务类型
  -> 恢复现状与有效文档
  -> 找复用点
  -> 进入对应 prompt
  -> 实施或补文档
  -> 文档同步 + 验证
  -> findings-first review
  -> 人工复核
```

## 5. 场景剧本

### 5.1 新需求 / 新能力

适用判断：

- 需要新增能力、流程或模块边界
- 当前仓库还没有已收敛的实现方案
- 需要先把需求和设计写清楚

推荐顺序：

1. `task-entry` 或 `task-router`
2. `new-session` 或 `standard-01-understand-current-state`
3. `design-task`
4. 补 `requirements/`、`design/`、必要时补 `tasks/` 或 `rfcs/`
5. 相关文档达到 `已接受 / 已生效` 后，再进入 `code-change` 或 `standard-02-minimal-implementation`
6. `standard-03-findings-first-review`
7. `standard-04-human-review-focus`

可以直接这样提问：

```text
请先按 task-router 工作，不要直接改代码。
任务目标：新增一个……
要求：先判断需要补哪些需求和设计文档，再给出后续实现顺序。
```

### 5.2 小改动 / 小修复

适用判断：

- 仍在已有功能边界内
- 不需要新开大方案或大范围重构
- 重点是最小改动、复用现有实现

推荐顺序：

1. `task-entry` 或 `task-router`
2. `small-change`
3. 必要时补 `standard-03-findings-first-review`
4. 必要时补 `standard-04-human-review-focus`

可以直接这样提问：

```text
请先按 task-router 工作，不要直接改代码。
任务目标：把现有……
要求：保持最小改动，先判断相关文档、复用点和需要同步更新的内容。
```

### 5.3 Bug 修复

适用判断：

- 已经出现错误、回归或异常行为
- 需要先确认影响范围和根因
- 修复后要重点检查回归风险

推荐顺序：

1. `task-entry` 或 `task-router`
2. `standard-01-understand-current-state`
3. 若属于已有功能内的小修复，走 `small-change`
4. 若涉及多处代码或已有设计边界调整，走 `code-change`
5. `standard-03-findings-first-review`
6. `standard-04-human-review-focus`

可以直接这样提问：

```text
请先按 task-router 工作，不要直接改代码。
任务目标：修复……
要求：先判断影响范围、相关文档和最小修复路径，再开始实施。
```

### 5.4 联调 / 对接修正

适用判断：

- 后端已完成，需要和前端、调用方或外部系统对齐
- 重点在接口契约、字段含义、错误处理、状态流转
- 可能需要同时改实现和文档

推荐顺序：

1. `task-entry` 或 `task-router`
2. `standard-01-understand-current-state`
3. 补查 `docs/api/`、`docs/design/`、必要时补 `docs/ui/`
4. 若只是局部兼容修正，走 `small-change`
5. 若涉及接口行为调整，走 `code-change`
6. 若需要跨 agent 接力，再补看 [agent-collaboration-protocol.md](agent-collaboration-protocol.md)
7. `standard-03-findings-first-review`

可以直接这样提问：

```text
请先按 task-router 工作，不要直接改代码。
任务目标：完成……联调并修正差异。
要求：先核对现有接口文档、实现事实和差异点，再给出最小修正方案。
```

### 5.5 新会话接手 / 换人接手

适用判断：

- 换电脑、换 agent、换协作者
- 当前会话上下文不完整
- 需要先恢复项目事实和当前阶段

推荐顺序：

1. [../../prompts/new-session.txt](../../prompts/new-session.txt)
2. `task-entry` 或 `task-router`
3. `standard-01-understand-current-state`
4. 再进入 `design-task`、`small-change`、`code-change` 或 review 路径

优先阅读：

1. [../index.md](../index.md)
2. [../onboarding.md](../onboarding.md)
3. [../evolution/INDEX.md](../evolution/INDEX.md)
4. [document-sync-map.md](document-sync-map.md)

可以直接这样提问：

```text
这是一个新会话，请先恢复项目上下文，不要直接改代码。
任务目标：继续推进……
要求：先判断当前有效文档、当前阶段、可复用实现和下一步最小动作。
```

## 6. 上一步的输出，下一步怎么接

无论前面走的是哪条路径，下一步最好沿用这些结果，不要每轮都重新问一遍：

- 当前任务类型
- 有效文档列表和状态
- 现有可复用实现
- 本次最小改动边界
- 需要同步的文档
- 计划执行的验证项

如果仓库启用了 `contracts/`，并且你准备把任务再交给其他 agent，可以再把这些结果收敛成结构化交接输入。

## 7. 什么情况下先补文档，不直接落代码

出现下列情况时，优先回到文档：

- 当前依赖文档还是 `草案`、`评审中` 或 `已废弃`
- 任务实际上是新需求，不是小改动
- 联调暴露出接口契约和实现事实不一致
- 这次改动会引入新边界、新公共抽象或新流程

## 关联代码

- [../../prompts/task-entry.txt](../../prompts/task-entry.txt)
- [../../prompts/new-session.txt](../../prompts/new-session.txt)
- [../../prompts/design-task.txt](../../prompts/design-task.txt)
- [../../prompts/code-change.txt](../../prompts/code-change.txt)
- [../../prompts/small-change.txt](../../prompts/small-change.txt)
- [../../prompts/standard-01-understand-current-state.txt](../../prompts/standard-01-understand-current-state.txt)
- [../../prompts/standard-02-minimal-implementation.txt](../../prompts/standard-02-minimal-implementation.txt)
- [../../prompts/standard-03-findings-first-review.txt](../../prompts/standard-03-findings-first-review.txt)
- [../../prompts/standard-04-human-review-focus.txt](../../prompts/standard-04-human-review-focus.txt)
- [../../tools/skills/task-router/SKILL.md](../../tools/skills/task-router/SKILL.md)
