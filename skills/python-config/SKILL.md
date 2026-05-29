---
name: python-config
description: Python configuration workflow for environment variables, config files, Pydantic settings, precedence rules, defaults, secrets, test isolation, and development/test/production separation.
---

# Python Config

## Rule

Make configuration typed, explicit, testable, and safe. Define precedence rules clearly and
avoid hidden global state that makes tests order-dependent or deployments surprising.

For greenfield personal-baseline apps and services, prefer Pydantic Settings for environment
and file-backed settings when validation is needed.

## Hard Stops

Stop and ask before changing configuration when:

- Environment variable names, prefixes, defaults, or precedence are unclear.
- Existing deployments, CLI flags, config files, or secrets management may depend on current
  behavior.
- Real secrets or production configuration values are present. Do not repeat secret values.
- Adding Pydantic Settings, dotenv loading, or config-file support would change project
  policy.
- Tests would read or mutate the user's real environment or config files.

## Configuration Defaults

- Precedence should be documented; for CLIs prefer `CLI flags > environment variables >
  config files > defaults` unless the project specifies otherwise.
- Use a stable environment prefix, typically the import package uppercased.
- Keep secrets out of logs, exceptions, test fixtures, and committed files.
- Prefer immutable settings objects or explicit settings injection.
- Do not load configuration at import time if tests or applications need different settings.
- Separate development, test, and production defaults deliberately.

## Pydantic Settings Guidance

- Use Pydantic models for validation and type coercion at config boundaries.
- Use field aliases or env names intentionally.
- Use `SecretStr` or equivalent secret types where values may be displayed.
- Validate paths, URLs, ports, log levels, and enum-like values explicitly.
- Keep settings construction centralized but injectable.

## Workflow

1. Inspect current settings, environment variables, config files, docs, tests, and deployment
   references.
2. Identify all consumers and compatibility constraints.
3. Define or preserve precedence rules.
4. Implement typed settings and explicit loading boundaries.
5. Add tests with `monkeypatch`, `tmp_path`, and isolated config files.
6. Update docs or README snippets when configuration surface changes.
7. Run focused tests and repository validation.

## Testing

Never depend on machine-local environment. Use `monkeypatch` to set and delete variables.
Use `tmp_path` for config files. Test defaults, env overrides, invalid values, missing
required values, and secret redaction when relevant.

## Completion

Report config keys changed, precedence rules, defaults, secret-handling decisions, tests run,
and deployment compatibility risks.
