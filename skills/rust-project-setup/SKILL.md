---
name: rust-project-setup
description: Set up a brand-new greenfield Rust crate or workspace after base-repo-setup, using modern Cargo layout, Edition 2024 when supported, explicit MSRV, rustfmt, Clippy, tests/docs, cargo-nextest when approved, cargo-deny/audit gates, and local just check validation. Use only for new Rust scaffolding, not migrations.
---

# Rust Project Setup

## Rule

Scaffold a brand-new Rust project; do not only propose a structure. Layer Rust-specific
conventions on top of `base-repo-setup` and target greenfield work only.

Greenfield Rust should be Cargo-first, safe by default, explicit about MSRV and features,
and dependency-minimal until a real domain need exists.

## Hard Stops

Stop before writing files when:

- The repository baseline is missing (`flake.nix`, `mise.toml`, `justfile`, `.gitignore`).
- The target already has `Cargo.toml`, `Cargo.lock`, `src/`, `tests/`, or files that would be
  overwritten.
- Crate name, app/library shape, workspace shape, edition, MSRV, license, or publish intent
  is unclear.
- The request is a migration of an existing Rust project; these skills are greenfield-only.
- Setup would introduce async runtime, HTTP framework, database, config framework,
  OpenTelemetry, unsafe code, FFI, or release automation without approval.

## Required Decisions

Ask and confirm:

1. Crate or workspace name. Use kebab-case package names and snake_case library crate names.
2. Shape: binary app, library crate, mixed app+lib, or workspace.
3. Edition. Recommend Rust 2024 when supported by the chosen stable toolchain.
4. MSRV. Libraries need explicit MSRV; apps may track stable unless release policy says
   otherwise.
5. License, description, repository URL, and publish intent.
6. Whether CLI, HTTP API, async, database, config, observability, benchmarks, docs examples,
   or release automation are in scope. Default is no; use specialized skills later.

## Greenfield Defaults

- Use stable Rust. Pin toolchain through repo policy when the project requires repeatability.
- Prefer `cargo new --bin` or `cargo new --lib` shape, then adjust deliberately.
- Use `src/main.rs` for binaries, `src/lib.rs` for libraries, and `tests/` for integration
  tests.
- Add a workspace only when multiple crates are requested.
- Track `Cargo.lock` for apps and binaries. Discuss lockfile policy for libraries and
  workspaces; default to tracking it in this personal baseline for reproducibility.
- Keep dependencies empty initially unless generated code imports them.
- Use `rustfmt`, Clippy, `cargo test`, `cargo test --doc`, and `cargo doc --no-deps` in
  validation.
- Use `cargo-nextest` only when approved or already standard; `cargo test` remains the
  portable baseline.
- Use `cargo-deny` for license/advisory policy and `cargo-audit` only when the repo chooses
  it; do not add both without need.

## Just Recipes

Keep `just check` as the canonical validation entrypoint. Prefer recipes like:

```make
fmt:
    cargo fmt --all

fmt-check:
    cargo fmt --all -- --check

lint:
    cargo clippy --all-targets --all-features -- -D warnings

test:
    cargo test --all-targets --all-features

doc:
    cargo doc --no-deps --all-features

check: fmt-check lint test doc
```

Add `nextest`, `deny`, `audit`, `coverage`, or `bench` recipes only when those tools are
approved and versioned through project tooling.

## Workflow

1. Verify the baseline repository files and Git root.
2. Ask all required decisions.
3. Create Cargo metadata, source skeleton, smoke tests, README updates, and just recipes.
4. Add `.gitignore` entries for generated Rust artifacts only when missing (`target/`,
   coverage/profiling outputs). Do not ignore `Cargo.lock` without approval.
5. Run `cargo fmt`, `cargo test`, `cargo clippy`, `cargo doc`, and `just check`.

## Completion

Report crate/workspace shape, edition/MSRV, lockfile policy, files created, dependencies
added or avoided, commands run, validation results, and intentionally skipped optional items
such as Tokio, Axum, Clap, SQLx, OpenTelemetry, CI, and release automation.
