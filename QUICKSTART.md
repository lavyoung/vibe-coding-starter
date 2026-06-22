# 5 分钟上手（管首次启用模板的最短路径，第一次落地 starter 时先查）

## 目标

这份文档用于让你在 5 分钟内完成模板初始化，并进入可协作状态。

第一次采用模板时，只按下面 5 步走：

1. 创建仓库或复制模板
2. 运行 `init_starter.py`
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

## 2. 运行 `init_starter.py`

推荐执行：

```bash
python scripts/init_starter.py \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单"
```

如果当前项目暂时没有界面层文档，可以改为：

```bash
python scripts/init_starter.py \
  --project-name your-project \
  --tech-stack "Java 17 + Spring Boot 3.3" \
  --build-command "mvn clean package" \
  --test-command "mvn test" \
  --main-modules "module-user,module-order" \
  --business-domains "用户,订单" \
  --disable-ui
```

## 3. 补 4 份核心文档

脚本会优先替换模板中的主要占位符。执行后，先补齐这 4 份文档或事实入口：

1. `AGENTS.md`
2. `docs/governance/document-sync-map.md`
3. `docs/architecture/current-architecture.md`
4. `docs/evolution/INDEX.md`

然后再补这些常见项目事实：

- 项目简介
- 部署形态
- 模块职责
- 核心依赖

如果项目有前端或管理端界面，再启用 `docs/ui/`。

## 4. 运行 `check_all.py`

检查脚本底层仍由 Python 实现，但已提供跨环境入口。推荐按你的环境直接运行：

```bash
python scripts/check_all.py
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

这一步会统一执行：

- `doc-sync`
- Markdown 相对链接检查
- 示例项目自检

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
- [.doc-sync.json](.doc-sync.json)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
- [scripts/doc_sync_check.ps1](scripts/doc_sync_check.ps1)
- [scripts/doc_sync_check.sh](scripts/doc_sync_check.sh)
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)
