---
name: java-unit-test-designer
description: Design Java unit test coverage before implementation. Use when planning tests for new methods, filling coverage gaps, reproducing bugs, defining refactor safety nets, or deciding which JUnit 5 techniques fit a method's complexity.
---

# Java 单元测试设计

有意图地设计覆盖率，而不是只写一条快乐路径测试。

## 先给方法复杂度分级

- `Quick`：逻辑简单、分支少。
- `Standard`：分支、校验或状态变化中等。
- `Complete`：复杂规则组合、工作流或多步状态流转。

## 按形状选择测试方法

- 输入校验与合法/非法输入用等价类。
- 范围、长度、数量与日期用边界值分析。
- 工作流与状态流转用场景化测试。
- 密集条件组合用决策表思维。
- 历史上脆弱或易漏的用例用错误猜测。

## 覆盖不止快乐路径

- 至少一条正常路径。
- 非法输入与 sad path 用例。
- 数字、数量或长度敏感时包含边界值。
- 方法抛出或映射失败时包含异常行为。
- 修复 bug 时先加回归复现。

## 有目的地推荐 JUnit 5 特性

- 每个测试用 `@DisplayName` 写可读中文目标。
- 方法有多个流程或状态时用 `@Nested`。
- 一个场景需要多个相关断言时用 `assertAll`。
- 异常类型、错误码与消息检查用 `assertThrows`。
- 有助于执行策略时用 `@Tag` 区分 core、slow、external-dependency。
- 测试可能挂起或阻塞时用 `@Timeout`。

## 产出覆盖率方案

- 说明被测方法及其职责。
- 说明所选复杂度级别与原因。
- 列出将应用的测试设计方法。
- 列出要覆盖的具体场景。
- 指出无法低成本覆盖的残余风险。

## 先选测试层

- **Unit**（Mockito + JUnit 5）：方法逻辑、状态机、决策、转换。
- **Contract**：XML statement id、SQL 关键字、路由路径、HTTP 方法、枚举稳定性——用反射或原始 XML/资源字符串断言。
- **Integration**（真实 MyBatis + 内存 H2）：真实 SQL 聚合正确性。
- 统计/聚合的正确性必须住在集成测试；单元 mock 只验证编排，永远不验证聚合。

## Mock 纪律

- 重构改变内部调用时，更新 mock/verify 到新契约，但业务断言保持不变。
- Mockito 默认不运行接口 `default` 方法的真实体：stub `default` 方法本身，而不是它内部调用的方法。
- 在降级所在层测试降级：兜底逻辑移入共享组件后，在消费方断言兜底结果，在该组件内测兜底本身。
- 否定断言用 `verifyNoInteractions`（权限拒绝/非法输入不得触达读模型或外部服务）。
- 公共 stub（如 i18n 消息工具）用 `lenient().when(...)`，避免每个用例都触发未用 stub 报错。

## 覆盖不止四个维度

至少：快乐路径、边界值、sad path/带稳定码的异常、空/null 输入。

- 默认值 + 上下越界（如 `null -> 5`、`0`/`101 -> error`）。
- 范围或成对输入规则的每个端点（如日期对只给 start 与只给 end）。
- 断言错误用 `error.getCode()`，永远不用消息字符串。

## 聚合/统计专项检查

- 空结果语义：无行的 `SELECT COUNT(*) ...` 返回**一行零值**，不是 null——断言零聚合，不是 null。
- 半开区间：在 `endExclusive` 恰好插入事实并断言被排除。
- 同日多重性：断言同日多条事实合并为一行且计数求和。
- 极值：验证 `SUM` over `long` 对超出 `int` 范围的值不溢出。
- 隔离：包含“其他租户”与“逻辑删除”行并断言被排除。
- 稳定排序：构造平局并断言决胜键与 `LIMIT` 上限。
- 独立事实时间：趋势聚合分别按注册时间与首单时间聚合；两列都验证。

## 测试数据构造

- 用参数化助手方法（如 `insertRecord(...)`）建行并减少重复。
- 每个用例在 `@BeforeEach` 重置数据（DELETE + INSERT）保证隔离。
- 拼接 SQL 时时间值加引号但 `NULL` 不加：`"NULL".equals(x) ? "NULL" : "'" + x + "'"`。

## 重构进共享协作者时迁移行为测试

重复逻辑（如租户循环、Redis 限流）从 Job/Service 移入共享 support 类时，测试必须迁移到现在拥有该行为的层。

- 行为测试（fail-open、空、全失败、边界）移到共享类自身测试；用真实实例 + mock 依赖测。
- 消费层把 `mockStatic(RedisUtils)` 换成 mock 新协作者，并用精确参数（key + window + scenario）断言委托契约，不用 `any()`。
- 保留短路边界：为让调用不可达的守卫条件加 `verify(collaborator, never()).method(...)`（如无异常）。
- 删除消费层前提已不成立的测试（如共享方法内部已 fail-open 时再 stub 协作者抛异常/null——null 返回在拆箱时 NPE）。
- Job 测试调用 `execute()` 继续通过，因为 support bean 是真实实例；循环现在在共享方法内运行。

## 防御性守卫与日志行为测试

- 每个 `Objects.requireNonNull(x, "name")` 守卫加 `assertThrows` 测试并断言消息——`assertEquals("alertKey", ex.getMessage())`，改名即破坏契约测试。
- 零/负 `Duration` 校验断言 `IllegalArgumentException` 且消息包含稳定短语（如 `must be positive`）。
- 分支返回值也发日志时，断言日志确实触发而不只是返回：捕获 logback `ListAppender`，按稳定子串过滤 `ERROR/WARN` 事件并断言恰好一条。
- 副作用重要时，同样断言短路/否定路径**不**发日志。

## 常见陷阱

- `hutool EnumUtil.fromString` 包装 `Enum.valueOf`，缺失即抛——写返回 null/空的安全循环。
- `verify(mock).method(any())` 与 `verify(mock, never()).method(...)` 不能在同一测试针对同一方法：`any()` 匹配所有调用。
- 重构后（类拆分/改名/签名变更）更新测试的 mock 类型、构造器与调用，同时保持业务断言。
- `@AssertTrue` 不能注入 i18n 占位符：带变量的校验文案收敛为 service 层参数化 ErrorCode 或用自定义注解。
- PowerShell `Set-Content -Encoding UTF8` 会写 BOM（`\ufeff`）破坏 `javac`（“非法字符”）——用 `[System.IO.File]::WriteAllText(path, text, UTF8Encoding(false))` 写，或去掉开头 BOM。
- 测试文件使用显式静态导入（非通配符）时必须逐个添加新断言；`assertThrows`/`assertTrue` 不会自动可用。
- 重构把 fail-open/null 处理移入共享方法后，消费层不要 stub 共享方法返回 `null`——原始类型返回拆箱即 NPE。
