# 导出为独立 GitHub 仓库

## 这份文档解决什么问题

这份文档说明如何把 `templates/vibe-coding-starter/` 从一个更大的工作仓库中单独导出，并发布成自己的 GitHub 模板仓库。

适用于你准备把这套 starter 独立公开时。

## 1. 目录检查清单

导出前，至少确认目录里有这些内容：

```text
vibe-coding-starter/
├── .github/
├── contracts/
├── .doc-sync.json
├── AGENTS.md
├── AGENTS.template.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── PUBLISHING.md
├── README.md
├── docs/
├── examples/
├── prompts/
├── scripts/
└── tools/skills/
```

后续可选补充：

- social preview 图片
- 示例项目
- 发布说明
- 版本记录与升级说明

## 2. 内容检查清单

发布前请确认：

- 不再包含项目私有业务规则
- 不再包含本地机器绝对路径
- 不再包含公司内部名称，除非你明确希望公开
- 通用 starter 中不再保留仓库私有构建命令
- 所有提示词脱离当前会话后仍然能看懂
- 所有 skills 对多个项目都仍然成立
- `contracts/` 中的 schema 仍然是通用模板，而不是某个项目的私有字段约定

## 3. 导出方式

### 方式 A：复制成一个新的独立仓库目录

在当前仓库外新建一个干净目录，再把 starter 整体复制过去。

推荐使用变量 + `robocopy`，因为它会连 `.github` 这类点目录一起带上：

```powershell
$SourceRepo = "<你的源仓库根目录>"
$TemplatePath = Join-Path $SourceRepo "templates\vibe-coding-starter"
$TargetRepo = "<导出的目标目录>"

New-Item -ItemType Directory -Force -Path $TargetRepo | Out-Null
robocopy $TemplatePath $TargetRepo /E /NFL /NDL /NJH /NJS /NP
```

然后初始化新的 git 仓库：

```powershell
Set-Location $TargetRepo
git init -b main
git add .
git commit -m "chore: initial public template release"
```

### 方式 B：先在大仓库里继续维护

如果你还没准备好立即拆分，可以先继续在当前仓库里维护模板目录，稳定后再导出。

## 4. 创建 GitHub 仓库

在 GitHub 上创建新的公开仓库：

- 名称：`vibe-coding-starter`
- 描述：
  `一个面向人类 + AI 协同交付的文档优先模板仓库，内含 AGENTS、文档治理规则、状态闸门和可复用 Codex skills。`

仓库创建好后执行：

```powershell
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## 5. 首次推送后要做什么

1. 开启 `Template repository`
2. 按 `PUBLISHING.md` 补 Topics
3. 开启 `Issues`
4. 按需开启 `Discussions`
5. 确认 README 渲染正常
6. 确认 Issue / PR 模板可见

## 6. 首版发布检查清单

- [ ] README 已按陌生访问者视角审过
- [ ] CHANGELOG 已存在
- [ ] UPGRADING 已存在
- [ ] LICENSE 已存在且版权主体正确
- [ ] CONTRIBUTING 已存在
- [ ] CODE_OF_CONDUCT 已存在
- [ ] PUBLISHING 已审阅
- [ ] Issue / PR 模板能正常工作
- [ ] 没有失效内部链接
- [ ] 仓库已标记为 template
- [ ] 首版 release 文案已准备

## 7. 推荐首个标签

```text
v0.1.0
```

## 8. 推荐首个提交信息

```text
chore: initial public template release
```
