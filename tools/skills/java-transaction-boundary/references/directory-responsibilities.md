# 事务相关目录职责（管事务流程中的边界划分，设计事务前先查）

在包含锁、CAS、多写、远程参与者、回滚或补偿的流程中使用以下边界。具体目录名必须匹配项目现状。

## 允许的依赖方向

```text
controller
  -> service interface
  -> service/<domain>/impl
       -> support / strategy / rule
       -> service/<domain>/transaction
            -> mapper
            -> client
       -> client / external wrapper

job
  -> service / 专用状态收敛组件
```

禁止 `support`、`client`、`mapper`、`transaction` 反向依赖用例 `impl`。

## 职责

| 目录/类型 | 负责 | 不负责 |
|---|---|---|
| `controller` | 协议适配、Bean Validation 触发、统一返回包装、请求语义 | 事务脚本、Mapper 调用、分布式锁、厂商报文组装 |
| `service/<domain>` 接口 | 稳定业务用例契约 | 持久化细节、事务实现、厂商协议类型 |
| `service/<domain>/impl` | 用例编排、当前上下文/权限、分支、分布式锁、调用事务执行器、回滚后处理、响应组装 | 原始 HTTP、重复 SQL 细节、超大原子写入脚本 |
| `service/<domain>/transaction` | 一个明确原子业务单元：CAS、必需写入、已接受设计要求的远程参与者调用、最终状态写入 | Controller 校验、权限解析、锁获取、响应格式化、通用工具行为 |
| `service/<domain>/rule` / `strategy` | 纯策略、状态规则、校验与计算 | Mapper、远程调用、事务注解、流程编排 |
| `service/<domain>/support` | 可复用领域读/查询/视图支持；可有界读编排与批量补全 | 数据库写入、事务注解、Controller 响应包装、无关通用工具 |
| `service/<domain>/client` / `external` / `feign` | 远程协议适配、厂商/请求映射、远程错误保留/重映射 | 业务状态机、本地事务所有权、Controller 响应语义 |
| `dal/mapper` | 租户感知查询/更新原语、CAS 谓词、批量持久化 | 跨聚合编排、远程调用、业务异常呈现 |
| `dal/dataobject` | 持久化形状 | 工作流方法、与存储无关的远程 DTO 字段 |
| `model/request`、`model/response` | 对外 API 输入/输出形状 | 事务命令、可变过程上下文 |
| 事务 `Command` / `Result` | 显式事务输入与输出 | HTTP 注解、持久化框架注解、隐藏可变输出 |
| `job` | 调度、扫描边界、trace ID、计数、条目隔离 | 覆盖全部扫描行的大事务、重复的业务流转规则 |

## 留在事务外

- 校验请求形状与当前登录上下文
- 检查权限与资源归属
- 获取 Redis/Redisson 锁
- 选择用例分支
- 把事务 Result 转成响应
- 事务回滚后记录或收敛失败

## 留在事务内

- 从预期状态 CAS 到处理中
- 写聚合与必需明细行
- 仅当已接受设计要求同一一致性边界时调用远程参与者
- 写最终状态并返回显式 Result
