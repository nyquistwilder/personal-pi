---
name: rust-quality
description: Rust quality workflow for cargo fmt, Clippy, warning fixes, import/module cleanup, dead-code removal, edition idioms, feature hygiene, and behavior-preserving cleanup in greenfield crates.
---

# Rust Quality

## Rule

Improve Rust code quality without changing behavior. Prefer mechanical, idiomatic,
reviewable changes aligned with `rustfmt`, Clippy, and project lints.

## Hard Stops

Stop when:

- A lint fix changes public API, feature semantics, error behavior, persistence, or wire
  formats.
- Removing apparently unused items could remove public exports, macro entry points, plugin
  hooks, migrations, examples, or build-tagged/platform-specific code.
- Adding `#[allow]`, changing lint levels, or disabling warnings would hide a real issue.
- Tooling policy is missing and adding strict Clippy/cargo-deny/nextest config is out of
  scope.

## Defaults

- Run `cargo fmt --all` and `cargo clippy --all-targets --all-features -- -D warnings` when
  the project can support it.
- Keep `#[allow]` narrow, local, and justified with a reason.
- Prefer removing dead private code over suppressing warnings.
- Preserve generated code; update generators instead of hand-editing when possible.
- Keep feature defaults minimal and avoid accidental dependency activation.

## Workflow

1. Inspect `Cargo.toml`, features, workspace config, rustfmt/clippy config, generated files,
   and wrappers.
2. Run fmt and Clippy through project commands when available.
3. Apply formatting, import cleanup, warning fixes, safe simplifications, and dead private
   code removal.
4. Run tests for touched crates and `just check`.

## Antipatterns

- Turning clear code into clever iterator chains solely for style.
- Adding broad crate-level allows.
- Fixing borrow/clippy issues with unnecessary clones everywhere.
- Changing module boundaries during lint cleanup.

## Completion

Report tools run, files cleaned, allows added with reasons, behavior assumptions, and
validation results.
