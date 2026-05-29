---
name: python-security
description: Python security workflow for secure implementation and review of secrets, input validation, path and command injection, unsafe deserialization, auth boundaries, dependency risks, filesystem safety, and network calls.
---

# Python Security

## Rule

Treat security-sensitive code as boundary work. Identify trust boundaries, validate inputs,
protect secrets, and prefer safe standard APIs over stringly or shell-based approaches.

Use this skill for security review, hardening, or fixes. Do not treat it as a generic linting
or dependency-update skill.

## Hard Stops

Stop and ask before proceeding when:

- Work involves real secrets, production systems, customer data, mutable user data, or
  incident response.
- A change may weaken authentication, authorization, encryption, audit logging, or data
  retention expectations.
- Testing would require live credentials, production endpoints, destructive operations, or
  vulnerability exploitation against third-party systems.
- You discover likely exposed secrets. Do not repeat secret values; ask how to rotate and
  purge them.
- The requested fix is to suppress or ignore a security finding without understanding risk.

## Security Checklist

Assess relevant boundaries:

- Secrets: no hard-coded credentials, tokens in logs, `.env` commits, or exception leaks.
- Input validation: parse and validate untrusted data with Pydantic or explicit validators.
- Paths: prevent traversal; resolve paths against allowed roots; avoid unsafe temp names.
- Subprocess: avoid `shell=True`; pass argument lists; validate executable and arguments.
- Deserialization: avoid unsafe pickle/yaml loaders for untrusted input.
- HTTP: use `httpx` with timeouts, TLS verification, bounded redirects, and safe error
  handling; do not log auth headers.
- Auth: enforce authorization at service boundaries, not only UI/CLI layers.
- Databases: use parameterized queries/ORM expressions; make transactions explicit.
- Files: set safe permissions for secrets; avoid writing outside intended directories.
- Dependencies: evaluate necessity, maintenance, licenses if relevant, and known
  vulnerabilities before adding or upgrading.

## Workflow

1. Identify assets, actors, trust boundaries, and expected threat model.
2. Inspect code paths that ingest input, access secrets, call networks, touch files, spawn
   processes, or enforce authorization.
3. Reproduce or demonstrate risk with safe local tests where practical.
4. Implement minimal hardening that preserves intended behavior.
5. Add regression tests for the security boundary when safe.
6. Run relevant tests and repository validation.
7. Report residual risk and operational actions such as secret rotation separately from code
   changes.

## Greenfield Defaults

- Prefer Pydantic settings and models for typed, validated external configuration and input.
- Prefer `secrets` for tokens, `hashlib`/`hmac` for integrity primitives, and vetted
  libraries for password hashing or cryptography.
- Prefer `tempfile` and `pathlib` over handcrafted temp paths.
- Prefer deny-by-default authorization checks and explicit allow-lists.
- Keep logs structured but redacted.

## Completion

Report boundaries reviewed, vulnerabilities fixed or ruled out, tests run, secrets handling
considerations, and any required manual operational follow-up.
