---
name: java-distributed-lock
description: Design, implement, refactor, or review distributed locking in a multi-instance Java service. Use when touching Redis lock keys, account or user balance concurrency, mobile locks, nested locks, lock ordering, watchdog renewal, lock release, batch locking, or database CAS alternatives.
---

# Java Distributed Lock

Reuse the project lock infrastructure and prove the concurrency invariant before adding a lock.

## 1. Select the existing capability

Use this order:

1. Use a declarative public-method lock annotation (for example `@Lock4j`) for a simple lock whose key can be expressed from method arguments.
2. Use the project's programmatic lock helper (for example `RedisUtil#executeWithLock(...)`) for programmatic scope, custom business exceptions, return values, or explicit acquisition waiting.
3. If neither entry supports a required behavior, add the smallest reusable overload to the project's lock util.

Do not add a new lock-manager abstraction, a domain-specific copy of the same abstraction, or direct scattered Redisson code.

A custom-exception programmatic overload may pass lease time `-1` to the underlying Redisson executor, use a bounded acquisition wait, release in `finally`, and log unlock failures without replacing the business result. Treat watchdog renewal as verified only for the overload and its tests; do not generalize it to older fixed-lease overloads or annotations without inspecting their configuration.

## 2. Define the protected resource and canonical key

Write the invariant first. The lock key must represent the resource, not the caller or operation.

- All mutations of the same protected resource (for example a user balance account) must use the same key domain, such as `tenantId + userId`.
- Build the key through the project's key constants class (for example `RedisKeyConstants`); do not duplicate string formats.
- Do not create separate "credit," "debit," "refund," or "reward" locks for the same resource.
- Use a tenant-plus-digest lock only before a stable resource ID exists or to close a registration race. Never place plaintext identifiers (for example mobile numbers) in Redis keys or logs.

If a future scope policy changes, change the resource-scope policy and key strategy deliberately; do not silently append one dimension to one path while other paths remain at the old scope.

## 3. Prevent nested-lock deadlocks

Inventory every path that can acquire more than one lock and produce a lock-order table.

- Prefer one canonical resource lock.
- If two locks are unavoidable, use one global acquisition order in every path.
- Never acquire lock A then lock B in one path and B then A in another.
- Do not hold a broad activity/batch lock while waiting for a resource lock, remote call, or item transaction.
- Release the first lock before switching identity domains when correctness allows it; otherwise encapsulate the common acquisition order in one helper.

Do not call a deadlock impossible because lock waits are bounded. A timeout limits duration but still causes failures and throughput collapse.

## 4. Prefer database CAS for database invariants

Use database CAS/unique constraints when the contested fact is already a single-row or indexed database invariant:

- distributed quantity and upper/lower bounds;
- versioned status transitions;
- idempotent unique records.

Keep the resource lock when multiple reads/writes must be serialized across rows or stores, with version CAS as the database safety net. Do not use a distributed lock as a substitute for missing transactional or unique constraints.

## 5. Keep lock and transaction boundaries small

- Resolve request context and perform non-critical remote prefetch before locking.
- Acquire the distributed lock outside the Spring database transaction.
- Enter a proxy-backed short transaction inside the lock.
- Do not wrap a whole batch, N remote calls, or multiple independent item transactions in one lock.
- Preserve original lock-competition behavior and error mapping unless a reviewed requirement changes it.

## 6. Verify behavior, not comments

Add tests for:

- exact key and acquisition timeout;
- lock-unavailable mapping;
- return value and exception propagation;
- release after success and failure;
- unlock failure not replacing the business outcome;
- watchdog lease argument for the selected overload;
- same-resource paths using the same key;
- canonical nested-lock order;
- concurrent CAS loss and idempotency;
- batch throughput or remote-call count when many items miss prefetch.

Use a real Redis/multi-process test for claims about cross-instance renewal or deadlock behavior when release readiness depends on it. Unit tests may verify call contracts but must not be reported as full distributed proof.
