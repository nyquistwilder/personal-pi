---
name: python-packaging
description: Python packaging workflow for pyproject metadata, build backends, package discovery, optional extras, console scripts, wheels, sdists, artifact checks, and publish readiness in uv-managed projects.
---

# Python Packaging

## Rule

Package Python projects so installs, editable development, wheels, and sdists are
reproducible and inspectable. Keep packaging metadata explicit and avoid publishing-oriented
changes unless publishing is in scope.

Use this skill for distributable libraries or applications. Use `python-project-setup` for
baseline new-project scaffolding and `python-release` for version bumps, tags, and publishing
operations.

## Hard Stops

Stop and ask before changing packaging when:

- The distribution name, import package name, versioning policy, or publishing target is
  unclear.
- A change may break existing imports, entry points, extras, artifact contents, or downstream
  consumers.
- Dynamic versioning, package data, native extensions, namespace packages, or monorepo
  packaging is involved and current policy is not documented.
- Publishing, tagging, uploading, deleting releases, or modifying remote package state would
  be required.
- Dependency additions are not clearly runtime, optional, or development-only.

## Packaging Defaults

For greenfield personal-baseline projects:

- Use `pyproject.toml` as the single packaging metadata source.
- Use Hatchling as the baseline build backend unless the project has a reason for another
  backend.
- Use a `src/` layout and explicitly configure wheel package inclusion.
- Include `py.typed` for typed packages.
- Use static versions by default and align package `__version__` when present.
- Keep runtime dependencies minimal and sorted.
- Use optional dependencies or extras only when they are part of a documented install
  contract.
- Generate and track `uv.lock` for applications and personal-baseline libraries.

## Workflow

1. Inspect `pyproject.toml`, lockfile, package layout, README, license, and current build
   backend.
2. Identify artifact consumers: local app, internal library, PyPI package, container, plugin,
   or CLI.
3. Validate project metadata: name, version, description, Python requirement, authors,
   license, readme, classifiers, URLs, scripts, and dependencies.
4. Validate package discovery and package data. Ensure unwanted files are excluded and
   required runtime files are included.
5. Build artifacts with uv, normally `uv build` or the project `just build` wrapper.
6. Inspect wheel and sdist contents. Confirm imports and console scripts work from the built
   artifact when practical.
7. Run `just check` or the repository validation command.

## Artifact Checks

Useful checks include:

```sh
uv build
python -m zipfile --list dist/*.whl
python -m tarfile --list dist/*.tar.gz
```

Use temporary virtual environments or `uv run --with dist/<wheel>` style smoke checks when
install behavior is the contract.

Do not commit `dist/`, `build/`, or `*.egg-info/` artifacts unless the repository explicitly
requires generated artifacts.

## Review Guidance

Flag missing or misleading metadata, undeclared runtime dependencies, accidental package data,
imports that work only from the source tree, broken console scripts, inconsistent versioning,
and extras that are undocumented or over-broad.

## Completion

Report metadata changed, artifact contents verified, build commands run, install or import
smoke tests run, and any publish-readiness gaps.
