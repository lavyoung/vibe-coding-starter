# 示例目录（管 starter 的参考样本，想看可落地成品时先查）

## 当前示例

- [minimal-task-board](minimal-task-board/README.md)
  一个最小但完整的文档优先示例项目，演示“任务路由 -> task-entry -> 需求 -> 设计 -> UI -> API -> 代码 -> doc-sync -> handoff”的完整链路。
- [spring-boot-device-center](spring-boot-device-center/README.md)
  一个更贴近企业后端结构的 Spring Boot 示例项目，演示“任务路由 -> task-entry -> 需求 -> 设计 -> API -> controller / service / repository -> test -> schema / upgrade -> doc-sync -> handoff”的完整链路。

## 使用方式

- 把它当成参考，不要原样当成你的业务模型
- 重点学习目录组织、状态闸门和同步方式
- 也一起看根目录的 `task-entry`、`task-router`、handoff 模板和 contracts 示例是怎样接入示例链路的
- 示例里现在也各自带了一份 `task-entry.json` 和 handoff 摘要实物，可直接对照“任务怎么开场、回合怎么收口”
- 真正落地时，改成你自己的业务名、代码目录和文档映射
