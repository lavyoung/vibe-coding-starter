# 一次完整需求演示（管 starter 从需求到代码到文档同步的完整走法，想看成品时先查）

如果你还没初始化自己的项目，先按 [QUICKSTART.md](QUICKSTART.md) 完成前 4 步；这份文档对应的是第 5 步：看一份完整演示。

## 这份文档解决什么问题

如果你已经理解模板原则，但还不知道“真实项目里到底怎么走一遍”，直接看这份演示。

## 演示目标

演示项目是：

- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)
- [examples/spring-boot-device-center/README.md](examples/spring-boot-device-center/README.md)

演示需求是：

- “任务详情页支持上传附件 URL”
- “管理端支持设备图片 URL 上传”

开始看具体示例前，先把这条新的模板入口链路补上：

1. 如果你还没判断该走设计、实现、升级还是 review，先用 [prompts/task-entry.txt](prompts/task-entry.txt)
2. 如果你希望把这一步沉淀成仓库内 skill，再看 [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md)
3. 如果你想先按场景看“下一步该用哪个 prompt”，再看 [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md)
4. 如果后续需要跨 agent 接力，再看 [docs/governance/agent-collaboration-protocol.md](docs/governance/agent-collaboration-protocol.md) 和 [contracts/README.md](contracts/README.md)

这两个示例和 playbook 的对应关系是：

- `minimal-task-board`：更接近“新需求进入后，按需求 -> 设计 -> UI -> API -> 实现 -> handoff”这条路径
- `spring-boot-device-center`：更接近“后端需求收敛后，按设计 -> API -> schema / upgrade -> test -> handoff”这条路径

## 完整链路

### 示例一：最小 Node.js 闭环

1. 结构化任务入口
   [docs/tasks/V1.2.0-task-attachment-upload-task-entry.json](examples/minimal-task-board/docs/tasks/V1.2.0-task-attachment-upload-task-entry.json)

2. 需求来源
   [docs/requirements/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/requirements/V1.2.0-task-attachment-upload.md)

3. 设计收敛
   [docs/design/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/design/V1.2.0-task-attachment-upload.md)

4. UI 场景说明
   [docs/ui/screens/task-detail-attachment-upload.md](examples/minimal-task-board/docs/ui/screens/task-detail-attachment-upload.md)

5. API 事实
   [docs/api/task-api.md](examples/minimal-task-board/docs/api/task-api.md)

6. 任务推进记录
   [docs/tasks/V1.2.0-task-attachment-upload.md](examples/minimal-task-board/docs/tasks/V1.2.0-task-attachment-upload.md)

7. 代码实现
   [src/server.js](examples/minimal-task-board/src/server.js)  
   [src/task-store.js](examples/minimal-task-board/src/task-store.js)

8. 自动化同步规则
   [.doc-sync.json](examples/minimal-task-board/.doc-sync.json)

9. 如需跨 agent 交接
   可直接看示例内的 [docs/tasks/V1.2.0-task-attachment-upload-handoff.md](examples/minimal-task-board/docs/tasks/V1.2.0-task-attachment-upload-handoff.md)
   同时对照根目录的 [docs/governance/project-handoff-checklist.md](docs/governance/project-handoff-checklist.md)
   与 [contracts/examples/handoff-summary.example.json](contracts/examples/handoff-summary.example.json)

### 示例二：Spring Boot 后端闭环

1. 结构化任务入口
   [docs/tasks/V1.2.0-device-image-upload-task-entry.json](examples/spring-boot-device-center/docs/tasks/V1.2.0-device-image-upload-task-entry.json)

2. 需求来源
   [docs/requirements/V1.2.0-device-image-upload.md](examples/spring-boot-device-center/docs/requirements/V1.2.0-device-image-upload.md)

3. 设计收敛
   [docs/design/V1.2.0-device-image-upload.md](examples/spring-boot-device-center/docs/design/V1.2.0-device-image-upload.md)

4. API 事实
   [docs/api/device-admin-api.md](examples/spring-boot-device-center/docs/api/device-admin-api.md)

5. 表结构事实
   [docs/sql/device-schema.md](examples/spring-boot-device-center/docs/sql/device-schema.md)

6. 升级说明
   [docs/upgrade/V1.2.0-device-image-upload.md](examples/spring-boot-device-center/docs/upgrade/V1.2.0-device-image-upload.md)

7. 任务推进记录
   [docs/tasks/V1.2.0-device-image-upload.md](examples/spring-boot-device-center/docs/tasks/V1.2.0-device-image-upload.md)

8. 代码实现
   [src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](examples/spring-boot-device-center/src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)  
   [src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](examples/spring-boot-device-center/src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)  
   [src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java](examples/spring-boot-device-center/src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java)
   [src/main/resources/db/migration/V1__create_devices_table.sql](examples/spring-boot-device-center/src/main/resources/db/migration/V1__create_devices_table.sql)
   [src/main/resources/db/migration/V2__create_device_images_table.sql](examples/spring-boot-device-center/src/main/resources/db/migration/V2__create_device_images_table.sql)

9. 测试验证
   [src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java](examples/spring-boot-device-center/src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java)

10. 自动化同步规则
   [.doc-sync.json](examples/spring-boot-device-center/.doc-sync.json)

11. 如需跨 agent 交接
   可直接看示例内的 [docs/tasks/V1.2.0-device-image-upload-handoff.md](examples/spring-boot-device-center/docs/tasks/V1.2.0-device-image-upload-handoff.md)
   同时对照根目录的 [docs/governance/project-handoff-checklist.md](docs/governance/project-handoff-checklist.md)
   与 [contracts/examples/handoff-summary.example.json](contracts/examples/handoff-summary.example.json)

## 你应该重点看什么

- 需求文档只写“业务要什么”，不抢设计工作
- 在真正进入示例实现前，可以先用 `task-entry` 或 `task-router` 做任务分流
- `*-task-entry.json` 让“第一次接手的人”先把目标、范围、约束和验证方式收成统一格式
- 设计文档在状态为 `已接受` 之前，不直接变成代码依据
- 实现完成后，`API / tasks / UI / design` 会一起留痕
- `.doc-sync.json` 只是自动化补充，不替代人工可读的治理文档
- 如果后续要换 agent 或换人继续做，优先把结果收敛成 handoff 模板或 `contracts/examples/*.json` 那样的结构

## 如何自己复刻一遍

1. 按 [QUICKSTART.md](QUICKSTART.md) 初始化一个新仓库
2. 先用 `task-entry` 或 `task-router` 给你的第一个任务分流
3. 若不想自己判断 prompt 顺序，先按 [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md) 选一条最接近的场景路径
4. 复制示例项目里的目录组织方式
5. 先写一份 `requirements`
6. 再补 `design / tasks / api / ui`
7. 最后把自己的代码目录映射进 `.doc-sync.json`

## 关联代码

- [examples/minimal-task-board](examples/minimal-task-board)
- [examples/spring-boot-device-center](examples/spring-boot-device-center)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
