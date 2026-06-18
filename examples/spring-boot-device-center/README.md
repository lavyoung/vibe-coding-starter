# spring-boot-device-center

一个更贴近企业后端结构的示例项目，用来演示 docs-first 模板在 `Java 17 + Spring Boot 3.3` 场景里的落地方式。

## 这个示例演示什么

- 如何用 `requirements / design / api / tasks / architecture` 驱动后端实现
- 如何组织 `controller / service / repository / test` 这类常见企业项目结构
- 如何用 `.doc-sync.json` 约束代码与文档同步
- 如何在不引入数据库的前提下，保留接近企业代码分层的示例

## 关键文件

- [AGENTS.md](AGENTS.md)
- [docs/evolution/INDEX.md](docs/evolution/INDEX.md)
- [docs/requirements/V1.2.0-device-image-upload.md](docs/requirements/V1.2.0-device-image-upload.md)
- [docs/design/V1.2.0-device-image-upload.md](docs/design/V1.2.0-device-image-upload.md)
- [docs/api/device-admin-api.md](docs/api/device-admin-api.md)
- [src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)
- [src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java](src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java)
- [.doc-sync.json](.doc-sync.json)

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
