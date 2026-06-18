# 当前系统整体架构基线（管当前模块边界、核心依赖和跨域约束，做跨域设计前先查）

## 文档元数据

- 文档类型：architecture-baseline
- 当前状态：草案
- 适用阶段：接手项目、跨域设计、架构评审
- 最近更新：YYYY-MM-DD

## 1. 系统概览

- 项目名称：`<PROJECT_NAME>`
- 技术栈：`<TECH_STACK>`
- 部署形态：`<单体 / 微服务 / 前后端分离 / 数据平台>`

## 2. 模块边界

- `<module-a>`：职责
- `<module-b>`：职责
- `<module-c>`：职责

## 3. 核心依赖

- `<database / mq / cache / object-storage / third-party-api>`

## 4. 横切约束

- 事务模型：
- 并发模型：
- 幂等策略：
- 配置管理：
- 日志与追踪：

## 5. 当前风险与待补齐项

- 风险 1
- 风险 2

## 关联代码

- `<path/to/module-or-config>`：说明关系
