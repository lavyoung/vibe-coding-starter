# spring-boot-device-center

一个更贴近企业后端结构的示例项目，用来演示 docs-first 模板在 `Java 17 + Spring Boot 3.3` 场景里的落地方式。

## 这个示例演示什么

- 如何用 `requirements / design / api / tasks / architecture` 驱动后端实现
- 如何组织 `controller / service / repository / test` 这类常见企业项目结构
- 如何用 `.doc-sync.json` 约束代码与文档同步
- 如何在不强制接入数据库的前提下，补齐 `docs/sql / docs/upgrade / db/migration` 这类真实团队常见资产

## 关键文件

- [AGENTS.md](AGENTS.md)
- [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
- [docs/requirements/V1.2.0-device-image-upload.md](docs/requirements/V1.2.0-device-image-upload.md)
- [docs/design/V1.2.0-device-image-upload.md](docs/design/V1.2.0-device-image-upload.md)
- [docs/api/device-admin-api.md](docs/api/device-admin-api.md)
- [docs/sql/device-schema.md](docs/sql/device-schema.md)
- [docs/upgrade/V1.2.0-device-image-upload.md](docs/upgrade/V1.2.0-device-image-upload.md)
- [src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)
- [src/main/resources/db/migration/V1__create_devices_table.sql](src/main/resources/db/migration/V1__create_devices_table.sql)
- [src/main/resources/db/migration/V2__create_device_images_table.sql](src/main/resources/db/migration/V2__create_device_images_table.sql)
- [src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java](src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java)
- [.doc-sync.json](.doc-sync.json)

## 迁移脚本说明

- 运行中的示例仍使用内存仓储，不要求你先配数据库
- 迁移脚本目录 `src/main/resources/db/migration/` 和配套的 `docs/sql`、`docs/upgrade` 用来演示真实团队常见的 schema 资产组织方式
- 如果你把这个示例改造成真实持久化实现，应让 `repository`、迁移脚本和文档一起演进

## 运行方式

```bash
mvn spring-boot:run
```

默认监听 `http://localhost:8080`。

## 测试方式

```bash
mvn test
```

## 示例请求

创建设备：

```bash
curl -X POST http://localhost:8080/admin/devices ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Front Desk Printer\"}"
```

上传设备图片：

```bash
curl -X POST http://localhost:8080/admin/devices/1/images ^
  -H "Content-Type: application/json" ^
  -d "{\"imageUrl\":\"https://cdn.example.com/devices/front-desk-1.png\"}"
```

查询设备：

```bash
curl http://localhost:8080/admin/devices/1
```

## 关联代码

- [src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)
- [src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java](src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java)
- [src/main/resources/db/migration/V1__create_devices_table.sql](src/main/resources/db/migration/V1__create_devices_table.sql)
- [src/main/resources/db/migration/V2__create_device_images_table.sql](src/main/resources/db/migration/V2__create_device_images_table.sql)
