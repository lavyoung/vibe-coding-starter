---
name: java-coding-standards
description: Apply shared Java service coding conventions for Spring Boot code. Use when creating or editing Java classes, records, services, repositories, exceptions, and tests that need consistent naming, immutability, Optional handling, logging, and package layout.
---

# Java 编码规范

编写清晰、可维护的 Java 17+ 代码，优先简单显式的结构，而不是取巧的捷径。

## 默认偏好

- 清晰优于紧凑。
- 实用之处优先不可变数据与 `final` 字段。
- 周围项目风格允许时，小体积不可变载体优先用 `record`。
- 类、方法、字段与常量的命名优先描述性。
- 领域专属异常优先于宽泛的通用失败。

## 命名一致

- 类、接口、枚举、record 用 `PascalCase`。
- 方法与字段用 `camelCase`。
- 常量用 `UPPER_SNAKE_CASE`。
- 包名小写且表达用途。

## 数据安全处理

- 查找类方法在“缺失是契约的一部分”时返回 `Optional<T>`。
- 字段、DTO 属性与方法参数不得使用 `Optional`。
- 避免把 `null` 当作隐藏业务信号。
- 调用边界支持时，请求输入使用 Bean Validation。

## 方法聚焦

- 方法保持短小、单一用途。
- 分支或转换步骤开始模糊意图时，抽取私有助手。
- 优先早返回，避免深嵌套。
- 用命名常量或枚举替换魔法数字与字符串。

## 集合与 Stream 谨慎使用

- 短小可读的转换用 stream。
- 管道变嵌套或带状态时回到循环。
- 数据不应变化时优先不可变集合工厂（如 `List.of()`）。
- 避免裸类型；保持泛型显式。

## 有意地日志与抛出

- 记录重要标识符与业务上下文。
- 避免吞掉异常。
- 重新抛出时用有用的领域上下文包装技术异常。
- 日志消息保持可搜索、结构化。

## 文件组织可预期

- 每个文件一个公开顶层类型。
- 成员顺序稳定：常量、字段、构造器、公开方法、私有助手。
- `src/test/java` 镜像 `src/main/java` 结构。
