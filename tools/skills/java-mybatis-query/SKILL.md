---
name: java-mybatis-query
description: Write or review Java data access code in MyBatis-Plus style. Use when adding Mapper methods, page/list queries, `LambdaQueryWrapperX` conditions, tenant/status/time filters, batch lookups, or N+1-safe database access.
---

# Java MyBatis Query

Keep query logic close to Mapper code and keep heavy filtering in SQL.

## Mapper Shape

- Prefer `BaseMapperX<DO>` plus `@Mapper`.
- Add concise default methods for common page, single-record, and bounded-list access.
- Build conditions with `LambdaQueryWrapperX` when the local mapper already uses it.
- Keep complex SQL in the business module's resource mapper directory (for example `src/main/resources/mapper/`); keep the Java Mapper focused on method contracts.
- Keep UI filtering policy, derived-status projection, remote enrichment, and response assembly in `service/**/support`, not in Mapper interfaces.

## Tenant and logical-delete behavior

Use the behavior verified by the project's interceptor integration test (for example `MybatisAnnotationSqlInterceptorIntegrationTest`):

- MyBatis-Plus built-in CRUD and Wrapper queries apply tenant and logical-delete conditions. Do not manually duplicate `tenant_id` or `deleted` there.
- Raw `@Select`/`@Update` and XML SQL receive the tenant condition from the tenant interceptor in the normal tenant context, but do not receive the logical-delete condition. Do not hand-write `tenant_id`; explicitly write `deleted = 0` when deleted rows must be excluded.
- Re-run the integration test after a framework/MyBatis interceptor upgrade. Do not preserve this conclusion only as a comment.
- A controlled global-code lookup may use `TenantUtils.executeIgnore`, but it must return only a locator such as `tenantId + primaryId`. Enter `TenantUtils.execute(targetTenantId)` and query again by primary key plus original case-sensitive code, enabled/status, and `deleted = 0` before building a response.

## Query Construction Rules

- Prefer `eqIfPresent`, `likeIfPresent`, `betweenIfPresent`, and explicit ordering helpers over manual if/else query assembly.
- Keep org/store, status, create-time, and similar index-aligned business filters explicit when required; rely on the verified interceptor rules above for tenant and logical deletion.
- Use `selectPage(req, wrapper)` for paged reads and keep the wrapper deterministic.
- Use `last("limit 1")` or `last("limit 2")` only when a bounded read is intentional and the surrounding code checks the implication.

## Performance Rules

- Avoid N+1 queries. Aggregate IDs first, then issue batch reads.
- Do not move large filtering, sorting, or aggregation work into Java when SQL can do it.
- Keep page size bounded through the existing request object rather than reading unbounded tables into memory.
- If a slow-query risk is obvious, state it before coding.

## Nullability Guidance

- Preserve the surrounding mapper style if existing methods return nullable DOs.
- When adding a higher-level helper or service method that represents optional presence, prefer `Optional<T>` at that boundary.
- Do not use `Optional` as DTO fields, entity fields, or method parameters.

## Validation Checklist

- Confirm the query can hit indexes with its main filters.
- Confirm page/list methods do not create an avoidable N+1 pattern.
- Confirm Java-side post-processing is lightweight.
- Confirm any added mapper method belongs in the existing business mapper rather than a new abstraction layer.
- Confirm raw SQL has an explicit logical-delete predicate and no duplicated tenant predicate.
- Confirm any ignore-tenant lookup returns only a locator and is followed by a target-tenant recheck.
- After code changes, verify with the repository's compile/test skill.
