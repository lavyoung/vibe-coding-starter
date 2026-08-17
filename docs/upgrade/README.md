# 升级文档说明（管版本发布、配置变更、DDL 和操作步骤，上线前先查）

## 文档元数据

- 文档类型：upgrade-guide
- 当前状态：已生效
- 适用阶段：发布准备、升级执行、联调收口
- 最近更新：2026-08-14

## 建议规则

- 按版本演进约束（见 [docs/README.md](../README.md)）组织：每个版本一个目录 `docs/upgrade/vX.Y.Z/`（如 `v1.1.1/`），版本目录之下才是真正的升级文件
- 新增升级文档时复制 [UPGRADE_TEMPLATE.md](UPGRADE_TEMPLATE.md)
- 每个版本目录至少包含：`upgrade.md`、`upgrade.sql`
- 若接口变化明显，补 API 变更说明，并同步 `docs/api/vX.Y.Z/` 契约
- 最新版本目录是当前升级事实源，历史版本目录仅作追溯

## 关联代码

- 升级文档必须与代码、配置和 SQL 现状一致
