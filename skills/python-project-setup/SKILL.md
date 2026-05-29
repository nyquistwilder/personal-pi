---
name: python-project-setup
description: Set up a brand-new uv-managed Python project after base-repo-setup, using sibling src/tests layout, baseline pyproject.toml, dependency groups, Ruff, ty, pytest with branch coverage, and local validation commands. Supports single-project repos and monorepo apps/libs/models. Use for new Python project scaffolding only, not existing project migration or domain-specific CLI/API/observability work.
---

# Python Project Setup

## Rule

Scaffold a brand-new Python project. Do not only propose a structure.

This skill layers Python-specific baseline conventions on top of `base-repo-setup`. It owns
new-project layout, uv adoption, baseline `pyproject.toml`, dependency groups, starter
package files, starter tests, Ruff, ty, pytest coverage, and repository validation wiring.

Keep this skill focused. Defer specialized or ongoing work to neighboring Python skills:

- Use `python-test` for detailed test creation, fixture design, regression tests, and test
  review.
- Use `python-packaging` for advanced packaging, publish readiness, optional extras,
  dynamic versioning, wheel/sdist inspection, and release artifact policy.
- Use `python-cli` for command structure, Typer implementation details, CLI UX, and CLI
  testing beyond the optional setup stub.
- Use `python-observability` for logging, metrics, tracing, structlog design, and
  diagnostics beyond the optional setup stub.
- Use `python-docs` for documentation, README expansion, docstring policy, examples, and
  keeping docs synchronized after setup.
- Use `python-ci`, `python-security`, `python-release`, or `python-dependency-management`
  when those concerns become the primary task.

## Hard Stops

Stop before writing files when any required condition is missing or ambiguous:

- The repository root must already appear initialized by `base-repo-setup`. Check the Git
  root and require core baseline files such as `flake.nix`, `mise.toml`, `justfile`, and
  `.gitignore`. Ask before any special-case setup without that baseline.
- Ask all required decisions explicitly. Defaults are recommendations, not permission. Do
  not infer silently.
- Always ask whether this is a single-project repo or a monorepo project.
- For monorepos, always ask the project kind and name. Standard kinds are `app`, `lib`, and
  `model`; custom categories require an exact parent directory and an app-like, lib-like,
  or model-like recommendation profile.
- If the target project root already contains `pyproject.toml`, `uv.lock`, `src/`, or
  `tests/`, inspect and ask before modifying. Never overwrite source, tests, config,
  lockfiles, README, or task files without explicit approval.
- If a target path exists as a file or otherwise conflicts with the intended directory
  layout, stop and ask.
- Validate distribution names and import package names before writing. Import package names
  must be valid Python identifiers or valid identifier segments for namespace packages, must
  not contain hyphens, and must not be Python keywords.
- Do not create `.python-version`, nested `mise.toml`, CI configuration, docs toolchains,
  tox/nox, security/audit tooling, hook systems, changelogs, badges, or extra package data
  unless explicitly requested.
- Do not add runtime dependencies except generated-code requirements approved during setup.
  CLI stubs require `typer`; logging stubs require `structlog`.

## Required Decisions

Before writing files, ask and confirm these decisions one at a time as needed:

1. Repository shape: `single` or `monorepo`.
2. For single-project repos: project profile: app-like, lib-like, or model-like.
3. For monorepos: kind and name.
   - `app` -> `apps/<name>`
   - `lib` -> `libs/<name>`
   - `model` -> `models/<name>`
   - custom -> ask exact parent directory and app-like/lib-like/model-like profile
4. Distribution name. Recommend the project or directory name normalized to kebab-case.
5. Import package name. Recommend the distribution name normalized to snake_case.
6. Short project description. Require this for metadata, README, and module docstrings.
7. Minimum Python version. Recommend `>=3.13` and do not add an upper bound.
8. Initial version. Recommend `0.1.0`.
9. Author metadata. Inspect `git config user.name` and `git config user.email`, then confirm
   before writing.
10. License metadata. Inspect the root `LICENSE` if present, recommend an obvious SPDX
    expression, and confirm before writing. Omit if unknown or unconfirmed.
11. CLI stub support. Recommend yes for apps, no for libs, and workflow-dependent for
    models. If accepted, follow the setup subset in `python-cli`.
12. If CLI is enabled: command name. Recommend the distribution name normalized to
    kebab-case.
13. structlog stub support. CLI support implies structlog. Recommend yes for apps and
    models; no for libs unless CLI is enabled or the user explicitly wants logging
    scaffolding. If accepted, follow the setup subset in `python-observability`.
14. If structlog is enabled: environment variable prefix. Recommend the import package name
    uppercased.
15. Namespace package support. Recommend no; use a regular package by default.
16. Publishing metadata. Recommend no classifiers, URLs, license-files, or changelog unless
    publishing is explicitly in scope. Use `python-packaging` for publish-focused work.

## Layout

Create one independent Python project per project root. Each project root owns its own
`pyproject.toml`, `uv.lock`, `src/`, `tests/`, and local `justfile` when nested in a
monorepo. Do not create a shared uv workspace by default.

Single-project layout:

```text
.
|-- pyproject.toml
|-- uv.lock
|-- README.md
|-- src/
|   `-- <import_package>/
|       |-- __init__.py
|       `-- py.typed
`-- tests/
    `-- test_<import_package>.py
```

Monorepo project layout:

```text
apps/<name>/
|-- pyproject.toml
|-- uv.lock
|-- README.md
|-- justfile
|-- src/
|   `-- <import_package>/
|       |-- __init__.py
|       `-- py.typed
`-- tests/
    `-- test_<import_package>.py
```

Use `libs/<name>/` for libraries and `models/<name>/` for AI/model projects. Create only the
selected category parent directory when missing; do not create unused `apps/`, `libs/`, or
`models/` directories.

Default to exactly one regular import package:

```text
src/<import_package>/__init__.py
```

Support namespace packages only when explicitly requested, and then adjust package paths,
Hatchling config, and tests accordingly.

Do not create `tests/__init__.py`, `tests/conftest.py`, `core.py`, or domain modules by
default.

## Tooling And Metadata

Use uv for dependency management and lockfiles. Always generate and track `uv.lock`,
including for libraries. Do not add `uv.lock` to `.gitignore`.

Use Hatchling as the baseline build backend for new packages:

```toml
[build-system]
requires = ["hatchling>=1.27"]
build-backend = "hatchling.build"
```

Use static versioning by default:

```toml
version = "0.1.0"
```

and:

```python
__version__ = "0.1.0"
```

Use PEP 735 dependency groups for tools:

```toml
[dependency-groups]
test = [
  "coverage",
  "pytest",
  "pytest-cov",
]
lint = [
  "ruff",
]
type = [
  "ty",
]
dev = [
  { include-group = "test" },
  { include-group = "lint" },
  { include-group = "type" },
]
```

Keep tool dependencies unconstrained in `pyproject.toml`; rely on `uv.lock` for exact
reproducibility. Sort runtime dependencies alphabetically. `typer` and `structlog` are
runtime dependencies only when generated code imports them.

Do not create a `[tool.uv]` section by default. Do not create ty configuration by default;
run ty from the Python project root so it can infer settings from `pyproject.toml`.

Use stable `pyproject.toml` ordering:

1. `[build-system]`
2. `[project]`
3. `[project.scripts]` when a CLI stub is enabled
4. `[dependency-groups]`
5. Hatch build target config
6. pytest and coverage config
7. Ruff config
8. ty config only if needed

## Pytest And Coverage

Generated projects must align with `python-test`: pytest, pytest-cov, coverage.py, branch
coverage, and an 80% global minimum.

Add this config to the project `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
  "--import-mode=importlib",
  "--cov=src",
  "--cov-branch",
  "--cov-report=term-missing",
  "--cov-report=html",
  "--cov-fail-under=80",
]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

Do not emit XML coverage by default. Keep coverage artifacts out of version control.

## Ruff

Use Ruff for formatting, import sorting, modernization, pytest rules, and common linting.

Default config:

```toml
[tool.ruff]
target-version = "py313"
src = ["src", "tests"]
line-length = 100

[tool.ruff.lint]
select = [
  "E",
  "F",
  "I",
  "B",
  "UP",
  "SIM",
  "RUF",
  "FA",
  "PT",
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
  "PLR2004",
  "S101",
]
```

Do not enable `ANN`, `D`, `PL`, or `S` by default. The `PLR2004` and `S101` test ignores are
intentional future-proofing and pytest policy documentation.

## Baseline Packaging

For new setup only, configure enough Hatchling metadata for editable installs, tests, and a
basic build. Defer advanced packaging, publishing, dynamic versioning, optional extras,
entry point policy beyond the optional CLI stub, and artifact inspection to
`python-packaging`.

Explicitly configure Hatchling package inclusion for the `src/` layout:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/<import_package>"]

[tool.hatch.build.targets.sdist]
include = [
  "src/<import_package>",
  "tests",
  "README.md",
  "pyproject.toml",
]
```

Include `src/<import_package>/py.typed` for every project profile. Do not add package data
beyond `py.typed` by default. Do not add `license-files` by default, especially for monorepo
subprojects where the root license is outside the project root.

## Generated Python Style

Generated text files use LF line endings and end with a trailing newline.

All generated Python files include:

```python
from __future__ import annotations
```

Place it after the module docstring and before imports or code. Add explicit return
annotations to all generated functions.

Use concise Google-style docstrings for generated production code. This setup skill only
owns starter-file docstrings; use `python-docs` for broader documentation and docstring
work.

Default package `__init__.py`:

```python
"""<Project description>."""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.1.0"
```

Default smoke test:

```python
from __future__ import annotations

from <import_package> import __version__


def test_package_exposes_version() -> None:
    assert __version__ == "0.1.0"
```

Use behavior-descriptive test names. Use `pytest.mark.parametrize` with IDs when generated
tests cover repeated setup-stub cases such as logging levels.

## Optional CLI And Observability Stubs

If the user enables a CLI during setup, create only the minimal agreed setup stub and follow
`python-cli` for canonical CLI details. The setup stub uses Typer, creates
`interfaces/cli.py`, adds a console script wrapper, includes global logging flags, and adds
a `version` command.

If the user enables structlog during setup, create only the minimal agreed logging stub and
follow `python-observability` for canonical logging details. CLI support implies structlog
support.

Do not let optional stubs turn this skill into a domain implementation skill. If the user
asks for command design, subcommands, logging architecture, metrics, tracing, or production
observability policy, switch to the specialized skill after the baseline project exists.

## README

Use `README.md` as the project readme relative to the Python project root.

- Single-project repos use the root README.
- Monorepo projects get a local README inside the project root.
- Never overwrite an existing README. Ask before appending generated sections.
- Create README only if missing.

Generated README content should be concise and include:

- project name and description
- uv as the dependency manager
- just as the primary task interface
- development commands: `just sync`, `just check`, `just lint`, `just type`, `just test`,
  and `just fix`
- pytest with branch coverage and an 80% minimum threshold
- logging configuration table when CLI/logging is enabled

Do not add badges by default. Use `python-docs` for substantive README, examples, API docs,
or documentation toolchain work.

## Just And Mise Integration

`just check` is the canonical validation command. Root `mise run check` should delegate to
`just check`:

```toml
[tasks.check]
run = "just check"
```

Inspect existing `mise.toml`; preserve existing tasks unless the delegation is missing and
safe to add. Do not create nested `mise.toml` files.

Single-project repos use the root `justfile`. Monorepo projects get a local project-level
`justfile` and root `just check` delegates to it.

Local Python project recipes:

```make
set shell := ["bash", "-euo", "pipefail", "-c"]

default: check

sync:
    uv sync --group dev

lock:
    uv lock

lint:
    uv run --group lint ruff format --check .
    uv run --group lint ruff check .

type:
    uv run --group type ty check

test:
    uv run --group test pytest

check: lint type test

fix:
    uv run --group lint ruff format .
    uv run --group lint ruff check --fix .

fix-unsafe:
    uv run --group lint ruff format .
    uv run --group lint ruff check --fix --unsafe-fixes .

build:
    uv build

clean:
    rm -rf .coverage .coverage.* htmlcov .pytest_cache .ruff_cache dist build *.egg-info
    find . -type d -name __pycache__ -prune -exec rm -rf {} +
```

Do not include pass-through recipes for pytest, Ruff, or ty by default. Do not remove
`.venv` in `clean` and do not create `clean-venv` by default.

For monorepo root aggregation, prefer changing directory:

```make
check-python-<name>:
    cd <project-root> && just check
```

If root `check` does not exist, create it. If it exists, add a project-specific recipe and
modify `check` only when the dependency pattern is clear. Otherwise ask before changing root
validation logic.

## Gitignore

Update the root `.gitignore` only. Add missing standard generated Python artifacts:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.ruff_cache/
.coverage
.coverage.*
htmlcov/
dist/
build/
*.egg-info/
```

Do not add `.mypy_cache/`, speculative `.ty/`, uv cache directories, or `uv.lock` ignores by
default.

## Workflow

1. Find the Git repository root and verify the base repo baseline files.
2. Ask and confirm every required decision.
3. Determine the Python project root.
4. Inspect target paths and hard-stop on existing Python project files unless approved.
5. Create the project directory and selected monorepo category parent when needed.
6. Create package, test, README, `pyproject.toml`, `py.typed`, and approved optional CLI or
   logging setup stubs.
7. Create or update the relevant `justfile` recipes.
8. Update root `.gitignore` with missing Python generated artifact entries.
9. Inspect root `mise.toml` and ensure `mise run check` delegates to `just check` when safe.
10. Run `uv sync --group dev` from the Python project root to generate `uv.lock`.
11. Run the local validation and build commands.
12. For monorepos, run root `just check` to verify aggregation.
13. Report decisions, files changed, commands run, validation results, and skipped optional
    items.

## Validation

For single-project repos, finish only after these pass from the project/repo root:

```sh
uv sync --group dev
just check
just build
```

For monorepo projects, finish only after these pass:

```sh
cd <project-root> && uv sync --group dev
cd <project-root> && just check
cd <project-root> && just build
just check
```

`just build` is required during setup completion even though it is not part of daily
`just check`.

If a command cannot be run, report the exact blocker and the command that remains unrun.

## Completion

Report:

- project root
- repository shape, monorepo kind/name, and recommendation profile
- distribution name and import package name
- Python version and initial version
- author and license metadata decisions
- CLI choice, command name, and environment variable prefix when relevant
- structlog choice and logging defaults when relevant
- files created and modified
- commands run and results
- coverage result and 80% branch coverage threshold status
- intentionally skipped optional items such as CI, docs toolchain, tox/nox, security tools,
  changelog, badges, or publishing metadata
