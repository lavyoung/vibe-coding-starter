---
name: java-unit-test-designer
description: Design Java unit test coverage before implementation. Use when planning tests for new methods, filling coverage gaps, reproducing bugs, defining refactor safety nets, or deciding which JUnit 5 techniques fit a method's complexity.
---

# Java Unit Test Designer

Design coverage intentionally instead of writing only a happy-path test.

## Classify Method Complexity First

- Mark the method as `Quick` for simple logic with few branches.
- Mark it as `Standard` for moderate branching, validation, or state changes.
- Mark it as `Complete` for complex rule combinations, workflows, or multi-step state transitions.

## Choose Test Methods By Shape

- Use equivalence classes for input validation and legal versus illegal inputs.
- Use boundary value analysis for ranges, lengths, counts, and dates.
- Use scenario-based tests for workflows and state transitions.
- Use decision-table thinking for dense condition combinations.
- Use error guessing for historically fragile or easy-to-miss cases.

## Cover More Than Happy Path

- Include at least one normal path.
- Include invalid input and sad-path cases.
- Include boundary values when numbers, counts, or lengths matter.
- Include exception behavior when the method throws or maps failures.
- Include regression reproduction first when fixing a bug.

## Recommend JUnit 5 Features Deliberately

- Use `@DisplayName` for every test with a readable Chinese goal.
- Use `@Nested` when the method has multiple flows or states.
- Use `assertAll` when one scenario needs several related assertions.
- Use `assertThrows` for exception type, error code, and message checks.
- Use `@Tag` for core, slow, or external-dependency distinctions when they help execution strategy.
- Use `@Timeout` when a test could hang or block.

## Produce A Coverage Plan

- State the method under test and its responsibility.
- State the chosen complexity level and why.
- List the test design methods you will apply.
- List the concrete scenarios to cover.
- Call out any remaining risk that cannot be covered cheaply.

## Pick A Test Layer Before Writing

- **Unit** (Mockito + JUnit 5): method logic, state machines, decisions, conversions.
- **Contract**: XML statement ids, SQL keywords, route paths, HTTP methods, enum stability — assert against reflection or the raw XML/resource string.
- **Integration** (real MyBatis + in-memory H2): real SQL aggregation correctness.
- For statistics/aggregation, correctness MUST live in integration tests; unit mocks only verify orchestration, never aggregation.

## Mocking Discipline

- When a refactor changes an internal call, update mock/verify to the new contract but keep the business assertions unchanged.
- Mockito does not run an interface `default` method's real body by default: stub the `default` method itself, not the method it calls internally.
- Test degradation where it lives: if fallback logic moves into a shared component, assert the fallback result in the consumer and test the fallback itself in that component.
- Use `verifyNoInteractions` for negative assertions (permission denied / invalid input must not reach the read model or external service).
- Use `lenient().when(...)` for common stubs (e.g. an i18n message util) so every case does not trip unused-stub errors.

## Cover More Than the Four Dimensions

Aim for at least: happy path, boundary value, sad path / exception with a stable code, and empty / null input.

- Default value + both over/under bounds (e.g. `null -> 5`, `0`/`101 -> error`).
- Every endpoint of a range or a paired-input rule (e.g. both start-only and end-only of a date pair).
- Assert error via `error.getCode()`, never a message string.

## Aggregation / Statistics-Specific Checks

- Empty-result semantics: `SELECT COUNT(*) ...` with no rows returns **one zero row**, not null — assert a zero aggregate, not null.
- Half-open ranges: insert a fact exactly at `endExclusive` and assert it is excluded.
- Same-day multiplicity: assert multiple facts on one day collapse into one row with summed counts.
- Extreme values: verify `SUM` over `long` does not overflow for values beyond `int` range.
- Isolation: include "other tenant" and "logically deleted" rows and assert they are excluded.
- Stable ordering: craft ties and assert tie-breakers plus the `LIMIT` cap.
- Independent fact times: trend aggregates by register time and first-order time separately; verify both columns.

## Test Data Construction

- Use parameterized helper methods (e.g. `insertRecord(...)`) to build rows and reduce duplication.
- Reset data per case in `@BeforeEach` (DELETE + INSERT) for isolation.
- When splicing SQL, quote time values but never `NULL`: `"NULL".equals(x) ? "NULL" : "'" + x + "'"`.

## Migrate Behavior Tests When Refactoring Into a Shared Collaborator

When duplicated logic (e.g. a tenant loop, a Redis-throttle) moves out of a Job/Service into a shared support class, tests must move to the layer that now owns the behavior.

- Move behavior tests (fail-open, empty, all-fail, boundaries) to the shared class's own test; test it with a real instance + mocked deps.
- At the consumer layer, replace `mockStatic(RedisUtils)` with mocking the new collaborator, and assert the delegation contract with exact args (key + window + scenario), not `any()`.
- Keep the short-circuit boundary: add `verify(collaborator, never()).method(...)` for the guard condition that makes the call unreachable (e.g. no anomaly).
- Delete consumer-level tests whose premise is now impossible at that layer (e.g. stubbing the collaborator to throw/null when the shared method already resolves fail-open internally — null return would NPE on unboxing).
- Job tests that call `execute()` keep passing because the support bean is a real instance; the loop now runs inside the shared method.

## Defensive Guard & Log-Behavior Tests

- For every `Objects.requireNonNull(x, "name")` guard, add an `assertThrows` test and assert the message — `assertEquals("alertKey", ex.getMessage())` — so a renamed message breaks the contract test.
- For zero/negative `Duration` validation, assert `IllegalArgumentException` and that the message contains the stable phrase (e.g. `must be positive`).
- When a branch returns a value but also emits a log, assert the log actually fires, not just the return: capture `logback` `ListAppender`, filter `ERROR/WARN` events by a stable substring, and assert exactly one.
- Assert the log is NOT emitted on the short-circuit/negative path too when the side effect matters.

## Common Pitfalls

- `hutool EnumUtil.fromString` wraps `Enum.valueOf` and throws on a miss — write a safe loop returning null/empty instead.
- `verify(mock).method(any())` and `verify(mock, never()).method(...)` cannot both target the same method in one test: `any()` matches all calls.
- After a refactor (class split / rename / signature change), update the test's mock type, constructor, and calls while keeping business assertions.
- `@AssertTrue` cannot inject i18n placeholders: for variable-bearing validation copy, converge to a parameterized ErrorCode in the service layer or use a custom annotation.
- PowerShell `Set-Content -Encoding UTF8` writes a BOM (`\ufeff`) that breaks `javac` ("非法字符") — write with `[System.IO.File]::WriteAllText(path, text, UTF8Encoding(false))`, or strip the leading BOM.
- A test file that uses explicit static imports (not a wildcard) must add each new assertion explicitly; `assertThrows`/`assertTrue` are not auto-available.
- When a refactor moves fail-open/null handling into a shared method, do not stub the shared method to return `null` at the consumer layer — a primitive return unboxes and NPEs.
