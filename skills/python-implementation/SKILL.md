---
name: python-implementation
description: Modern Python production implementation workflow for adding features, changing behavior, refactoring modules, and designing maintainable public APIs in uv-managed src/tests projects. Use for day-to-day code changes, not primarily tests, typing, packaging, APIs, CLIs, data, or database work.
---

# Python Implementation

## Rule

Implement the smallest clear production change that satisfies the public behavior contract.
Prefer explicit boundaries, simple data models, typed interfaces, and testable design over
premature abstractions or framework-first code.

For greenfield personal-baseline work, target modern Python as of 2026: Python 3.13+, uv,
Ruff, ty, pytest, `from __future__ import annotations`, Pydantic for external validation,
`httpx` for HTTP, and clear separation between domain logic and adapters.

## Hard Stops

Stop and ask before writing code when:

- The intended behavior, public API, error contract, or compatibility requirement is unclear.
- A change may break existing public imports, CLI flags, HTTP contracts, persistence schema,
  serialized data, or documented behavior.
- The implementation would call live services, production databases, real secrets, or mutable
  user files without an explicit test and safety plan.
- A new runtime dependency seems useful but the standard library or existing dependencies
  may be enough.
- The task is primarily tests, typing, quality cleanup, packaging, security, performance,
  API, CLI, database, data, or config work; use the more specific Python skill instead.

## Design Defaults

- Keep domain logic independent from transport, CLI, database, filesystem, and network
  adapters whenever practical.
- Prefer functions and small cohesive classes over inheritance hierarchies.
- Use dataclasses for internal simple records; use Pydantic models at external input/output
  boundaries that need validation, parsing, or JSON schema.
- Prefer `pathlib.Path`, timezone-aware datetimes, `enum.StrEnum`, context managers, and
  explicit dependency injection for clocks, clients, and stores.
- Use `httpx` for new HTTP client code. Always set timeouts and avoid module-level clients
  unless lifecycle is explicitly managed.
- Raise specific exceptions with actionable messages. Do not swallow exceptions silently.
- Keep modules small enough that imports are cheap and side-effect free.

## Workflow

1. Inspect repository layout, `pyproject.toml`, task files, and existing conventions.
2. Identify the public behavior and the narrowest module boundary to change.
3. Read nearby code and tests before designing a new abstraction.
4. Add or update tests when behavior changes; defer detailed test policy to `python-test`.
5. Implement in small, reviewable steps with explicit types on public functions.
6. Keep I/O at the edges and make side-effecting boundaries injectable or mockable.
7. Run the narrowest relevant tests with uv.
8. Run lint/type checks affected by the change.
9. Run the repository validation command, normally `just check`.

## Tooling Assumptions

Assume uv-managed projects with sibling `src/` and `tests/` when working in the personal
baseline. Preserve existing wrappers such as `just check` and `mise run check`.

Do not add generated files, caches, or one-off scripts to version control. Do not introduce
new tool versions outside project configuration such as `flake.nix`.

## Review Guidance

When reviewing implementation changes, prioritize correctness, public contract stability,
readability, testability, error handling, type clarity, security boundaries, and whether the
chosen dependency or abstraction is justified.

## Completion

Before handing work back, report:

- behavior implemented or refactored
- public APIs or compatibility risks changed
- dependencies added or intentionally avoided
- tests and validation commands run
- remaining assumptions or follow-up work
