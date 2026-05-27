---
name: base-repo-setup
description: Strict personal workflow for scaffolding a brand-new Git repository from a universal baseline. Use when Codex is asked to initialize, scaffold, set up, bootstrap, or create a new repository/project/repo before adding language, framework, application, release, deployment, or ecosystem-specific files. The skill copies the bundled base repository assets, replaces required placeholders, generates flake.lock, trusts mise, installs prek hooks, and runs validation.
---

# Base Repo Setup

## Rule

Scaffold the repository. Do not only propose a structure.

This baseline is mandatory, strict, and language-agnostic. Do not add optional directories, language files, framework files, package manager files, docs, tests, source trees, changelog files, contribution files, security files, or release/deployment config unless the user explicitly asks for a later project profile after this baseline is complete.

## Required Context

Read `references/base-repo-policy.md` before changing files. It is the source of truth for the baseline file list, tool ownership, naming, indentation, hooks, CI, Nix, mise, formatting, linting, and security scanning.

Read `references/scaffold-workflow.md` when executing the scaffold. It gives the exact input rules, command sequence, validation expectations, and failure handling.

## Execution

Use the bundled script for deterministic file creation:

```sh
python3 <skill-dir>/scripts/scaffold_base_repo.py <target-repo> \
  --project-name "<PROJECT_NAME>" \
  --overview "<ONE_PARAGRAPH_PROJECT_OVERVIEW>" \
  --layout "<SHORT_DESCRIPTION_OF_REPO_LAYOUT>" \
  --copyright-holder "<COPYRIGHT HOLDER>"
```

Then run the required initialization commands from the target repository:

```sh
nix flake lock
git add flake.lock
mise trust
mise run install-hooks
mise run check
```

If mise cannot be used, run the direct fallback from the policy:

```sh
nix develop
just install-hooks
just check
```

Do not skip `nix flake lock`; `flake.lock` is required in real repositories even though it is not stored in the asset template.

## Missing Inputs

Infer `project-name` from the target directory name when the user does not provide it.

Use the current calendar year for `--year` when omitted.

Use `git config user.name` for `copyright-holder` only if the user did not provide a holder and the value is clearly available. Otherwise ask for the missing holder before scaffolding.

Ask for a one-paragraph overview and layout description if the user did not provide enough information to replace the README placeholders. Do not invent project purpose text.

## Completion

Finish only after:

- The target is a Git repository.
- The baseline files are staged so Nix can evaluate the Git-backed flake.
- All bundled baseline files are present.
- `flake.lock` exists.
- Required placeholders are gone from every copied text file, including `README.md`, `LICENSE`, and `flake.nix`.
- Hooks were installed or a concrete blocker was reported.
- `mise run check` or the fallback `just check` was run, with the result reported.
