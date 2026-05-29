---
name: rust-review
description: Review Rust changes for correctness, ownership, API ergonomics, error handling, unsafe boundaries, async behavior, tests, performance, features, dependency choices, and greenfield conventions. Use for review-only Rust tasks.
---

# Rust Review

## Rule

Provide actionable, evidence-backed findings prioritized by correctness, safety, public
contracts, and maintainability. Do not rewrite code unless explicitly asked.

## Review Focus

Check ownership design, lifetime complexity, public API ergonomics, error types, panic paths,
`unsafe`/FFI justification, feature flags, dependency choices, async cancellation, task
lifecycle, tests, docs, security boundaries, observability fields, and performance risks.

## Antipatterns To Flag

- `unwrap`/`expect` on user input, I/O, network, database, or request path failures.
- Public APIs overfit to internal lifetimes or expose implementation details.
- Traits with a single implementation and no clear boundary value.
- Default features that surprise library users.
- Tokio runtime creation inside libraries.
- `Arc<Mutex<_>>` used as a design shortcut.
- Unsafe blocks without local safety comments and tests/Miri evidence where practical.

## Workflow

1. Inspect the diff, `Cargo.toml`, features, tests, and nearby code.
2. Run or recommend focused checks: `cargo test`, `cargo clippy`, `cargo fmt --check`,
   `cargo deny check`, `cargo audit`, or `cargo nextest` when configured.
3. Identify blocking issues before optional style suggestions.
4. Tie findings to concrete code and explain impact.
5. Suggest small idiomatic fixes.

## Completion

Return findings by severity, validation performed or skipped, and areas not reviewed.
