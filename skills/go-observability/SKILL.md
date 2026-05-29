---
name: go-observability
description: Greenfield Go observability workflow for log/slog structured logging, metrics, tracing, diagnostics, health checks, pprof, correlation IDs, and operator-friendly errors without leaking secrets.
---

# Go Observability

## Rule

Add telemetry that answers operational questions while preserving privacy, performance, and
testability. Use stdlib `log/slog` as the greenfield logging default.

## Hard Stops

Stop before:

- Logging secrets, credentials, tokens, PII, request bodies, or sensitive business data.
- Changing production log format, levels, field names, metric names, or trace backend without
  approval.
- Exposing pprof/debug/health endpoints publicly without access controls.
- Adding OpenTelemetry, Prometheus, or logging libraries without a clear consumer and test
  strategy.

## Defaults

- Use `log/slog` with JSON handler for production-style logs and text handler for local CLI
  output when useful.
- Pass `*slog.Logger` explicitly or store it in app/server structs; avoid hidden global
  mutable loggers.
- Use stable structured fields: operation, component, request ID, status, duration, and
  non-sensitive IDs.
- Put spans/logs at I/O, request, job, and queue boundaries; avoid noisy per-item logs in hot
  loops.
- Use OpenTelemetry only when tracing/metrics have a backend or explicit integration target.
- Use `net/http/pprof` only behind local/admin-only exposure.

## Workflow

1. Identify operational questions and consumers: developer logs, production logs, metrics,
   traces, health, or profiling.
2. Add logs/spans/metrics/health checks at meaningful boundaries.
3. Propagate correlation/request IDs through context when needed.
4. Add tests for stable fields, redaction, handler behavior, or health responses when
   practical.
5. Run tests, lint, and `just check`.

## Antipatterns

- Logging and returning the same error at every layer.
- Free-form string logs when structured fields are needed.
- Metrics with high-cardinality labels.
- Tracing every small function instead of request/I/O boundaries.
- Global logger configuration in libraries.

## Completion

Report signals added, fields/metrics/spans, redaction choices, dependencies, tests, and
validation results.
