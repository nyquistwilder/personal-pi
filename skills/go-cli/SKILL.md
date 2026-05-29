---
name: go-cli
description: Greenfield Go CLI workflow for command shape, flags, environment integration, stdin/stdout/stderr discipline, exit codes, shell-friendly UX, Cobra or stdlib flag choices, and CLI tests.
---

# Go CLI

## Rule

Build CLIs that are predictable for humans and scripts. Keep parsing and process exit at the
edge; put core behavior in testable packages.

## Hard Stops

Ask before:

- Adding Cobra, changing public flags/subcommands, changing output formats, or changing exit
  codes.
- Performing destructive filesystem/network/database actions.
- Reading secrets, writing shell completions into user directories, or modifying global
  config.
- Introducing interactive prompts for automation-oriented commands.

## Defaults

- Use stdlib `flag` for simple single-command tools.
- Use `spf13/cobra` only for public multi-command CLIs, nested help, completions, or
  long-term command growth.
- Keep `main` tiny: call `run(ctx, args, stdin, stdout, stderr) int` or equivalent.
- Write requested machine-readable output to stdout; diagnostics and progress to stderr.
- Use stable, documented exit codes: `0` success, `1` generic failure, `2` usage error unless
  the project defines more.
- Make environment variables explicit and documented.

## Testing

Test command behavior without `os.Exit` in tests. Pass explicit args and buffers. Use real
subprocess tests only for installed binary behavior, signals, or shell integration. Assert
stdout, stderr, exit code, config/env precedence, and side effects.

## Workflow

1. Define command contract: name, args, flags, env vars, stdin/stdout/stderr, exit codes.
2. Choose stdlib `flag` or Cobra based on real complexity.
3. Keep business logic out of command parsing.
4. Add tests for success, usage errors, failure paths, and output stability.
5. Run targeted tests, `go test ./...`, `go vet`, lint, and `just check`.

## Antipatterns

- Calling `os.Exit` deep in business logic.
- Logging to stdout or printing requested data to stderr.
- Hidden env vars, machine-local config defaults, or prompts in scripts.
- Cobra for a one-flag internal tool.

## Completion

Report command contract, dependency choice, flags/env vars, exit codes, tests, and
validation results.
