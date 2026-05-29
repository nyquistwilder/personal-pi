---
name: rust-release
description: Rust release workflow for version bumps, changelogs, tags, cargo package, crates.io publishing, release-plz, cargo-dist, checksums, binaries, SBOMs, safeguards, and post-release verification.
---

# Rust Release

## Rule

Validate before publishing and require explicit approval for irreversible operations.

## Hard Stops

Stop before:

- Tagging, publishing to crates.io, pushing release pages, signing artifacts, uploading
  binaries, publishing containers, or using credentials.
- Releasing from a dirty tree or with failing validation unless explicitly approved.
- Adding `release-plz`, `cargo-dist`, signing, SBOM, or provenance automation without
  approval.
- Publishing public crates without checking SemVer and package contents.

## Defaults

- Run full validation, inspect `cargo package`, and keep generated artifacts out of git.
- Use `cargo semver-checks` for public library crates when configured or before publishing.
- Use `release-plz` for crate release PRs/changelogs/version bumps when approved.
- Use `cargo-dist` for binary distribution when cross-platform installers/artifacts are
  needed and approved.
- Generate checksums for binary artifacts; add signing/SBOM/provenance only when policy
  requires it.
- Start new automation with dry runs.

## Workflow

1. Inspect version policy, changelog, git state, CI, crate metadata, features, and release
   targets.
2. Confirm target version and publish targets.
3. Run `just check`, package/build/doc checks, semver checks when relevant, and
   `cargo package --list`.
4. Build artifacts in ignored directories and inspect contents.
5. Ask before tagging, publishing, signing, or uploading.
6. Verify published crates or artifacts when approved.

## Completion

Report target version, files changed, artifacts, package checks, tag/publish actions
performed or skipped, and verification results.
