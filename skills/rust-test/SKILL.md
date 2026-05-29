---
name: rust-test
description: Rust testing workflow for unit, integration, doc, snapshot, property, async, regression, and coverage-aware tests in greenfield Cargo projects. Use for creating, improving, validating, or reviewing Rust tests.
---

# Rust Test

## Rule

Test public behavior with deterministic tests. Prefer unit tests near implementation,
integration tests for crate behavior, doctests for documented examples, and regression tests
for bugs.

## Hard Stops

Stop before:

- Tests touch production services, real secrets, user files, live databases, or shared
  mutable infrastructure.
- Adding test dependencies such as `insta`, `proptest`, `quickcheck`, `testcontainers`,
  `wiremock`, `mockall`, or Tokio test utilities without approval or project precedent.
- Snapshot tests would hide unclear behavior instead of documenting an intentional contract.
- Async or concurrency tests rely on sleeps rather than deterministic synchronization.

## Defaults

- Use `#[test]`, module-level unit tests, `tests/*.rs` integration tests, and doctests.
- Use `#[tokio::test]` only for Tokio projects; keep runtime features explicit.
- Use `tempfile` when filesystem isolation is needed and approved.
- Use `assert_eq!`/`matches!` and meaningful failure messages; avoid over-broad snapshots.
- Use `insta` only for stable structured output where focused assertions are worse.
- Use `proptest` for parsers, serializers, normalizers, and invariant-heavy code.
- Use `wiremock` or local `axum`/`hyper` test servers for HTTP clients; never call live
  services by default.
- Use `cargo-nextest` when already configured; otherwise `cargo test` is the baseline.

## Workflow

1. Inspect existing tests, features, fixtures, and wrapper commands.
2. For bugs, write or run a focused failing regression test first when practical.
3. Cover success, failure, edge cases, cancellation, and public error behavior.
4. Keep fixtures small and local; use files only when file format/path behavior is contract.
5. Run targeted `cargo test <name>` or package-specific tests.
6. Run full `cargo test --all-targets --all-features` or project wrapper.
7. Run doctests, async tests, property seeds, snapshots, or coverage only when relevant.
8. Run `just check` before handing back.

## Coverage

Use `cargo llvm-cov` only when configured or approved. Coverage is a signal; do not add weak
assertions or test-only branches to raise a number. Prefer assertions that would fail for
real regressions.

## Completion

Report tests added, commands run, async/snapshot/property/container choices, coverage result
when measured, and remaining untested risk.
