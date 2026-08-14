---
name: java-spring-openapi-doc-generator
description: Generate or improve Spring Boot API definition-layer code and OpenAPI 3 annotations in this repository. Use when creating Controller endpoint skeletons, request/response objects, enum validation, i18n validation messages, Swagger annotations, or front-end mock responses from an accepted version design document.
---

# Java Spring OpenAPI Doc Generator

Generate API definition-layer code so callers can understand and integrate the contract without reading service implementation code.

## Input Document Gate

- Prefer an accepted/effective/landed version design, API contract, or task document as the source of truth.
- Before generating code, distinguish "new endpoint" from "existing endpoint change".
- Extract at least: controller package, controller name, `@Tag`, `@RequestMapping`, HTTP method, request JSON example, response JSON example, and whether the endpoint is new or modified.
- If the source document is missing key contract details, state the missing fields before implementing instead of inventing business semantics.

## API Definition Phase Scope

When the user says the current stage is only API definition / table design / front-end contract scaffolding, stay within:

- `controller`
- `request`
- `response`
- `dto`
- `enum`
- validation i18n files under `resources/i18n/validation_message*.properties`
- API examples and explanatory text in the source design document when explicitly requested

Do not implement these unless the user explicitly asks:

- `service` or `service.impl`
- complex statistics or aggregation logic
- transaction orchestration
- remote calls
- MQ / Job / Listener
- real data backfill scripts

## Document Controllers

- Add `@Tag` with a concise module name and one-sentence description.
- Add `@Operation` for each endpoint.
- Keep `summary` short and action-oriented.
- Use a text block for `description` when the endpoint needs rules, examples, enum meanings, or response notes.
- Use the project route prefix through the existing constants class (for example `SharedCarWashConstants.PREFIX`).
- Check existing controllers before adding routes; do not create duplicate `HTTP Method + Path` mappings.
- Keep method signatures, request types, response types, and route semantics complete even when the method body is temporary.

## Document Parameters

- Add `@Parameter` for important path and query parameters.
- Use real examples, not placeholders such as `123`, `xxx`, or `foo`.
- Mark required parameters explicitly.
- Explain enum or status values in Chinese when the caller needs them.

## Document DTOs And VOs

- Add class-level `@Schema(description = "...")`.
- Add field-level `@Schema` with at least `description` and `example`.
- Add `requiredMode = REQUIRED` for required fields when appropriate.
- Add `allowableValues` for enum-like string fields.
- Put request objects under the existing `model.request.xxx` style package and response objects under `model.response.xxx` unless nearby code uses a different established pattern.
- For `LocalDateTime` fields, use 13-digit millisecond timestamp examples when the project web starter serializes `LocalDateTime` as milliseconds; match the convention proven by nearby fields.
- Do not use formatted date-time string examples such as `2026-05-12 08:00:14` for `LocalDateTime` API fields when the project serializes milliseconds.
- For amount fields, follow the existing interface-layer convention: response values are usually `BigDecimal` yuan; DO/database fields are usually integer/long cents.
- For page endpoints, use request types that inherit the project page-request base class (for example `WebPageRequest`) and response shapes based on the project page wrapper (for example `PageResult<T>`).

## Validation, I18n, And Enums

- Do not hard-code Chinese validation messages in annotations.
- Validation messages must reference i18n keys, for example `@NotNull(message = "{profit.share.account.id.not.null}")`.
- When adding validation keys, update all project validation bundles: the default plus every maintained locale (for example `validation_message.properties`, `validation_message_zh_CN.properties`, `validation_message_zh_TW.properties`, and `validation_message_en_US.properties`).
- For enum-like request fields, prefer adding or reusing an enum and validate with the framework's enum-validation annotations (for example `@InEnum` or `@StringInEnum`); do not rely only on comments such as `1-xxx, 2-yyy`.
- Integer enums should implement the valuable-array interface (for example `IntArrayValuable`) and string enums the string variant (for example `StringArrayValuable`) when the project framework provides them.

## Front-End Mock Response Boundary

If the user explicitly needs front-end integration before real business implementation, prefer temporary controller-direct mock responses.

- Use this only for newly added endpoints or the current version's newly added endpoint group.
- Do not enter service, mapper, statistics, or remote-call logic.
- Do not introduce a mock framework.
- Build response objects directly in the controller and return the standard project wrapper.
- Page endpoints must return at least one realistic example row unless the design document explicitly requires an empty result.
- Keep list/detail examples consistent for the same business ids, organization ids, account ids, and timestamps.
- Use private `mockXxx()` helper methods inside the controller when examples would otherwise clutter endpoint methods.

## Keep The Output Useful

- Explain validation rules for write operations.
- Add request examples for body-based POST or PUT endpoints.
- Add response structure notes when callers would otherwise misread nested data.
- Mark i18n-sensitive display fields when the value shown to users depends on language context.
- Keep JSON examples in documents copyable: do not use `//` comments inside JSON blocks; prefer `_comment_xxx` fields or surrounding prose.

## Review Before Finishing

- Confirm each endpoint has `@Operation`.
- Confirm each DTO or VO field that matters to callers has `@Schema`.
- Confirm examples are realistic and formatted consistently.
- Confirm enum, status, and validation semantics are visible to API consumers.
- Confirm request/response fields match the source design examples.
- Confirm there is no duplicate `HTTP Method + Path` route.
- Confirm all `LocalDateTime` `@Schema(example)` values match the project serialization convention (13-digit millisecond timestamps when the web starter serializes milliseconds).
- Confirm enum request fields have enum validation where appropriate.
- Confirm validation i18n keys exist in all required validation bundles.
