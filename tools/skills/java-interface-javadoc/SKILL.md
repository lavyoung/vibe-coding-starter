---
name: java-interface-javadoc
description: Write or improve Javadocs for Java interfaces in this repository. Use when adding interface comments, documenting method contracts, clarifying params and returns, or aligning interface-level comments with the project's Chinese Javadoc style.
---

# Java 接口 Javadoc

把接口契约写清楚，让调用方不读实现也能理解行为。

## 按项目风格写类级 Javadoc

- 开头一行简短中文摘要。
- 至少一行 `<p>1. ...</p>` 说明接口职责。
- 相邻文件使用 `<a href="mailto:email">name</a>` 格式时，`@author` 保持一致。
- `@since` 格式与相邻文件一致。
- 星号对齐与间距贴合相邻接口的既有风格。

## 把方法 Javadoc 写成契约

- 第一行说明方法做什么。
- 仅当有业务规则、副作用或使用约束时使用额外 `<p>` 块。
- 每个参数都要 `@param`。
- 每个非 void 方法都要 `@return`。
- 空结果、可空与异常行为在影响调用方时必须说明。
- 有助于读者理解时，用 `{@link ...}` 指向枚举、配置键或相关类型。

## 显式说明缺失语义

- 新接口真正建模缺失时优先 `Optional<T>`。
- 签名无法变更时，说明返回 `null`、空列表、空 map 还是部分空对象。
- 不要让调用方猜缺失数据语义。

## 完成前复核

- 确认接口有类级 Javadoc。
- 确认每个公开方法有 Javadoc。
- 确认每个参数与非 void 返回都有说明。
- 确认缺失与异常行为在需要处显式。
