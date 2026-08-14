# 项目事实档案（管项目差异化事实，初始化或接手项目时先查）

## 文档元数据

- 文档类型：project-profile
- 当前状态：已生效
- 适用阶段：项目初始化、新会话接手、构建测试、技术栈专项实现
- 最近更新：YYYY-MM-DD

本文件只记录可由代码、配置或团队确认的项目事实；不要把待讨论方案或业务规则写成既有事实。

## 1. 基础信息

- 项目名称：`<PROJECT_NAME>`
- 技术栈：`<TECH_STACK>`
- 主模块或工作区包：`<MAIN_MODULES>`
- 主要业务域：`<BUSINESS_DOMAINS>`
- 编码：UTF-8

## 2. 开发与验证入口

- 构建命令：`<BUILD_COMMAND>`
- 测试命令：`<TEST_COMMAND>`
- 格式化 / lint 命令：`<LINT_COMMAND_OR_NOT_APPLICABLE>`
- 本地运行前置条件：`<LOCAL_PREREQUISITES>`

## 3. 架构与契约事实

- API 契约位置与统一返回模型：`<API_CONTRACT_LOCATION_AND_RESULT_MODEL>`
- 身份、租户或数据范围模型：`<AUTHORIZATION_SCOPE_MODEL>`
- 数据访问方式与迁移位置：`<DATA_ACCESS_AND_MIGRATION_LOCATION>`
- 异步执行器与并发控制入口：`<ASYNC_AND_CONCURRENCY_ENTRYPOINTS>`
- 外部系统适配边界：`<EXTERNAL_INTEGRATION_BOUNDARIES>`

## 4. 专项 skills 启用条件

- Java 编码规范（命名、不可变性、Optional、日志、文件组织）：`tools/skills/java-coding-standards/`
- Java 接口 Javadoc 契约：`tools/skills/java-interface-javadoc/`
- Java 分层或类职责调整：`tools/skills/java-service-structure/`
- Spring 事务边界调整：`tools/skills/java-transaction-boundary/`
- 分布式锁、锁键或并发控制调整：`tools/skills/java-distributed-lock/`
- MyBatis-Plus 查询、Mapper 或分页条件调整：`tools/skills/java-mybatis-query/`
- 接口定义层 / OpenAPI / Swagger / 校验 i18n：`tools/skills/java-spring-openapi-doc-generator/`
- JUnit 5 测试设计（覆盖率方案、边界与回归）：`tools/skills/java-unit-test-designer/`
- 异步任务或线程池复用：`tools/skills/java-async-thread-pool/`
- 第三方接入或防腐层：`tools/skills/java-client-adapter/`
- Controller 接口契约与统一返回包装：`tools/skills/java-controller-contract/`
- 错误码与 i18n 文案：`tools/skills/java-error-code-i18n/`
- 修改既有行为、共享组件、配置或脚本：`tools/skills/safe-code-change/`
- 完成代码或文档变更：`tools/skills/post-change-check/`

仅在项目事实与任务相符时使用专项 skill；不要因模板存在就虚构框架、基础设施或部署模型。

## 关联代码

- [AGENTS.md](../AGENTS.md)
- [docs/architecture/current-architecture.md](architecture/current-architecture.md)
- [docs/governance/document-sync-map.md](governance/document-sync-map.md)
