---
name: python-cli
description: Typer-first Python command-line application workflow for designing, implementing, testing, or reviewing CLI commands, options, subcommands, entry points, stdout/stderr behavior, exit codes, and environment-driven configuration in uv-managed Python projects.
---

# Python CLI

## Rule

Design and implement Python command-line interfaces with explicit user contracts, stable exit
behavior, and tests. Preserve existing CLI framework choices unless the user is setting up a
new project from the personal baseline, where Typer is preferred.

Use this skill for CLI work after a Python project exists. Use `python-project-setup` only
for the minimal new-project CLI stub.

## Hard Stops

Stop and ask before changing CLI behavior when any required contract is unknown:

- Existing CLI framework or command layout is unclear.
- A change could break documented flags, subcommands, exit codes, stdout, stderr, or
  environment-variable behavior.
- The CLI would call live services, production systems, real secrets, or mutable user files
  during tests.
- A command's intended user-facing behavior is not knowable from code, docs, tests, or the
  user request.
- The project does not use uv-based tooling and the task requires adding CLI dependencies.

## Layout

For new Typer CLIs in this personal baseline, put interface adapters under:

```text
src/<import_package>/interfaces/
|-- __init__.py
`-- cli.py
```

Reserve `interfaces/` for external interaction boundaries such as `cli.py`, `tui.py`,
`api.py`, or `ui.py`. Keep domain logic outside CLI modules when behavior grows beyond
argument parsing and orchestration.

Console script entry points should target a wrapper function, not the Typer app object:

```toml
[project.scripts]
<command-name> = "<import_package>.interfaces.cli:main"
```

Expose both:

```python
app = typer.Typer()


def main() -> None:
    app()
```

Use the `app` object in tests with `typer.testing.CliRunner`.

## Typer Defaults

Use Typer for new baseline CLI code. Do not use `argparse` for new personal-baseline CLI
scaffolds.

Default generated CLI shape:

- a Typer `app`
- a root callback for global options
- a `version` command
- no invented domain commands unless requested

CLI command names should default to the distribution name normalized to kebab-case. Users
may choose a shorter or more specific command name.

Use concise, user-facing docstrings on Typer callback and command functions because Typer can
surface them in help text. Avoid verbose internal implementation details in CLI help.

## Logging And Environment Configuration

For the personal baseline, CLI logging uses structlog through the project's observability
helpers. CLI support implies structlog support.

Global logging options:

- `--log-level`
- `--log-json/--no-log-json`

Configuration precedence:

```text
CLI flags > environment variables > defaults
```

Defaults:

```text
log level: info
JSON logs: false
```

Environment variable names should use the configured project prefix:

```text
<ENV_PREFIX>_LOG_LEVEL
<ENV_PREFIX>_LOG_JSON
```

Default the environment prefix from the import package name uppercased, e.g.
`my_package -> MY_PACKAGE`.

Use `enum.StrEnum` for CLI log level choices. Keep the enum in
`observability/logging.py`, not in `interfaces/cli.py`, so other interfaces can reuse it.

Supported log levels:

- `debug`
- `info`
- `warning`
- `error`
- `critical`

Do not support `warn` or `notset` by default.

Rely on Typer/Click native boolean env var parsing for `--log-json/--no-log-json`.

## Testing

Test CLI behavior through `typer.testing.CliRunner` unless the process boundary itself is
the contract.

Generated or added CLI tests should assert stable behavior, such as:

- command exits successfully
- `version` prints the package version
- valid logging flags do not break command invocation
- env var log level works
- env var JSON logging works
- invalid log level exits nonzero

Avoid exact CLI help text assertions by default; Typer/Click help formatting can be brittle.
Assert only stable help fragments when help output itself is the contract.

Do not test private callback choreography. Test observable command behavior.

## Completion

Before handing work back:

- Run the narrowest relevant CLI test target with uv.
- Run the project validation command, normally `just check`.
- Report commands run, CLI behavior covered, entry points changed, environment variables
  added or changed, and any compatibility risks.
