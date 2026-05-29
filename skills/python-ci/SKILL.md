---
name: python-ci
description: Python continuous integration workflow for reproducible uv installs, lockfile-aware jobs, lint/type/test/coverage stages, matrix testing, caching, artifacts, security checks, and release gates aligned with local wrappers.
---

# Python CI

## Rule

Keep CI aligned with local validation. CI should run the same repository wrapper commands that
developers run, with reproducible uv installs and lockfile-aware behavior.

Use this skill for CI configuration or review. Use `python-release` for publishing workflows
and release automation.

## Hard Stops

Stop and ask before changing CI when:

- The CI provider, branch protections, required checks, or secret availability is unclear.
- Changes may publish packages, create tags/releases, deploy, rotate secrets, or mutate remote
  systems.
- The repository is a monorepo and project selection/matrix policy is unspecified.
- Caches, artifacts, or logs may expose secrets or sensitive data.
- Adding new tools would diverge from local `just check` or `mise run check` without approval.

## CI Defaults

- Install and use uv reproducibly.
- Respect `uv.lock` with frozen or locked installs where appropriate.
- Run local wrappers such as `just check`; do not duplicate long command lists unless needed.
- Separate lint, type, test, build, and release gates when useful, but keep local parity.
- Cache uv and Python dependencies safely using lockfile keys.
- Upload coverage or build artifacts only when explicitly needed.
- Keep generated artifacts out of git.

## Workflow

1. Inspect local task wrappers, `pyproject.toml`, lockfiles, Nix/mise setup, and existing CI.
2. Identify required checks and project matrix.
3. Add or modify jobs to install tooling and run wrapper commands.
4. Ensure CI does not rely on undeclared machine state or unpinned external behavior.
5. Validate YAML syntax where possible.
6. Run local `just check` and any CI-equivalent command available locally.

## Review Guidance

Flag CI that bypasses local wrappers, ignores lockfiles, runs tests without coverage policy,
uses broad secrets, has unsafe pull-request secret exposure, uploads unnecessary artifacts, or
performs irreversible release/deploy actions without gates.

## Completion

Report CI files changed, jobs/checks added, local parity commands, cache/artifact behavior,
secrets or permission considerations, and validations run.
