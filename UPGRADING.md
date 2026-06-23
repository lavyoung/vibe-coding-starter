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
- `CLAUDE.md`
- `AGENTS.template.md`
- `docs/index.md`
- `docs/README.md`
- `docs/onboarding.md`
- `docs/evolution/INDEX.md`
- `docs/governance/document-sync-map.md`
- `docs/governance/agent-collaboration-protocol.md`

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
- 项目自己已经沉淀为事实源的 `contracts/examples/*.json`

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
   - `CLAUDE.md`
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

## 10. 从 v0.3.0 升级到 v0.3.1 时重点看什么

如果你当前使用的是 `v0.3.0`，升级到 `v0.3.1` 时建议重点吸收下面几类变化：

1. 统一任务入口已经补齐
   新增：
   - `prompts/task-entry.txt`

   如果你希望用户不用先自己判断该走设计、实现、小改动还是 review，这个统一入口通常值得直接同步。

2. 新会话和跨人接力现在有了单点快照与交接模板
   新增：
   - `docs/evolution/current-snapshot.md`
   - `docs/governance/project-handoff-checklist.md`

   这两份文档都属于通用模板能力，适合合并进你的项目后，再替换成项目自己的当前事实。

3. 多 agent 协作有了基础结构化约束
   新增：
   - `contracts/task-entry.schema.json`
   - `contracts/handoff-summary.schema.json`

   如果你的项目会同时使用 Codex、Claude 或其他 agent，这两份 schema 值得同步参考；若你暂时只靠自然语言协作，也可以先不启用。

4. 统一检查入口补了 starter 关键资产检查
   `scripts/check_all.py` 现在除了 `doc-sync`、链接检查和示例自检，还会检查：
   - `task-entry`
   - `current-snapshot`
   - `project-handoff-checklist`
   - `contracts/*.schema.json`

   如果你的项目不准备引入这些能力，需要同时评估是否调整本地 `check_all.py`，不要直接覆盖后再手工删除文件。

5. 文档入口和治理说明已经同步到新闭环
   建议按 diff 合并这些入口文档：
   - `README.md`
   - `QUICKSTART.md`
   - `docs/index.md`
   - `docs/README.md`
   - `docs/onboarding.md`
   - `docs/evolution/INDEX.md`
   - `docs/governance/ai-collaboration-best-practices.md`
   - `docs/governance/document-sync-map.md`
   - `EXPORTING.md`

6. 升级时的最小建议
   如果你只想吸收最有价值的模板能力，优先顺序建议是：
   1. `prompts/task-entry.txt`
   2. `docs/evolution/current-snapshot.md`
   3. `docs/governance/project-handoff-checklist.md`
   4. `contracts/*.schema.json`
   5. `scripts/check_all.py` 与相关入口文档

## 11. 从 v0.3.1 升级到 v0.4.0 时重点看什么

如果你当前使用的是 `v0.3.1`，升级到 `v0.4.0` 时建议重点吸收下面几类变化：

1. 多 agent 协作入口已经补成更完整的闭环
   新增：
   - `CLAUDE.md`
   - `docs/governance/agent-collaboration-protocol.md`
   - `contracts/README.md`
   - `contracts/examples/task-entry.example.json`
   - `contracts/examples/handoff-summary.example.json`
   - `tools/skills/task-router/`

   如果你的项目会在 Codex、Claude 或其他 agent 之间交接任务，这一组能力通常值得优先同步。

2. 示例项目已经从“只演示主线文档”升级到“入口 + 收口”都有实物
   两个示例现在都各自包含：
   - `docs/tasks/*-task-entry.json`
   - `docs/tasks/*-handoff.md`

   如果你希望新人或新会话能直接对照一条完整链路，这部分参考价值比单纯看 README 更高。

3. 初始化脚本和检查脚本的跨环境入口更完整了
   新增：
   - `scripts/init_starter.ps1`
   - `scripts/init_starter.sh`

   同时模板已经明确：公开脚本入口应同步维护 `.py / .ps1 / .sh`。如果你的项目已经改过 `scripts/`，建议按 diff 合并，不要只同步单一平台入口。

4. 统一检查入口现在会兜住更多模板一致性问题
   `scripts/check_all.py` 现在除了原有检查，还会覆盖：
   - 示例是否保留完整的 `task-entry -> handoff` 闭环
   - 示例里的 `task-entry` 顶层结构是否仍符合根目录 contract
   - 公开 Python 脚本是否保留对应的 PowerShell / shell 包装入口

   如果你的项目已经裁剪了示例、contracts 或脚本入口，需要在升级前先判断是同步这些能力，还是相应调整本地检查规则。

5. 模板现在自带一层轻量脚本自测和统一行尾策略
   新增：
   - `.gitattributes`
   - `tests/test_check_all.py`

   如果你的仓库也在 Windows 和 macOS / Linux 混用，这部分通常值得直接同步，能减少行尾噪音并固定关键治理检查行为。

6. shell 入口的运行前提已经明确写进文档
   `README.md` 与 `QUICKSTART.md` 现在明确说明：
   - `check_all.sh` / `doc_sync_check.sh` 仍依赖 `python3` 或 `python`
   - 若要跑完整示例自检，还需要 `node`、`mvn` 和正确配置的 `JAVA_HOME`
   - 如果只想验证统一入口或治理检查，可先用 `bash scripts/check_all.sh --skip-examples`

7. 升级时的最小建议
   如果你只想吸收最有价值的 `v0.4.0` 能力，优先顺序建议是：
   1. `CLAUDE.md`
   2. `docs/governance/agent-collaboration-protocol.md`
   3. `contracts/examples/*.json`
   4. `tools/skills/task-router/`
   5. `scripts/init_starter.ps1` 与 `scripts/init_starter.sh`
   6. `scripts/check_all.py`、`tests/test_check_all.py` 与相关入口文档

## 12. 从 v0.4.0 升级到 v0.4.1 时重点看什么

如果你当前使用的是 `v0.4.0`，升级到 `v0.4.1` 时建议重点看下面两类变化：

1. `CLAUDE.md` 和 `contracts/` 已经从“默认带上”收口为“按需启用”
   现在模板口径已经明确：
   - `CLAUDE.md` 只有在你需要兼容会自动读取该文件的 agent 时才保留
   - `contracts/` 只有在你需要固定任务入口 / 交接摘要格式时才启用

   如果你的项目本来就没用这两项，这次升级的意义主要是减少误导，不必为了跟模板保持一致而强行补齐它们。

2. `check_all.py` 不再把这两项当成强制资产
   现在即使你的仓库没有：
   - `CLAUDE.md`
   - `contracts/*.schema.json`
   - `contracts/examples/*.json`

   基础检查也仍然可以通过；只有当你主动启用了 `contracts/`，相关 schema / example 检查才会继续生效。

3. 升级时的最小建议
   如果你只想吸收 `v0.4.1` 的核心变化，优先顺序建议是：
   1. `scripts/check_all.py`
   2. `tests/test_check_all.py`
   3. `README.md`
   4. `QUICKSTART.md`
   5. `contracts/README.md`
   6. `CLAUDE.md`
