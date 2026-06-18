# 5 分钟上手（管首次启用模板的最短路径，第一次落地 starter 时先查）

## 目标

这份文档用于让你在 5 分钟内把模板变成“可以开始协作”的仓库，而不是只停留在复制文件。

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

## 2. 替换 6 个占位项

先在 `AGENTS.md`、`README.md`、`.doc-sync.json` 里替换：

- `<PROJECT_NAME>`
- `<TECH_STACK>`
- `<BUILD_COMMAND>`
- `<TEST_COMMAND>`
- `<MAIN_MODULES>`
- `<BUSINESS_DOMAINS>`

## 3. 先补 4 份事实文档

至少先补齐：

1. `docs/governance/document-sync-map.md`
2. `docs/architecture/current-architecture.md`
3. `docs/evolution/INDEX.md`
4. 当前第一份需求或设计文档

如果项目有前端或管理端界面，再启用 `docs/ui/`。

## 4. 定制 `.doc-sync.json`

把默认规则改成你项目自己的目录模式，例如：

- `src/routes/**`
- `src/services/**`
- `src/repositories/**`
- `src/pages/**`

原则是：

- 代码目录命中后，必须能映射到至少一类文档目录
- `.doc-sync.json` 只负责机器校验
- `docs/governance/document-sync-map.md` 仍保留给人和 AI 阅读

## 5. 本地跑一轮 `doc-sync`

示例命令：

```bash
python scripts/doc_sync_check.py --changed-file src/routes/tasks.js --changed-file docs/api/tasks.md
```

如果你希望直接按 git diff 检查，也可以运行：

```bash
python scripts/doc_sync_check.py
```

## 6. 开启 CI

模板自带：

- `.github/workflows/doc-sync.yml`

只要仓库用了 GitHub Actions，这条检查就会在 PR 和 `main` 分支 push 时执行。

## 7. 看一份完整演示

接着看：

- [DEMO.md](DEMO.md)
- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)

## 关联代码

- [.doc-sync.json](.doc-sync.json)
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py)
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml)
