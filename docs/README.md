# docs 目录说明（管 `docs/` 目录组织规则，新增或重构文档目录时先查）

## 文档元数据

- 文档类型：docs-directory-guide
- 当前状态：已生效
- 适用阶段：文档维护、目录调整、AI 接手项目
- 最近更新：YYYY-MM-DD

`docs/` 目录统一按“文档类型 + 业务域”组织，避免不同类型文档混放。

## 统一入口

- 人类与 AI 的统一入口是 [docs/index.md](index.md)
- 当前阶段主线入口是 [docs/evolution/INDEX.md](evolution/INDEX.md)

## 目标结构

```text
docs/
├── index.md
├── onboarding.md
├── evolution/
├── governance/
├── architecture/
├── rfcs/
├── explanation/
│   └── adr/
├── requirements/
├── design/
├── tasks/
├── upgrade/
├── api/
├── sql/
├── ui/                (可选)
└── README.md
```

## 分类规则

- `requirements/`：业务要什么
- `design/`：准备怎么做
- `tasks/`：怎么拆、做到哪
- `rfcs/`：方案未拍板前的提案
- `explanation/adr/`：已接受的关键决策
- `architecture/`：系统整体基线
- `upgrade/`：上线和升级要同步什么
- `api/`：接口契约和示例
- `sql/`：表结构和脚本
- `ui/`：页面、弹窗、上传和交互事实源；仅在项目存在稳定界面时启用
- `governance/`：文档治理规则、同步矩阵、状态闸门
- `governance/ai-collaboration-best-practices.md`：推荐的人类 + AI 协作节奏与标准会话提示词
- `evolution/`：当前主线入口

## 关联代码

- 无直接业务代码；治理规则入口见 [AGENTS.md](../AGENTS.md)
