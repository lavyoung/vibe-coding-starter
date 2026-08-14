---
name: java-spring-openapi-doc-generator
description: Generate or improve Spring Boot API definition-layer code and OpenAPI 3 annotations in this repository. Use when creating Controller endpoint skeletons, request/response objects, enum validation, i18n validation messages, Swagger annotations, or front-end mock responses from an accepted version design document.
---

# Java Spring OpenAPI 文档生成

生成接口定义层代码，让调用方不读 service 实现即可理解并集成契约。

## 输入文档闸门

- 以已接受/已生效/已落地的版本设计、接口契约或任务文档为事实源。
- 生成前先区分“新端点”与“既有端点变更”。
- 至少提取：controller 包、controller 名、`@Tag`、`@RequestMapping`、HTTP 方法、请求 JSON 示例、响应 JSON 示例，以及端点是新增还是修改。
- 源文档缺失关键契约细节时，先说明缺失字段再实现，不要凭空发明业务语义。

## 接口定义阶段范围

当用户说明当前阶段仅限接口定义 / 表设计 / 前端契约脚手架时，只改：

- `controller`
- `request`
- `response`
- `dto`
- `enum`
- `resources/i18n/validation_message*.properties` 下的校验 i18n 文件
- `docs/api/vX.Y.Z/` 下可导入的 OpenAPI YAML 契约（默认契约产出，见下文“OpenAPI YAML 契约产出”）
- 用户明确要求时，源设计文档中的 API 示例与解释文本

用户未明确要求时不得实现：

- `service` 或 `service.impl`
- 复杂统计或聚合逻辑
- 事务编排
- 远程调用
- MQ / Job / Listener
- 真实数据回填脚本

## OpenAPI YAML 契约产出

仓库 `docs/api/` 的职责是可导入的 OpenAPI YAML 契约，随已接受设计文档生成；Markdown 不再作为默认契约输出。

- 生成 `docs/api/vX.Y.Z/<domain>-api.yaml`（版本化契约按版本目录组织，文件名按业务域），OpenAPI 3.x 形态：顶层 `openapi`、`info`、`paths` 与 `components.schemas`。
- YAML 必须可被常见工具导入（swagger-ui / redoc / openapi-generator）：合法 YAML、`$ref` 可解析、示例真实、无遗留草案路径。
- YAML 中的路径、方法、请求/响应结构与错误码必须与已接受设计示例一致；不维护第二份 Markdown 契约作为事实源。
- 仅当 YAML 无法表达人类补充说明（业务规则、错误语义、联调注意点）时允许 `*-notes.md`；它不是契约本体。
- 不把草案接口写进正式 YAML；契约未接受前保持文件外或整体显式标注草案。

## 文档化 Controller

- 每个端点加 `@Tag`：简洁模块名 + 一句话描述。
- 每个端点加 `@Operation`。
- `summary` 简短、动作导向。
- 端点需要规则、示例、枚举含义或响应说明时，用文本块写 `description`。
- 通过既有路由前缀常量类使用项目路由前缀。
- 加路由前先检查既有 controller；不创建重复 `HTTP Method + Path`。
- 方法体临时时也要保持签名、请求类型、响应类型与路由语义完整。

## 文档化参数

- 重要路径与查询参数加 `@Parameter`。
- 用真实示例，不用 `123`、`xxx`、`foo` 等占位。
- 必填参数显式标注。
- 调用方需要时用中文解释枚举或状态值。

## 文档化 DTO 与 VO

- 类级加 `@Schema(description = "...")`。
- 字段级 `@Schema` 至少包含 `description` 与 `example`。
- 适当时必填字段加 `requiredMode = REQUIRED`。
- 枚举型字符串字段加 `allowableValues`。
- 请求对象放既有 `model.request.xxx` 风格包，响应对象放 `model.response.xxx`，除非相邻代码有不同既定模式。
- `LocalDateTime` 字段：项目 web starter 按毫秒序列化时使用 13 位毫秒时间戳示例；以相邻字段证实的约定为准。
- 项目按毫秒序列化时，`LocalDateTime` API 字段不要用 `2026-05-12 08:00:14` 这类格式化日期串示例。
- 金额字段遵循既有接口层约定：响应值通常是 `BigDecimal` 元；DO/数据库字段通常是整型/长整型分。
- 分页端点：请求类型继承项目分页请求基类（如 `WebPageRequest`），响应形状基于项目分页包装（如 `PageResult<T>`）。

## 校验、i18n 与枚举

- 注解中不写死中文校验文案。
- 校验消息引用 i18n key，例如 `@NotNull(message = "{profit.share.account.id.not.null}")`。
- 新增校验 key 时更新全部项目校验 bundle：默认与每个维护语言区（如 `validation_message.properties`、`validation_message_zh_CN.properties`、`validation_message_zh_TW.properties`、`validation_message_en_US.properties`）。
- 枚举型请求字段优先新增或复用枚举，并用框架枚举校验注解（如 `@InEnum` 或 `@StringInEnum`）校验；不要只靠 `1-xxx, 2-yyy` 注释。
- 框架提供时，整型枚举实现可取值数组接口（如 `IntArrayValuable`），字符串枚举实现对应字符串变体（如 `StringArrayValuable`）。

## 前端 Mock 响应边界

用户明确需要前端在真实业务实现前先联调时，优先 controller 直出临时 mock 响应。

- 只用于新增端点或当前版本新增端点组。
- 不进入 service、mapper、统计或远程调用逻辑。
- 不引入 mock 框架。
- 直接在 controller 构造响应对象并返回项目标准包装。
- 分页端点至少返回一行真实示例，除非设计文档明确要求空结果。
- 同一业务 id、组织 id、账户 id 与时间戳在列表/详情示例间保持一致。
- 示例会让端点方法变吵时，controller 内用私有 `mockXxx()` 助手。

## 让产出有用

- 写操作说明校验规则。
- body 型 POST/PUT 端点给请求示例。
- 调用方可能误读嵌套数据时补响应结构说明。
- 展示值随语言变化时标注 i18n 敏感字段。
- 文档中的 JSON 示例保持可复制：JSON 块内不用 `//` 注释；优先 `_comment_xxx` 字段或正文说明。

## 完成前复核

- 每个端点有 `@Operation`。
- 每个对调用方重要的 DTO/VO 字段有 `@Schema`。
- 示例真实且格式一致。
- 枚举、状态与校验语义对 API 消费方可视。
- 请求/响应字段与源设计示例一致。
- 无重复 `HTTP Method + Path` 路由。
- `docs/api/vX.Y.Z/` 下存在与设计示例一致的可导入 OpenAPI YAML 契约（不得只有 Markdown 契约）。
- 全部 `LocalDateTime` `@Schema(example)` 值符合项目序列化约定（web starter 按毫秒序列化时用 13 位毫秒时间戳）。
- 枚举请求字段在适当处有枚举校验。
- 校验 i18n key 存在于全部必需 bundle。
