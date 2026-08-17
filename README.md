# vibe-coding-starter

一个面向“人类 + AI 协同交付”的文档优先模板仓库，内含可直接生效的 `AGENTS.md`、可按需保留的 `CLAUDE.md` 兼容入口、文档治理骨架、状态闸门规则、复用优先协作约束和 17 个可复用 skills。

如果你是通过模板创建了一个新项目，请先把本文件标题、首段简介和仓库描述替换成你自己的项目信息；`vibe-coding-starter` 只是上游模板名。

## 第一次使用就按这 5 步

如果你想先快速试起来，不用先通读整个仓库，直接按这个顺序：

1. 复制模板到新项目
2. 运行 `init_starter`
3. 补 4 份核心文档
4. 运行检查脚本
5. 看一份完整需求演示

对应入口按这条链路继续看：

- 第 1 到 4 步： [QUICKSTART.md](QUICKSTART.md)
- 第 5 步： [DEMO.md](DEMO.md)

## 为什么值得用（对比裸 AGENTS.md）

只写一份裸 `AGENTS.md`（3~5 条“请先写文档”的约定）5 分钟就能建好，但所有约束都靠自觉，常见结局是：

| 裸 AGENTS.md 没有的机制 | 实际发生什么 |
|---|---|
| 文档状态闸门 | 草稿被 AI 当成实现依据，返工后才被发现 |
| 代码 -> 文档同步矩阵 | 改代码忘改文档，下次接手被旧文档误导 |
| 机器校验 / CI 拦截 | 规则是否执行全凭运气，PR 拦不住 |
| 可复用 skill | 每个新会话重新“教” AI 规则，口径慢慢漂移 |
| 交接协议 | 换人 / 换会话 = 重新讲一遍背景 |

本模板用约 30 分钟初始化，换回的是这些**可执行**的保障：

| 能力 | 裸 AGENTS.md | 本模板 |
|---|---|---|
| 文档状态闸门 | 无 | 有：`已接受 / 已生效 / 已落地` 才能落码 |
| 代码 -> 文档同步 | 口头约定 | 同步矩阵 + `.doc-sync.json` + CI 强制校验 |
| 新会话恢复上下文 | 翻聊天记录 | 单点快照 + 演进索引 + 交接模板 |
| AI 行为约束 | 无 | 17 个可复用 skill，`AGENTS.md` 0.3 设强制门禁 |
| 跨 agent / 跨会话交接 | 无 | JSON Schema 结构化 task-entry / handoff |
| 接口契约 | 无 | 可导入的 OpenAPI YAML，随设计文档生成 |
| 参考实现 | 无 | 2 个可运行示例项目（Node / Spring Boot） |

拿来即用的资产（都是仓库里可数的事实）：

- **17 个 skill**：任务路由、文档驱动实现、安全改动、收口检查、代码评审 5 个通用能力，外加 12 个 Java 专项（服务结构、事务边界、分布式锁、MyBatis 查询、Controller 契约、OpenAPI 生成、错误码 i18n、异步线程池、客户端防腐层、单元测试设计、编码规范、接口 Javadoc）
- **9 个跨平台脚本入口**（3 组 × `*.py` / `*.ps1` / `*.sh`）：模板初始化、doc-sync 校验、统一自检
- **治理骨架**：状态闸门、同步矩阵、版本演进约束、契约与结构事实目录（含 OpenAPI YAML 契约体系）
- **结构化交接**：`contracts/*.schema.json` 与可直接复用的示例

### 这套体系的代价

价值主张的另一半是诚实说明成本，避免拿模板套错项目：

- **初始化约 30 分钟**：运行 `init_starter` + 补 4 份核心文档
- **每个版本有持续维护成本**：同步维护需求 / 设计 / 升级 / 契约文档（有模板与 skill 约束，常规每轮约 10~30 分钟）
- **不适合轻量场景**：一次性脚本、临时试验仓库、生命周期很短的小项目直接用裸 `AGENTS.md` 更合适
- **防呆边界**：文档状态枚举、关联代码引用路径、同步规则命中均有脚本校验（`doc_sync_check.py`，含 `--scan-all` 存量治理），但“契约与实现内容是否一致”无法静态校验，靠契约测试与评审兜底

结论：这套体系适合**长期演进、AI 参与度高、需要跨人跨会话接力**的项目；判断口径见文末“适合 / 不适合什么项目”。

## 这套模板要解决什么问题

很多 AI 协作项目最后都会卡在同几个地方：

- 代码改得比共识快
- 新会话恢复不了上下文
- 设计草稿被直接当成实现依据
- 代码改了，但文档没有同步

这套模板不是某个具体业务模板，而是一套面向仓库协作的基础约束与目录骨架：

- 文档先行
- 代码后行
- 只有有效文档才能落代码
- 改动前先找现有复用点，不默认从零开始造轮子
- 新成员和新会话可以只靠仓库内文档恢复上下文
- 可以用单点快照先恢复“当前阶段、主线和下一步”

它除了帮助团队“把文档补齐”，也在帮助团队“把代码演进方式管住”：

- 让 AI 在实现前先说明当前可复用的模块、组件、脚本和边界
- 避免把一次小改动写成新的抽象层
- 在 review 和 PR 阶段显式检查是否出现重复实现、边界漂移和不必要复杂度

## 你会得到什么

- `AGENTS.md`
  新仓库创建后即可生效的项目级协作约束起始版
- `CLAUDE.md`
  可按需保留的兼容入口；只有在会自动读取 `CLAUDE.md` 的 agent 场景下才需要
- `AGENTS.template.md`
  便于二次抽取或对照修改的模板副本
- `docs/`
  一套完整的文档优先目录骨架，包含用于新会话和交接的单点快照入口
- `contracts/`
  可按需启用的结构化任务入口 / 交接摘要格式说明和示例
- `.doc-sync.json`
  一份可直接定制的机器校验规则文件
- `prompts/`
  新会话、设计阶段、代码改动阶段、小功能点修改时可直接复用的提示词
- `scripts/`
  可在本地和 CI 复用的 `doc-sync` 校验脚本、模板初始化脚本和统一自检入口
- `tools/skills/`
  17 个可复用 skill：
  - 通用：`task-router`、`doc-driven-implementation`、`post-change-check`、`code-review`、`safe-code-change`
  - Java 专项（栈绑定）：`java-service-structure`、`java-transaction-boundary`、`java-distributed-lock`、`java-mybatis-query`、`java-controller-contract`、`java-spring-openapi-doc-generator`、`java-error-code-i18n`、`java-async-thread-pool`、`java-client-adapter`、`java-unit-test-designer`、`java-coding-standards`、`java-interface-javadoc`
  - 注：`java-*` 为栈绑定技能，非 Java 项目按 [tools/skills/README.md](tools/skills/README.md) 裁剪
- `examples/`
  两个可直接参考的示例项目

## 核心原则

1. 仓库是事实源，不是聊天记录。
2. 新工作先从文档开始，而不是从猜测开始。
3. `草案`、`评审中` 只能用于讨论，不能直接作为实现依据。
4. 只有 `已接受`、`已生效`、`已落地` 的文档才能支撑正式实现。
5. 改动前先找现有复用路径，优先扩展已有实现，不重复造轮子。
6. 代码改动结束前，必须补一轮文档同步检查。

## 目录结构

```text
vibe-coding-starter/
├── .github/workflows/
├── contracts/          (可选：需要固定任务入口 / 交接格式时启用)
├── .doc-sync.json
├── AGENTS.md
├── CLAUDE.md           (可选：需要兼容会自动读取该文件的 agent 时保留)
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
│   ├── sql/
│   └── ui/              (可选：有界面项目时启用)
├── examples/
├── prompts/
├── scripts/
└── tools/skills/
```

## 快速开始

首页只保留第一次采用最短路径，详细操作统一看 [QUICKSTART.md](QUICKSTART.md)：

1. 复制模板到新项目
2. 运行 `init_starter`
3. 补 4 份核心文档
4. 运行检查脚本
5. 看 [DEMO.md](DEMO.md) 里的完整需求演示

第一次真正进入实现前，再按 [QUICKSTART.md](QUICKSTART.md) 里的说明先让 AI 识别现有复用点。

## 统一入口 + 4 条标准会话提示词

如果你不想先自己判断该用哪个 prompt，先从这个统一入口开始：

- [prompts/task-entry.txt](prompts/task-entry.txt)
  先让 agent 判断这是需求、设计、代码改动、小修复、升级还是 review，再路由到后续流程

最省事的用法是直接发这 2 行：

```text
任务目标：
要求：
```

如果你更希望把这一步沉淀成仓库内可复用 skill，也可以直接用：

- [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md)
  先做任务分流、文档状态检查和复用点识别，再决定进入哪个 prompt 或协作协议

如果你已经知道当前要走哪条路径，再直接顺序使用下面 4 条标准提示词：

1. [prompts/standard-01-understand-current-state.txt](prompts/standard-01-understand-current-state.txt)
2. [prompts/standard-02-minimal-implementation.txt](prompts/standard-02-minimal-implementation.txt)
3. [prompts/standard-03-findings-first-review.txt](prompts/standard-03-findings-first-review.txt)
4. [prompts/standard-04-human-review-focus.txt](prompts/standard-04-human-review-focus.txt)

如果是第一次进入某个任务，推荐顺序是：

1. `task-entry`
2. 按路由结果进入 `standard-01` / `design-task` / `code-change` / `small-change`
3. 实现完成后再走 `standard-03` 和 `standard-04`

对应的方法论说明见：

- [docs/governance/ai-collaboration-best-practices.md](docs/governance/ai-collaboration-best-practices.md)
- [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md)
- [docs/governance/agent-collaboration-protocol.md](docs/governance/agent-collaboration-protocol.md)

如果你想直接照场景走，不自己拼提示词顺序，优先看：

- [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md)
  把“新需求 / 小改动 / bug 修复 / 联调修正 / 新会话接手”分别串成固定顺序

## 5 分钟上手

- [QUICKSTART.md](QUICKSTART.md)：第一次采用模板时的唯一详细入口

## doc-sync 与 CI 校验

- [.doc-sync.json](.doc-sync.json)：维护机器可校验的代码 -> 文档映射规则
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)：`doc-sync` 的 Python 主实现
- [scripts/doc_sync_check.ps1](scripts/doc_sync_check.ps1)：Windows PowerShell 入口
- [scripts/doc_sync_check.sh](scripts/doc_sync_check.sh)：macOS / Linux shell 入口
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)：默认接入 PR 与 `main` 分支校验，在 CI 中通过统一入口运行 `doc-sync`、链接检查和示例自检

`check_all` 现在还会顺带检查 starter 关键资产是否齐全，例如：

- `prompts/task-entry.txt`
- `docs/evolution/current-snapshot.md`
- `docs/governance/project-handoff-checklist.md`
- `docs/governance/agent-collaboration-protocol.md`
- 公开脚本入口对应的 `scripts/*.ps1` 与 `scripts/*.sh`

如果仓库启用了 `contracts/`，还会额外检查：

- `contracts/*.schema.json`
- `contracts/examples/*.json`

对示例项目，它还会额外确认：

- 每个示例都至少有一份 `*-task-entry.json`
- 每个示例都至少有一份 `*-handoff.md`
- 如果仓库启用了 `contracts/`，示例里的 `task-entry` 顶层结构也会继续对照根目录 schema

## 本地统一检查入口

初始化脚本也提供了同样的跨环境入口：

```bash
# Python 入口
python scripts/init_starter.py

# shell 入口
bash scripts/init_starter.sh
```

```powershell
./scripts/init_starter.ps1
```

> **技术栈感知裁剪**：`--tech-stack` 命中 `java` / `spring` 关键词时保留 12 个 Java 专项 skill；其他技术栈（如 `Go 1.22`、`Python 3.12`、`Node.js 20`）初始化时会自动删除 `tools/skills/java-*`，并同步精简 `AGENTS.md` 门禁与 `docs/project-profile.md` §4；未提供 `--tech-stack` 时不裁剪。完整参数与用法见 [QUICKSTART.md](QUICKSTART.md) §2。

- [scripts/check_all.py](scripts/check_all.py)：统一检查的 Python 主实现
- [scripts/check_all.ps1](scripts/check_all.ps1)：Windows PowerShell 入口
- [scripts/check_all.sh](scripts/check_all.sh)：macOS / Linux shell 入口

示例：

```bash
# Python 入口
python scripts/check_all.py

# shell 入口
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

说明：

- `check_all.sh` / `doc_sync_check.sh` 只是 shell 包装入口，仍依赖 `python3` 或 `python`
- 若要让 `check_all.sh` 跑完整示例自检，还需要本机具备 `node`、`mvn`，并正确配置 `JAVA_HOME`
- 如果当前 shell 环境只想先验证治理检查或包装脚本本身，可先运行 `bash scripts/check_all.sh --skip-examples`

## 一次完整需求演示

- [DEMO.md](DEMO.md)：完成初始化后的下一步入口
- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)
- [examples/spring-boot-device-center/README.md](examples/spring-boot-device-center/README.md)

## 内置 skills

### `doc-driven-implementation`

适用于以下场景：

- 需要从仓库文档恢复上下文
- 需要判断哪些文档是当前有效依据
- 需要先识别现有可复用实现，再决定改动落点
- 需要先验文档状态再决定能不能落代码

详见 [tools/skills/doc-driven-implementation/SKILL.md](tools/skills/doc-driven-implementation/SKILL.md)。

### `task-router`

适用于以下场景：

- 任务刚进入仓库，还没明确该走设计、实现、升级还是 review
- 需要先确认有效文档依据，再决定后续路径
- 需要先识别可复用的 prompt、skill、脚本和边界，再决定如何推进

详见 [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md)。

### `post-change-check`

适用于以下场景：

- 代码或文档改完后做最后一轮收口检查
- 核对文档同步、状态闸门和验证步骤
- 确认有没有留下重复实现或不必要抽象
- 在结束当前回合前输出变更范围和残余风险

详见 [tools/skills/post-change-check/SKILL.md](tools/skills/post-change-check/SKILL.md)。

### `code-review`

适用于以下场景：

- 提交前做一轮 reviewer 视角冷审
- 变更完成后再检查 bug、回归风险和测试缺口
- 需要对照文档和实现检查是否失真

详见 [tools/skills/code-review/SKILL.md](tools/skills/code-review/SKILL.md)。

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

- [CHANGELOG.md](CHANGELOG.md)
- [UPGRADING.md](UPGRADING.md)
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
