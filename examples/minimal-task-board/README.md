# minimal-task-board

一个最小示例项目，用来演示这套 starter 在真实仓库里的落地方式。

## 这个示例演示什么

- 如何先把需求整理成一份结构化 `task-entry`
- 如何写第一份需求文档
- 如何把需求收敛为设计和 UI 文档
- 如何让 API、任务状态和代码一起落地
- 如何用 `.doc-sync.json` 约束“改代码时顺手改文档”

## 关键文件

- [AGENTS.md](AGENTS.md)
- [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
- [docs/tasks/V1.2.0-task-attachment-upload-task-entry.json](docs/tasks/V1.2.0-task-attachment-upload-task-entry.json)
- [docs/requirements/V1.2.0-task-attachment-upload.md](docs/requirements/V1.2.0-task-attachment-upload.md)
- [docs/design/V1.2.0-task-attachment-upload.md](docs/design/V1.2.0-task-attachment-upload.md)
- [docs/api/task-api.md](docs/api/task-api.md)
- [docs/ui/screens/task-detail-attachment-upload.md](docs/ui/screens/task-detail-attachment-upload.md)
- [docs/tasks/V1.2.0-task-attachment-upload-handoff.md](docs/tasks/V1.2.0-task-attachment-upload-handoff.md)
- [src/server.js](src/server.js)
- [src/task-store.js](src/task-store.js)
- [.doc-sync.json](.doc-sync.json)

## 运行方式

```bash
node src/server.js
```

默认监听 `http://localhost:3000`。

## 示例请求

查询任务：

```bash
curl http://localhost:3000/tasks/task-1
```

上传附件：

```bash
curl -X POST http://localhost:3000/tasks/task-1/attachments ^
  -H "Content-Type: application/json" ^
  -d "{\"filename\":\"spec.png\",\"url\":\"https://cdn.example.com/spec.png\"}"
```

## 关联代码

- [src/server.js](src/server.js)
- [src/task-store.js](src/task-store.js)
