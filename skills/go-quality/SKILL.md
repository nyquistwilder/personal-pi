---
name: go-quality
description: Go quality workflow for gofmt, go vet, staticcheck, golangci-lint when configured, import hygiene, dead-code removal, warning fixes, and behavior-preserving cleanup in greenfield modules.
---

# Go Quality

## Rule

Improve Go code quality without changing behavior. Prefer mechanical, idiomatic, reviewable
changes aligned with `gofmt`, `go vet`, `staticcheck`, and project wrappers.

## Hard Stops

Stop and ask when:

- A lint fix changes public API, wire behavior, error semantics, concurrency behavior, or
  persistence schema.
- Removing apparently unused code could remove public exports, plugins, generated hooks,
  migrations, build-tagged files, or CLI entry points.
- A proposed suppression, build tag, or `//nolint` hides a real bug or lacks justification.
- Tooling is missing and adding `staticcheck`/`golangci-lint` is a policy change.

## Defaults

- Always run `gofmt`; use `goimports` only if already configured or approved.
- Run `go vet ./...` and `staticcheck ./...` for greenfield projects.
- Use `golangci-lint` only when configured; do not add a huge lint preset by default.
- Keep `//nolint` comments narrow and include a reason.
- Preserve generated files. Do not hand-edit generated code unless generation is unavailable
  and the user approves.

## Workflow

1. Inspect `go.mod`, build tags, generated files, and just/mise/CI wrappers.
2. Run `gofmt -w` or check mode as appropriate.
3. Run the configured lint commands.
4. Apply safe import cleanup, dead private code removal, simplifications, and warning fixes.
5. Run tests for touched packages and `just check`.

## Antipatterns

- Broad package reshuffles during lint cleanup.
- Adding `utils` packages to satisfy import cycles.
- Replacing clear code with clever generics for style.
- Suppressing `errcheck`, `staticcheck`, or `vet` findings without root-cause review.

## Completion

Report tools run, files cleaned, suppressions added with reasons, behavior-preserving
assumptions, and validation results.
