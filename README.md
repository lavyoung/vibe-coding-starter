# vibe-coding-starter

一个面向“人类 + AI 协同交付”的文档优先模板仓库，内含可直接生效的 `AGENTS.md`、文档治理骨架、状态闸门规则、复用优先协作约束和可复用的 Codex skills。

如果你是通过模板创建了一个新项目，请先把本文件标题、首段简介和仓库描述替换成你自己的项目信息；`vibe-coding-starter` 只是上游模板名。

## 第一次使用就按这 5 步

如果你想先快速试起来，不用先通读整个仓库，直接按这个顺序：

1. 复制模板到新项目
2. 运行 `python scripts/init_starter.py`
3. 补 4 份核心文档
4. 运行检查脚本
5. 看一份完整需求演示

对应入口按这条链路继续看：

- 第 1 到 4 步： [QUICKSTART.md](QUICKSTART.md)
- 第 5 步： [DEMO.md](DEMO.md)

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

它除了帮助团队“把文档补齐”，也在帮助团队“把代码演进方式管住”：

- 让 AI 在实现前先说明当前可复用的模块、组件、脚本和边界
- 避免把一次小改动写成新的抽象层
- 在 review 和 PR 阶段显式检查是否出现重复实现、边界漂移和不必要复杂度

## 你会得到什么

- `AGENTS.md`
  新仓库创建后即可生效的项目级协作约束起始版
- `AGENTS.template.md`
  便于二次抽取或对照修改的模板副本
- `docs/`
  一套完整的文档优先目录骨架
- `.doc-sync.json`
  一份可直接定制的机器校验规则文件
- `prompts/`
  新会话、设计阶段、代码改动阶段、小功能点修改时可直接复用的提示词
- `scripts/`
  可在本地和 CI 复用的 `doc-sync` 校验脚本、模板初始化脚本和统一自检入口
- `tools/skills/`
  三个通用 Codex skill：
  - `doc-driven-implementation`
  - `post-change-check`
  - `code-review`
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
├── .doc-sync.json
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
2. 运行 `python scripts/init_starter.py`
3. 补 4 份核心文档
4. 运行检查脚本
5. 看 [DEMO.md](DEMO.md) 里的完整需求演示

第一次真正进入实现前，再按 [QUICKSTART.md](QUICKSTART.md) 里的说明先让 AI 识别现有复用点。

## 4 条标准会话提示词

如果你希望按固定节奏和 AI 协作，可以直接顺序使用：

1. [prompts/standard-01-understand-current-state.txt](prompts/standard-01-understand-current-state.txt)
2. [prompts/standard-02-minimal-implementation.txt](prompts/standard-02-minimal-implementation.txt)
3. [prompts/standard-03-findings-first-review.txt](prompts/standard-03-findings-first-review.txt)
4. [prompts/standard-04-human-review-focus.txt](prompts/standard-04-human-review-focus.txt)

对应的方法论说明见：

- [docs/governance/ai-collaboration-best-practices.md](docs/governance/ai-collaboration-best-practices.md)

## 5 分钟上手

- [QUICKSTART.md](QUICKSTART.md)：第一次采用模板时的唯一详细入口

## doc-sync 与 CI 校验

- [.doc-sync.json](.doc-sync.json)：维护机器可校验的代码 -> 文档映射规则
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)：`doc-sync` 的 Python 主实现
- [scripts/doc_sync_check.ps1](scripts/doc_sync_check.ps1)：Windows PowerShell 入口
- [scripts/doc_sync_check.sh](scripts/doc_sync_check.sh)：macOS / Linux shell 入口
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)：默认接入 PR 与 `main` 分支校验，在 CI 中通过统一入口运行 `doc-sync`、链接检查和示例自检

## 本地统一检查入口

- [scripts/check_all.py](scripts/check_all.py)：统一检查的 Python 主实现
- [scripts/check_all.ps1](scripts/check_all.ps1)：Windows PowerShell 入口
- [scripts/check_all.sh](scripts/check_all.sh)：macOS / Linux shell 入口

示例：

```bash
python scripts/check_all.py
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

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
