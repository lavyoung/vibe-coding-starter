# 任务接口说明（管示例项目对外契约，联调或核对接口时先查）

## 文档元数据

- 文档类型：api-contract
- 当前状态：已落地
- 适用阶段：联调、验证、回顾
- 最近更新：2026-06-18

## 1. 查询任务

- `GET /tasks/{taskId}`

成功响应示例：

```json
{
  "id": "task-1",
  "title": "整理 starter 文档",
  "attachments": []
}
```

## 2. 新增任务附件

- `POST /tasks/{taskId}/attachments`

请求体示例：

```json
{
  "filename": "spec.png",
  "url": "https://cdn.example.com/spec.png"
}
```

## 关联代码

- [../../src/server.js](../../src/server.js)
