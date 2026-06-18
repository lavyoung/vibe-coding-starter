# 文档清单与同步矩阵（管示例项目代码和文档的同步关系，改示例代码前先查）

## 文档元数据

- 文档类型：governance-map
- 当前状态：已生效
- 适用阶段：需求分析、代码实现、示例演示
- 最近更新：2026-06-18

## 代码 -> 文档同步矩阵

| 代码模块 | 必须同步的文档 | 同步动作 |
|---|---|---|
| `src/server.js` | `docs/api/task-api.md` + `docs/design/V1.2.0-task-attachment-upload.md` | 接口行为变化时同步 API 和设计 |
| `src/task-store.js` | `docs/design/V1.2.0-task-attachment-upload.md` + `docs/tasks/V1.2.0-task-attachment-upload.md` | 领域规则变化时同步设计和任务状态 |

## 自动化补充

- 机器可校验规则见 [../../.doc-sync.json](../../.doc-sync.json)
- 本地校验脚本复用上层 starter 的 [../../../../scripts/doc_sync_check.py](../../../../scripts/doc_sync_check.py)

## 关联代码

- [../../src/server.js](../../src/server.js)
- [../../src/task-store.js](../../src/task-store.js)
