---
name: java-client-adapter
description: Extend or refactor third-party integrations behind client, strategy, wrapper, or anti-corruption layers. Use when adding 渠道接入, remote API calls, vendor adapters, error remapping, or payment/notification/device integrations.
---

# Java 客户端适配与防腐层

把厂商关注点留在边缘，让业务服务只说项目语言。

## 分层规则

- 业务编排留在 `service/<domain>/impl`。
- 远程协议细节、厂商 DTO、签名与 HTTP 客户端细节放 `service/external`、`service/feign`、`service/<domain>/client`、`util` 或既有 strategy/wrapper 层。
- 配置放既有配置位置（如 `model/config`、`model/config/properties`、`framework/properties`）。

## 首选模式

- 新建适配器前先搜 `service/feign`、`service/external`、既有 client 与直接 API 用法；若项目级门面已拥有同一远程调用与失败语义，复用它，不新增领域前缀的单方法包装。
- 多渠道能力优先复用目标业务域已有的 registry/strategy/adapter 模式。
- 远程统一返回包装（如 `CommonResult`）时，把 `checkError()` 或显式错误映射集中在包装/服务边界。
- 厂商枚举、字段名与状态码先转成本地枚举或命令再进入核心业务逻辑。
- 用新包装替换旧包装时，比较失败是被抛出、吞掉、默认化还是表示为缺失；结构复用不得静默改变这些外部可见语义。

## 新增渠道或厂商

1. 找到最近既有业务边界（支付、通知、设备代理、外部 API 等）。
2. 先新增或扩展本地命令/DTO 抽象。
3. 在该抽象后实现厂商 client。
4. 通过既有选择机制注册或注入。
5. 把远程失败映射为项目标准异常与错误码。

## 禁止事项

- 业务 service 方法不直接依赖厂商原始请求/响应类，除非目标包现状如此且改动超出范围。
- 不在业务 service 方法里手拼 HTTP 细节。
- 项目已有本地枚举或命令类型时不直接暴露厂商渠道码。
- 不引入唯一行为只是给通用成员/用户查询改名的领域 client；除非有多个消费方或真实协议映射规则，保持小领域投影贴近实际调用方。

## 校验清单

- 业务服务仍依赖本地抽象而非厂商载荷。
- 配置走标准配置层。
- 远程错误在一处检查或重映射。
- 改动没有绕过既有 strategy/adapter 扩展点。
- 代码改动后按仓库编译/测试 skill 验证。
