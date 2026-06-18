# 设备中心表结构说明（管当前示例的表结构事实，查看 schema 或排查迁移时先查）

## 文档元数据

- 文档类型：sql-fact
- 当前状态：已落地
- 适用阶段：表结构设计、迁移脚本核对、示例讲解
- 最近更新：2026-06-18

## 1. 当前表结构

本示例额外提供一组与领域模型对齐的迁移脚本，用来演示真实团队常见的 `schema + upgrade` 资产组织方式。

### `devices`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | `bigint` | 主键 | 设备 ID |
| `name` | `varchar(128)` | 非空 | 设备名称 |
| `created_at` | `timestamp` | 非空 | 创建时间 |
| `updated_at` | `timestamp` | 非空 | 最后更新时间 |

### `device_images`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | `bigint` | 主键 | 图片记录 ID |
| `device_id` | `bigint` | 非空，外键 | 所属设备 |
| `image_url` | `varchar(512)` | 非空 | 图片 URL |
| `created_at` | `timestamp` | 非空 | 创建时间 |

## 2. 与代码的关系

- 运行中的示例仍使用内存仓储，不直接连接数据库。
- 这份表结构用于说明：当团队从内存实现演进到持久化实现时，`docs/sql`、迁移脚本和升级说明应该如何与设计一起同步。

## 3. 对应迁移脚本

- [../../src/main/resources/db/migration/V1__create_devices_table.sql](../../src/main/resources/db/migration/V1__create_devices_table.sql)
- [../../src/main/resources/db/migration/V2__create_device_images_table.sql](../../src/main/resources/db/migration/V2__create_device_images_table.sql)

## 关联代码

- [../../src/main/java/com/example/devicecenter/model/Device.java](../../src/main/java/com/example/devicecenter/model/Device.java)
- [../../src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java](../../src/main/java/com/example/devicecenter/repository/InMemoryDeviceRepository.java)
