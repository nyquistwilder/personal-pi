---
name: go-ci
description: Go CI workflow for reproducible toolchains, module cache, fmt/vet/staticcheck/test/race/build/govulncheck jobs, artifacts, and release gates aligned with local just check.
---

# Go CI

## Rule

CI must mirror local validation and make failures actionable. Keep `just check` as the local
source of truth when present.

## Hard Stops

Ask before:

- Adding or changing CI providers, paid services, credentials, release secrets, or publishing
  jobs.
- Requiring nightly/development Go versions or changing the repository toolchain policy.
- Uploading coverage, SBOMs, binaries, or containers to external systems.
- Making CI-only checks that developers cannot run locally.

## Defaults

- Use stable Go from project policy with `actions/setup-go` on GitHub Actions when GitHub CI
  is already used or requested.
- Cache modules/build cache through official CI mechanisms.
- Run `go mod download` or `go mod verify`, `gofmt` check, `go vet`, `staticcheck`,
  `go test ./...`, `go test -race ./...` when affordable, `go build ./...`, and
  `govulncheck ./...`.
- Prefer invoking `just check`; keep detailed commands in `justfile` to align local and CI.
- Upload test/coverage artifacts only when the project consumes them.

## Workflow

1. Inspect local wrappers, Go version policy, existing CI, and release gates.
2. Add or update CI to call local wrappers and install required tools reproducibly.
3. Configure module/build caches without caching generated artifacts in git.
4. Separate fast PR checks from slower scheduled/security/race matrices when needed.
5. Validate YAML and run local `just check`.

## Antipatterns

- CI commands drifting from local `just check`.
- Installing latest tools with no version policy.
- Ignoring `go.sum` changes or skipping `go mod tidy` checks.
- Race/security scans only after release.

## Completion

Report CI files changed, jobs/checks, toolchain/cache strategy, local validation, and release
gates.
