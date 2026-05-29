---
name: go-config
description: Greenfield Go configuration workflow for flags, environment variables, config files, precedence rules, typed config structs, validation, secrets, and test isolation.
---

# Go Config

## Rule

Configuration must be explicit, typed, validated, and testable. Keep loading at application
edges and pass typed config into packages.

## Hard Stops

Ask before:

- Changing config precedence, names, defaults, file locations, or environment variable
  contracts.
- Reading global machine files, user home config, real secrets, or production env by default.
- Adding config libraries for simple flags/env needs.
- Logging config that may contain secrets.

## Defaults

- Prefer stdlib `flag`, `os.LookupEnv`, and typed structs for simple apps.
- Use `caarlos0/env/v11` only when env parsing and validation become repetitive and approved.
- Use TOML/YAML/JSON config files only when the app needs file-based configuration; choose
  one format intentionally.
- Define clear precedence, commonly: defaults < config file < environment < CLI flags.
- Validate config once at startup and fail fast with actionable errors.
- Redact secrets in logs, errors, and `%+v` dumps.

## Workflow

1. Define settings, types, defaults, required values, validation, and precedence.
2. Implement loaders that accept explicit args/env/file readers for tests.
3. Avoid package-level config reads outside `main` or app initialization.
4. Add tests for defaults, overrides, validation errors, precedence, and redaction.
5. Run targeted tests, `go test ./...`, lint, and `just check`.

## Antipatterns

- Reading environment variables deep inside domain code.
- Hidden defaults that differ between tests and production.
- Global mutable config objects.
- Viper-style broad configuration stacks for small services unless explicitly approved.
- Printing full config structs that contain secrets.

## Completion

Report config contract, precedence, secret handling, dependency choices, tests, and
validation results.
