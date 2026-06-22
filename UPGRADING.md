# 模板升级说明

本文件说明已使用 `vibe-coding-starter` 的项目，后续如何吸收模板更新，同时避免把项目私有事实覆盖掉。

## 1. 先判断你的升级目标

升级前，先回答两个问题：

1. 你要同步的是模板能力，还是业务项目事实？
2. 你当前仓库里哪些文件已经被项目深度定制？

如果目标只是引入新脚本、新示例、新工作流说明，应优先只同步模板能力相关文件。

## 2. 建议直接覆盖的文件

以下文件通常属于模板能力本身，若上游模板有更新，可以优先比较后覆盖：

- `.github/`
- `prompts/`
- `scripts/`
- `tools/skills/`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `PUBLISHING.md`
- `EXPORTING.md`
- `CHANGELOG.md`
- `UPGRADING.md`

覆盖前仍建议先 review diff，避免把你本地新增的自定义检查或发布说明直接冲掉。

## 3. 建议按 diff 合并的文件

以下文件通常同时承载模板能力和项目入口信息，不建议无脑整文件覆盖：

- `README.md`
- `QUICKSTART.md`
- `AGENTS.md`
- `AGENTS.template.md`
- `docs/index.md`
- `docs/README.md`
- `docs/onboarding.md`
- `docs/evolution/INDEX.md`
- `docs/governance/document-sync-map.md`

建议做法：

1. 先看上游模板新增了哪些规则或入口
2. 再把这些内容合并到你当前仓库
3. 保留你项目自己的名称、命令、模块和业务域事实

## 4. 通常应保留项目自定义的文件

以下文件一旦落到实际项目，通常已经是项目事实源，不应直接被模板覆盖：

- `docs/requirements/**`
- `docs/design/**`
- `docs/tasks/**`
- `docs/api/**`
- `docs/sql/**`
- `docs/upgrade/**`
- `docs/ui/**`
- 项目自身代码目录
- 项目自己的 `.doc-sync.json`

如果模板升级涉及这些目录，通常应按“新规则参考 + 本地手工合并”的方式处理。

## 5. 推荐升级步骤

1. 先看 [CHANGELOG.md](CHANGELOG.md)，确认本次需要吸收哪些变化
2. 把上游模板更新拉到单独分支或临时目录
3. 先覆盖模板能力文件，再手工合并入口文档
4. 检查 `.doc-sync.json` 是否需要同步新规则
5. 运行：

```bash
python scripts/check_all.py
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

6. 人工重点 review：
   - `AGENTS.md`
   - `README.md`
   - `QUICKSTART.md`
   - `docs/governance/document-sync-map.md`

## 6. 升级后至少确认什么

- 项目名称、技术栈、构建命令等占位信息没有被回滚成模板值
- 项目自定义的文档状态口径仍然一致
- `doc-sync` 规则仍能覆盖你的代码目录
- 新增脚本或 skill 没有与项目现有工作流冲突
- 示例项目仍只作为参考，不会误导为项目真实业务模型

## 7. 什么时候不建议立即升级

以下情况建议先暂缓：

- 你当前分支正在处理大规模业务改动
- 你本地已经深度改造 `AGENTS.md` 或治理文档，但还没来得及收敛
- 你尚未明确哪些文件属于模板能力，哪些属于项目事实

## 8. 最小判断原则

如果某项更新不能直接提升“初始化效率、文档同步可靠性、示例参考价值、本地验证能力”，可以不急着第一时间升级。

## 9. 从 v0.2.0 升级到 v0.3.0 时重点看什么

如果你当前使用的是 `v0.2.0`，升级到 `v0.3.0` 时建议重点吸收下面几类变化：

1. 首次采用路径更短了
   `README.md`、`QUICKSTART.md`、`DEMO.md` 已经被收口成更明确的入口链路，适合直接按 diff 合并到你的项目入口文档。

2. 检查脚本补齐了跨平台入口
   新增：
   - `scripts/check_all.ps1`
   - `scripts/check_all.sh`
   - `scripts/doc_sync_check.ps1`
   - `scripts/doc_sync_check.sh`

   如果你的团队同时使用 Windows 和 macOS / Linux，这部分通常值得直接覆盖同步。

3. 本地与 CI 的统一检查入口更完整了
   `scripts/check_all.py` 现在支持更清晰的分组输出与 `--base / --head`，`.github/workflows/doc-sync.yml` 也改成了通过统一入口覆盖：
   - `doc-sync`
   - Markdown 链接检查
   - 示例自检

4. Review 与 PR 流程约束更明确了
   如果你希望团队 review 时固定按“文档状态 -> diff -> 测试”的顺序检查，建议同步这些文件：
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `tools/skills/code-review/`
   - `prompts/standard-03-findings-first-review.txt`
   - `docs/governance/ai-collaboration-best-practices.md`
   - `docs/governance/document-sync-map.md`

5. Spring Boot 示例更贴近真实团队
   `examples/spring-boot-device-center/` 新增了 `docs/sql`、`docs/upgrade` 和 `db/migration`，如果你希望示例更容易映射到真实后端项目，这部分值得同步参考。
