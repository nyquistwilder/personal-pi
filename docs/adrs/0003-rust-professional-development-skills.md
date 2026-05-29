# ADR 0003: Organize Rust Skills By Greenfield Professional Development Workflows

- Status: Accepted
- Date: 2026-05-29

## Context

This repository stores personal, opinionated agent skill definitions. The Python skill set
shows that focused workflow skills activate better than one monolithic language skill. Rust
projects have their own recurring professional workflows: project setup, implementation,
tests, quality tooling, debugging, review, crates and dependency management, security,
performance, command-line applications, HTTP services, async systems, database access,
configuration, observability, CI, documentation, and releases.

The Rust skills target greenfield projects only. That allows modern defaults: stable Rust,
Edition 2024 for new crates when supported by the selected toolchain, explicit MSRV policy,
Cargo-first workflows, `rustfmt`, Clippy with project-approved lints, strong error types,
feature flags used deliberately, `tracing` for diagnostics, `tokio` only when async is
needed, and safe Rust by default. Unsafe code, FFI, global mutable state, and irreversible
release operations require explicit approval.

A single `rust` skill would be easy to discover but would combine unrelated instructions for
borrow-checker design, async cancellation, crate metadata, database migrations, cargo
features, unsafe review, and release publishing. Starting with framework-specific skills
would also be premature because greenfield Rust should first establish crate boundaries,
validation commands, and library/application conventions.

## Decision

Create a family of focused Rust skills organized by workflow and domain. Each skill should
include narrow activation criteria, hard stops, greenfield defaults, workflow steps,
validation expectations, and completion reporting.

Core workflow skills:

1. `rust-project-setup`
2. `rust-implementation`
3. `rust-test`
4. `rust-quality`
5. `rust-debug`
6. `rust-review`
7. `rust-crates`
8. `rust-security`
9. `rust-performance`

Specialized greenfield skills:

1. `rust-cli`
2. `rust-api`
3. `rust-async`
4. `rust-database`
5. `rust-config`
6. `rust-observability`
7. `rust-ci`
8. `rust-docs`
9. `rust-release`

## Skill Responsibilities

### `rust-project-setup`

Use for creating brand-new Rust crates or workspaces after the repository baseline exists.
It owns `Cargo.toml`, workspace shape, `src/`, tests, examples when requested, lint/test
recipes, README stubs, and validation wiring.

### `rust-implementation`

Use for production code changes: features, refactors, ownership design, trait boundaries,
error handling, public APIs, and maintainability.

### `rust-test`

Use for unit, integration, doc, snapshot, property, and async tests; test fixtures; coverage
when configured; deterministic behavior; and regression tests.

### `rust-quality`

Use for `cargo fmt`, Clippy, import/module cleanup, warning fixes, dead-code removal,
edition-idiom modernization, and behavior-preserving cleanup.

### `rust-debug`

Use for reproducing failures, panics, borrow/trait errors, flaky tests, deadlocks, async
hangs, and targeted fixes with regression tests.

### `rust-review`

Use for reviewing Rust diffs for correctness, API ergonomics, ownership, error handling,
unsafe boundaries, tests, performance risks, features, and dependency choices.

### `rust-crates`

Use for adding, removing, upgrading, or auditing dependencies, Cargo features, workspace
inheritance, MSRV compatibility, lockfile policy, and publish metadata.

### `rust-security`

Use for secure Rust development and review: secrets, unsafe code, FFI, command execution,
path handling, deserialization, auth boundaries, TLS, dependency advisories, and supply
chain risk.

### `rust-performance`

Use for benchmarking, profiling, allocation analysis, algorithmic optimization, Criterion,
flamegraphs, async runtime overhead, and before/after measurement.

### `rust-cli`

Use for command-line applications: clap command shape, args, env integration, stdout/stderr,
exit codes, completions, config integration, and CLI tests.

### `rust-api`

Use for HTTP APIs and services: Axum or project-selected framework, request/response
contracts, validation, status codes, structured errors, auth hooks, OpenAPI concerns, and
service tests.

### `rust-async`

Use for async Rust: Tokio, futures, cancellation, timeouts, task lifecycle, channels,
streams, `Send`/`Sync` boundaries, shutdown, and deterministic async tests.

### `rust-database`

Use for persistence: SQLx or project-selected access, migrations, transactions, pooling,
query correctness, test databases, and isolation from real data.

### `rust-config`

Use for typed configuration: env vars, files, CLI overrides, defaults, validation, secrets,
precedence, and test isolation.

### `rust-observability`

Use for `tracing`, metrics, diagnostics, spans, correlation IDs, health checks, and error
messages that help operators without leaking secrets.

### `rust-ci`

Use for CI: stable toolchains, cache strategy, fmt/clippy/test/doc/audit jobs, matrix
builds, artifacts, and release gates aligned with local `just check`.

### `rust-docs`

Use for README, crate-level docs, rustdoc, doctests, examples, CLI help, API contracts,
architecture notes, and keeping docs synchronized with behavior.

### `rust-release`

Use for release preparation: version bumps, changelog, tags, `cargo package`, publishing,
checksums, binaries, SBOMs, and post-release verification.

## Activation Rules

Use the skill matching the user's primary intent. Tests use `rust-test`; Clippy cleanup uses
`rust-quality`; dependency and feature work uses `rust-crates`; async design uses
`rust-async`; release operations use `rust-release`. Skills may reference neighboring
concerns but should keep the canonical workflow in the most specific skill.

## Consequences

The Rust skill set will be precise, reviewable, and suitable for modern greenfield work. The
cost is maintaining more files and avoiding drift in shared conventions such as validation
commands, edition policy, and dependency standards.

## Alternatives Considered

A single `rust` skill was rejected as too broad. Framework-specific skills such as
`rust-axum`, `rust-clap`, `rust-sqlx`, or `rust-tokio` are deferred until repeated work
justifies them. Legacy migration and no-std embedded Rust are out of scope for this
initial greenfield set.

## Related Work

- `docs/adrs/0001-python-professional-development-skills.md`
- `skills/base-repo-setup/SKILL.md`
