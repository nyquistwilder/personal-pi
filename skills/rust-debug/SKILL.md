---
name: rust-debug
description: Rust debugging workflow for reproducing failures, panics, compiler diagnostics, trait/borrow errors, flaky tests, async hangs, deadlocks, and targeted fixes with regression tests.
---

# Rust Debug

## Rule

Reproduce first, identify root cause, then make the smallest targeted fix. Prefer compiler
diagnostics, tests, backtraces, and tracing evidence over broad rewrites.

## Hard Stops

Stop before:

- Touching live systems, real secrets, production data, or destructive operations.
- Adding `unsafe`, changing public APIs, or weakening error contracts solely to silence an
  error.
- Suppressing panics, Clippy findings, or test flakes without understanding root cause.
- Fixing async hangs with sleeps or unbounded timeouts.

## Workflow

1. Capture failing command, panic, compiler diagnostic, backtrace, log, race/deadlock symptom,
   or hang.
2. Reproduce with the narrowest `cargo test`, `cargo check`, or executable command.
3. Isolate root cause using `RUST_BACKTRACE=1`, targeted tests, Clippy, `dbg!`/temporary
   tracing, Miri for unsafe/suspicious UB, sanitizers when configured, or `tokio-console` for
   async runtime issues.
4. Add a regression test when practical.
5. Apply a targeted fix and remove temporary diagnostics.
6. Run the original failing command, targeted tests, full tests, Clippy, and `just check`.

## Completion

Report reproduction, root cause, fix, regression tests, commands, and remaining risks.
