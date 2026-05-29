---
name: python-quality
description: Python code quality workflow for Ruff formatting/linting, import hygiene, dead-code removal, syntax modernization, and behavior-preserving cleanup in uv-managed src/tests projects.
---

# Python Quality

## Rule

Make Python code cleaner without changing behavior. Prefer mechanical, idiomatic, and
reviewable improvements that align with the project's configured formatter, linter, and task
wrappers.

Use this skill for Ruff, formatting, imports, modernization, unused code, and safe cleanup.
Use `python-implementation` when behavior changes are intended.

## Hard Stops

Stop and ask before making cleanup changes when:

- A lint finding cannot be fixed without changing behavior or public API contracts.
- Existing formatting or lint tooling is unclear and adding Ruff or changing config would be
  project policy work.
- Cleanup would remove apparently unused public exports, plugin hooks, migrations, scripts,
  tests, fixtures, or entry points.
- Auto-fixes include unsafe changes that have not been explicitly approved.
- The task is primarily typing, debugging, tests, security, performance, or packaging.

## Quality Defaults

For greenfield personal-baseline projects, prefer Ruff for formatting, import sorting, and
linting. Preserve the repository's configured rules.

Typical safe changes:

- run formatter and import sorter
- remove unused private imports, variables, and functions
- modernize syntax where Ruff indicates it is safe
- simplify obvious boolean, context manager, and collection patterns
- replace deprecated stdlib aliases with modern equivalents
- keep generated caches and artifacts out of version control

Avoid broad rewrites, clever one-liners, churn in unrelated files, and cosmetic changes that
make reviews harder.

## Workflow

1. Inspect `pyproject.toml`, `ruff.toml`, just/mise tasks, and existing style.
2. Run the narrowest relevant lint or format check with uv, for example:
   `uv run --group lint ruff check .` or the project wrapper.
3. Apply safe formatter output and targeted lint fixes.
4. For Ruff fixes, prefer safe fixes first. Use `--unsafe-fixes` only with explicit approval
   and review every change.
5. Run tests if cleanup touched executable code.
6. Run the repository validation command, normally `just check`.

## Review Guidance

When reviewing quality-only diffs, look for accidental behavior changes, public API removal,
new ignores without justification, broad churn, inconsistent style, and places where a lint
suppression is masking a real design issue.

## Completion

Report formatting/lint commands run, files cleaned, unsafe fixes avoided or approved,
behavior-preserving assumptions, and validation results.
