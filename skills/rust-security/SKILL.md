---
name: rust-security
description: Secure Rust development and review workflow for secrets, unsafe code, FFI, path handling, command execution, deserialization, auth boundaries, TLS, dependency advisories, and supply-chain risk.
---

# Rust Security

## Rule

Use safe Rust by default and treat external input, secrets, unsafe code, FFI, filesystem
paths, subprocesses, network calls, auth, and dependencies as explicit security boundaries.

## Hard Stops

Stop before:

- Introducing or modifying `unsafe`, FFI, custom allocators, or raw pointer code.
- Touching real secrets, production systems, customer data, incident evidence, or destructive
  operations.
- Weakening TLS, authentication, authorization, tenant isolation, audit logging, or data
  retention.
- Executing user-controlled commands, accepting unbounded deserialization, or writing outside
  intended directories.
- Suppressing `cargo deny`, `cargo audit`, scanner, or review findings without risk approval.

## Defaults

- Validate inputs at boundaries with explicit parsing or approved validation crates.
- Use `secrecy`/`zeroize` for long-lived secrets that may otherwise be logged or retained.
- Avoid logging secrets and sensitive fields; redact at the type or formatter boundary.
- Enforce path containment after canonicalization where paths touch untrusted input.
- Use fixed executables and explicit args for subprocesses; avoid shell invocation.
- Prefer Rustls TLS stacks unless platform policy requires native TLS.
- Run `cargo deny check` and/or `cargo audit` when configured.
- For unsafe code, require local safety comments, narrow unsafe blocks, tests, and Miri or
  sanitizer evidence when practical.

## Workflow

1. Identify assets, actors, trust boundaries, and threat model.
2. Inspect unsafe/FFI, parsing, auth, paths, subprocesses, logs, network, database, and
   dependencies.
3. Reproduce risk with safe local tests where practical.
4. Implement minimal hardening and malicious-input regression tests.
5. Run tests, deny/audit/scanners when configured, Clippy, and `just check`.
6. Separate code fixes from operational actions such as secret rotation.

## Antipatterns

- `unwrap` on untrusted input or protocol parsing.
- Raw string SQL/commands built from user input.
- `Debug` output for config structs containing secrets.
- Unsafe blocks without documented invariants.
- Dependency feature defaults that pull in unwanted TLS/crypto/native code.

## Completion

Report risks, mitigations, tests/scans, unsafe status, secrets avoided, and residual risk.
