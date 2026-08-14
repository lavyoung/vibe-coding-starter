---
name: java-async-thread-pool
description: Implement async and concurrent workflows with the project executor model. Use when adding 异步任务, retries, delayed work, status sync, external calls, or distributed-safe concurrency control.
---

# Java 异步与线程池

先复用仓库既有执行器，并把多实例安全作为默认要求。

以项目的统一线程池注册类为准（例如 `CustomExecutors.java` 与 `ThreadPoolProperties`）。

## 先选既有执行器

- 优先复用与业务目的匹配的既有 Bean 执行器（统计、批量、延迟、监控、外部 API、设备命令等）；以项目实际注册清单为准。
- 说明为什么现有执行器都不合适，再新增执行器。

## 安全实现异步

- 新增业务代码不引入 `new Thread()`。
- 不在业务代码里创建临时本地 `ThreadPoolExecutor`。
- 优先 `CompletableFuture.runAsync(...)` / `supplyAsync(...)` 并注入执行器 Bean。
- 长异步编排超过可读范围时拆成小私有方法。

## 尊重事务边界

- 业务正确性依赖已提交状态时，提交后再触发异步工作。
- 事务范围紧扣数据库写入。
- 不用超大事务包住长远程编排。

## 为多实例部署设计

- 不把 JVM 本地锁当作最终并发控制。
- 独占性必须跨实例存活时，优先 Redis、Redisson 或数据库 CAS。
- 不清楚前先说明单节点与多节点假设。

## 确需新增执行器时

- 新增实现 `ThreadPoolProperties` 的属性类。
- 在统一注册类（如 `CustomExecutors`）集中注册 Bean。
- 按业务目的命名，不按单个调用方命名。

## 收尾复核

- 异步代码使用注入的项目执行器。
- 分布式安全没有委托给仅本地的锁。
- 事务边界保持有意图且短小。
- 重试与重复触发下行为可预期。
