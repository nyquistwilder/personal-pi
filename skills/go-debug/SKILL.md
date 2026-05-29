---
name: go-debug
description: Go debugging workflow for reproducing failures, panics, errors, flaky tests, data races, deadlocks, goroutine leaks, and targeted fixes with regression tests.
---

# Go Debug

## Rule

Reproduce first, identify root cause, then make the smallest targeted fix. Prefer concrete
commands, logs, traces, race detector evidence, and regression tests over speculative
rewrites.

## Hard Stops

Stop before:

- Touching live systems, real credentials, production data, or destructive operations.
- Suppressing a panic, error, race, flaky test, or linter finding without understanding the
  root cause.
- Changing public API or error semantics just to make a failure disappear.
- Adding sleeps as a concurrency fix.

## Workflow

1. Capture the failing command, input, panic, stack trace, log, race report, or hang
   symptoms.
2. Reproduce with the narrowest `go test`, executable command, or integration harness.
3. Isolate root cause with table tests, `-run`, `-count`, `-race`, `-trace`, pprof, logs,
   Delve, or targeted instrumentation.
4. For flakes, run repeated tests with `go test -count=N` and remove shared state/order
   assumptions.
5. For races/deadlocks, identify goroutine ownership, channel close responsibility,
   cancellation, and lock order.
6. Add a regression test when practical.
7. Apply a minimal fix.
8. Run the original failing command, targeted tests, `go test ./...`, relevant race checks,
   and `just check`.

## Diagnostics Defaults

- Use `GOTRACEBACK=all` or goroutine dumps for hangs.
- Use `go test -race` for shared memory bugs.
- Use `go test -run TestName -count=100` for flakes.
- Use `go test -bench ... -run '^$' -cpuprofile` only when performance is implicated.
- Add temporary logs only during investigation; remove or convert them to intentional
  `slog` diagnostics before completion.

## Completion

Report reproduction, root cause, fix, regression tests, commands run, and remaining risks or
unreproduced symptoms.
