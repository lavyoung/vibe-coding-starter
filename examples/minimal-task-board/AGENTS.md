# minimal-task-board 项目专属约束

## 1. 项目事实

- 项目名称：`minimal-task-board`
- 技术栈：`Node.js 20 + 原生 http + 内存存储`
- 主模块：`src/`
- 主要业务域：`tasks`
- 构建命令：`无构建步骤`
- 测试命令：`node --test`

## 2. 文档入口

开始工作前优先读取：

1. [docs/index.md](docs/index.md)
2. [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
3. [docs/governance/document-sync-map.md](docs/governance/document-sync-map.md)
4. 与当前任务最相关的 `requirements / design / api / ui / tasks`

## 3. 文档状态闸门

- `已接受`、`已生效`、`已落地` 才能作为实现依据
- `草案`、`评审中` 只能用于讨论

## 4. 自动化补充

- 机器校验规则见 [.doc-sync.json](.doc-sync.json)
- 本地校验命令复用上层 starter 的 `scripts/doc_sync_check.py`

## 关联代码

- [src/server.js](src/server.js)
- [src/task-store.js](src/task-store.js)
