# 5 分钟上手（管首次启用模板的最短路径，第一次落地 starter 时先查）

## 目标

这份文档用于让你在 5 分钟内完成模板初始化，并进入可协作状态。

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

## 2. 先运行初始化脚本

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

## 3. 再补手工事实项

脚本会优先替换模板中的主要占位符。执行后，再检查并补齐这些事实：

- 项目简介
- 部署形态
- 模块职责
- 核心依赖

## 4. 先补 4 份事实文档

至少先补齐：

1. `docs/governance/document-sync-map.md`
2. `docs/architecture/current-architecture.md`
3. `docs/evolution/INDEX.md`
4. 当前第一份需求或设计文档

如果项目有前端或管理端界面，再启用 `docs/ui/`。

## 5. 定制 `.doc-sync.json`

把默认规则改成你项目自己的目录模式，例如：

- `src/routes/**`
- `src/services/**`
- `src/repositories/**`
- `src/pages/**`

原则是：

- 代码目录命中后，必须能映射到至少一类文档目录
- `.doc-sync.json` 只负责机器校验
- `docs/governance/document-sync-map.md` 仍保留给人和 AI 阅读

## 6. 本地跑一轮 `doc-sync`

示例命令：

```bash
python scripts/doc_sync_check.py --changed-file src/routes/tasks.js --changed-file docs/api/tasks.md
```

如果你希望直接按 git diff 检查，也可以运行：

```bash
python scripts/doc_sync_check.py
```

如果你希望一次完成本地基础检查，可以直接运行：

```bash
python scripts/check_all.py
```

## 7. 开启 CI

模板自带：

- `.github/workflows/doc-sync.yml`

仓库启用 GitHub Actions 后，这条检查会在 PR 和 `main` 分支 push 时执行。

## 8. 看一份完整演示

接着看：

- [DEMO.md](DEMO.md)
- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)

## 关联代码

- [scripts/check_all.py](scripts/check_all.py)
- [scripts/init_starter.py](scripts/init_starter.py)
- [.doc-sync.json](.doc-sync.json)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)
