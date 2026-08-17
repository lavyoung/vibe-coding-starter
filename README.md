# vibe-coding-starter

> **Language**: English | [中文版](README_ZH.md)

A docs-first template repository for "human + AI co-delivery", with an immediately effective `AGENTS.md`, an optional `CLAUDE.md` compatibility entry, a documentation governance skeleton, document status gates, reuse-first collaboration constraints, and 17 reusable skills.

If you created a new project from this template, replace this file's title, intro, and repository description with your own project info; `vibe-coding-starter` is just the upstream template name.

## Start with these 5 steps

If you want to try it out quickly without reading the whole repository first, follow this order:

1. Copy the template to a new project
2. Run `init_starter`
3. Fill in 4 core documents
4. Run the check scripts
5. Read a full requirement walkthrough

Continue through these entry points:

- Steps 1 to 4: [QUICKSTART.md](QUICKSTART.md)
- Step 5: [DEMO.md](DEMO.md)

## Why it's worth it (vs. a bare AGENTS.md)

Writing a bare `AGENTS.md` (3–5 "please write docs first" conventions) takes 5 minutes, but every constraint relies on discipline, and the usual outcomes are:

| Mechanism a bare AGENTS.md lacks | What actually happens |
|---|---|
| Document status gate | A draft is treated as an implementation basis by AI; the rework is only discovered later |
| Code → doc sync matrix | Docs are forgotten when code changes; the next handover is misled by stale docs |
| Machine checks / CI interception | Rule enforcement is pure luck; PRs can't catch it |
| Reusable skills | Every new session re-"teaches" AI the rules, and the wording drifts |
| Handover protocol | Changing person / session = re-explaining all context |

This template costs about 30 minutes to initialize and returns these **enforceable** guarantees:

| Capability | Bare AGENTS.md | This template |
|---|---|---|
| Document status gate | None | Yes: only `已接受` / `已生效` / `已落地` can back code |
| Code → doc sync | Verbal convention | Sync matrix + `.doc-sync.json` + enforced CI checks |
| New session context recovery | Scrolling chat history | Single-point snapshot + evolution index + handover template |
| AI behavior constraints | None | 17 reusable skills with mandatory gates in `AGENTS.md` §0.3 |
| Cross-agent / cross-session handover | None | JSON Schema structured task-entry / handoff |
| API contracts | None | Importable OpenAPI YAML, generated alongside design docs |
| Reference implementations | None | 2 runnable example projects (Node / Spring Boot) |

Ready-to-use assets (all countable facts in this repository):

- **17 skills**: 5 generic capabilities (task routing, doc-driven implementation, safe changes, post-change checks, code review) plus 12 Java-specific ones (service structure, transaction boundaries, distributed locks, MyBatis queries, controller contracts, OpenAPI generation, error-code i18n, async thread pools, client adapters, unit test design, coding standards, interface Javadoc)
- **9 cross-platform script entry points** (3 groups × `*.py` / `*.ps1` / `*.sh`): template initialization, doc-sync validation, unified self-checks
- **Governance skeleton**: status gates, sync matrix, version-evolution constraints, contract and structural fact directories (including the OpenAPI YAML contract system)
- **Structured handover**: `contracts/*.schema.json` with directly reusable examples

### The cost of this system

The other half of the value proposition is honestly stating the cost, so you don't apply the template to the wrong project:

- **~30 minutes to initialize**: run `init_starter` + fill in 4 core documents
- **Ongoing maintenance cost per release**: keep requirements / design / upgrade / contract docs in sync (templates and skills constrain it; typically ~10–30 minutes per round)
- **Not for lightweight scenarios**: one-off scripts, throwaway experiment repos, and short-lived toy projects are better off with a bare `AGENTS.md`
- **Foolproofing boundary**: doc status enums, linked-code reference paths, and sync-rule hits are all script-checked (`doc_sync_check.py`, including `--scan-all` inventory governance), but "whether contract and implementation content match" cannot be statically verified — contract tests and review are the backstop

Conclusion: this system fits projects that are **long-lived, AI-intensive, and need cross-person / cross-session handover**; see "Suitable projects" / "Unsuitable projects" at the end.

## What problem does this template solve

Many AI collaboration projects end up stuck in the same places:

- Code moves faster than consensus
- New sessions can't recover context
- Design drafts are used as implementation basis directly
- Code changed, but docs were not synced

This template is not a business template; it is a set of repository-level collaboration constraints and a directory skeleton:

- Docs first
- Code second
- Only valid docs can back code
- Find existing reuse points before changing anything; don't default to building from scratch
- New members and new sessions can recover context from the repository's docs alone
- A single-point snapshot can recover "current phase, main line, and next step" first

Besides helping teams "get the docs in place", it also helps teams "keep the code evolution under control":

- AI states currently reusable modules, components, scripts, and boundaries before implementing
- Avoids turning a small change into a new abstraction layer
- Review and PR phases explicitly check for duplicate implementations, boundary drift, and unnecessary complexity

## What you get

- `AGENTS.md`
  An immediately effective project-level collaboration constraint starter once the repo is created
- `CLAUDE.md`
  Optional compatibility entry; only needed when an agent auto-reads `CLAUDE.md`
- `AGENTS.template.md`
  A template copy for secondary extraction or side-by-side edits
- `docs/`
  A complete docs-first directory skeleton, including single-point snapshot entries for new sessions and handovers
- `contracts/`
  Optional structured task-entry / handoff format specs and examples
- `.doc-sync.json`
  A directly customizable machine-checkable rules file
- `prompts/`
  Reusable prompts for new sessions, design phase, code-change phase, and small-fix edits
- `scripts/`
  Reusable `doc-sync` validation scripts, the template initializer, and the unified self-check entry for local and CI use
- `tools/skills/`
  17 reusable skills:
  - Generic: `task-router`, `doc-driven-implementation`, `post-change-check`, `code-review`, `safe-code-change`
  - Java-specific (stack-bound): `java-service-structure`, `java-transaction-boundary`, `java-distributed-lock`, `java-mybatis-query`, `java-controller-contract`, `java-spring-openapi-doc-generator`, `java-error-code-i18n`, `java-async-thread-pool`, `java-client-adapter`, `java-unit-test-designer`, `java-coding-standards`, `java-interface-javadoc`
  - Note: `java-*` skills are stack-bound; non-Java projects trim them per [tools/skills/README.md](tools/skills/README.md)
- `examples/`
  Two directly referenceable example projects

## Core principles

1. The repository is the source of truth, not the chat log.
2. New work starts from docs, not from guesses.
3. `草案` (Draft) / `评审中` (In Review) are for discussion only; they cannot be implementation basis.
4. Only `已接受` (Accepted) / `已生效` (Effective) / `已落地` (Landed) docs can support real implementation.
5. Find existing reuse paths before changing anything; prefer extending existing implementations over reinventing wheels.
6. Before code changes are finished, a doc-sync check round is mandatory.

## Directory layout

```text
vibe-coding-starter/
├── .github/workflows/
├── contracts/          (optional: enable when fixing task-entry / handoff formats)
├── .doc-sync.json
├── AGENTS.md
├── CLAUDE.md           (optional: keep when an agent auto-reads this file)
├── AGENTS.template.md
├── docs/
│   ├── index.md
│   ├── onboarding.md
│   ├── evolution/
│   ├── governance/
│   ├── architecture/
│   ├── rfcs/
│   ├── explanation/adr/
│   ├── requirements/
│   ├── design/
│   ├── tasks/
│   ├── upgrade/
│   ├── api/
│   ├── sql/
│   └── ui/              (optional: enable for projects with a UI)
├── examples/
├── prompts/
├── scripts/
└── tools/skills/
```

## Quick start

The homepage keeps only the shortest first-use path; detailed operations all live in [QUICKSTART.md](QUICKSTART.md):

1. Copy the template to a new project
2. Run `init_starter`
3. Fill in 4 core documents
4. Run the check scripts
5. Read the full requirement walkthrough in [DEMO.md](DEMO.md)

Before the first real implementation, follow [QUICKSTART.md](QUICKSTART.md) to have AI identify existing reuse points first.

## Unified entry + 4 standard session prompts

If you don't want to decide which prompt to use yourself, start from this unified entry:

- [prompts/task-entry.txt](prompts/task-entry.txt)
  Have the agent classify the request as requirement, design, code change, small fix, upgrade, or review, then route to the follow-up flow

The easiest usage is sending these 2 lines:

```text
Task goal:
Requirements:
```

If you prefer to bake this step into a reusable skill, use:

- [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md)
  Classify the task, check doc status and reuse points first, then decide which prompt or collaboration protocol to enter

If you already know which path to take, use these 4 standard prompts in order:

1. [prompts/standard-01-understand-current-state.txt](prompts/standard-01-understand-current-state.txt)
2. [prompts/standard-02-minimal-implementation.txt](prompts/standard-02-minimal-implementation.txt)
3. [prompts/standard-03-findings-first-review.txt](prompts/standard-03-findings-first-review.txt)
4. [prompts/standard-04-human-review-focus.txt](prompts/standard-04-human-review-focus.txt)

For a first entry into any task, the recommended order is:

1. `task-entry`
2. Enter `standard-01` / `design-task` / `code-change` / `small-change` per the routing result
3. After implementation, go through `standard-03` and `standard-04`

Methodology references:

- [docs/governance/ai-collaboration-best-practices.md](docs/governance/ai-collaboration-best-practices.md)
- [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md)
- [docs/governance/agent-collaboration-protocol.md](docs/governance/agent-collaboration-protocol.md)

If you want to follow a scenario directly instead of assembling prompt orders yourself, see:

- [docs/governance/prompt-workflow-playbook.md](docs/governance/prompt-workflow-playbook.md)
  Chains "new requirement / small change / bug fix / integration fix / new session handover" into fixed orders

## 5-minute onboarding

- [QUICKSTART.md](QUICKSTART.md): the only detailed entry for first-time template adoption

## doc-sync and CI checks

- [.doc-sync.json](.doc-sync.json): maintains machine-checkable code → doc mapping rules
- [scripts/doc_sync_check.py](scripts/doc_sync_check.py): Python main implementation of `doc-sync`
- [scripts/doc_sync_check.ps1](scripts/doc_sync_check.ps1): Windows PowerShell entry
- [scripts/doc_sync_check.sh](scripts/doc_sync_check.sh): macOS / Linux shell entry
- [.github/workflows/doc-sync.yml](.github/workflows/doc-sync.yml): wired into PR and `main` branch checks by default; runs `doc-sync`, link checks, and example self-checks through the unified entry in CI

`check_all` also checks that the starter's key assets are present, e.g.:

- `prompts/task-entry.txt`
- `docs/evolution/current-snapshot.md`
- `docs/governance/project-handoff-checklist.md`
- `docs/governance/agent-collaboration-protocol.md`
- `scripts/*.ps1` and `scripts/*.sh` counterparts for public script entries

If `contracts/` is enabled, it additionally checks:

- `contracts/*.schema.json`
- `contracts/examples/*.json`

For example projects it additionally confirms:

- Every example has at least one `*-task-entry.json`
- Every example has at least one `*-handoff.md`
- If `contracts/` is enabled, example `task-entry` top-level shapes are validated against the root schema

## Local unified check entry

The initializer also provides the same cross-environment entries:

```bash
# Python entry
python scripts/init_starter.py

# shell entry
bash scripts/init_starter.sh
```

```powershell
./scripts/init_starter.ps1
```

> **Stack-aware trimming**: when `--tech-stack` hits the `java` / `spring` keywords, the 12 Java-specific skills are kept; for other stacks (e.g. `Go 1.22`, `Python 3.12`, `Node.js 20`) initialization automatically removes `tools/skills/java-*` and trims the `AGENTS.md` gates and `docs/project-profile.md` §4 accordingly; without `--tech-stack` nothing is trimmed. Full parameters and usage: [QUICKSTART.md](QUICKSTART.md) §2.

- [scripts/check_all.py](scripts/check_all.py): Python main implementation of the unified checks
- [scripts/check_all.ps1](scripts/check_all.ps1): Windows PowerShell entry
- [scripts/check_all.sh](scripts/check_all.sh): macOS / Linux shell entry

Examples:

```bash
# Python entry
python scripts/check_all.py

# shell entry
bash scripts/check_all.sh
```

```powershell
./scripts/check_all.ps1
```

Notes:

- `check_all.sh` / `doc_sync_check.sh` are thin shell wrappers that still rely on `python3` or `python`
- Running the full example self-checks via `check_all.sh` also requires `node`, `mvn`, and a correctly configured `JAVA_HOME`
- To only validate the governance checks or the wrapper scripts in the current shell, run `bash scripts/check_all.sh --skip-examples` first

## A full requirement walkthrough

- [DEMO.md](DEMO.md): the next step after initialization
- [examples/minimal-task-board/README.md](examples/minimal-task-board/README.md)
- [examples/spring-boot-device-center/README.md](examples/spring-boot-device-center/README.md)

## Built-in skills

### `doc-driven-implementation`

Fits these scenarios:

- Recovering context from repository docs
- Judging which docs are currently valid basis
- Identifying existing reusable implementations before deciding where to change
- Verifying doc status before deciding whether code can land

See [tools/skills/doc-driven-implementation/SKILL.md](tools/skills/doc-driven-implementation/SKILL.md).

### `task-router`

Fits these scenarios:

- A task just arrived and it is not yet clear whether it is design, implementation, upgrade, or review
- Confirming valid doc basis before deciding the follow-up path
- Identifying reusable prompts, skills, scripts, and boundaries before deciding how to proceed

See [tools/skills/task-router/SKILL.md](tools/skills/task-router/SKILL.md).

### `post-change-check`

Fits these scenarios:

- Final closing checks after code or docs changed
- Verifying doc sync, status gates, and validation steps
- Confirming no duplicate implementations or unnecessary abstractions were left behind
- Outputting change scope and residual risks before ending the round

See [tools/skills/post-change-check/SKILL.md](tools/skills/post-change-check/SKILL.md).

### `code-review`

Fits these scenarios:

- A cold reviewer-perspective pass before committing
- Re-checking bugs, regression risks, and test gaps after a change is complete
- Comparing docs and implementation for drift

See [tools/skills/code-review/SKILL.md](tools/skills/code-review/SKILL.md).

## Recommended workflow

```text
Requirement appears
  ↓
Land in requirements/ first
  ↓
When a solution design is needed, add design/ or an RFC
  ↓
Docs reach a valid status
  ↓
Then land code from valid docs
  ↓
Sync docs / api / sql / upgrade
  ↓
Run post-change check
```

## Suitable projects

- Long-lived backend systems
- Internal platforms
- Delivery flows with heavy AI involvement
- Projects that need cross-person, cross-session handover
- Teams that want design and implementation context accumulated in the repository

## Unsuitable projects

- One-off scripts
- Throwaway experiment repos
- Short-lived small toy projects

## Release & reuse

If you plan to publish this as a GitHub template repository, read these first:

- [CHANGELOG.md](CHANGELOG.md)
- [UPGRADING.md](UPGRADING.md)
- [PUBLISHING.md](PUBLISHING.md)
- [EXPORTING.md](EXPORTING.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Status vocabulary

This template uses the following statuses by default (the Chinese tokens are the actual values used in doc metadata):

- `草案` (Draft): created, still being filled in
- `评审中` (In Review): under discussion, not finalized
- `已接受` (Accepted): decided; can serve as implementation basis
- `已生效` (Effective): governance rules, directory guides, and process specs officially enabled
- `已落地` (Landed): implemented and doc sync completed
- `已废弃` (Deprecated): no longer a current valid proposal

## License

[MIT](LICENSE)
