---
name: safe-code-change
description: Safely change existing behavior while preserving user worktree changes and collecting compatibility evidence. Use when modifying existing code paths, shared components, configuration, scripts, merge resolutions, staging, or commits.
---

# 安全改动既有行为

对既有行为的修改，编译通过不等于兼容。先保留事实与证据，再做最小改动。

## 1. 冻结工作区与范围

开始前记录：

1. `git branch --show-current`、`git log -1 --oneline`、`git status --short`、staged 文件、unstaged 文件、untracked 文件与 merge 状态。
2. 预先存在的脏文件属于用户；除非用户明确包含，不得暂存、还原、格式化或合并它们。
3. 编辑前、提交前、交接前三次确认目标分支。
4. 列出本次确切的生产入口与文件范围；不要把 review 意见扩展为无关清理。
5. 用户暂停或替换任务时，立即停止当前实现，开始新任务前重新检查工作区。

不得凭 IDE 截图或摘要声称"全部已暂存"。用命令证明：

```powershell
git diff --cached --name-status
git diff --name-status
git ls-files --others --exclude-standard
```

当请求是"暂存全部 Java 代码"时，验证没有 `.java` 文件仍处于 unstaged 或 untracked。

## 2. 设计前先建立事实

一起读已接受设计与实际代码路径。对每个拟议改动记录：

- 当前调用方与被调用方
- 请求/响应与错误行为
- 数据库写入与顺序
- 事务与锁边界
- 外部调用与失败行为
- 证明该行为的测试

未解决的事实显式标记。不要把不确定的评审意见变成代码。框架/平台行为以可执行集成测试为准，不凭注释或记忆。

## 3. 建立真实改前基线

改动既有路径前：

1. 定义正常、拒绝、边界、并发、外部调用顺序、数据库副作用、回滚与异常行为。
2. 在改前提交、隔离 worktree 或等价已发布构件上运行基线。
3. 记录提交 hash、测试类、命令、测试数与结果。
4. 改后重跑同一基线，再为新增需求跑增量测试。

与行为改动同一提交新增的测试是有用的回归覆盖，但除非它在改前版本执行过，不能作为旧行为证据。

真正的新端点从已接受 OpenAPI/设计建立契约基线，并保留相邻既有端点测试。

除非需求明确批准，不改变既有重试次数、抛出的异常、"记录并继续"、调用顺序、事务粒度或部分成功语义。

## 4. 最小且职责对齐的改动

- Controller 只做校验、委托与统一返回包装。
- 业务查询/视图组装放 `service/**/support`；不把 UI 过滤、状态投影或远程补全放进 Mapper 接口。
- 已有领域转换器时用 MapStruct；不在用例服务里留机械字段拷贝。
- 可复用生成器、时钟、链接构建器仅在多个调用方或明确领域职责时放入既有 `util` 或领域 `support` 边界。
- 当前时间与系统区转换用业务时钟；业务日期校验放领域 rule/support，不放时钟工具。
- 在租户切换、CAS、锁顺序、状态投影等非显而易见处加简洁行注释；不复述平凡赋值。
- 只删除本次改动直接产生的孤儿代码；不删除无关历史代码。
- 不返回 `availableOperations` 等 UI 控制字段；前端菜单/UI 权限只控制可见性，后端仍在入口执行身份、数据范围、当前状态与操作资格校验。
- 管理端与 C 端 Java 包分开组织；已接受契约没有时，不发明 `/admin`、`/app` URL 段。
- 保留已接受的更新契约细节，如同一版本 CAS 更新里的可选状态变更。
- 普通同步请求从租户上下文取 `tenantId`，不加入每个业务方法签名；仅异步、回调、跨租户扫描、受控租户切换或保留解析上下文的不可变事务命令显式传递。

按改动领域读对应 skill：

- 分布式锁：`tools/skills/java-distributed-lock/SKILL.md`
- MyBatis 查询：`tools/skills/java-mybatis-query/SKILL.md`
- 事务边界：`tools/skills/java-transaction-boundary/SKILL.md`
- 架构、包、方法、转换、工具与注释：`tools/skills/java-service-structure/SKILL.md`

## 5. 保护批量与资金流

- 余额入账/出账走公共余额服务，用语义明确的不同方法；兼容性要求"记录并告警继续"时保留旧出账失败行为，不因公共服务能抛异常就抛。
- 批量中每个独立成功条目一个短事务；批量预取与远程调用在条目事务外。
- 避免 N+1；批量预取缺失时仅在关闭已证实的注册竞态时允许锁内单次复检，并度量大量缺失场景。
- 不在远程调用与逐条目事务外包外层批量锁。
- 只有相同一致性责任时才提取重复核心写入；不为单一调用方建通用批量框架或共享 `Result` 类型。

## 6. 带证据评审与合并

评审时引用确切文件、方法、行、测试与命令，并区分：

- 已确认缺陷
- 局部顾虑/权衡
- 需要测试的证据缺口
- 不应实施的建议

分支合并：

1. 保留预先存在的脏文件。
2. 逐个冲突合并兼容行为；不未经检查就整体接受一侧。
3. 尊重明确文件排除，直到用户覆盖。
4. 在最终合并树上跑测试，不只在一个父提交上跑。
5. 验证合并提交有两个父提交且源分支是祖先。
6. 用户未要求不推送。

## 7. 强制交接检查

宣布完成前验证：

- 分支与 HEAD 是预期的
- 无 merge 状态或冲突标记
- staged、unstaged、untracked 文件分别报告
- 未包含范围外 Java/配置/文档文件
- `git diff --check` 通过
- 改前基线与改后回归结果已记录
- 已接受设计、OpenAPI、实现计划与项目快照按需同步
- 残余环境缺口明确说明，不当作已验证

## 交付证据

说明改动范围、改前与改后验证、未覆盖项，以及是否保留了既有行为。若未能建立基线，明确原因与风险。
