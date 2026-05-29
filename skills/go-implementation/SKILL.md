---
name: go-implementation
description: Modern Go production implementation workflow for greenfield features, refactors, package boundaries, context-aware APIs, error contracts, maintainability, and standard-library-first code. Use for day-to-day Go code changes, not primarily tests, modules, APIs, CLIs, databases, security, or performance.
---

# Go Implementation

## Rule

Implement the smallest clear production change that satisfies the behavior contract. Prefer
simple functions, small packages, explicit errors, context-aware side effects, and standard
library code over framework-first abstractions.

## Hard Stops

Ask before changing code when:

- Public API, wire format, CLI flag, HTTP route, database schema, or error contract is
  unclear or could break users.
- The change would add a dependency that stdlib or existing dependencies can satisfy.
- The change would introduce goroutines, background work, global mutable state, reflection,
  code generation, `unsafe`, or cgo without a clear lifecycle and test plan.
- Code would call live services, production databases, real secrets, or mutable user files.
- The task is primarily tests, concurrency design, module work, security, performance, API,
  CLI, database, config, observability, or release work; use the specialized Go skill.

## Design Defaults

- Keep package APIs narrow. Export only what external callers need.
- Define interfaces at the consumer boundary, not in the producer package “just in case”.
- Pass `context.Context` as the first parameter for operations that may block, do I/O, call
  services, or respect cancellation. Do not store contexts in structs.
- Return errors instead of panicking for expected failures. Use `fmt.Errorf("...: %w", err)`
  for wrapping and `errors.Is`/`errors.As` for inspection.
- Avoid sentinel errors unless callers need stable classification.
- Keep constructors explicit and avoid hidden package-level initialization.
- Keep I/O, clock, randomness, subprocesses, filesystem, and network behind small seams that
  can be tested.
- Prefer clear loops and small helpers over clever generic abstractions.
- Avoid `init` except for unavoidable registration in tests or generated integrations.

## Dependency Defaults

Use stdlib first. Approved greenfield preferences when a dependency is truly needed:

- `github.com/google/go-cmp/cmp` for complex test diffs.
- `github.com/go-chi/chi/v5` for HTTP routing only when stdlib `http.ServeMux` is not enough.
- `github.com/spf13/cobra` for multi-command public CLIs; stdlib `flag` for simple CLIs.
- `github.com/jackc/pgx/v5` for PostgreSQL drivers/pools and `database/sql` compatibility.
- `github.com/golang-migrate/migrate/v4` for migrations when SQL migrations are needed.
- OpenTelemetry packages only when an operational tracing target exists.

Do not add these speculatively.

## Workflow

1. Inspect `go.mod`, package layout, tests, and task wrappers.
2. Identify the public behavior and the narrowest package boundary to change.
3. Read nearby code and tests before introducing abstractions.
4. Add or update tests for behavior changes; defer detailed test policy to `go-test`.
5. Implement in small steps, keeping errors and side effects explicit.
6. Run `gofmt` on touched files.
7. Run targeted `go test` commands, then `go test ./...`.
8. Run `go vet`, `staticcheck` or project lint wrapper, and `just check`.

## Antipatterns

- Premature interfaces, `manager`/`service` packages without cohesive behavior, and `utils`
  packages.
- Frameworks for basic routing, config, logging, or dependency injection.
- Package-level clients, clocks, mutable config, or loggers that make tests order-dependent.
- Ignoring returned errors, string-matching errors, or logging and returning the same error
  at every layer.
- Starting goroutines without cancellation, ownership, and shutdown tests.

## Completion

Report behavior changed, public API/error impacts, dependencies added or avoided, tests and
validation commands, and remaining assumptions.
