---
name: go-review
description: Review Go changes for correctness, simplicity, API shape, error handling, context use, concurrency safety, tests, observability, security, performance, and module hygiene. Use for review-only Go tasks.
---

# Go Review

## Rule

Provide actionable, evidence-backed findings prioritized by correctness, safety,
maintainability, and public contracts. Do not rewrite code unless explicitly asked.

## Review Focus

Check:

- Public API, CLI, HTTP, database, and serialized contract compatibility.
- Error wrapping, classification, and caller-visible messages.
- Context propagation, timeouts, cancellation, and resource cleanup.
- Goroutine ownership, channel close rules, lock ordering, race risks, and leak risks.
- Package boundaries, exported names, interfaces, and dependency direction.
- Tests for public behavior, failure paths, race-prone code, and regressions.
- `slog` fields, redaction, and operator usefulness.
- Dependency necessity, module hygiene, licenses, and vulnerability implications.
- Performance risks such as unbounded memory, N+1 I/O, excessive allocations, or hidden
  quadratic behavior.

## Workflow

1. Inspect the diff, `go.mod`, tests, and nearby code.
2. Run or recommend focused checks when useful: `go test ./...`, `go test -race ./...`,
   `go vet`, `staticcheck`, `govulncheck`, and `just check`.
3. Separate blockers from optional improvements.
4. Tie every finding to a concrete file/line and explain impact.
5. Suggest the smallest idiomatic fix.

## Antipatterns To Flag

- Context stored in structs, ignored cancellations, or missing timeouts around I/O.
- Interfaces defined before there are multiple consumers or a test seam need.
- `panic` for ordinary errors, ignored errors, string-matched errors, or double logging.
- Global mutable clients/config/loggers that make tests order-dependent.
- Goroutines without lifecycle ownership or tests.
- Broad dependencies for tasks stdlib handles.

## Completion

Return findings by severity, include validation performed or not performed, and list areas
not reviewed.
