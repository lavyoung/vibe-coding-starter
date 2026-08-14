---
name: java-transaction-boundary
description: Design, implement, or review Spring transaction boundaries with explicit consistency sets, proxy-safe invocation, and small transactions. Use when changing @Transactional, multi-write workflows, CAS state transitions, compensation, or remote calls near a transaction.
---

# Java 事务边界

保持每个业务事务显式、代理安全且尽量小。不要仅为复用 `@Transactional` 建立继承层级。使用前确认项目实际采用 Spring 事务模型。

## 必读引用

- 决定每个步骤由哪个包承担前，先读 [references/directory-responsibilities.md](references/directory-responsibilities.md)。
- 实现或重构时，同时读 [references/transaction-executor-template.md](references/transaction-executor-template.md)，套用最小的适用模板。
- 改动已确认的事务边界前，读生效业务设计与 `docs/architecture/current-architecture.md`。

## 工作流

1. 识别一致性集合：列出必须一起成功或回滚的状态 CAS、数据库写入、远程调用与最终状态。
2. 识别必须留在事务外的步骤：请求校验、权限/上下文解析、分布式锁获取、响应组装与回滚后收敛通常在外。
3. 验证代理路径：事务公开方法必须经由另一个 Spring Bean 调用；拒绝私有方法注解与同类自调用。
4. 选择最简模式：
   - 整个公开用例恰好是一个短事务、无需外层锁或回滚后编排时，在用例 Service 上标注 `@Transactional`。
   - 编排包围原子核心、多个写入或状态流转需要显式、或失败处理必须在回滚后运行时，用领域 `XxxTransactionExecutor`。
   - 只有短小本地数据库块且编程式边界比另一个 Bean 更清晰时，用 `TransactionTemplate`。
5. 用项目标准异常、租户感知持久化、稳定日志与显式结果对象实现。
6. 验证回滚、CAS 失败、远程失败、最终状态写入失败、代理激活与任何 Seata/XID 要求。
7. 交接前执行 `post-change-check`。

## 强制约束

- 不引入 `AbstractTransactionExecutor`、`BaseTransactionService` 或类似继承层级仅为复用事务注解或 `execute` 方法。
- 分布式锁保持在数据库事务外，除非已接受设计明确要求。
- 事务方法内不得捕获并吞掉必须触发回滚的异常。
- 返回显式 Result；不得通过修改输入 Session、DO、Command、DTO 或上下文对象传递结果。
- 把 `@Transactional` 当本地 Spring 事务边界；未验证目标环境、数据源集成、XID 传播与远程参与者行为前，不宣称分布式一致性。
- 部分成功批量场景每个条目一个独立提交的短事务；不在整个批量外包外层事务或宽分布式锁。
- 远程批量预取与管理员/会员查询移到条目事务外；仅当条目级远程复检关闭已证实的竞态时允许。
- 保留既有路径的原始异常、重试、告警与"继续 vs 中止"语义，除非已接受需求明确改变。
- 不给旧 CAS 路径加新共享服务支持的重试。

## 交付内容

报告：

1. 事务入口与代理调用路径。
2. 事务内外操作。
3. 回滚与回滚后行为。
4. 并发/CAS 与幂等行为。
5. Seata/XID 假设与环境依赖。
6. 已加或缺失的测试。

代码变更同时执行 `safe-code-change` 与 `post-change-check`。
