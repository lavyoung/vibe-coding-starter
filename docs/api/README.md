# API 契约说明（管对外接口契约的 OpenAPI YAML 事实源，接口设计、联调与对接前先查）

## 文档元数据

- 文档类型：api-guide
- 当前状态：已生效
- 适用阶段：接口设计、前后端联调、第三方对接
- 最近更新：2026-08-14

## 职责与默认产出

- `docs/api/` 是对外接口契约的**事实源**，默认产出**可导入的 OpenAPI YAML**（OpenAPI 3.x，如 `openapi: 3.1.0`），随同设计文档生成。
- 默认不再以 Markdown 作为接口契约输出；人读说明可由工具从 YAML 渲染，或按需补一份 `*-notes.md` 作为 YAML 无法表达的人类补充说明（如业务规则、错误语义、联调注意点），它不是契约本体。
- OpenAPI YAML 必须能被主流工具导入解析：swagger-ui / redoc / openapi-generator / 各语言 client 生成器。

## 文件位置与命名规则

- 契约文件按版本目录组织（版本演进约束见 [docs/README.md](../README.md)）：`docs/api/vX.Y.Z/<domain>-api.yaml`，如 `docs/api/v1.1.1/task-api.yaml`。
- 文件名按业务域命名（`<domain>-api.yaml`），版本体现在目录名，不在文件名里重复。
- 同一版本内存在多份契约时按业务域拆分多个文件。
- 禁止把契约文件直接放在 `docs/api/` 根；根只保留本 README 与可选的 `*-notes.md` 目录说明。
- 最新版本目录是当前契约事实源，历史版本目录仅作追溯。

## 最小结构约定

```yaml
openapi: 3.1.0
info:
  title: <domain> API
  version: v1.x
  description: 由 <对应设计文档> 随附生成，可导入 swagger-ui / openapi-generator
paths:
  /<route-prefix>/<endpoint>:
    get:
      operationId: <domain>_<action>
      parameters:
        - name: <param>
          in: query
          schema:
            type: string
      responses:
        "200":
          description: OK
components:
  schemas:
    XxxResp:
      type: object
      properties:
        code:
          type: integer
```

## 完整示例

- 可直接导入的完整契约示例见 [v1.0.0/task-api.yaml](v1.0.0/task-api.yaml)（任务域 CRUD：分页查询、创建、详情、CAS 更新、逻辑删除，含枚举、`$ref` 复用与统一返回包装）。
- 新项目复制该文件到 `docs/api/vX.Y.Z/` 并按业务域改写，作为该版本的第一个契约文件。

## 建议规则

- 生成时机：设计文档进入 `已接受` 后、接口落代码前随设计文档一起生成；接口行为变化时同步更新。
- 内容要求：明确路径、方法、请求 / 响应结构、错误码与示例；示例使用真实业务值，不用 `123`、`xxx` 等占位。
- 有效性要求：文件可通过 OpenAPI 结构校验；禁止保留已不存在的路径。
- 状态约束：不要把草案接口写成已发布事实；接口未定稿前可标注 `x-draft: true` 或放在评审文档中，不写入正式 YAML。
- 不把厂商字段、签名细节、HTTP 实现细节写进对外契约；它们属于防腐层实现。

## 关联代码

- 接口契约必须与 Controller / Route / Contract 对应代码保持一致；改端点时同步更新 YAML，见 `docs/governance/document-sync-map.md`。
