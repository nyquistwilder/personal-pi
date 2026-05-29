---
name: rust-config
description: Greenfield Rust configuration workflow for typed settings, environment variables, config files, CLI overrides, defaults, validation, precedence rules, secret redaction, and test isolation.
---

# Rust Config

## Rule

Configuration must be explicit, typed, validated, and testable. Keep loading separate from
business logic and pass typed config into services.

## Hard Stops

Ask before:

- Changing precedence, variable names, defaults, file locations, or compatibility contracts.
- Reading global machine files, user home config, real secrets, or production env by default.
- Adding config libraries for simple env/CLI needs.
- Logging config that may contain secrets.

## Defaults

- Prefer Clap/env/std parsing for simple apps.
- Use typed structs with `serde` when files are needed.
- Use `figment` or `config` only for layered config from files/env/CLI and only when
  approved or already present.
- Define precedence explicitly, commonly: defaults < config file < environment < CLI.
- Validate once at startup and fail fast with actionable errors.
- Use `secrecy`/redaction wrappers for secret values when they may be logged or debugged.

## Workflow

1. Define settings, defaults, required values, validation, and precedence.
2. Implement loaders that accept explicit sources for tests.
3. Avoid reading env/files inside domain logic.
4. Add tests for defaults, overrides, precedence, validation errors, and redaction.
5. Run tests and `just check`.

## Antipatterns

- Global mutable config.
- Hidden environment reads deep in libraries.
- `.env` loading in production paths without policy.
- Printing full config structs with secrets.

## Completion

Report config contract, precedence, secret handling, dependencies, tests, and validation
results.
