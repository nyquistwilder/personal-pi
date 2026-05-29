---
name: go-modules
description: Go module and dependency workflow for adding, removing, upgrading, replacing, auditing, tidying, and evaluating dependencies, module paths, workspaces, tool versions, licenses, and vulnerability posture in greenfield Go projects.
---

# Go Modules

## Rule

Keep dependencies minimal, explicit, reproducible, and justified. Prefer the standard
library or existing dependencies when sufficient, and keep module metadata tidy.

## Hard Stops

Ask before:

- Adding large frameworks, code generators, CLIs, ORMs, telemetry stacks, or crypto/auth
  libraries.
- Changing module path, minimum Go version, `toolchain`, workspace shape, or public import
  paths.
- Adding `replace` directives, private modules, pseudo-versions, forks, cgo dependencies, or
  transitive dependency pinning.
- Removing or downgrading unrelated modules to resolve conflicts.
- Accepting a vulnerable, unmaintained, or incompatible dependency without explicit risk
  approval.

## Defaults

- Use `go get` for dependency add/upgrade/downgrade and `go mod tidy` afterward.
- Commit `go.mod` and `go.sum` changes together.
- Avoid `replace` in committed code except for approved local development or temporary fork
  policies with comments.
- Prefer small, well-maintained modules with compatible licenses, stable APIs, low
  transitive footprint, and current Go support.
- Run `govulncheck ./...` when available.
- Keep tool versioning in `flake.nix`, `mise.toml`, CI setup, or approved `tools.go` policy;
  do not rely on one-off global installs.

## Approved Greenfield Preferences

Use only when the need is real and approved:

- HTTP routing: stdlib `http.ServeMux` first; `go-chi/chi/v5` for richer routing/middleware.
- CLI: stdlib `flag` first; `spf13/cobra` for public multi-command CLIs.
- Config: stdlib env/flags first; `caarlos0/env/v11` for structured env parsing when needed.
- Database: `jackc/pgx/v5`; `golang-migrate/migrate/v4` for migrations.
- Testing: `google/go-cmp`; `testcontainers-go` only for integration tests that need real
  services.
- Observability: stdlib `log/slog`; OpenTelemetry packages only with an operational target.

Avoid adding `testify`, global DI containers, web frameworks, ORMs, or logging libraries by
default.

## Workflow

1. Identify why a dependency is needed and whether stdlib/existing code can satisfy it.
2. Inspect `go.mod`, `go.sum`, Go version, build tags, and transitive footprint.
3. Check license, maintenance, vulnerabilities, cgo use, platform support, and API stability.
4. Add/remove/upgrade with Go commands, for example:

   ```sh
   go get example.com/module@latest
   go get example.com/module@v1.2.3
   go get example.com/module@none
   go mod tidy
   ```

5. Run targeted tests, `go test ./...`, `go vet`, `staticcheck`, `govulncheck`, and
   `just check`.
6. Document new user-facing dependencies or tool requirements.

## Completion

Report dependency/module changes, rationale, versions, transitive or license/security
concerns, commands run, lockfile/checksum changes, and validation results.
