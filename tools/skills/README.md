# 技能库（tools/skills）

本目录存放可复用 skill。每个 skill 是一个独立目录，包含 `SKILL.md`（正文）与 `agents/openai.yaml`（UI / 工具链元数据）。

## 1. 技能库结构

skill 分两类：

| 类别 | 判定 | 当前清单 |
|---|---|---|
| 通用技能 | 与具体技术栈无关，任何项目都适用 | `task-router`（任务路由）、`doc-driven-implementation`（文档驱动实现）、`safe-code-change`（安全改动既有行为）、`post-change-check`（收口检查）、`code-review`（代码评审） |
| 栈绑定技能 | 规则深度依赖某技术栈 / 框架语感（如 Spring、MyBatis-Plus、Redisson） | 12 个 `java-*`：服务结构、事务边界、分布式锁、MyBatis 查询、Controller 契约、OpenAPI 生成、错误码 i18n、异步线程池、客户端防腐层、单元测试设计、编码规范、接口 Javadoc |

命名约定：

- 通用技能**不带栈前缀**（如 `task-router`）。
- 栈绑定技能**必须带 `<栈名>-` 前缀**（如 `java-service-structure`），前缀即“可裁剪边界”。

> 本模板以 Java 系为示例栈（技能库作者的主技术栈），因此 17 个 skill 中 12 个是 `java-*`。这是“电池内置”设计，不是必须保留的内容。

## 2. 非 Java 项目：3 步裁剪

1. **删除栈绑定技能目录**：`Remove-Item tools/skills/java-* -Recurse`（bash：`rm -rf tools/skills/java-*`）。
2. **精简引用**：删除 `AGENTS.md` 0.2 / 0.3 与 `docs/project-profile.md` §4 中的 Java 条目。若把 `docs/project-profile.md` 的“技术栈”字段改为非 Java，则 `AGENTS.md` 0.3 门禁自动失效，只需再删 0.2 中的 `java-*` 匹配说明。
3. **补位**：用 [`tools/skills/_template/SKILL.md`](_template/SKILL.md) 写自己栈的专项 skill，命名用 `<栈名>-<主题>`，并按需在 `AGENTS.md` 0.3 登记强制门禁。

## 3. 新增 skill 规范

- **优先通用**：能写成与栈无关原则的，先写成通用技能；只有框架强相关的规则才写栈绑定技能，避免技能库继续向单一技术栈偏斜。
- **命名**：目录名即 skill 名；通用不带前缀，栈绑定带 `<栈名>-` 前缀。
- **frontmatter**：`name` 与目录同名；`description` 用一句话说明适用场景（供工具链语义匹配，可保留英文）。
- **正文**：中文为主，代码符号与示例保持原文；至少包含：说明、触发场景、工作流、校验清单。
- **元数据**：同目录 `agents/openai.yaml` 提供 `interface.display_name` / `short_description` / `default_prompt`。
- **门禁联动**：需要强制门禁的，在 `AGENTS.md` 0.3 登记“区域 → SKILL.md 路径”，并在 `task-router`、`post-change-check`、`safe-code-change` 中同步衔接。

## 4. 维护注意

- 修改技能正文、重命名或删除技能时，同步检查：`AGENTS.md`、`docs/project-profile.md`、`task-router`、`post-change-check`、`safe-code-change`、`README.md` 技能清单与 `CHANGELOG.md`。
- 示例项目（`examples/`）若引用技能库路径，一并检查。
