---
name: rust-implementation
description: Modern Rust production implementation workflow for greenfield features, refactors, ownership design, trait boundaries, public APIs, error handling, maintainable safe Rust, and dependency-minimal code. Use for day-to-day Rust code changes, not primarily tests, crates, async, security, performance, APIs, CLIs, or databases.
---

# Rust Implementation

## Rule

Implement the smallest clear production change that satisfies the behavior contract. Prefer
safe Rust, explicit ownership, small modules, clear error types, and testable boundaries over
premature traits, macros, or dependencies.

## Hard Stops

Ask before:

- Changing public APIs, serialized formats, CLI flags, HTTP routes, feature flags, MSRV, or
  error contracts.
- Adding dependencies when std or existing crates may be enough.
- Introducing `unsafe`, FFI, global mutable state, runtime-wide singletons, procedural macros,
  or code generation.
- Calling live services, production databases, real secrets, or mutable user files.
- The task is primarily tests, async, crates, security, performance, API, CLI, database,
  config, observability, or release work; use the specialized Rust skill.

## Design Defaults

- Use concrete types until a trait boundary is justified by multiple implementations, tests,
  or external API ergonomics.
- Keep lifetimes simple. Prefer owned data at public boundaries when it improves usability.
- Return `Result<T, E>` for recoverable failures; reserve `panic!` for bugs and impossible
  invariants.
- Use `thiserror` for library/domain errors and `anyhow` at binary/application edges only
  when approved or already standard.
- Keep I/O, time, randomness, network, filesystem, and process effects at adapters or behind
  narrow injected boundaries.
- Prefer explicit modules over macro-heavy architecture.
- Use `tracing` instrumentation only when observability is in scope; do not log from every
  function.
- Avoid `Arc<Mutex<_>>` until shared ownership and synchronization are truly needed.

## Approved Greenfield Preferences

Use only when needed and approved:

- Errors: `thiserror` for libraries, `anyhow` for binaries.
- Async: Tokio, plus `futures` utilities when required.
- CLI: `clap` derive for non-trivial CLIs.
- HTTP API: Axum with Tower/Tower HTTP.
- HTTP client: `reqwest` with Rustls and explicit timeouts.
- Serialization: `serde`, `serde_json`, `toml` for external formats.
- Config: simple env/CLI first; `figment` or `config` only for layered file/env needs.
- Observability: `tracing`, `tracing-subscriber`, OpenTelemetry only with a backend.
- Database: SQLx for async SQL; Diesel only when sync ORM-style compile-time query builder
  is explicitly chosen.

## Workflow

1. Inspect `Cargo.toml`, features, module layout, tests, and wrappers.
2. Identify public behavior and the narrowest module boundary to change.
3. Add/update tests for behavior changes; defer detailed test policy to `rust-test`.
4. Implement with safe Rust, clear ownership, and explicit errors.
5. Run `cargo fmt`, targeted tests, `cargo test`, `cargo clippy`, and `just check`.

## Antipatterns

- Traits named after one implementation “for testability” when a concrete fake would do.
- Cloning everything to appease the borrow checker without considering ownership.
- `unwrap`/`expect` in library or request-path code for recoverable input failures.
- Broad feature defaults that pull async, TLS, DB, or CLI stacks into library users.
- Global runtimes, global mutable config, and hidden background tasks.

## Completion

Report behavior changed, API/error impacts, dependencies added or avoided, tests and
validation, and remaining assumptions.
