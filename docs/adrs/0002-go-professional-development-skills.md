# ADR 0002: Organize Go Skills By Greenfield Professional Development Workflows

- Status: Accepted
- Date: 2026-05-29

## Context

This repository stores personal, opinionated agent skill definitions. The Python skill set
establishes a useful pattern: define focused skills around professional development
workflows rather than one large language skill. Go development has similar recurring work:
new project setup, production implementation, tests, quality checks, debugging, review,
module and dependency work, security, performance, command-line tools, HTTP services,
concurrency, databases, configuration, observability, CI, documentation, and releases.

The intended scope for the Go skills is greenfield development only. Greenfield projects can
use modern defaults without preserving legacy layouts, old module policies, or deprecated
libraries. This makes the skills stricter and more useful: prefer standard-library-first
solutions, small packages, explicit interfaces at consumer boundaries, context-aware APIs,
structured logging with `log/slog`, conventional Go testing, reproducible module usage,
and simple deployment-friendly binaries.

A monolithic `go` skill would be discoverable but too broad. It would mix unrelated rules
for concurrency safety, module publishing, HTTP contracts, database migrations, and release
operations. Very narrow framework-specific skills would also be premature because greenfield
Go work should start with standard library and project conventions before choosing optional
frameworks.

## Decision

Create a family of focused Go skills organized by workflow and domain. Each skill should
include narrow activation criteria, hard stops, a practical workflow, greenfield defaults,
validation expectations, and completion reporting.

Core workflow skills:

1. `go-project-setup`
2. `go-implementation`
3. `go-test`
4. `go-quality`
5. `go-debug`
6. `go-review`
7. `go-modules`
8. `go-security`
9. `go-performance`

Specialized greenfield skills:

1. `go-cli`
2. `go-api`
3. `go-concurrency`
4. `go-database`
5. `go-config`
6. `go-observability`
7. `go-ci`
8. `go-docs`
9. `go-release`

## Skill Responsibilities

### `go-project-setup`

Use for creating brand-new Go modules after the repository baseline exists. It owns module
layout, `go.mod`, `go.sum`, command and internal package skeletons, baseline tests,
`justfile` integration, lint/test/build recipes, and minimal documentation.

### `go-implementation`

Use for day-to-day production code: features, refactors, package boundaries, public APIs,
error contracts, and maintainability. It should prefer small packages, simple composition,
context-aware side-effecting APIs, and standard-library-first code.

### `go-test`

Use for tests, benchmarks, fuzz tests, table-driven cases, `httptest`, `testing/slogtest`,
`testcontainers` only when justified, race detection, coverage, and deterministic test data.

### `go-quality`

Use for `gofmt`, `go vet`, `staticcheck`, `golangci-lint`, import hygiene, dead-code
cleanup, and behavior-preserving modernization.

### `go-debug`

Use for reproducing failures, tracing panics and errors, data races, deadlocks, flaky tests,
and targeted fixes with regression tests.

### `go-review`

Use for reviewing Go diffs for correctness, simplicity, API shape, concurrency safety,
error handling, observability, tests, and module hygiene.

### `go-modules`

Use for adding, removing, upgrading, replacing, or auditing module dependencies and for
module path or workspace decisions.

### `go-security`

Use for secure Go development and review: secrets, path traversal, command execution,
networking, TLS, auth boundaries, deserialization, dependency vulnerabilities, and safe
filesystem/database behavior.

### `go-performance`

Use for profiling, benchmarks, allocation analysis, CPU/memory optimization, pprof,
trace, race-aware concurrency changes, and before/after measurement.

### `go-cli`

Use for command-line tools: command shape, flags, environment integration, stdout/stderr,
exit codes, shell-friendly UX, and CLI tests.

### `go-api`

Use for HTTP APIs and services: routing, handlers, middleware, validation, status codes,
structured errors, OpenAPI concerns, auth hooks, and service boundary tests.

### `go-concurrency`

Use for goroutines, channels, mutexes, contexts, cancellation, worker pools, pipelines,
timeouts, lifecycle management, and race-free shutdown.

### `go-database`

Use for persistence: `database/sql`, transactions, migrations, query correctness, test
databases, generated query tools when approved, and data isolation.

### `go-config`

Use for configuration: flags, environment variables, config files, precedence rules,
typed config structs, validation, secrets, and test isolation.

### `go-observability`

Use for logging, metrics, tracing, diagnostics, health checks, pprof endpoints, and
operator-friendly errors without leaking secrets.

### `go-ci`

Use for CI: reproducible toolchains, module cache, lint/test/race/build/security jobs,
artifacts, and release gates aligned with local `just check`.

### `go-docs`

Use for documentation: README, package docs, examples, CLI help, API contracts, diagrams,
and keeping docs synchronized with behavior.

### `go-release`

Use for release preparation: versioning, changelog, tags, goreleaser or equivalent when
approved, checksums, SBOMs, container images, and post-release verification.

## Activation Rules

Use the skill matching the user's primary intent. Testing requests use `go-test`; lint-only
requests use `go-quality`; race/deadlock tasks use `go-concurrency` or `go-debug` depending
on whether the user asks for design or investigation; dependency tasks use `go-modules`.
Skills may reference adjacent concerns but should not duplicate their full workflows.

## Consequences

The Go skill set will be more maintainable and precise than a single broad skill. The cost
is more files and the need to keep shared conventions aligned. Greenfield-only scope reduces
ambiguity and lets the skills be opinionated about modern Go defaults.

## Alternatives Considered

A single `go` skill was rejected as too broad. Framework-specific skills such as
`go-chi`, `go-gin`, `go-cobra`, or `go-sqlc` are deferred until repeated work justifies
them. Legacy migration skills are out of scope for this greenfield set.

## Related Work

- `docs/adrs/0001-python-professional-development-skills.md`
- `skills/base-repo-setup/SKILL.md`
