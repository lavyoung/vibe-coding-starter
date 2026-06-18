# 当前架构基线（管示例项目当前结构，理解代码分层时先查）

## 文档元数据

- 文档类型：architecture-baseline
- 当前状态：已生效
- 适用阶段：设计、实现、演示
- 最近更新：2026-06-18

## 结构说明

- `src/server.js`：HTTP 入口，负责路由和请求体解析
- `src/task-store.js`：内存任务仓库与附件上传规则
- `docs/`：需求、设计、API、UI、任务与治理入口

## 关联代码

- [../../src/server.js](../../src/server.js)
- [../../src/task-store.js](../../src/task-store.js)
