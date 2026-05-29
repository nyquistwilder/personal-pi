---
name: rust-docs
description: Rust documentation workflow for README, crate-level docs, rustdoc, doctests, examples, CLI help, API contracts, architecture notes, and keeping docs synchronized with greenfield behavior.
---

# Rust Docs

## Rule

Document behavior that users and maintainers need. Prefer rustdoc examples and doctests for
public API usage.

## Hard Stops

Ask before:

- Documenting unsupported behavior or changing public contracts only to match docs.
- Adding docs sites, mdBook, OpenAPI generation, badges, diagrams-as-code, or hosting.
- Publishing docs externally or changing versioned docs.

## Defaults

- Use README for project usage, install/run commands, development workflow, and operational
  notes.
- Use `//!` crate docs for crate-level guidance.
- Add doc comments for public items in libraries.
- Use examples and doctests for public API flows.
- Keep CLI help generated from Clap where possible.
- Keep HTTP API docs tied to typed schemas/OpenAPI only when OpenAPI is part of the contract.

## Workflow

1. Inspect code, tests, README, rustdoc, examples, CLI help, and API docs.
2. Update docs near the behavior changed.
3. Add runnable examples or doctests when snippets are public contracts.
4. Run `cargo test --doc`, relevant tests, `cargo doc --no-deps`, and `just check`.

## Antipatterns

- README snippets that cannot compile or run.
- Public library items without comments.
- Duplicating API contracts in several unsynchronized docs.
- Documenting implementation details as stable guarantees.

## Completion

Report docs changed, examples/doctests run, behavior verified, and remaining gaps.
