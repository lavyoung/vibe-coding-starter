# 设备管理接口说明（管示例接口契约，联调和核对行为时先查）

## 文档元数据

- 文档类型：api-spec
- 当前状态：已落地
- 适用阶段：联调、测试、示例讲解
- 最近更新：2026-06-18

## 接口列表

### `POST /admin/devices`

- 请求体：`{"name":"Front Desk Printer"}`
- 返回：设备 ID、设备名称、图片列表

### `GET /admin/devices/{id}`

- 返回：设备详情

### `POST /admin/devices/{id}/images`

- 请求体：`{"imageUrl":"https://cdn.example.com/device-1.png"}`
- 返回：更新后的设备详情
- 异常：当图片数量超过 3 张时返回 `409`

## 关联代码

- [../../src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](../../src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [../../src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java](../../src/test/java/com/example/devicecenter/controller/DeviceAdminControllerTest.java)
