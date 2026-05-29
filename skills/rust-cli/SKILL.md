---
name: rust-cli
description: Greenfield Rust CLI workflow for clap command structure, args, environment integration, stdin/stdout/stderr discipline, exit codes, completions, config integration, and CLI tests.
---

# Rust CLI

## Rule

Build CLIs that are predictable for humans and scripts. Keep parsing and process exit at the
edge; put core logic in testable library modules.

## Hard Stops

Ask before:

- Adding Clap, changing public flags/subcommands/output formats/exit codes, or generating
  completions into user directories.
- Performing destructive actions, reading secrets, modifying global config, or adding
  interactive prompts.
- Adding color/progress/rendering libraries when plain output is sufficient.

## Defaults

- Use `clap` derive for non-trivial CLIs when approved; manual std parsing is acceptable for
  tiny internal tools.
- Use `main` only for parse/config/logging/bootstrap and process exit.
- Return `Result` from testable command functions; convert errors to user-facing messages at
  the edge.
- Use stdout for requested output; stderr for diagnostics/progress.
- Use stable exit codes: `0` success, `1` runtime failure, `2` usage error unless documented
  otherwise.
- Integrate `tracing`/logging via explicit flags only when observability is in scope.

## Testing

Test core command functions directly. Use `assert_cmd` and `predicates` only when approved or
already present for binary-level tests. Assert args, env vars, stdin/stdout/stderr, exit
codes, config precedence, and side effects.

## Workflow

1. Define command contract: args, flags, env vars, stdin/stdout/stderr, exit codes.
2. Choose manual parsing or Clap based on real complexity.
3. Keep business logic outside parsing.
4. Add tests for success, usage errors, runtime failures, and output stability.
5. Run CLI tests, full tests, Clippy, and `just check`.

## Completion

Report command contract, flags/env vars, exit codes, dependency choices, tests, and
validation.
