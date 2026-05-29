---
name: python-docs
description: Python documentation workflow for README usage, docstrings, examples, CLI help, HTTP API contracts, architecture notes, and keeping docs synchronized with tested behavior.
---

# Python Docs

## Rule

Document behavior users and maintainers need, and keep examples synchronized with code. Prefer
small executable or validated examples over prose that can drift.

Use this skill for documentation work, not for broad implementation unless docs reveal a
behavior gap the user approves fixing.

## Hard Stops

Stop and ask before changing docs when:

- Documented behavior conflicts with code/tests and the intended source of truth is unclear.
- Examples require real credentials, production endpoints, mutable user files, or sensitive
  data.
- Public API, CLI, or HTTP contract changes would be needed to make docs accurate.
- Adding a docs toolchain, publishing site, badges, or generated API docs is not explicitly
  requested.

## Documentation Defaults

- README should cover purpose, install/sync, common commands, minimal usage, tests, and
  configuration basics.
- Docstrings should explain public behavior, parameters when non-obvious, return values when
  useful, raised exceptions that callers handle, and important side effects.
- Prefer concise Google-style docstrings for greenfield personal-baseline code.
- Keep private helper docstrings rare unless they clarify complex logic.
- CLI docs should align with Typer help and stable command behavior.
- API docs should align with Pydantic models and OpenAPI behavior.

## Workflow

1. Inspect README, docs, docstrings, CLI help, API schemas, tests, and examples.
2. Identify the audience: user, contributor, operator, API client, or maintainer.
3. Verify examples against current behavior when practical.
4. Update docs close to the behavior they describe.
5. Add or update tests for examples when documentation becomes a contract.
6. Run documentation checks or relevant tests, then repository validation when appropriate.

## Examples

Prefer examples that are:

- minimal but realistic
- deterministic
- free of secrets and production endpoints
- copy/paste-safe
- covered by tests, doctests, or smoke checks when practical

## Review Guidance

Flag stale commands, undocumented configuration, examples that cannot run, misleading error
or status-code docs, missing migration notes, and docstrings that restate implementation
instead of public behavior.

## Completion

Report docs changed, behavior verified, examples tested or not tested, commands run, and any
remaining documentation gaps.
