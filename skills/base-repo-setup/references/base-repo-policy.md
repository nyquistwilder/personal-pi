# Base Repository Structure

This specification defines the universal baseline for new repositories. It is intentionally language- and framework-agnostic, so it can support web applications, mobile applications, command-line tools, libraries, and infrastructure projects without forcing empty application directories.

The starter files live in `assets/base-repo-structure/`. Copy those files into a new repository, replace placeholders, generate `flake.lock`, install hooks, and run the validation command before the first commit.

## Design Principles

- Keep the universal baseline strict and small. Language, framework, platform, release, and deployment conventions belong in optional profiles added later.
- Make `flake.nix` the source of truth for baseline tool versions.
- Make `mise.toml` the source of truth for project environment variables and local workflow entrypoints.
- Make `justfile` the source of truth for task composition.
- Make `prek.toml` the source of truth for local Git hooks.
- Keep CI authoritative and reproducible by running through the Nix dev shell.
- Prefer configuration files at the repository root unless a tool convention requires a subdirectory.
- Prefer `kebab-case` for generic directories and `snake_case` for generic files. Allow both. Discourage `camelCase` unless an ecosystem convention requires it.
- Prefer tabs for indentation when no language specification, official style guide, strong ecosystem convention, or formatter contract says otherwise.

## Required Baseline Files

```text
.
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .gitleaks.toml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .ls-lint.yml
├── .prettierignore
├── .prettierrc.json
├── .rumdl.toml
├── .trivyignore
├── AGENTS.md
├── LICENSE
├── README.md
├── flake.nix
├── justfile
├── mise.local.toml.example
├── mise.toml
├── prek.toml
├── statix.toml
├── trivy.yaml
└── typos.toml
```

`flake.lock` is required in real repositories, but it is not part of the starter assets. Generate it during initialization with `nix flake lock`, then commit it.

Do not include `assets/`, `scripts/`, `docs/`, `src/`, `tests/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CODEOWNERS`, or `SECURITY.md` in the universal initialized repo unless the project actually needs them.

## EditorConfig

`.editorconfig` is the cross-editor indentation and whitespace contract. The default is tabs, displayed at width 4:

```ini
indent_style = tab
indent_size = tab
tab_width = 4
```

Use spaces only when required or strongly expected by a language, data format, or formatter:

| Files | Indentation |
| --- | --- |
| C, C++, JavaScript, TypeScript, CSS, SQL, Dockerfile | tabs, width 4 |
| Bash/sh, Go, CUE, Makefile | tabs, width 4 |
| JSON, JSONC, TOML, Nix, Markdown, YAML, Terraform/HCL | 2 spaces |
| Python, Rust, Zig, Java | 4 spaces |

Helm chart YAML follows the YAML rule. Helm helper templates such as `*.tpl` are intentionally left for a Helm profile because generic template files are ambiguous.

Markdown keeps `trim_trailing_whitespace = false` because trailing spaces can be meaningful, although the style preference is to avoid hard-break whitespace where practical.

## Initialization

1. Copy the contents of `assets/base-repo-structure/` into the new repository root.
2. Replace placeholders:
   - `<PROJECT_NAME>` in `README.md` and `flake.nix`.
   - `<ONE_PARAGRAPH_PROJECT_OVERVIEW>` in `README.md`.
   - `<SHORT_DESCRIPTION_OF_REPO_LAYOUT>` in `README.md`.
   - `<YEAR>` and `<COPYRIGHT HOLDER>` in `LICENSE`.
   - Optional local values in `mise.local.toml.example`.
3. Stage the baseline files so Nix can evaluate the Git-backed flake:

   ```sh
   git add .
   ```

4. Generate and stage the lock file:

   ```sh
   nix flake lock
   git add flake.lock
   ```

5. Trust the mise config after inspecting it:

   ```sh
   mise trust
   ```

6. Install local Git hooks:

   ```sh
   mise run install-hooks
   ```

7. Validate the repository:

   ```sh
   mise run check
   ```

The direct fallback is:

```sh
nix develop
just install-hooks
just check
```

## Environment Variables

`mise.toml` is committed and may contain only non-secret defaults, such as `PROJECT_ENV = "development"`. Do not put secrets, credentials, tokens, machine-specific paths, or private service URLs in `mise.toml`.

Use ignored `mise.local.toml` for local secrets and machine-specific overrides. Commit `mise.local.toml.example` with commented examples only, so required local variables are documented without being active.

`.env` and `.env.*` are ignored defensively because many frameworks create or consume them even though mise is the baseline environment manager. Do not include `.env.example` in the universal baseline; add it only in a profile that explicitly needs dotenv files.

## Formatting

`nix fmt` is the universal formatting command. It is backed by `treefmt-nix` and formats all baseline-supported file types:

- Nix with `nixfmt`.
- Markdown with `rumdl`.
- TOML with `taplo`.
- YAML with `yamlfmt`.
- JSON and JSONC with `prettier`.
- Shell scripts with `shfmt`.

Focused formatter recipes are available through `just`:

```sh
just fmt
just fmt-nix
just fmt-md
just fmt-toml
just fmt-yaml
just fmt-json
just fmt-shell
just fmt-check
```

## Linting

The baseline lint set is:

- Nix: `statix check .` and `deadnix --fail .`.
- Markdown: `rumdl check .`.
- TOML: `taplo check`.
- YAML: `yamlfmt -lint .`.
- JSON: `jq` syntax validation for `.json` files.
- GitHub Actions: `actionlint`.
- Shell: `shellcheck`, only when shell files exist.
- File naming: `ls-lint`.
- EditorConfig: `editorconfig-checker`.
- Spelling: `typos`, blocking in CI and local validation.

Run all linting with:

```sh
just lint
```

Granular recipes are available for local debugging:

```sh
just lint-nix
just lint-md
just lint-toml
just lint-yaml
just lint-json
just lint-actions
just lint-shell
just lint-file-names
just lint-editorconfig
just lint-spelling
```

## Security Scanning

Gitleaks is the primary secret scanner. It runs in local pre-commit hooks and in `just check`:

```sh
just security-gitleaks
```

Full-history secret scanning is a manual audit command:

```sh
just security-gitleaks-history
```

Trivy runs in `just check` and CI, not in local pre-commit hooks. It blocks only on `HIGH` and `CRITICAL` vulnerability and misconfiguration findings. Ignored Trivy findings must be documented in `.trivyignore` with a reason, reviewer, and expiry date.

```sh
just security-trivy
```

## Git Hooks

The baseline uses `prek` with native `prek.toml`.

Install both hook types explicitly:

```sh
prek install --hook-type pre-commit --hook-type commit-msg
```

The pre-commit hook may auto-format files. Developers must review and re-stage any modified files before committing. The hook also runs linting and Gitleaks, but does not run Trivy.

The commit-msg hook enforces Conventional Commits locally with a lightweight `just commit-msg-check` recipe.

Allowed commit types:

```text
build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test
```

Allowed scope pattern:

```text
[a-z0-9._-]+
```

Allowed exceptions:

```text
Merge ...
Revert ...
fixup! ...
squash! ...
```

Baseline CI does not enforce commit ranges because that depends on branch policy, PR style, squash merge behavior, and release workflow.

## CI

The universal CI target is Linux only. The GitHub Actions workflow installs Nix with the Determinate Systems installer action and then runs:

```sh
nix develop --command just check
```

CI runs checks, not auto-formatting. It does not require mise because mise is the local workflow layer.

## Nix

The baseline uses flakes only. Do not include `shell.nix` or `default.nix` unless a specific project has a compatibility requirement.

`flake.nix` uses:

- `nixos-unstable`, pinned by `flake.lock`.
- Plain flake outputs, not `flake-parts`.
- Inline supported systems:
  - `x86_64-linux`
  - `aarch64-linux`
  - `aarch64-darwin`
- `formatter.<system>` for `nix fmt`.
- `checks.<system>.formatting` for `nix flake check`.
- `devShells.default` for all baseline tools.

Do not put project runtime environment variables in the dev shell. Mise owns project env vars.

## Naming

Generic directory names should prefer `kebab-case`. Generic file names should prefer `snake_case`. Both are allowed.

`camelCase` is discouraged except where required by ecosystem conventions. Conventional files such as `README.md`, `LICENSE`, `AGENTS.md`, `Dockerfile`, `Makefile`, `flake.nix`, and tool config files are explicitly allowed.

Future project profiles may add exceptions such as `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Info.plist`, or platform asset names.

## Optional Profiles

Optional profiles are intentionally deferred. Add profile documents later for concrete needs such as:

- Web applications.
- Mobile applications.
- CLI tools.
- Public libraries.
- Release automation.
- Docker/container deployment.
- Language ecosystems such as JavaScript, Python, Rust, Go, Swift, Kotlin, or Java.

Profiles may add directories, package manager files, runtime declarations in `mise.toml`, extra formatters/linters, CI matrix entries, release policy, changelog tooling, or framework-specific ignore rules.
