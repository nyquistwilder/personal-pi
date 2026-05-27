# <PROJECT_NAME>

<ONE_PARAGRAPH_PROJECT_OVERVIEW>

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

<SHORT_DESCRIPTION_OF_REPO_LAYOUT>

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
