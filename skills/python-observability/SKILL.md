---
name: python-observability
description: Python observability workflow for adding, configuring, testing, or reviewing structured logging, structlog integration, log levels, JSON/console rendering, context propagation, diagnostics, metrics, and tracing in uv-managed Python projects.
---

# Python Observability

## Rule

Add observability that is explicit, testable, operator-friendly, and safe. Prefer structured
logging with clear configuration boundaries. Do not configure global logging at import time.

Use this skill for observability work after a Python project exists. Use
`python-project-setup` only for the minimal new-project logging stub.

## Hard Stops

Stop and ask before changing observability behavior when:

- Existing logging, metrics, tracing, or diagnostics policy is unclear.
- A change could alter production log formats, field names, levels, destinations, or
  ingestion expectations.
- Logs may include secrets, tokens, credentials, PII, or sensitive business data.
- A library would configure global logging automatically or mutate application logging at
  import time.
- Tests would depend on live services, external collectors, production telemetry, or mutable
  user configuration.

## Layout

For the personal Python baseline, put reusable observability helpers under:

```text
src/<import_package>/observability/
|-- __init__.py
`-- logging.py
```

`observability/__init__.py` should contain a concise module docstring and
`from __future__ import annotations`.

Applications and interfaces may call `configure_logging()`. Libraries may expose
`get_logger()` but must not configure global logging automatically.

## Structlog Baseline

Use typed structlog stdlib integration for new baseline logging code.

`get_logger()` returns a precise logger type:

```python
structlog.stdlib.BoundLogger
```

Do not use `Any` for the logger return type in the baseline helper.

Configure structlog with:

```python
structlog.configure(
    processors=processors,
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

Use direct structlog rendering by default, not `ProcessorFormatter`. Introduce
`ProcessorFormatter` only when stdlib/third-party log integration is a real requirement.

Default processor chain:

- `structlog.contextvars.merge_contextvars`
- `structlog.stdlib.add_logger_name`
- `structlog.stdlib.add_log_level`
- `structlog.processors.TimeStamper(fmt="iso")`
- `structlog.processors.StackInfoRenderer()`
- `structlog.processors.format_exc_info`
- console or JSON renderer

Default local rendering is human-readable console logs. JSON logs must be available through
an explicit option for production-style ingestion.

## Logging Configuration API

Use a central `LogLevel` enum in `observability/logging.py`:

```python
from enum import StrEnum


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
```

Supported log levels are exactly:

- `debug`
- `info`
- `warning`
- `error`
- `critical`

Do not support `warn` or `notset` by default.

Public helpers accept `str | LogLevel`:

```python
def parse_log_level(level: str | LogLevel) -> int: ...

def configure_logging(*, level: str | LogLevel = LogLevel.INFO, json_logs: bool = False) -> None: ...

def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger: ...
```

Invalid log levels should raise `ValueError` from logging helpers. CLI layers should convert
that into a user-friendly parameter error.

Repeated `configure_logging()` calls must be deterministic. Use:

```python
logging.basicConfig(..., force=True)
structlog.reset_defaults()
```

before configuring structlog.

## Tests

Test observability behavior without depending on production sinks or exact decorative
console formatting.

Useful tests include:

- valid log levels parse to stdlib logging integers
- invalid log levels raise `ValueError`
- console logging configuration does not crash
- JSON logging configuration does not crash
- repeated configuration is deterministic enough for tests and CLI invocations

Use `pytest.mark.parametrize` with IDs for repeated log-level cases.

Avoid asserting exact timestamp strings, terminal colors, or full rendered log lines unless
format stability is the explicit contract.

## Safety

Do not log secrets or sensitive values. When adding logging around inputs, configs,
exceptions, HTTP requests, database operations, or model/data workflows, consider redaction
and field-level sensitivity explicitly.

Prefer structured fields that help operators diagnose failures:

- stable identifiers
- operation names
- non-sensitive status values
- durations when measured correctly
- exception information when safe

Do not add metrics, tracing, OpenTelemetry, external collectors, or production shipping
configuration by default. Ask for the operational target and test strategy first.

## Completion

Before handing work back:

- Run the narrowest relevant observability tests with uv.
- Run the project validation command, normally `just check`.
- Report commands run, logging behavior covered, configuration surface changed, and any
  sensitive-data or production-format considerations.
