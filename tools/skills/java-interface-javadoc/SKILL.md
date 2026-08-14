---
name: java-interface-javadoc
description: Write or improve Javadocs for Java interfaces in this repository. Use when adding interface comments, documenting method contracts, clarifying params and returns, or aligning interface-level comments with the project's Chinese Javadoc style.
---

# Java Interface Javadoc

Document interface contracts clearly enough that callers understand behavior without reading the implementation.

## Write Class Javadocs In Project Style

- Start with a short Chinese summary line.
- Add at least one `<p>1. ...</p>` line that states the interface responsibility.
- Keep `@author` in `<a href="mailto:email">name</a>` format when nearby files use it.
- Keep `@since` format consistent with nearby files.
- Match the existing spacing and star alignment used by nearby interfaces.

## Write Method Javadocs As Contracts

- State what the method does on the first line.
- Use extra `<p>` blocks only for business rules, side effects, or usage constraints.
- Add `@param` for every parameter.
- Add `@return` for every non-void method.
- Explain empty-result, nullable, and exception behavior when it matters.
- Use `{@link ...}` for enums, config keys, or related types when that helps the reader.

## Document Absence Explicitly

- Prefer `Optional<T>` when a new interface truly models absence.
- If a signature cannot change, document whether it returns `null`, an empty list, an empty map, or a partially empty object.
- Do not leave callers guessing about missing data semantics.

## Review Before Finishing

- Confirm the interface has class-level Javadoc.
- Confirm every public interface method has Javadoc.
- Confirm every parameter and non-void return is documented.
- Confirm absence and exception behavior is explicit where needed.
