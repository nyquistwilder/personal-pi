# Agent Instructions

## Environment

Use the Nix development shell for tooling:

```sh
nix develop
```

The primary local workflow uses mise:

```sh
mise run check
```

## Validation

Run before handing work back:

```sh
just check
```

## Tooling Rules

- Do not introduce baseline tool versions outside `flake.nix`.
- Keep project environment variables in `mise.toml` or ignored `mise.local.toml`.
- Keep generated files out of version control unless the project explicitly requires them.
