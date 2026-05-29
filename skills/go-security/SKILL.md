---
name: go-security
description: Secure Go development and review workflow for secrets, input validation, path traversal, subprocess safety, auth boundaries, TLS, deserialization, filesystem/database safety, dependency vulnerabilities, and supply-chain risk.
---

# Go Security

## Rule

Treat security-sensitive code as boundary work. Identify trust boundaries, validate inputs,
protect secrets, use safe stdlib APIs, and keep dependencies and logging safe by default.

## Hard Stops

Stop before:

- Touching real secrets, customer data, production systems, or incident-response evidence.
- Weakening authentication, authorization, TLS verification, audit logging, or retention
  behavior.
- Executing user-controlled commands, writing outside intended directories, or running
  destructive migrations.
- Adding crypto/auth/security dependencies without threat model and maintenance review.
- Suppressing `govulncheck`, `gosec`, scanner, or code-review findings without risk
  approval.

## Checklist

- Secrets: no hard-coded credentials, env dumps, token logs, or secret-bearing error values.
- Input validation: parse and bound untrusted values at boundaries; reject ambiguous input.
- Paths: use `filepath.Clean`, `filepath.IsLocal`, allowlisted roots, and post-resolution
  containment checks; avoid handcrafted temp names.
- Subprocess: avoid shell invocation; use fixed executables and explicit args; pass context;
  validate inputs.
- HTTP/TLS: keep TLS verification on; configure timeouts; limit body sizes; avoid logging
  auth headers.
- Auth: enforce authorization at service boundaries, not only handlers or UI layers.
- Serialization: bound JSON/YAML/protobuf input sizes and reject unknown or unsupported
  fields when the contract requires it.
- Database: use parameters, transactions, least-privilege users, and migration safeguards.
- Files: use safe permissions for secrets and atomic writes where corruption matters.
- Dependencies: run `govulncheck`; review licenses, maintenance, and transitive risk.

## Defaults

Prefer stdlib security primitives: `crypto/rand`, `crypto/subtle`, `crypto/hmac`,
`crypto/sha256`, `net/http` timeouts, `os.OpenInRoot` or containment-safe path handling when
available, `os.CreateTemp`, and `exec.CommandContext`. Use vetted password hashing,
JWT/OIDC, or crypto libraries only when the protocol requires them and they are approved.

## Workflow

1. Identify assets, actors, trust boundaries, and threat model.
2. Inspect input, secrets, auth, paths, subprocesses, network, database, logs, and modules.
3. Reproduce risk with safe local tests when practical.
4. Implement minimal hardening and malicious-input regression tests.
5. Run `go test ./...`, race checks when relevant, `govulncheck`, configured scanners, and
   `just check`.
6. Separate code fixes from operational actions such as secret rotation.

## Completion

Report boundaries reviewed, vulnerabilities fixed or ruled out, tests/scans run, secrets
handling considerations, residual risks, and required manual follow-up.
