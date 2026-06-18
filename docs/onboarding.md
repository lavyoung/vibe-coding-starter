# 项目接手与新会话开场指南（管新人接手、AI 新会话恢复上下文，开始工作前先查）

## 文档元数据

- 文档类型：onboarding-guide
- 当前状态：已生效
- 适用阶段：新人接手、AI 新会话、需求澄清前
- 最近更新：YYYY-MM-DD

## 1. 标准接手顺序

1. [AGENTS.md](../AGENTS.md)
2. [docs/index.md](index.md)
3. [docs/evolution/INDEX.md](evolution/INDEX.md)
4. [docs/governance/document-sync-map.md](governance/document-sync-map.md)
5. 与当前任务最相关的 `requirements / design / tasks / upgrade / api` 文档

## 2. 项目文档工作流

```text
收到需求
  ↓
先找 requirements
  ↓
判断是否需要新增 design / RFC / tasks
  ↓
先落文档，再推进实现
  ↓
改代码时按同步矩阵回查受影响文档
  ↓
改完代码再补文档收口
```

## 3. 三条硬规则

1. 不要把草案文档写成已实现事实。
2. 不要在相关文档仍是 `草案`、`评审中` 时直接落代码。
3. 不要只看会话上下文，必须回到 `docs/` 和 `AGENTS.md` 恢复事实。

## 4. 给 AI 的开场提示词

开场提示词统一见：

- [prompts/new-session.txt](../prompts/new-session.txt)
- [prompts/design-task.txt](../prompts/design-task.txt)
- [prompts/code-change.txt](../prompts/code-change.txt)

## 关联代码

- 无直接业务代码；治理规则入口见 [AGENTS.md](../AGENTS.md)
