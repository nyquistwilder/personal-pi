# skills

skills is a personal repository of opinionated Codex skill definitions, supporting
scripts, reference material, and bundled assets used to capture repeatable workflows
and tool conventions.

## Requirements

- Nix with flakes enabled
- mise

## Setup

```sh
mise trust
mise run install-hooks
mise run shell
```

## Development

```sh
mise run fmt
mise run check
```

Direct Nix fallback:

```sh
nix develop
just check
```

## Project Structure

Each top-level directory represents a skill and may contain SKILL.md plus supporting
references, scripts, agents, or assets needed by that skill.

## Troubleshooting

If mise tasks do not run, verify that the project config is trusted:

```sh
mise trust
```

If Nix commands fail after editing flake inputs, regenerate the lock file:

```sh
nix flake lock
```

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
