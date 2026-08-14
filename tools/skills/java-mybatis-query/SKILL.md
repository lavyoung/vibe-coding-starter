---
name: java-mybatis-query
description: Write or review Java data access code in MyBatis-Plus style. Use when adding Mapper methods, page/list queries, `LambdaQueryWrapperX` conditions, tenant/status/time filters, batch lookups, or N+1-safe database access.
---

# Java MyBatis 查询

查询逻辑贴近 Mapper 代码，重过滤留在 SQL。

## Mapper 形态

- 优先 `BaseMapperX<DO>` + `@Mapper`。
- 常见分页、单条与有界列表访问加简洁 default 方法。
- 本地 mapper 已用时用 `LambdaQueryWrapperX` 构造条件。
- 复杂 SQL 放业务模块资源 mapper 目录（如 `src/main/resources/mapper/`）；Java Mapper 只保持方法契约。
- UI 过滤策略、派生状态投影、远程补全与响应组装放 `service/**/support`，不放 Mapper 接口。

## 租户与逻辑删除行为

以项目拦截器集成测试（如 `MybatisAnnotationSqlInterceptorIntegrationTest`）验证的行为为准：

- MyBatis-Plus 内置 CRUD 与 Wrapper 查询自动应用租户与逻辑删除条件；不要在那里手写重复的 `tenant_id` 或 `deleted`。
- 正常租户上下文中的原始 `@Select`/`@Update` 与 XML SQL 由租户拦截器追加租户条件，但不会追加逻辑删除条件。不要手写 `tenant_id`；需要排除已删行时必须显式写 `deleted = 0`。
- 框架/MyBatis 拦截器升级后重跑集成测试；不要只把这个结论留在注释里。
- 受控全局码查询可用 `TenantUtils.executeIgnore`，但只能返回 `tenantId + primaryId` 这类定位符；进入 `TenantUtils.execute(targetTenantId)` 后按主键 + 原始大小写敏感码、启用/状态与 `deleted = 0` 再次查询再组装响应。

## 查询构造规则

- 优先 `eqIfPresent`、`likeIfPresent`、`betweenIfPresent` 与显式排序助手，而不是手写 if/else 拼查询。
- 组织/门店、状态、创建时间等索引对齐的业务过滤在需要时显式；租户与逻辑删除按上面验证过的拦截器规则。
- 分页读用 `selectPage(req, wrapper)` 且 wrapper 保持确定性。
- `last("limit 1")` 或 `last("limit 2")` 仅当有界读是有意的且周围代码检查其含义时使用。

## 性能规则

- 避免 N+1。先聚合 ID 再批量读。
- 大过滤、排序或聚合不搬进 Java，SQL 能做的留给 SQL。
- 页大小通过既有请求对象保持有界，不把无界表读进内存。
- 明显慢查询风险先说明再写码。

## 可空性指引

- 既有方法返回可空 DO 时保持周围 mapper 风格。
- 高层助手或 service 方法表达可选存在时，该边界优先 `Optional<T>`。
- 不用 `Optional` 作 DTO 字段、实体字段或方法参数。

## 校验清单

- 确认查询主过滤条件可命中索引。
- 确认分页/列表方法没有可避免的 N+1。
- 确认 Java 侧后处理轻量。
- 确认新增 mapper 方法归属既有业务 mapper，而不是新抽象层。
- 确认原始 SQL 有显式逻辑删除谓词且不重复租户谓词。
- 确认 ignore-tenant 查询只返回定位符，并随后在目标租户复检。
- 改动后按仓库编译/测试 skill 验证。
