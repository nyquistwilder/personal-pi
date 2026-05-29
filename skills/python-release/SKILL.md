---
name: python-release
description: Python release workflow for version bumps, changelogs, release notes, tags, wheel/sdist validation, publishing safeguards, and post-release verification.
---

# Python Release

## Rule

Prepare releases with explicit approval for irreversible operations. Validate artifacts before
publishing and keep version, changelog, tags, and distribution metadata consistent.

Use this skill for release preparation and publishing. Use `python-packaging` for packaging
metadata and artifact structure outside a release process.

## Hard Stops

Stop and ask before:

- Creating, moving, or deleting git tags or GitHub/GitLab releases.
- Publishing to PyPI, TestPyPI, internal indexes, containers, or deployment systems.
- Bumping versions without knowing the target version and versioning policy.
- Using credentials, tokens, signing keys, or trusted publishing configuration.
- Releasing with failing tests, dirty working tree, or unreviewed generated artifacts unless
  the user explicitly accepts the risk.

## Release Defaults

- Prefer a clean git working tree before release validation.
- Use static versioning unless the project already uses dynamic versioning.
- Build wheels and sdists with uv or the project wrapper.
- Inspect artifacts before upload.
- Keep `dist/` artifacts out of git unless repository policy says otherwise.
- Use TestPyPI or a dry run when introducing a new publishing path.

## Workflow

1. Inspect version sources, changelog/release notes, packaging metadata, CI status, and git
   state.
2. Confirm target version, release scope, and publish target.
3. Update version and changelog/release notes if requested.
4. Run full validation, normally `just check` plus build/artifact checks.
5. Inspect wheel and sdist contents.
6. Ask for explicit approval before tagging or publishing.
7. Perform approved irreversible operations only after validation.
8. Verify published artifact or release page when applicable.

## Artifact Validation

Run the project's build command and inspect contents, for example:

```sh
uv build
python -m zipfile --list dist/*.whl
python -m tarfile --list dist/*.tar.gz
```

Smoke-test import and console scripts from the built wheel when practical.

## Completion

Report target version, files changed, validation commands, artifact checks, tag/publish
operations performed or skipped, and post-release verification results.
