# ADR 0001: Organize Python Skills By Professional Development Workflows

- Status: Accepted
- Date: 2026-05-28

## Context

This repository stores personal, opinionated agent skill definitions. It already includes
`skills/python-test`, a focused skill for pytest-first Python testing with `uv`, sibling
`src/` and `tests/` directories, branch coverage, and repository validation.

Python development work is broader than testing. A professional workflow commonly includes
project setup, implementation, refactoring, typing, quality checks, debugging, review,
packaging, security, performance, documentation, release work, and domain-specific tasks
such as CLIs, HTTP APIs, async code, databases, configuration, observability, and data
processing.

A single broad Python skill would be easy to discover, but it would also be too large and
ambiguous. It would mix unrelated hard stops, tools, and workflows. For example, testing
requires fixture and coverage policy; packaging requires build metadata and artifact
validation; security requires threat-boundary review; performance requires measurement and
benchmarking. Combining these concerns into one skill would make activation less precise
and increase the risk that an agent applies the wrong rules to a task.

At the same time, creating very small skills for every library or framework would fragment
the repository. That would make the skill set harder to maintain and would require the agent
to choose between too many overlapping instructions.

## Decision

Develop a family of focused Python skills organized around professional development
workflows instead of one monolithic Python skill or many narrowly framework-specific skills.

The existing `python-test` skill remains the testing authority. Additional Python skills
will be added incrementally, with each skill covering a distinct task category and defining
clear activation criteria, hard stops, workflow steps, tooling expectations, and completion
requirements.

The core skill set should cover the everyday professional development loop:

1. `python-project-setup`
2. `python-implementation`
3. `python-test`
4. `python-typing`
5. `python-quality`
6. `python-debug`
7. `python-review`
8. `python-packaging`
9. `python-security`
10. `python-performance`

Specialized skills may then be added for common Python domains and operational workflows:

1. `python-cli`
2. `python-api`
3. `python-async`
4. `python-database`
5. `python-data`
6. `python-config`
7. `python-observability`
8. `python-ci`
9. `python-docs`
10. `python-release`
11. `python-dependency-management`

## Skill Responsibilities

### `python-project-setup`

Use for initializing or standardizing Python repositories. This skill should cover creating
or migrating to a sibling `src/` and `tests/` layout, configuring `pyproject.toml`, adopting
`uv`, setting up dependency groups, adding baseline test/lint/type tooling, and integrating
repository validation commands such as `just check` or `mise run check`.

This skill should not replace the generic base repository setup workflow. Instead, it should
layer Python-specific conventions on top of the repository baseline.

### `python-implementation`

Use for day-to-day production code changes: implementing features, changing behavior,
refactoring modules, adding public functions or classes, and improving design while
preserving contracts.

This skill should emphasize simple designs, public behavior, explicit boundaries, small
modules, maintainability, and testability. It should avoid prematurely adding abstractions,
frameworks, or dependencies.

### `python-test`

Use for creating, improving, validating, or reviewing tests. This skill already exists and
is responsible for pytest style, fixtures, regression tests, coverage, deterministic
boundaries, and `uv`-based test execution.

Other Python skills may require tests, but they should defer detailed test workflow rules to
`python-test` when the task is primarily test creation or test improvement.

### `python-typing`

Use for type annotation and static analysis work. This skill should cover modern Python
typing practices, public API annotations, gradual typing, protocols, generics, overloads,
`TypedDict`, `Literal`, `Self`, typed decorators, context managers, and resolving mypy or
pyright issues.

It should prefer type designs that clarify contracts without overfitting implementation
details or making ordinary code unnecessarily complex.

### `python-quality`

Use for linting, formatting, import hygiene, dead-code removal, syntax modernization, and
behavior-preserving cleanup. This skill should focus on mechanical and idiomatic code
quality, especially when resolving Ruff, formatter, or import-order findings.

It should avoid behavior changes unless the user explicitly requests them or a finding
cannot be fixed safely without a small, documented behavior-preserving refactor.

### `python-debug`

Use for investigating failures, reproducing bugs, tracing exceptions, isolating root cause,
and fixing defects. This skill should prefer a reproducible failure, a minimal failing test
or command, root-cause analysis, and then a targeted fix.

When practical, it should pair bug fixes with regression tests and avoid speculative changes
that are not tied to the observed failure.

### `python-review`

Use for reviewing Python changes without necessarily editing code. This skill should assess
correctness, maintainability, tests, typing, security, performance, public API stability,
error handling, and repository conventions.

It should prioritize actionable findings and distinguish blocking issues from optional
improvements.

### `python-packaging`

Use for packaging libraries or applications. This skill should cover `pyproject.toml` build
metadata, build backends, package discovery, dependency declarations, optional extras,
console scripts, versioning, wheels, sdists, artifact checks, and publish readiness.

It should be separate from project setup because a repository can be a valid Python project
without being a distributable package.

### `python-security`

Use for secure development and security review. This skill should cover secrets, input
validation, path traversal, command injection, unsafe deserialization, authentication and
authorization boundaries, dependency vulnerabilities, file permissions, network calls, and
safe subprocess usage.

It should treat live production systems, real secrets, and mutable user data as hard
boundaries requiring explicit approval.

### `python-performance`

Use for profiling and optimization. This skill should require measurement before and after
meaningful performance changes, prefer algorithmic improvements over micro-optimization,
and consider CPU, memory, I/O, allocation behavior, concurrency, and benchmarking
reliability.

It should avoid premature optimization and should preserve correctness with tests or
benchmarks that make regressions visible.

### `python-cli`

Use for command-line applications. This skill should cover command structure, arguments,
options, subcommands, stdout and stderr discipline, exit codes, configuration integration,
help text, shell-friendly UX, and CLI testing.

It should be framework-aware without requiring a specific CLI library. Existing project
choices such as `argparse`, Click, Typer, or custom command dispatch should be preserved
unless the user approves a change.

### `python-api`

Use for HTTP APIs and services. This skill should cover request and response contracts,
validation, structured errors, status codes, service boundaries, OpenAPI concerns,
authentication hooks, in-process test clients, and framework-specific patterns for tools
such as FastAPI, Flask, or Django.

It should keep business logic separated from transport concerns when practical.

### `python-async`

Use for async and concurrency work. This skill should cover `asyncio`, AnyIO, Trio,
structured concurrency, cancellation, timeouts, async context managers, task lifecycle,
resource cleanup, async clients, and deterministic tests.

It should be careful around event loop ownership, blocking calls inside async code, sleeps,
and cancellation safety.

### `python-database`

Use for persistence work. This skill should cover database access patterns, transactions,
connection management, migrations, SQLAlchemy or project-specific data layers, query
correctness, test databases, and avoiding accidental use of developer or production data.

It should make transaction boundaries explicit and keep tests isolated from real mutable
systems.

### `python-data`

Use for data processing. This skill should cover CSV, JSON, Parquet, pandas, Polars,
schema validation, deterministic transformations, missing or malformed data, memory-aware
processing, and reproducible ETL-style workflows.

It should prefer explicit schemas and small representative fixtures over opaque snapshots or
large checked-in datasets.

### `python-config`

Use for configuration and settings. This skill should cover environment variables, config
files, typed settings, precedence rules, defaults, test isolation, secrets, and separation
between development, test, and production environments.

It should avoid hidden global configuration that makes tests order-dependent or deployments
surprising.

### `python-observability`

Use for logging, metrics, tracing, and diagnostics. This skill should cover structured
logging, useful exceptions, correlation or request context, metrics hooks, trace spans, and
operator-friendly error messages.

It should add observability in a way that is testable and does not leak secrets.

### `python-ci`

Use for continuous integration. This skill should cover reproducible `uv` installs,
lockfile-aware jobs, lint/type/test/coverage stages, matrix testing, caching, artifacts,
security checks, and release gates.

It should preserve repository wrapper commands so local and CI validation remain aligned.

### `python-docs`

Use for Python documentation. This skill should cover README usage, API documentation,
docstrings, examples, CLI help, HTTP API contracts, architecture notes, and keeping docs in
sync with behavior.

It should prefer executable or validated examples when possible.

### `python-release`

Use for release preparation and publishing. This skill should cover version bumps,
changelogs, tags, release notes, wheel and sdist validation, publishing safeguards, and
post-release verification.

It should be explicit about irreversible operations and require approval before publishing
or tagging when those operations affect remote systems.

### `python-dependency-management`

Use for adding, removing, upgrading, or evaluating Python dependencies. This skill should
cover `uv` commands, lockfile updates, dependency groups, optional extras, conflict
resolution, minimal dependency choices, vulnerability awareness, and reproducibility.

It should avoid adding dependencies when the standard library or existing project
dependencies are sufficient.

## Activation Rules

Each skill should have a narrow description so the agent activates it only for relevant
requests. When a task crosses skill boundaries, prefer the skill matching the primary user
intent. Examples:

- A request to add tests uses `python-test`, even if small production changes are needed for
  testability.
- A request to fix mypy errors uses `python-typing`, even if it requires minor code cleanup.
- A request to investigate a failing command uses `python-debug`, even if the final fix adds
  a regression test.
- A request to prepare a package for PyPI uses `python-packaging` or `python-release`, not
  `python-project-setup`.
- A request to review a Python diff uses `python-review`, not every specialized skill at
  once.

Skills should avoid duplicating detailed instructions from each other. They may reference
neighboring responsibilities, but the canonical workflow should live in the most specific
skill.

## Implementation Plan

Add skills incrementally in priority order:

1. Keep and refine `python-test`.
2. Add the core workflow skills: `python-project-setup`, `python-implementation`,
   `python-typing`, `python-quality`, `python-debug`, and `python-review`.
3. Add distribution and risk skills: `python-packaging`, `python-security`, and
   `python-performance`.
4. Add domain and operations skills as real tasks require them: `python-cli`, `python-api`,
   `python-async`, `python-database`, `python-data`, `python-config`,
   `python-observability`, `python-ci`, `python-docs`, `python-release`, and
   `python-dependency-management`.

Each new skill should include:

- frontmatter with `name` and an activation-focused `description`
- a concise rule or purpose statement
- hard stops for unsafe or ambiguous work
- a workflow checklist
- project layout and tooling assumptions
- completion requirements
- review guidance when applicable

## Consequences

### Positive

- Skill activation becomes more precise.
- Each skill can contain stronger, task-specific hard stops.
- The existing `python-test` skill remains focused and does not become a catch-all.
- Future Python workflows can be added without rewriting a monolithic instruction file.
- The repository will better reflect real professional Python development responsibilities.
- Reviews and maintenance are easier because each skill has a clear boundary.

### Negative

- More skill files must be created and maintained.
- Some tasks will cross skill boundaries and require judgment about the primary intent.
- Naming and descriptions must be kept precise to avoid overlapping activation.
- Shared conventions may drift if repeated across many skills.

### Mitigations

- Add skills incrementally instead of all at once.
- Keep descriptions narrow and activation-oriented.
- Avoid duplicating detailed guidance between skills.
- Use ADRs and shared references when a convention applies across multiple Python skills.
- Periodically review the skill set for overlap, obsolete guidance, and missing workflows.

## Alternatives Considered

### One monolithic `python` skill

A single broad Python skill would be easy to find and could centralize all conventions.
However, it would become long, hard to maintain, and less precise. It would mix unrelated
instructions for testing, typing, packaging, APIs, CLIs, security, and performance. This
would increase the chance of applying irrelevant rules to simple tasks.

This alternative is rejected.

### Only keep `python-test`

Keeping only the existing test skill avoids maintenance cost, but it leaves no captured
workflow for many recurring Python tasks. Agents would need to infer project preferences for
implementation, typing, packaging, review, and other professional activities.

This alternative is rejected.

### Create framework-specific skills first

Framework-specific skills such as `python-fastapi`, `python-django`, `python-sqlalchemy`,
or `python-pandas` could be useful later. Starting there would prematurely fragment the
repository and would not capture framework-agnostic Python practices.

This alternative is deferred. Framework-specific skills may be added later when repeated
work justifies them.

## Related Work

- `skills/python-test/SKILL.md`
- `skills/base-repo-setup/SKILL.md`
