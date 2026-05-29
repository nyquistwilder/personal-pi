---
name: python-review
description: Python code review workflow for assessing diffs or existing code for correctness, maintainability, tests, typing, security, performance, public API stability, and project-convention fit without necessarily editing files.
---

# Python Review

## Rule

Review Python changes for actionable risk. Prioritize correctness, public contracts,
security, data safety, tests, and maintainability over style preferences.

Use this skill when the primary request is review or assessment. Do not edit files unless the
user explicitly asks for fixes.

## Hard Stops

Stop and ask when:

- The review target is unclear: branch, commit range, files, PR diff, or working tree.
- The expected review mode is unclear: blocking defects only, full review, security review,
  performance review, or maintainability review.
- Running validation would touch production systems, live credentials, real databases, or
  mutable user data.
- The code contains apparent secrets or sensitive data; report carefully without repeating
  secret values.

## Review Checklist

Assess, as relevant:

- Correctness: edge cases, error handling, state transitions, serialization, resources.
- Public contracts: imports, CLI flags, HTTP status codes, schemas, database migrations,
  config names, log fields, and documented behavior.
- Tests: meaningful behavior coverage, regression coverage, deterministic boundaries,
  branch coverage policy, and no live-service dependence.
- Typing: honest annotations, no unnecessary `Any`, safe casts/ignores, clear protocols.
- Maintainability: small modules, clear boundaries, no premature abstraction, readable names.
- Security: secrets, injection, path traversal, unsafe deserialization, authz/authn, safe
  subprocess and filesystem handling.
- Performance: algorithmic complexity, memory use, I/O patterns, connection/client reuse,
  avoid unmeasured optimization claims.
- Observability: useful non-sensitive logs/errors, metrics/traces only where appropriate.
- Project conventions: uv groups, Ruff/ty/pytest wrappers, src/tests layout, generated files.

## Workflow

1. Identify the review target using git status, diff, or the user's supplied files.
2. Read the relevant code, tests, configuration, and documentation.
3. Optionally run narrow validation if safe and useful.
4. Group findings by severity and cite file paths and lines when possible.
5. Distinguish blocking issues from non-blocking suggestions.
6. Avoid rewriting the author's code in the review unless providing a minimal illustrative
   snippet clarifies the fix.

## Finding Format

Prefer concise, actionable findings:

- Severity: `blocking`, `high`, `medium`, `low`, or `nit`.
- Location: file and line or symbol.
- Problem: what can go wrong.
- Recommendation: how to fix or what decision is needed.

If no material findings are found, say so and mention the areas reviewed and checks run.

## Completion

Report review scope, commands run or not run, findings by severity, and any assumptions or
follow-up questions.
