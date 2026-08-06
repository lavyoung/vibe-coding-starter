---
name: safe-code-change
description: Safely change existing behavior while preserving user worktree changes and collecting compatibility evidence. Use when modifying existing code paths, shared components, configuration, scripts, merge resolutions, staging, or commits.
---

# 安全改动既有行为

对既有行为的修改，编译通过不等于兼容。先保留事实与证据，再做最小改动。

## 1. 保护工作区与范围

开始前记录当前分支、HEAD、merge 状态，以及 staged、unstaged、untracked 文件。

- 预先存在的改动属于用户；不得暂存、还原、格式化或混入本次变更。
- 明确本次生产入口、调用链和文件范围；不要把 review 建议扩展为无关清理。
- 提交或交接前再次核对分支与三类工作区状态。

## 2. 建立改前行为基线

对已有路径，先明确并尽可能执行可重复基线：正常结果、拒绝路径、边界、异常、外部调用顺序、写入副作用、事务/并发语义。

- 记录基线的提交、命令、测试和结果。
- 与本次改动一起新增的测试只能证明新回归覆盖；除非它在改前版本执行过，否则不能作为旧行为证据。
- 信息不足时明确缺口，不要把推测写成兼容结论。

## 3. 进行最小且可追踪的改动

- 保持既有错误处理、重试、调用顺序、事务粒度、部分成功语义，除非有效需求或设计明确要求改变。
- 优先复用当前模块边界；只删除由本次改动直接产生的孤儿代码。
- 不为单一调用引入新的公共抽象、包装层或通用框架。

## 4. 改后复核

- 对改前基线执行同一验证，并补充本次需求新增的用例。
- 运行 `git diff --check`，确认无冲突标记。
- 分别报告 staged、unstaged、untracked 文件；不要把用户原有改动算入本次范围。
- 代码或文档变更完成后，继续执行 `post-change-check`。

## 交付证据

说明改动范围、改前与改后验证、未覆盖项，以及是否保留了既有行为。若未能建立基线，明确原因与风险。
