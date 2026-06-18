# 发布说明

## 仓库身份建议

- 推荐仓库名：
  `vibe-coding-starter`
- 推荐描述：
  `一个面向人类 + AI 协同交付的文档优先模板仓库，内含 AGENTS、文档治理规则、状态闸门和可复用 Codex skills。`

## 推荐 GitHub Topics

- `template`
- `starter-kit`
- `docs-first`
- `ai-collaboration`
- `codex`
- `project-template`
- `workflow`
- `documentation`

## 推荐仓库设置

1. 仓库设为 `Public`
2. 开启 `Template repository`
3. 开启 `Issues`
4. 如果希望社区参与讨论，开启 `Discussions`
5. 补齐 repository topics
6. 后续可补一张 social preview 图片

## 推荐首个版本号

- `v0.1.0`
  表示第一版公开可用的 starter kit

后续准备发布新版本前，先更新：

- [CHANGELOG.md](CHANGELOG.md)
- [UPGRADING.md](UPGRADING.md)

## 建议首版 Release 文案

```text
vibe-coding-starter 首次公开发布。

包含内容：
- AGENTS 模板
- 文档优先目录骨架
- 文档治理与状态闸门规则
- 新会话与代码改动阶段提示词
- 通用 Codex skills：doc-driven-implementation / post-change-check
```

## 建议 GitHub About 简介

可以直接使用：

`文档优先的人类 + AI 协作交付模板仓库`

## 发布前检查清单

- [ ] README 已按陌生访问者视角审过
- [ ] CHANGELOG 已更新到本次准备发布的版本
- [ ] 升级说明已同步到当前模板能力
- [ ] LICENSE 已存在且版权主体正确
- [ ] CONTRIBUTING 已存在
- [ ] Issue / PR 模板已存在
- [ ] 不再包含本地机器绝对路径
- [ ] 不再包含公司私有假设
- [ ] skill 没有硬编码到单一仓库
- [ ] starter 占位符仍保持通用
- [ ] 仓库已标记为 template
