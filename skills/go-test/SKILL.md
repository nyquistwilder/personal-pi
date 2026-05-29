---
name: go-test
description: Go testing workflow for unit, integration, fuzz, benchmark, httptest, slogtest, race-aware, table-driven, and regression tests in greenfield modules. Use for creating, improving, validating, or reviewing Go tests.
---

# Go Test

## Rule

Test public behavior with deterministic, fast, race-free tests. Prefer the standard
`testing` package, table-driven cases, subtests, fuzzing for parsers, and benchmarks only
when performance is the contract.

## Hard Stops

Stop before writing or running tests when:

- Tests would touch production services, real secrets, live databases, user home files, or
  mutable shared infrastructure.
- Adding test dependencies such as `go-cmp`, `testcontainers-go`, `testify`, golden snapshot
  helpers, or clock libraries has not been approved or established by the project.
- The behavior contract is unknowable from code, docs, existing tests, or user request.
- Race-prone concurrency cannot be observed deterministically.

## Defaults

- Use `*_test.go`, `TestXxx`, `BenchmarkXxx`, and `FuzzXxx`.
- Put black-box tests in package `<name>_test` when exercising public APIs; use same-package
  tests only for unexported behavior that is stable and valuable to test directly.
- Prefer table tests with descriptive case names and `t.Run`.
- Use `t.Helper`, `t.Cleanup`, `t.TempDir`, and `t.Setenv`.
- Use `httptest` for HTTP servers/clients and avoid fixed ports.
- Use `testing/slogtest` for custom slog handlers.
- Use native fuzzing for parsers, decoders, normalizers, and state machines with broad input
  spaces.
- Use `go test -race ./...` for concurrency changes and before release gates when practical.

## Assertion Style

Prefer plain `if got != want { t.Fatalf(...) }` for simple values. Use `cmp.Diff` from
`go-cmp` for nested structs, slices, maps, protobuf-like data, or readable diffs. Avoid
`testify` in greenfield code unless the project has approved it; it often hides simple
control flow and adds a broad dependency.

## Boundaries

- Time: inject clocks or use explicit synchronization. Avoid sleeps as proof of correctness.
- Filesystem: use `t.TempDir`; assert permissions and paths when they are contract.
- Environment: use `t.Setenv`; do not depend on developer machine state.
- Network: use `httptest.Server` or custom `http.RoundTripper`; never call live services by
  default.
- Databases: use transaction rollbacks, temporary databases, or approved containers; never
  point at developer or production DBs.
- Subprocesses: mock command runners for unit tests; use real subprocesses only for CLI or
  process-contract tests.
- Logging: test stable fields or handlers, not decorative formatting.

## Workflow

1. Inspect existing test layout, helpers, fixtures, and wrapper commands.
2. For bugs, write or run a focused failing regression test first when practical.
3. Cover success, failure, edge cases, cancellation, and error classification.
4. Keep fixtures small and inline unless file format/path behavior is the contract.
5. Run the narrowest package test first: `go test ./path/to/pkg -run TestName`.
6. Run `go test ./...`; add `-race` for concurrency or shared-state changes.
7. Run fuzz seeds or benchmarks only when relevant.
8. Run `just check` before handing back.

## Coverage

Coverage is a signal, not the goal. Use `go test -cover ./...` when coverage policy exists
or when adding substantial code. Do not add shallow tests or exclusions only to raise a
number. Prefer mutation-resistant assertions over line coverage padding.

## Completion

Report tests added or changed, commands run, race/fuzz/benchmark choices, coverage result
when measured, and remaining untested risks.
