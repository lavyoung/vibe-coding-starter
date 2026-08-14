# 事务执行器模板（管原子写入的最小结构，事务编排复杂时先查）

## 1. 模式选择

| 场景 | 建议模式 |
|---|---|
| 整个公开用例是一个短事务 | 在具体 Service 公开方法上放 `@Transactional` |
| 锁/校验/分支包围多个原子写入 | `XxxServiceImpl` + `XxxTransactionExecutor` |
| 失败收敛必须发生在回滚之后 | 外层 Service + 事务执行器 |
| 短小本地数据库块需要精确内联边界 | 复用现有 `TransactionTemplate`；无重复证据不新增包装 |
| 只是想复用 `@Transactional` 的写法 | 重复写注解，不建抽象基类 |
| 涉及分布式远程参与者 | 遵循已接受的 Seata 设计并验证 XID/环境行为 |

## 2. 外层编排模板

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class XxxServiceImpl implements XxxService {

    private final XxxRules xxxRules;
    private final XxxTransactionExecutor transactionExecutor;

    @Override
    public XxxResp handle(XxxReq request) {
        Long tenantId = resolveTenantId();
        DomainObject current = loadCurrent(request, tenantId);
        xxxRules.validate(current, tenantId);

        try {
            XxxTransactionExecutor.Result result = transactionExecutor.execute(
                    new XxxTransactionExecutor.Command(tenantId, current.getId(), current.getVersion()));
            return buildResponse(result);
        } catch (ServiceException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            handleAfterRollback(current, tenantId, exception);
            throw ServiceExceptionUtil.exception(BUSINESS_HANDLE_FAILED);
        }
    }
}
```

按领域调整异常处理。并发请求可能已完成时不要盲目标记失败；需要时重新加载并解析当前状态。

## 3. 事务执行器模板

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class XxxTransactionExecutor {

    private final XxxMapper xxxMapper;
    private final XxxDetailMapper xxxDetailMapper;

    @Transactional(rollbackFor = Exception.class)
    public Result execute(Command command) {
        LocalDateTime now = LocalDateTime.now();
        if (!xxxMapper.tryMarkProcessing(command.id(), command.tenantId(), command.expectedVersion(), now)) {
            log.info("Business transaction lost CAS: tenantId={}, businessId={}, expectedVersion={}",
                    command.tenantId(), command.id(), command.expectedVersion());
            throw ServiceExceptionUtil.exception(BUSINESS_PROCESSING);
        }

        Long resultId = persistResult(command, now);
        if (!xxxMapper.markSucceeded(command.id(), command.tenantId(), resultId, now)) {
            log.error("Business transaction final state write failed: tenantId={}, businessId={}, resultId={}",
                    command.tenantId(), command.id(), resultId);
            throw ServiceExceptionUtil.exception(BUSINESS_HANDLE_FAILED);
        }
        return new Result(resultId, now);
    }

    public record Command(Long tenantId, Long id, Long expectedVersion) {
    }

    public record Result(Long resultId, LocalDateTime successTime) {
    }
}
```

## 4. 测试模板

至少覆盖：

```text
Given CAS 成功且所有写入成功
When execute 被调用
Then 返回 Result 并写入最终状态

Given CAS 失败
When execute 被调用
Then 不调用 CAS 之后的远程 client 或持久化

Given 最终状态写入失败
When execute 被调用
Then 抛出领域异常
```

新增高风险边界时，至少加一个 Spring 支撑的测试：通过代理调用 Bean 并证明真实数据库写入被回滚。仅 Mockito 测试不能证明 `@Transactional` 生效。
