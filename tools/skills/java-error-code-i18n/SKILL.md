---
name: java-error-code-i18n
description: Add or adjust business error codes, user-visible exception messages, and i18n-sensitive exception mappings.
---

# Java 错误码与国际化

让业务错误集中、可追踪、对外安全。

## 先检查

- 读项目业务错误码常量类（如 `XxxErrorCodeConstants.java`）。
- 新增常量前先找到最近领域块。
- 当前业务错误码段以项目约定为准（例如 `1_017_000_000`）。
- 先判断失败是否真的面向用户；内部失败可继续映射既有全局/内部码，不需要专属码。

## 新增或修改业务错误

- 常量放在匹配业务段落（权限、组织、设备、支付、订单、账户等）。
- 名称显式且面向业务。
- 文案贴合项目现有措辞。
- 通过项目异常工具抛出（如 `ServiceExceptionUtil.exception(...)` 或已导入的静态 `exception(...)`）。
- 重映射远程或第三方失败时，转成最接近的本地业务码，不把厂商文本泄漏进核心服务。

## 国际化与用户可见语义

- 对外展示的异常消息、可控枚举标签、配置驱动的可见文本默认视为 i18n 敏感，用户自主输入除外。
- 检查 `src/main/resources/i18n/` 相关文件。
- Bean Validation 消息的边界来自注解时，用插值占位符（`{min}`、`{max}`、`{value}`、`{integer}`、`{fraction}`），不在资源消息里写死重复约束值。
- 默认、`zh_CN`、`zh_TW`、`en_US` 等所有 bundle 保持相同占位符契约。
- 领域消息保持简洁；上下文已能识别主体时不机械加模块名前缀。
- 只在必要时保留用户提供的值，绝不暴露密钥或不必要的个人数据。

## 验证

- 改变 Bean Validation 消息时，对代表性合法/非法值跑真实 `Validator` 测试。
- 断言渲染消息包含注解的实际边界且无未解析 `{...}` token。
- 同一 key 存在于多个 bundle 时逐个维护语言区验证。
- Controller 校验改动用 MockMvc 验证全局异常处理器与项目标准响应形状。

## 校验清单

- 常量位于正确数字段。
- 抛出点使用项目异常工具。
- Controller 返回类型保持标准包装。
- 用户可见错误确认 i18n/资源影响。
- 注解驱动的边界被插值而非写死在文案。
- 语言区测试渲染值且无未解析占位符。
- 改动后按仓库编译/测试 skill 验证。
