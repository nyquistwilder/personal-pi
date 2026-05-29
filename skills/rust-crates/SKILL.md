---
name: rust-crates
description: Rust crate and dependency workflow for adding, removing, upgrading, auditing, feature-gating, workspace inheritance, lockfile policy, MSRV compatibility, licenses, advisories, and publish metadata in greenfield Cargo projects.
---

# Rust Crates

## Rule

Keep dependencies minimal, feature flags deliberate, and Cargo metadata reproducible. Prefer
std or existing crates before adding new dependencies.

## Hard Stops

Ask before:

- Adding large frameworks, async runtimes, ORMs, crypto/auth crates, proc macros, build
  scripts, native dependencies, or generated-code tools.
- Changing crate name, workspace shape, MSRV, edition, feature defaults, lockfile policy, or
  publish metadata.
- Enabling broad default features, vendoring, git/path dependencies, forks, or yanked
  versions.
- Accepting license, advisory, maintenance, or supply-chain risk without approval.

## Defaults

- Use `cargo add`, `cargo remove`, and `cargo update -p <crate>` when available instead of
  broad hand edits.
- Keep direct dependency versions compatible with Cargo SemVer expectations; avoid needless
  exact pins in libraries.
- Disable default features when unnecessary and choose Rustls over native TLS/OpenSSL unless
  platform policy requires otherwise.
- Keep feature flags additive. Features must not silently change semantics or remove APIs.
- Track `Cargo.lock` for apps/binaries and personal-baseline workspaces; discuss library
  policy explicitly.
- Check license, maintenance, MSRV, feature graph, transitive size, advisories, and unsafe
  surface.
- Use `cargo-deny` for license/advisory policy when configured; use `cargo-audit` for RustSec
  advisory scanning when configured.

## Approved Greenfield Preferences

Use only when needed and approved:

- CLI: `clap`.
- Errors: `thiserror` for libraries, `anyhow` for apps.
- Async/runtime: `tokio`; `futures` for combinators/traits.
- HTTP server: `axum`, `tower`, `tower-http`.
- HTTP client: `reqwest` with Rustls and explicit timeouts.
- Serialization/validation: `serde`, `serde_json`, `toml`, `validator` when validation
  derives are justified.
- Config: std env/CLI first; `figment` or `config` for layered config.
- Observability: `tracing`, `tracing-subscriber`; OpenTelemetry only with backend.
- Database: `sqlx` for async SQL and migrations; Diesel only when its model is explicitly
  chosen.
- Testing: `insta`, `proptest`, `wiremock`, `testcontainers`, `tempfile` only as justified.

## Workflow

1. Identify why the crate is needed and whether existing code/std can satisfy it.
2. Inspect workspace dependencies, features, lockfile, MSRV, and publish policy.
3. Evaluate license, advisories, maintenance, downloads/community, transitive features,
   native dependencies, and binary size/runtime impact.
4. Add/remove/upgrade with Cargo commands and explicit feature choices.
5. Run `cargo tree -e features` when feature behavior matters.
6. Run targeted tests, full tests, Clippy, deny/audit when configured, and `just check`.
7. Document user-facing dependencies or feature flags.

## Completion

Report dependency decisions, feature choices, versions, lockfile changes, commands,
license/security/MSRV concerns, and risk tradeoffs.
