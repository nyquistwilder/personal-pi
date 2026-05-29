---
name: python-dependency-management
description: Python dependency management workflow for adding, removing, upgrading, evaluating, and locking dependencies with uv groups, optional extras, conflict resolution, vulnerability awareness, and minimal dependency choices.
---

# Python Dependency Management

## Rule

Add or change dependencies deliberately. Prefer the standard library or existing dependencies
when sufficient, keep runtime dependencies minimal, and use uv to maintain reproducible
lockfiles.

Use this skill when dependency changes are the primary task.

## Hard Stops

Stop and ask before changing dependencies when:

- The dependency's purpose, runtime vs dev/test group, optional-extra contract, or version
  policy is unclear.
- A change may affect public install requirements, package size, licenses, security posture,
  or deployment compatibility.
- Resolving conflicts would require removing or downgrading unrelated packages.
- The project does not use uv and migration is not in scope.
- A dependency would be used for secrets, crypto, auth, database, network, or data processing
  and risk/maintenance has not been considered.

## Dependency Defaults

- Use `uv add` and `uv remove` rather than hand-editing dependency lists when possible.
- Keep tool dependencies in PEP 735 dependency groups such as `test`, `lint`, `type`, and
  `dev`.
- Keep runtime dependencies in `[project].dependencies` only when imported by production
  code.
- Use optional dependencies/extras for optional integrations that are part of install
  contracts.
- Keep direct dependencies sorted when hand editing.
- Commit lockfile changes with dependency changes.
- Do not pin broad runtime dependencies unnecessarily in `pyproject.toml`; rely on `uv.lock`
  for exact reproducibility unless compatibility requires bounds.

## Approved Greenfield Preferences

When the need is real and approved, prefer these libraries for new personal-baseline work:

- Pydantic for external validation and settings boundaries
- FastAPI for HTTP APIs
- Typer for CLIs
- SQLModel for typed relational persistence when appropriate
- Polars, PyArrow, and DuckDB for data processing/analytics
- OpenTelemetry libraries for telemetry integrations when an operational target is known
- httpx for HTTP clients
- Rich for terminal rendering when plain output is insufficient

Do not add these libraries speculatively.

## Workflow

1. Identify why the dependency is needed and whether existing code can satisfy the need.
2. Classify dependency scope: runtime, optional extra, test, lint, type, docs, build, or dev.
3. Check project policy, license/security/maintenance concerns, and compatibility.
4. Use uv to add/remove/upgrade and update the lockfile.
5. Run relevant import/tests for the feature and repository validation.
6. Document new user-facing dependencies or optional extras when applicable.

## Useful Commands

```sh
uv add <package>
uv add --group test <package>
uv remove <package>
uv lock --upgrade-package <package>
uv sync --group dev
```

Adjust group names to the repository convention.

## Completion

Report dependencies changed, why they are needed, scope/group, lockfile updates, commands
run, and any license/security/compatibility concerns.
