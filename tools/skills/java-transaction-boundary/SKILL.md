---
name: java-transaction-boundary
description: Design, implement, or review Spring transaction boundaries with explicit consistency sets, proxy-safe invocation, and small transactions. Use when changing @Transactional, multi-write workflows, CAS state transitions, compensation, or remote calls near a transaction.
---

# Java 事务边界

使用前先阅读 [目录职责参考](references/directory-responsibilities.md) 与 [事务执行器模板](references/transaction-executor-template.md)，并确认项目实际采用 Spring 事务模型。

## 工作流

1. 列出一致性集合：状态 CAS、数据库写入、必要的远程参与者与最终状态。
2. 明确事务外步骤：输入校验、身份/权限、分布式锁获取、响应组装、失败后的补偿或收敛通常应在事务外。
3. 验证代理调用路径；`@Transactional` 的公开方法必须经由 Spring Bean 调用，禁止依赖私有方法或自调用注解。
4. 选择最简单模式：整个用例恰好是一个短事务时可在服务方法上标注；编排包围原子写入或需回滚后处理时，使用独立事务执行器；仅在边界更清晰时使用已有 `TransactionTemplate`。
5. 验证回滚、CAS 失败、远程失败、最终状态写入失败，以及幂等与并发假设。

## 强制约束

- 不要仅为复用 `@Transactional` 或 `execute` 方法建立抽象基类。
- 不要把长时间远程调用、批处理循环或宽范围锁放入一个事务。
- 事务内不得吞掉必须触发回滚的异常。
- 用显式 Result 返回事务结果；不要通过修改输入 DTO、DO 或上下文对象传递隐式结果。
- 分布式锁通常应在数据库事务外获取；若项目另有设计，以已接受设计为准。
- 不得把本地 `@Transactional` 宣称为分布式一致性；须验证数据源、参与者和上下文传播。

## 交付内容

报告事务入口和代理路径、事务内外操作、回滚与补偿、CAS/幂等假设及实际测试。代码变更同时执行 `safe-code-change` 与 `post-change-check`。
