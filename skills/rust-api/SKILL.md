---
name: rust-api
description: Greenfield Rust HTTP API workflow for Axum or project-selected frameworks, handlers, middleware, validation, status codes, structured errors, auth hooks, OpenAPI concerns, Tower services, and service tests.
---

# Rust API

## Rule

Keep transport concerns at the edge and domain logic in testable services. Prefer Axum for
greenfield async HTTP APIs when a framework is approved.

## Hard Stops

Ask before:

- Choosing/changing framework, routes, schemas, status codes, auth policy, CORS, rate limits,
  or error formats.
- Calling live services, production databases, real secrets, or external identity providers
  in tests.
- Adding OpenAPI generators, middleware stacks, validation derive crates, or OpenTelemetry.
- Weakening TLS, auth, tenant isolation, request limits, or audit behavior.

## Defaults

- Use Axum with Tokio, Tower, and Tower HTTP for new async APIs when approved.
- Use typed request/response models with `serde`.
- Keep handlers thin: extract, authorize, call service, map result.
- Use typed application state; avoid global state.
- Map domain errors to structured transport errors with stable status codes and response
  bodies.
- Add request size limits, timeouts, and graceful shutdown for services.
- Use `tracing` spans at request and important I/O boundaries.
- Use `utoipa` for OpenAPI only when schema generation is explicitly needed.

## Testing

Use in-process service tests with `tower::ServiceExt` or framework-established patterns.
Avoid real network ports where possible. Assert status, headers when meaningful, JSON shape,
validation errors, auth hooks, and side effects through isolated stores.

## Workflow

1. Define route, method, schema, status codes, errors, auth, and compatibility needs.
2. Choose Axum or existing project framework based on approved scope.
3. Implement thin handlers over services/state.
4. Add middleware only for concrete needs: request ID, tracing, auth, CORS, compression,
   timeouts, body limits, or recovery.
5. Add tests for success, validation, auth, errors, and cancellation.
6. Run targeted tests, full tests, Clippy, and `just check`.

## Antipatterns

- Business logic embedded in handlers.
- Returning raw internal errors to clients.
- Creating Tokio runtimes inside libraries or handlers.
- Logging request bodies or auth headers.
- OpenAPI schemas that are not tested against real responses.

## Completion

Report API contract, framework/dependency choices, validation and error behavior, auth
assumptions, tests, and validation results.
