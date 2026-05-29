---
name: go-project-setup
description: Set up a brand-new greenfield Go module after base-repo-setup, using modern Go modules, cmd/internal layout when useful, standard-library-first defaults, slog, tests, lint/security wrappers, and local just check validation. Use only for new Go scaffolding, not migrations.
---

# Go Project Setup

## Rule

Scaffold a brand-new Go project; do not only propose a structure. Layer Go-specific
conventions on top of `base-repo-setup` and target greenfield work only.

Greenfield Go should be boring, small, standard-library-first, and easy to build as a single
static-ish binary. Add frameworks only when the problem justifies them.

## Hard Stops

Stop before writing files when:

- The repository baseline is missing (`flake.nix`, `mise.toml`, `justfile`, `.gitignore`).
- The target already has `go.mod`, `go.sum`, `cmd/`, `internal/`, or source files that would
  be overwritten.
- Module path, binary/library shape, minimum Go version, license, or public API intent is
  unclear.
- The user asks for legacy migration, framework migration, or preserving pre-existing Go
  layout; these greenfield skills are not migration skills.
- A dependency, external service, database, or generated-code tool would be introduced
  without explicit approval.

## Required Decisions

Ask and confirm these before scaffolding:

1. Module path. Recommend a canonical VCS path such as `github.com/<owner>/<repo>` when
   publishable, or a private module path for internal work.
2. Project shape: binary app, library module, or multi-command app.
3. Minimum Go version and toolchain policy. Recommend the current stable Go from the repo
   environment; set the `go` directive intentionally and add a `toolchain` directive only
   when the project wants toolchain auto-selection.
4. Binary name and `cmd/<name>` path for apps.
5. Initial package names. Recommend short lowercase names without underscores.
6. Whether HTTP API, CLI, database, config files, or observability scaffolding is in scope.
   Default is no; use specialized skills after the baseline exists.

## Greenfield Defaults

- Use Go modules. Track `go.mod` and `go.sum`.
- Prefer standard library first: `testing`, `net/http`, `log/slog`, `flag`, `context`,
  `database/sql`, `errors`, `cmp`, `slices`, `maps`, and `iter` when supported by the
  chosen Go version.
- Keep dependencies out of the initial scaffold unless generated code imports them.
- Use `cmd/<binary>/main.go` for apps and `internal/` for app-private packages.
- Use root package files for small libraries; add subpackages only around cohesive concepts.
- Do not create `pkg/` by default. It is not a public API guarantee and often becomes a junk
  drawer.
- Keep `main` thin: parse config, configure logging, construct dependencies, call `run`.
- Use `log/slog` for logging. Do not introduce zap, zerolog, or logrus in greenfield code
  without a specific operational reason.
- Use native tests with table cases and subtests. Add `go-cmp` only when diffs are materially
  better than `==` or `reflect.DeepEqual`.

## Layout

Small binary app:

```text
.
|-- go.mod
|-- go.sum
|-- cmd/
|   `-- <binary>/
|       `-- main.go
|-- internal/
|   `-- app/
|       |-- app.go
|       `-- app_test.go
`-- README.md
```

Small library:

```text
.
|-- go.mod
|-- go.sum
|-- <package>.go
|-- <package>_test.go
`-- README.md
```

Use `internal/<domain>` for application internals and short public package names for library
APIs. Split packages by responsibility, not by layer names such as `utils`, `helpers`, or
`common`.

## Tooling

Wire local commands through `just` and keep `just check` as the canonical validation
interface. Prefer this baseline:

```make
fmt:
    gofmt -w .

fmt-check:
    test -z "$(gofmt -l .)"

vet:
    go vet ./...

lint:
    staticcheck ./...

test:
    go test ./...

test-race:
    go test -race ./...

vuln:
    govulncheck ./...

build:
    go build ./...

check: fmt-check vet lint test build vuln
```

Use `golangci-lint` only when the project explicitly wants an aggregate runner; keep
`gofmt`, `go vet`, `staticcheck`, `go test`, and `govulncheck` understandable without it.
Add tool versions through `flake.nix`, `mise.toml`, `go install` tool recipes, or an
approved tool-management policy; do not hide versions in ad-hoc scripts.

## Workflow

1. Verify the baseline repository files and Git root.
2. Ask all required decisions.
3. Create `go.mod`, source skeleton, smoke tests, README updates, and just recipes.
4. Add `.gitignore` entries only for generated Go artifacts if missing (`bin/`, `coverage.*`,
   `*.test`, `*.prof`). Do not ignore `go.sum`.
5. Run `go mod tidy`.
6. Run `gofmt`, `go test ./...`, `go vet ./...`, `staticcheck ./...` when available, and
   `just check`.

## Completion

Report module path, Go/toolchain policy, project shape, files created, dependencies added or
avoided, commands run, validation results, and intentionally skipped optional items such as
HTTP frameworks, CLI frameworks, database, OpenTelemetry, release automation, or CI.
