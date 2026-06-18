# 一次完整需求演示（管 starter 从需求到代码到文档同步的完整走法，想看成品时先查）

## 这份文档解决什么问题

如果你已经理解模板原则，但还不知道“真实项目里到底怎么走一遍”，直接看这份演示。

## 演示目标

演示项目是：

- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)

演示需求是：

- “任务详情页支持上传附件 URL”

## 完整链路

1. 需求来源  
   [docs/requirements/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/requirements/V1.2.0-task-attachment-upload.md)

2. 设计收敛  
   [docs/design/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/design/V1.2.0-task-attachment-upload.md)

3. UI 场景说明  
   [docs/ui/screens/task-detail-attachment-upload.md](examples/minimal-task-board/docs/ui/screens/task-detail-attachment-upload.md)

4. API 事实  
   [docs/api/task-api.md](examples/minimal-task-board/docs/api/task-api.md)

5. 任务推进记录  
   [docs/tasks/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/tasks/V1.2.0-task-attachment-upload.md)

6. 代码实现  
   [src/server.js](examples/minimal-task-board/src/server.js)  
   [src/task-store.js](examples/minimal-task-board/src/task-store.js)

7. 自动化同步规则  
   [.doc-sync.json](examples/minimal-task-board/.doc-sync.json)

## 你应该重点看什么

- 需求文档只写“业务要什么”，不抢设计工作
- 设计文档在状态为 `已接受` 之前，不直接变成代码依据
- 实现完成后，`API / tasks / UI / design` 会一起留痕
- `.doc-sync.json` 只是自动化补充，不替代人工可读的治理文档

## 如何自己复刻一遍

1. 按 [QUICKSTART.md](QUICKSTART.md) 初始化一个新仓库
2. 复制示例项目里的目录组织方式
3. 先写一份 `requirements`
4. 再补 `design / tasks / api / ui`
5. 最后把自己的代码目录映射进 `.doc-sync.json`

## 关联代码

- [examples/minimal-task-board](examples/minimal-task-board)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
