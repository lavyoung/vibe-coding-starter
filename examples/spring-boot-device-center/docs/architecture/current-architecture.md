# 当前系统整体架构基线（管示例分层边界和运行形态，查看后端结构时先查）

## 文档元数据

- 文档类型：architecture-baseline
- 当前状态：已落地
- 适用阶段：接手项目、架构讲解、代码定位
- 最近更新：2026-06-18

## 系统概览

- 项目名称：`spring-boot-device-center`
- 技术栈：`Java 17 + Spring Boot 3.3.4 + Maven`
- 部署形态：`单体后端服务`

## 模块边界

- `controller`：承接 HTTP 接口
- `service`：落地业务规则
- `repository`：屏蔽数据访问细节
- `model`：承载请求、响应和领域对象
- `db/migration`：承载示例的 schema 迁移脚本

## 当前说明

- 为了保持示例最小可运行，仓储层使用内存实现
- 示例额外补齐了 `docs/sql`、`docs/upgrade` 和 `db/migration`，用来说明真实团队常见的 schema 资产组织方式
- 示例重点是文档驱动实现和常见后端分层，不是完整数据库集成

## 关联代码

- [../../src/main/java/com/example/devicecenter/controller/DeviceAdminController.java](../../src/main/java/com/example/devicecenter/controller/DeviceAdminController.java)
- [../../src/main/java/com/example/devicecenter/service/DefaultDeviceService.java](../../src/main/java/com/example/devicecenter/service/DefaultDeviceService.java)
- [../../src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java](../../src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java)
- [../../src/main/resources/db/migration/V1__create_devices_table.sql](../../src/main/resources/db/migration/V1__create_devices_table.sql)
