---
name: rust-observability
description: Greenfield Rust observability workflow for tracing, structured logs, metrics, spans, correlation IDs, OpenTelemetry, health checks, diagnostics, and operator-friendly errors without leaking secrets.
---

# Rust Observability

## Rule

Add telemetry that answers operational questions while preserving privacy, performance, and
testability. Use `tracing` as the greenfield diagnostics baseline.

## Hard Stops

Stop before:

- Logging secrets, tokens, credentials, PII, request bodies, or sensitive business data.
- Changing production log formats, levels, field names, metric names, trace sampling, or
  telemetry backends without approval.
- Setting a global tracing subscriber in a library.
- Exposing debug, metrics, pprof-like, or health endpoints publicly without access controls.
- Adding OpenTelemetry/Prometheus dependencies without a clear consumer and test strategy.

## Defaults

- Libraries emit `tracing` spans/events but do not configure subscribers.
- Binaries configure `tracing-subscriber` at startup.
- Use JSON logs for production ingestion and pretty/compact logs for local CLI/dev only when
  explicitly selected.
- Add spans at request, job, queue, database, and external I/O boundaries.
- Use stable structured fields: operation, component, request ID, trace/span IDs, status,
  duration, and non-sensitive IDs.
- Use OpenTelemetry and OTLP only when traces/metrics cross service boundaries or a backend
  exists.
- Avoid holding `Span::enter()` guards across `.await`; use `#[instrument]`,
  `.instrument(span)`, or scoped synchronous spans.

## Workflow

1. Identify operational questions and consumers: developer logs, production logs, metrics,
   traces, health, or profiling.
2. Add spans, events, metrics, health checks, or diagnostics at meaningful boundaries.
3. Propagate correlation/request IDs through request/task context when needed.
4. Add tests for stable fields, redaction, subscriber-free libraries, or health responses
   when practical.
5. Run tests, Clippy, and `just check`.

## Antipatterns

- `println!` diagnostics in services instead of structured `tracing` events.
- Logging and returning the same error at every layer.
- High-cardinality metric labels.
- Tracing every small function instead of boundary operations.
- Global subscriber configuration in reusable crates.

## Completion

Report signals added, fields/metrics/spans, redaction choices, dependencies, tests, and
validation results.
