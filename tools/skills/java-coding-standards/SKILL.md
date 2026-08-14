---
name: java-coding-standards
description: Apply shared Java service coding conventions for Spring Boot code. Use when creating or editing Java classes, records, services, repositories, exceptions, and tests that need consistent naming, immutability, Optional handling, logging, and package layout.
---

# Java Coding Standards

Write clear, maintainable Java 17+ code and prefer simple, explicit structures over clever shortcuts.

## Apply These Defaults

- Prefer clarity over compactness.
- Prefer immutable data and `final` fields where practical.
- Prefer records for small immutable carriers when the surrounding project style allows them.
- Prefer descriptive names for classes, methods, fields, and constants.
- Prefer domain-specific exceptions over broad generic failures.

## Name Things Consistently

- Use `PascalCase` for classes, interfaces, enums, and records.
- Use `camelCase` for methods and fields.
- Use `UPPER_SNAKE_CASE` for constants.
- Keep package names lowercase and purpose-driven.

## Handle Data Safely

- Return `Optional<T>` from lookup-style methods when absence is part of the contract.
- Do not use `Optional` for fields, DTO properties, or method parameters.
- Avoid `null` as a hidden business signal.
- Use Bean Validation for request inputs when the call boundary supports it.

## Keep Methods Focused

- Keep methods short and single-purpose.
- Extract private helpers when branching or transformation steps start to blur intent.
- Prefer early returns over deep nesting.
- Replace magic numbers and strings with named constants or enums.

## Use Collections And Streams Carefully

- Use streams for short, readable transformations.
- Switch back to loops when a stream pipeline becomes nested or stateful.
- Prefer immutable collection factories such as `List.of()` when data should not change.
- Avoid raw types; keep generics explicit.

## Log And Throw Intentionally

- Log important identifiers and business context.
- Avoid swallowing exceptions.
- Wrap technical exceptions with useful domain context when rethrowing.
- Keep log messages searchable and structured.

## Keep Files Predictable

- Keep one public top-level type per file.
- Keep member order stable: constants, fields, constructor, public methods, then private helpers.
- Mirror `src/main/java` structure under `src/test/java`.
