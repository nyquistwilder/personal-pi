---
name: python-typing
description: Python static typing workflow for adding annotations, designing typed APIs, resolving ty/mypy/pyright findings, and modernizing type hints in uv-managed src/tests projects without overcomplicating implementation.
---

# Python Typing

## Rule

Use types to clarify contracts and catch real defects. Prefer modern, readable annotations
that describe public behavior without exposing unnecessary implementation detail.

For greenfield personal-baseline projects, annotate public functions, methods, dataclass and
Pydantic fields, context managers, decorators, and async boundaries. Keep private local code
simple unless inference is poor or static analysis needs help.

## Hard Stops

Stop and ask before changing typing when:

- The runtime contract is unclear or type changes may alter public API compatibility.
- Fixing a type error requires behavior changes rather than annotations or small safe
  refactors.
- A dependency lacks type information and the choice is between adding stubs, ignoring, or
  replacing the dependency.
- The project's canonical checker is unclear and adding ty, mypy, pyright, or stub packages
  would change project policy.
- The task is primarily implementation, tests, quality cleanup, or generated API schema work;
  use the more specific skill.

## Modern Typing Defaults

- Prefer built-in generics: `list[str]`, `dict[str, int]`, `tuple[str, ...]`.
- Prefer `X | None` over `Optional[X]` and `A | B` over `Union[A, B]`.
- Use `typing.Self`, `Literal`, `Final`, `ClassVar`, `Protocol`, `TypedDict`, `TypeGuard` or
  `TypeIs` when they clarify a real contract.
- Use `collections.abc` for abstract containers and callables.
- Use `Protocol` for structural dependencies instead of concrete classes when testing or
  adapter boundaries benefit.
- Use `@overload` only when callers receive meaningfully different return types.
- Use `TypeVar`, `ParamSpec`, and `Concatenate` for generic decorators and wrappers.
- Avoid `Any`. If unavoidable, keep it at the boundary and narrow it quickly.
- Do not add broad `# type: ignore` comments. Use the narrowest code and include a reason
  when the checker supports one.

## Pydantic And Data Models

Use Pydantic for external validation boundaries, not as a replacement for every internal
record. Annotate fields precisely and prefer explicit defaults.

- Use `BaseModel` for validated external input/output.
- Use `Field(...)` for constraints, aliases, descriptions, and default factories.
- Use `Annotated[...]` when constraints or metadata improve schema clarity.
- Keep domain types stable even if transport schemas change.

## Workflow

1. Inspect `pyproject.toml`, lockfile, and wrapper commands to identify the configured type
   checker. In the personal baseline, prefer `uv run --group type ty check`.
2. Run the narrowest relevant type check to reproduce findings.
3. Read public API usage, tests, and docs before changing annotations.
4. Add or refine annotations at public boundaries first.
5. Use small behavior-preserving refactors when needed to make types honest.
6. Re-run the narrow type check, then the repository validation command.

## Review Guidance

Flag types that are misleading, too broad, too narrow, dependent on private implementation,
or hiding defects through `Any`, casts, or ignores. Prefer contracts that help callers and
future maintainers.

## Completion

Report type checker commands run, findings resolved, public API typing changes, any ignores
or casts added with reasons, and checks not run.
