---
name: python-test
description: Pytest-first Python testing workflow for creating, improving, validating, or reviewing tests, fixtures, regression tests, coverage enforcement, and testability changes in Python repositories. Use for Python test work only when the repository uses or is being held to an existing sibling src/ and tests/ layout, uv-based Python tooling, and branch coverage reporting with an 80% minimum threshold.
---

# Python Tests

## Rule

Create, improve, validate, or review Python tests with pytest, uv, and coverage. Prefer meaningful behavior coverage over coverage padding.

## Hard Stops

Stop before writing tests when any required condition is missing:

- `src/` and `tests/` must both exist and must be sibling directories. Do not create or relocate them under this skill. Ask the user whether to refactor into this layout or use another skill.
- Python dependency and test tooling must use `uv`. If the repo does not use uv, ask whether to set up or migrate to uv.
- If pytest, coverage.py, or pytest-cov configuration is missing, ask before adding test tooling or coverage config.
- If coverage is not configured to report branch coverage and fail below 80%, ask before changing coverage policy.
- If tests would hit live network, production databases, real external services, real secrets, or the user's mutable filesystem, ask before proceeding or refactor to an isolated boundary.
- If the intended behavior is unknowable from code, docs, existing tests, or the user request, ask for the missing contract.

## Workflow

1. Inspect the layout: require sibling `src/` and `tests/`.
2. Inspect tooling: read `pyproject.toml`, `uv.lock`, task files, CI, and existing pytest/coverage config.
3. Inspect nearby tests, `conftest.py`, fixtures, helpers, and assertion style.
4. Identify the public behavior, regression, branch, or boundary contract to test.
5. For bug fixes, write or run a focused failing regression test before the fix when practical.
6. Write function-style pytest tests near the relevant existing tests.
7. Run the narrowest direct target first with uv.
8. Run the configured coverage command and enforce the 80% branch coverage floor.
9. Run the repo's canonical validation command before handing work back.
10. Report covered behavior, commands run, coverage result, and remaining gaps.

## Layout And Imports

Use the existing sibling layout:

```text
.
|-- src/
|-- tests/
```

Default new test files to `tests/test_<module>.py` and test functions to `test_<behavior>()`. Keep tests inside functions. Use test classes only when strictly necessary or when maintaining existing class-based tests.

Import through the installed public package path. Do not mutate `sys.path`, import by raw file path, or add local path hacks to make tests pass. If imports fail, verify package metadata, editable install behavior, uv environment setup, and pytest import mode.

Keep helper code private to a test module until it is reused. Put shared fixtures in `tests/conftest.py`; put plain shared builders in `tests/helpers.py` or `tests/factories.py`. Do not import test helpers from production `src/` code.

## Tooling

Use uv for Python dependency and test commands. For narrow direct runs, prefer:

```sh
uv run --group test pytest tests/test_example.py -q
```

For final validation, prefer the repo's wrapper command when present, such as `just check`, `mise run check`, or CI-equivalent project commands.

When adding test tooling with approval, use the repo's existing uv convention. Default to a `test` dependency group unless the repo already keeps test tools in a clear `dev` group:

```sh
uv add --group test pytest pytest-cov coverage
```

Ask before adding optional tools such as Hypothesis, async plugins, HTTP mocking plugins, pytest-xdist, tox, nox, mutation testing, or factory libraries.

## Coverage

Require coverage reporting with branch coverage and an 80% global minimum. Preserve existing coverage policy unless the user approves changing it.

When creating new pytest and coverage config with approval, prefer `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
  "--import-mode=importlib",
  "--cov=src",
  "--cov-branch",
  "--cov-report=term-missing",
  "--cov-report=html",
  "--cov-fail-under=80",
]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

Keep generated coverage artifacts out of version control. Add ignore entries for `.coverage`, `.coverage.*`, `htmlcov/`, and `coverage.xml` if missing and coverage tooling is being configured. Do not emit XML coverage by default unless CI or a coverage service already consumes it.

Use exclusions narrowly. Keep existing exclusions and allow justified cases such as generated code, `if TYPE_CHECKING:`, defensive impossible branches, unavailable platform/version branches, and trivial CLI wrappers. Do not exclude code just to reach 80%.

## Test Style

Use plain `assert` statements so pytest can show assertion introspection. Avoid unittest-style assertions unless maintaining existing unittest tests.

Use clear arrange-act-assert structure with blank lines when it improves scanning. Avoid comments like `# Arrange` unless the repo already uses them or the setup is otherwise hard to read. Prefer expressive test names over docstrings or comments.

Assert the strongest stable contract:

- Assert exact deterministic return values, exceptions, serialized payloads, public API responses, exit codes, and file contents.
- Use broader assertions for intentionally unstable details such as generated IDs, timestamps, unordered collections, or irrelevant formatting.
- Use `pytest.approx` for floating-point values.
- Use `pytest.raises(..., match=...)` when stable error text is part of the contract.

Example:

```python
import pytest


def test_parse_port_rejects_out_of_range_value():
    with pytest.raises(ValueError, match="between 1 and 65535"):
        parse_port("70000")
```

Use `pytest.mark.parametrize` when cases share the same setup and assertion. Give cases IDs when failures would otherwise be hard to interpret:

```python
import pytest


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param(" Alice ", "alice", id="trim-and-lower"),
        pytest.param("BOB", "bob", id="lowercase"),
    ],
)
def test_normalize_name(raw, expected):
    assert normalize_name(raw) == expected
```

## Fixtures And Data

Keep setup local until reuse justifies a fixture. Default fixtures to function scope. Use `conftest.py` only for fixtures shared across multiple files.

Avoid `autouse=True` unless it enforces a cross-suite invariant, such as blocking network access or clearing global state. Prefer explicit fixture parameters.

Prefer small inline test data. Use `tests/fixtures/` only for stable, intentional file fixtures where file format or path behavior is the contract. Avoid broad snapshots unless the repo already uses snapshot testing and explicit assertions would be worse.

Use factories already present in the repo. Do not introduce a factory library by default; use local builders first.

Use `yield` fixtures for resources that need teardown. Avoid cleanup that depends on test order.

## Boundaries

Mock boundaries, not internal choreography. Use `monkeypatch`, existing `mocker` fixtures, or `unittest.mock` for network, time, subprocesses, environment variables, expensive services, and nondeterminism. Avoid tests that mainly assert private helper calls.

Use `tmp_path` for filesystem behavior:

```python
def test_write_config_creates_parent_directory(tmp_path):
    target = tmp_path / "settings" / "app.toml"

    write_config(target, {"debug": True})

    assert target.read_text() == "debug = true\n"
```

Use `monkeypatch` for environment variables and seams:

```python
def test_token_comes_from_environment(monkeypatch):
    monkeypatch.setenv("APP_TOKEN", "test-token")

    assert load_token() == "test-token"
```

Handle important boundary types directly:

- Network: default tests must not make live calls. Mock outbound HTTP. Add integration tests only with explicit marker/config or user approval, and never against production by accident.
- Databases: use repo-established test databases, transactions, or fixtures. Never point tests at developer or production databases.
- Time: inject clocks or monkeypatch time providers. Avoid machine-local timezone and current-date assumptions. Prefer timezone-aware datetimes where behavior crosses boundaries.
- Filesystem: use `tmp_path`, minimal file trees, and realistic missing-path, permission, malformed-file, and content assertions when relevant.
- Subprocesses: mock for unit tests; use real subprocesses only when process behavior, entry points, signals, exit codes, stdout, or stderr are the contract.
- CLI I/O: use existing CLI runners when present. Otherwise use `capsys`, `capfd`, explicit function inputs, or subprocesses only when needed.
- Logging and warnings: use `caplog`, `pytest.warns`, or `recwarn` only when logs or warnings are part of the contract.
- Async: follow existing async test patterns. Use AnyIO or pytest-asyncio only when already present or approved.
- HTTP/API: use the repo's in-process test client pattern when present. Keep guidance framework-agnostic.
- Concurrency: test with deterministic synchronization primitives and observable outcomes. Avoid sleeps as proof of correctness.

## Property-Based Tests

Encourage Hypothesis when code has broad input spaces or invariants: parsers, normalization, validation, math, sorting, deduplication, serialization round-trips, and state machines.

Use Hypothesis if it is already installed. Ask before adding it:

```sh
uv add --group test hypothesis
```

Keep strategies focused and assertions invariant-based:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_sort_preserves_values(values):
    result = sort_values(values)

    assert result == sorted(values)
    assert len(result) == len(values)
```

Prefer Hypothesis or explicit examples over unseeded randomness. If random data is unavoidable, seed it deterministically and make failures reproducible.

## Regression And Testability

For bug fixes, add the regression test in the most relevant existing test file. Create `tests/test_<module>.py` only when no appropriate file exists. Avoid generic `test_regressions.py` unless the repo already uses that pattern.

Generated tests must assert public contracts and fail for meaningful regressions. Do not copy implementation branches into tests or add shallow assertions just to raise coverage.

Test private helpers directly only when they contain substantial stable logic that is hard to observe otherwise, or when the repo already treats them as internal contracts.

Prefer small testability refactors when code directly reaches into time, network, filesystem, subprocesses, environment variables, or global state. Keep refactors behavior-preserving. Do not add production branches, flags, or public APIs solely to increase coverage.

## Reliability

Keep the default suite fast, deterministic, and order-independent. Avoid wall-clock sleeps, real services, uncontrolled randomness, mutable global state, hidden collection-time work, current working directory assumptions, locale assumptions, and timezone assumptions.

Preserve existing marker policy. Register any new markers before use. Use `xfail` only for documented known bugs or unsupported behavior with a clear reason. Use `skip` only for unavailable optional dependencies or platform features. Do not skip or xfail to make the suite pass.

Preserve warnings-as-errors policy. Do not enable warnings as errors globally unless the repo already does or the user asks.

If the repo uses pytest-xdist or another parallel runner, ensure tests avoid shared temp paths and process-global resources.

## Review Mode

When reviewing tests without editing code, prioritize findings about missing public behavior coverage, weak assertions, flaky dependencies, excessive mocking, layout violations, uv/tooling gaps, coverage enforcement gaps, and tests that would not fail for real regressions.

## Completion

Before handing work back:

- Run the narrowest relevant uv pytest target.
- Run coverage and confirm branch coverage is reported and total coverage is at least 80%.
- Run the repo's canonical validation command when available.
- Report commands run, behavior covered, coverage percentage, threshold result, unrun checks, and remaining test gaps.
