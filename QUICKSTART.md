# 5 分钟上手（管首次启用模板的最短路径，第一次落地 starter 时先查）

## 目标

这份文档用于让你在 5 分钟内完成模板初始化，并进入可协作状态。

第一次采用模板时，只按下面 5 步走：

1. 创建仓库或复制模板
2. 运行 `init_starter`
3. 补 4 份核心文档
4. 运行 `check_all.py`
5. 看一份完整需求演示

## 1. 创建仓库或复制模板

优先方式：

- 直接使用 GitHub 的 `Use this template`

手动复制至少带上这些内容：

```text
.github/
.doc-sync.json
AGENTS.md
AGENTS.template.md
docs/
prompts/
scripts/
tools/skills/
```

按需再带上：

- `CLAUDE.md`
  只有在你需要兼容会自动读取该文件的 agent 时才保留
- `contracts/`
  只有在你需要固定任务入口 / 交接摘要格式时才启用

## 2. 运行 `init_starter`

推荐执行：

```bash
# Python 入口
python scripts/init_starter.py \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单"

# shell 入口
bash scripts/init_starter.sh \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单"
```

```powershell
./scripts/init_starter.ps1 `
  --project-name your-project `
  --tech-stack "Java 17 + Spring Boot 3.3" `
  --build-command "mvn clean package" `
  --test-command "mvn test" `
  --main-modules "module-user,module-order" `
  --business-domains "用户,订单"
```

如果当前项目暂时没有界面层文档，可以改为：

```bash
# Python 入口
python scripts/init_starter.py \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单" \
  --disable-ui

# shell 入口
bash scripts/init_starter.sh \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单" \
  --disable-ui
```

```powershell
./scripts/init_starter.ps1 `
  --project-name your-project `
  --tech-stack "Java 17 + Spring Boot 3.3" `
  --build-command "mvn clean package" `
  --test-command "mvn test" `
  --main-modules "module-user,module-order" `
  --business-domains "用户,订单" `
  --disable-ui
```

## 3. 补 4 份核心文档

脚本会优先替换模板中的主要占位符。执行后，先补齐这 4 份文档或事实入口：

1. `AGENTS.md`
2. `docs/governance/document-sync-map.md`
3. `docs/architecture/current-architecture.md`
4. `docs/evolution/INDEX.md`

如果团队会使用会自动读取 `CLAUDE.md` 的 agent，也顺手确认 `CLAUDE.md` 与 `AGENTS.md` 保持同口径。

然后再补这些常见项目事实：

- 项目简介
- 部署形态
- 模块职责
- 核心依赖

如果项目有前端或管理端界面，再启用 `docs/ui/`。

当项目开始进入持续迭代后，建议尽早启用这两份补充文档：

- `docs/evolution/current-snapshot.md`
- `docs/governance/project-handoff-checklist.md`

如果你预计会同时使用多个 agent 或跨人交接，也可以按需启用并补看：

- `contracts/README.md`
- `contracts/task-entry.schema.json`
- `contracts/handoff-summary.schema.json`
- `contracts/examples/task-entry.example.json`
- `contracts/examples/handoff-summary.example.json`

### 3.1 第一次实现前先确认现有复用点

不要一补完文档就立刻让 AI 开始写代码。第一次真正进入实现前，至少先让它回答：

- 当前仓库里有哪些模块、组件、脚本、配置或约束可以直接复用
- 这次需求应该扩展现有边界，还是确实需要新增抽象
- 如果它打算新增公共能力，为什么现有实现不能承载

推荐直接从这些入口开始：

- [prompts/task-entry.txt](prompts/task-entry.txt)
- [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md)
- [prompts/new-session.txt](prompts/new-session.txt)
- [prompts/code-change.txt](prompts/code-change.txt)
- [prompts/standard-01-understand-current-state.txt](prompts/standard-01-understand-current-state.txt)

如果你不想先自己判断该走设计、实现、升级还是 review，优先用 `task-entry.txt` 作为统一入口。
如果你希望把这一步沉淀成仓库内 skill，优先用 `task-router` 做同样的分流动作。
如果仓库启用了 `contracts/`，且你准备把这份任务再交给另一个 agent，优先把结果补成 `contracts/task-entry.schema.json` 对应结构。

最简开场可以直接复制：

```text
请先按 task-router 工作，不要直接改代码。
任务目标：
要求：
```

这样做的价值很直接：

- 更容易让第一次改动贴着现有项目演进
- 更不容易把小需求写成新框架
- 更适合后续换人或换电脑继续接手
- 更容易让 Codex、Claude 或其他 agent 共享同一份任务口径

## 4. 运行 `check_all.py`

检查脚本底层仍由 Python 实现，但已提供跨环境入口。推荐按你的环境直接运行：

```bash
python scripts/check_all.py
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

说明：

- `check_all.sh` / `doc_sync_check.sh` 仍依赖 `python3` 或 `python`
- 若要让 `check_all.sh` 跑完整示例自检，还需要本机具备 `node`、`mvn`，并正确配置 `JAVA_HOME`
- 如果当前 shell 环境只想先验证统一入口或治理检查，可先运行 `bash scripts/check_all.sh --skip-examples`

这一步会统一执行：

- `doc-sync`
- Markdown 相对链接检查
- 示例项目自检
- starter 关键资产检查
- 示例闭环资产检查（`task-entry / handoff`）
- 公开脚本入口的跨环境包装检查（`.py / .ps1 / .sh`）

如果你希望先理解或定制 `doc-sync` 规则，再看下面这部分。

## 4.1 按需定制 `.doc-sync.json`

把默认规则改成你项目自己的目录模式，例如：

- `src/routes/**`
- `src/services/**`
- `src/repositories/**`
- `src/pages/**`

原则是：

- 代码目录命中后，必须能映射到至少一类文档目录
- `.doc-sync.json` 只负责机器校验
- `docs/governance/document-sync-map.md` 仍保留给人和 AI 阅读

## 4.2 单独跑一轮 `doc-sync`

示例命令：

```bash
python scripts/doc_sync_check.py --changed-file src/routes/tasks.js --changed-file docs/api/tasks.md
bash scripts/doc_sync_check.sh --changed-file src/routes/tasks.js --changed-file docs/api/tasks.md
```

```powershell
./scripts/doc_sync_check.ps1 --changed-file src/routes/tasks.js --changed-file docs/api/tasks.md
```

如果你希望直接按 git diff 检查，也可以运行：

```bash
python scripts/doc_sync_check.py
bash scripts/doc_sync_check.sh
```

```powershell
./scripts/doc_sync_check.ps1
```

## 4.3 开启 CI

模板自带：

- `.github/workflows/doc-sync.yml`

仓库启用 GitHub Actions 后，这条检查会在 PR 和 `main` 分支 push 时执行，并通过统一入口：

- 按变更范围运行 `doc-sync`
- 同时补充链接检查和示例自检
- 同时检查示例是否仍保留完整的 `task-entry -> handoff` 演示链路

## 5. 看一份完整需求演示

接着看：

- [DEMO.md](DEMO.md)
- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)
- [examples/spring-boot-device-center/README.md](examples/spring-boot-device-center/README.md)

## 关联代码

- [scripts/check_all.py](scripts/check_all.py)
- [scripts/check_all.ps1](scripts/check_all.ps1)
- [scripts/check_all.sh](scripts/check_all.sh)
- [scripts/init_starter.py](scripts/init_starter.py)
- [scripts/init_starter.ps1](scripts/init_starter.ps1)
- [scripts/init_starter.sh](scripts/init_starter.sh)
- [.doc-sync.json](.doc-sync.json)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
- [scripts/doc_sync_check.ps1](scripts/doc_sync_check.ps1)
- [scripts/doc_sync_check.sh](scripts/doc_sync_check.sh)
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)
