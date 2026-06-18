# spring-boot-device-center 项目专属约束

## 1. 项目事实

- 项目名称：`spring-boot-device-center`
- 技术栈：`Java 17 + Spring Boot 3.3.4 + Maven + MockMvc`
- 主模块：`src/main/java`、`src/test/java`
- 主要业务域：`device-admin`
- 构建命令：`mvn clean package`
- 测试命令：`mvn test`

## 2. 文档入口

开始工作前优先读取：

1. [docs/index.md](docs/index.md)
2. [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
3. [docs/governance/document-sync-map.md](docs/governance/document-sync-map.md)
4. 与当前任务最相关的 `requirements / design / api / sql / upgrade / tasks / architecture`

## 3. 文档状态闸门

- `已接受`、`已生效`、`已落地` 才能作为实现依据
- `草案`、`评审中` 只能用于讨论

## 4. 自动化补充

- 机器校验规则见 [.doc-sync.json](.doc-sync.json)
- 本地校验脚本复用上层 starter 的 `scripts/doc_sync_check.py`

## 关联代码

- [src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)
