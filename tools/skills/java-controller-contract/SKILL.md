---
name: java-controller-contract
description: Build or update Spring Boot controllers with the project API contract. Use when adding interfaces, modifying request or response DTO flow, page endpoints, validation, Swagger annotations, or project-standard response wrapper shapes.
---

# Java Controller 接口契约

让 Controller 保持薄，让对外契约保持一致。

## 契约规则

- 普通端点返回项目标准包装（如 `CommonResult<T>`）。
- 分页端点返回项目分页包装（如 `CommonResult<PageResult<T>>`）。
- 用包装的成功方法（如 `CommonResult.success(...)`），不手拼 JSON。
- 业务异常由服务层经既有异常系统抛出。
- 新增或修改端点前，检查附近 controller 与全仓库是否有重复 `HTTP Method + Path`。
- 仅接口定义阶段时，controller 方法保持完整签名、正确路由、校验、Swagger 注解与必要时的临时占位/mock 返回。

## 注解模式

- 保留 `@RestController`、`@RequestMapping` 与 Swagger `@Tag` / `@Operation`。
- 在 Spring Boot 3.3+ / Spring Framework 6.1 基线，Controller 类不加类级 `@Validated`；请求体保留 `@Valid`，方法参数用 Bean Validation 约束，让 Spring MVC 原生方法校验拥有请求路径。
- 移除或改变 Controller 校验注解时，加 MockMvc 测试证明实际异常类型、全局异常映射与标准包装响应；仅编译测试不足。
- 请求体 DTO 用 `@RequestBody @Valid`；查询/路径参数沿用所在包既有习惯。
- 复用项目路由前缀常量。
- 注入依赖保持最小，通常每个 controller 关注一个服务入口。
- 管理端与 C 端 Java 包分开组织；已接受契约没有时，不发明 `/admin`、`/app` URL 段。
- 对外 C 端端点默认只允许 `GET` 或 `POST`；契约声明 `PUT`/`PATCH`/`DELETE` 时先修正契约再实施。
- 精确限定的匿名端点放专用公开 controller，只在这些方法上标注放行注解；绝不整路径放行。
- 不把入口级注解（如 `@OrgPermission`）当数据范围授权；管理端组织/门店/资源操作按组织数据权限 skill 显式校验。

## 实现步骤

1. 找同业务域最近既有 controller。
2. 镜像其路由结构、请求 DTO 包与响应 VO 包。
3. controller 方法聚焦校验、委托与响应包装。
4. 分支业务逻辑、事务控制与远程编排推进服务层。
5. 严格使用已接受 OpenAPI 的路径与方法，包括已确认的显式动作后缀（如 `/create`）。

## 临时 Mock 响应

仅当用户明确需要前端先联调而真实服务未实现时，用 controller 直出 mock 响应。

- 只用于当前版本新增端点组。
- 不引入 mock 框架，也不为实现接口联调写 service/mapper。
- 构造类型化响应对象并用标准包装返回。
- 分页 mock 返回分页包装且至少一行真实示例，除非契约明确要求空结果。
- 同一 controller 的列表/详情/写成功示例保持 id 与业务字段一致。
- mock 构造会让端点方法变吵时，优先私有 `mockXxx()` 助手。

## 禁止事项

- 不在 Controller 拼非标准 JSON map。
- 不在 Controller 捕获业务异常手工重写。
- 不在端点方法里嵌入第三方 HTTP 细节或厂商 DTO 翻译。
- 不新增分页包装变体。
- 不以 mock 端点为由跳过请求/响应类型、导入、校验、Swagger 注解或项目返回包装。
- 不返回 `availableOperations`、按钮权限等 UI 控制字段；前端菜单权限只负责可见性，后端仍校验身份、数据范围、资源归属、状态、版本与操作资格。
- 不让 Controller 授权只依赖前端隐藏入口。

## 校验清单

- 方法签名返回项目标准包装。
- 请求校验注解与 DTO 输入形状匹配。
- Controller 类不依赖类级 `@Validated`；改变的参数校验路径有 MockMvc 覆盖。
- 服务方法拥有业务决策与异常抛出。
- 对外端点保留 Swagger 注解。
- 新增路由不冲突。
- 对外 C 端路由只使用 `GET` 或 `POST`。
- 匿名访问限定在明确接受的端点方法。
- 组织数据访问显式授权，而非从入口级注解推断。
- 更新端点暴露所有已接受可变字段并保留版本 CAS 行为。
- 改动后按仓库编译/测试 skill 验证。
