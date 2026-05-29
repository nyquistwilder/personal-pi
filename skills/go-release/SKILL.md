---
name: go-release
description: Go release workflow for versioning, changelogs, tags, goreleaser when approved, checksums, SBOMs, binaries, container images, safeguards, and post-release verification.
---

# Go Release

## Rule

Validate before publishing and require explicit approval for irreversible operations.

## Hard Stops

Stop before:

- Creating tags, pushing tags, publishing GitHub releases, uploading binaries, publishing
  containers, signing artifacts, or using credentials.
- Releasing from a dirty tree or failing validation unless explicitly approved.
- Introducing GoReleaser, signing, SBOM, or container release automation without approval.
- Changing module path or public import compatibility during release prep without migration
  planning.

## Defaults

- Run full local validation, including tests, race checks when practical, lint, build, and
  vulnerability checks.
- For libraries, ensure semantic import versioning rules are respected for v2+ modules.
- For binaries, build reproducible artifacts for target OS/architectures, generate
  checksums, and keep artifacts out of git.
- Use GoReleaser only when cross-platform release automation is needed and approved; start
  with dry runs.
- Generate SBOMs/signatures only when project release policy requires them.

## Workflow

1. Inspect version policy, changelog, git state, CI, module metadata, and release targets.
2. Confirm target version, artifacts, and irreversible steps.
3. Run `just check`, `go test ./...`, `go test -race ./...` when feasible, `go build ./...`,
   and `govulncheck ./...`.
4. Build/package artifacts and checksums in ignored directories.
5. Ask before tagging, pushing, publishing, or signing.
6. Verify published modules, binaries, checksums, and release notes after approval.

## Completion

Report target version, files changed, validation, artifacts/checksums, tag/publish actions
performed or skipped, and post-release verification.
