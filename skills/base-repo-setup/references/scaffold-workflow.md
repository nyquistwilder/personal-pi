# Scaffold Workflow

Use this workflow exactly when creating a new repository baseline.

## Inputs

Required:

- Target repository path.
- Project name. Infer from the target directory name if omitted.
- One-paragraph project overview for `README.md`.
- Short repository layout description for `README.md`.
- Copyright holder for `LICENSE`. Use `git config user.name` only when the user omitted the holder and the value exists.
- Copyright year. Use the current calendar year if omitted.

Ask only for missing text that cannot be inferred. Do not ask about file layout, tools, hooks, CI, formatting, linting, security scanning, indentation, naming, or optional directories; those are fixed by `base-repo-policy.md`.

## Target Rules

The target path may be missing, empty, or an initialized Git repository containing only `.git`.

Refuse to scaffold into a directory containing any project files. Do not merge this baseline over an existing project and do not overwrite files.

The repository must be initialized with Git. If `.git` does not exist, initialize it.

## File Creation

Run:

```sh
python3 <skill-dir>/scripts/scaffold_base_repo.py <target-repo> \
  --project-name "<PROJECT_NAME>" \
  --overview "<ONE_PARAGRAPH_PROJECT_OVERVIEW>" \
  --layout "<SHORT_DESCRIPTION_OF_REPO_LAYOUT>" \
  --copyright-holder "<COPYRIGHT HOLDER>"
```

The script copies `assets/base-repo-structure/`, replaces placeholders in every copied text file, refuses non-empty targets, runs `git init` when needed, and stages the baseline with `git add .`.

## Required Post-Scaffold Commands

Run from the target repository:

```sh
nix flake lock
git add flake.lock
mise trust
mise run install-hooks
mise run check
```

If `mise` is unavailable or cannot be trusted in the current environment, use the direct fallback:

```sh
nix develop
just install-hooks
just check
```

The fallback is not a way to skip Nix. It is only a way to bypass mise as the local workflow layer.

Keep the initial `git add .` behavior from the scaffold script. Nix flakes in Git repositories evaluate the Git-tracked file set, so `flake.nix` must be staged before `nix flake lock` runs. Stage `flake.lock` immediately after generating it.

## Validation

Confirm:

- `flake.lock` exists.
- The baseline files and generated `flake.lock` are staged for the first commit.
- The required baseline files listed in `base-repo-policy.md` exist.
- No required placeholders remain in copied text files, including `README.md`, `LICENSE`, and `flake.nix`.
- No prohibited universal-baseline files were added: `assets/`, `scripts/`, `docs/`, `src/`, `tests/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CODEOWNERS`, or `SECURITY.md`.
- Hook installation was attempted and any blocker is reported concretely.
- `mise run check` or `just check` completed, or the exact failing command and failure reason is reported.

## Reporting

Report the target path, files created, lockfile status, hook status, and validation result. Keep the summary factual. Do not suggest language or framework next steps unless the user asks for a profile.
