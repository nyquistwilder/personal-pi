---
name: rust-ci
description: Rust CI workflow for greenfield Cargo projects using stable toolchains, caching, fmt, Clippy, tests/nextest, docs, audit/deny jobs, feature matrices, coverage, artifacts, and release gates aligned with local just check.
---

# Rust CI

## Rule

CI must mirror local validation and make failures actionable. Keep `just check` as the local
source of truth when present.

## Hard Stops

Ask before:

- Adding providers, paid services, release credentials, publishing crates, signing, or
  uploading artifacts externally.
- Requiring nightly, changing MSRV/toolchain policy, or expanding supported OS/targets.
- Adding slow feature matrices, coverage uploads, Miri/sanitizers, or container services to
  every PR without approval.

## Defaults

- Use stable Rust and project `rust-toolchain.toml` or repo toolchain policy.
- Cache Cargo registry/git/build outputs through CI mechanisms.
- Fast PR gate: fmt check, Clippy with warnings denied, tests, doctests/docs, and build.
- Use `cargo nextest` when configured; keep `cargo test --doc` for doctests.
- Use `cargo deny check` and/or `cargo audit` when configured.
- Scheduled/protected checks may add `cargo hack` feature/MSRV matrix, coverage with
  `cargo llvm-cov`, Miri/sanitizers for unsafe-heavy code, and dependency update checks.
- Prefer invoking `just check` rather than duplicating command logic in YAML.

## Workflow

1. Inspect local commands, toolchain policy, workspace shape, and existing CI.
2. Add or update jobs to call wrappers and install tools reproducibly.
3. Configure caches and artifacts without committing generated outputs.
4. Split fast PR checks from slower scheduled/release checks when needed.
5. Validate YAML and run local `just check`.

## Antipatterns

- CI commands drifting from local wrappers.
- Installing latest cargo tools without a version policy.
- Running only `cargo build` and no tests/lints.
- Ignoring feature combinations, MSRV, or security until release.

## Completion

Report CI files changed, jobs, cache/tool strategy, local validation, and release gates.
