# vibe-coding-starter

一个面向“人类 + AI 协同交付”的文档优先模板仓库，内含可直接生效的 `AGENTS.md`、文档治理骨架、状态闸门规则和可复用的 Codex skills。

如果你是通过模板创建了一个新项目，请先把本文件标题、首段简介和仓库描述替换成你自己的项目信息；`vibe-coding-starter` 只是上游模板名。

## 这套模板要解决什么问题

很多 AI 协作项目最后都会卡在同几个地方：

- 代码改得比共识快
- 新会话恢复不了上下文
- 设计草稿被直接当成实现依据
- 代码改了，但文档没有同步

这套模板不是某个具体业务模板，而是一套“仓库内协作操作系统”：

- 文档先行
- 代码后行
- 只有有效文档才能落代码
- 新成员和新会话可以只靠仓库内文档恢复上下文

## 你会得到什么

- `AGENTS.md`
  新仓库创建后即可生效的项目级协作约束起始版
- `AGENTS.template.md`
  便于二次抽取或对照修改的模板副本
- `docs/`
  一套完整的文档优先目录骨架
- `prompts/`
  新会话、设计阶段、代码改动阶段可直接复用的提示词
- `tools/skills/`
  两个通用 Codex skill：
  - `doc-driven-implementation`
  - `post-change-check`

## 核心原则

1. 仓库是事实源，不是聊天记录。
2. 新工作先从文档开始，而不是从猜测开始。
3. `草案`、`评审中` 只能用于讨论，不能直接作为实现依据。
4. 只有 `已接受`、`已生效`、`已落地` 的文档才能支撑正式实现。
5. 代码改动结束前，必须补一轮文档同步检查。

## 目录结构

```text
vibe-coding-starter/
├── AGENTS.md
├── AGENTS.template.md
├── docs/
│   ├── index.md
│   ├── onboarding.md
│   ├── evolution/
│   ├── governance/
│   ├── architecture/
│   ├── rfcs/
│   ├── explanation/adr/
│   ├── requirements/
│   ├── design/
│   ├── tasks/
│   ├── upgrade/
│   ├── api/
│   └── sql/
├── prompts/
└── tools/skills/
```

## 快速开始

### 1. 复制骨架到新项目

至少复制这些内容：

```text
AGENTS.md
AGENTS.template.md
docs/
prompts/
tools/skills/
```

如果你是通过 GitHub 的 `Use this template` 创建新仓库，`AGENTS.md` 会随仓库一起生成，不需要再额外改名。

### 2. 替换占位信息

开始使用前，至少替换 `AGENTS.md`、`README.md` 和相关文档里的这些占位信息：

- `<PROJECT_NAME>`
- `<TECH_STACK>`
- `<BUILD_COMMAND>`
- `<TEST_COMMAND>`
- `<MAIN_MODULES>`
- `<BUSINESS_DOMAINS>`

### 3. 先补齐 4 份核心事实文档

在真正开始实现前，先补齐：

1. `AGENTS.md`
2. `docs/governance/document-sync-map.md`
3. `docs/architecture/current-architecture.md`
4. `docs/evolution/INDEX.md`

### 4. 用内置提示词启动工作

直接使用：

- [prompts/new-session.txt](prompts/new-session.txt)
- [prompts/design-task.txt](prompts/design-task.txt)
- [prompts/code-change.txt](prompts/code-change.txt)

## 内置 skills

### `doc-driven-implementation`

适用于以下场景：

- 需要从仓库文档恢复上下文
- 需要判断哪些文档是当前有效依据
- 需要先验文档状态再决定能不能落代码

详见 [tools/skills/doc-driven-implementation/SKILL.md](tools/skills/doc-driven-implementation/SKILL.md)。

### `post-change-check`

适用于以下场景：

- 代码或文档改完后做最后一轮收口检查
- 核对文档同步、状态闸门和验证步骤
- 在结束当前回合前输出变更范围和残余风险

详见 [tools/skills/post-change-check/SKILL.md](tools/skills/post-change-check/SKILL.md)。

## 推荐工作流

```text
需求出现
  ↓
先落 requirements/
  ↓
需要方案设计时，补 design/ 或 RFC
  ↓
文档进入有效状态
  ↓
再从有效文档落代码
  ↓
同步 docs / api / sql / upgrade
  ↓
执行 post-change check
```

## 适合什么项目

- 长期演进的后端系统
- 内部平台
- AI 参与度高的交付流程
- 需要跨人、跨会话接力的项目
- 希望把设计与实现上下文沉淀在仓库里的团队

## 不适合什么项目

- 一次性脚本
- 临时试验仓库
- 生命周期很短的小型玩具项目

## 发布与复用

如果你准备把它发布成 GitHub 模板仓库，请先看：

- [PUBLISHING.md](PUBLISHING.md)
- [EXPORTING.md](EXPORTING.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 状态口径补充

本模板默认使用以下状态：

- `草案`：已创建，仍在补充
- `评审中`：正在讨论，还未定稿
- `已接受`：方案已拍板，可以作为实现依据
- `已生效`：治理规则、目录说明、流程规范已正式启用
- `已落地`：方案已实现并完成文档同步
- `已废弃`：不再作为当前有效方案

## 许可证

[MIT](LICENSE)
