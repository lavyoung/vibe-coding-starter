# 事务执行器模板（管原子写入的最小结构，事务编排复杂时先查）

## 模式选择

| 场景 | 建议模式 |
|---|---|
| 整个公开用例就是一个短事务 | 在具体服务公开方法上使用 `@Transactional` |
| 校验、锁或分支包围多个原子写入 | 外层用例服务 + 独立事务执行器 |
| 失败后必须在回滚后收敛 | 外层服务捕获后处理，事务执行器只承担原子写入 |
| 局部数据库边界更清晰 | 复用现有 `TransactionTemplate` |

## 结构示意

```java
@Component
class XxxTransactionExecutor {

    @Transactional(rollbackFor = Exception.class)
    Result execute(Command command) {
        // 1. CAS 进入处理中；失败立即终止后续写入
        // 2. 持久化一致性集合
        // 3. 写入最终状态；失败抛出异常以触发回滚
        return new Result();
    }

    record Command(Long id, Long expectedVersion) {
    }

    record Result() {
    }
}
```

## 最低验证

- CAS 成功且写入成功时返回明确结果。
- CAS 失败时不执行后续写入或远程调用。
- 最终状态写入失败时回滚。
- 高风险边界至少有一项经 Spring 代理与真实持久化验证的回滚测试；Mockito 测试不能证明事务已生效。
