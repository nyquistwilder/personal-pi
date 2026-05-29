---
name: go-api
description: Greenfield Go HTTP API workflow for net/http or chi services, routing, handlers, middleware, validation, status codes, structured errors, auth hooks, OpenAPI concerns, and service tests.
---

# Go API

## Rule

Build HTTP APIs around explicit contracts. Keep handlers thin, domain logic testable, and
network/server concerns at the edge.

## Hard Stops

Ask before:

- Choosing or changing routing frameworks, public routes, request/response schemas, status
  codes, auth policy, CORS, rate limits, or error formats.
- Calling live services, production databases, real secrets, or external identity providers
  in tests.
- Adding OpenAPI generators, middleware stacks, or validation libraries.
- Weakening TLS, auth, tenant isolation, request limits, or audit behavior.

## Defaults

- Prefer stdlib `net/http` and Go's modern `http.ServeMux` for simple APIs.
- Use `go-chi/chi/v5` when path params, middleware composition, route groups, or larger API
  shape justify it.
- Use typed request/response structs with `encoding/json` at the transport boundary.
- Use `json.Decoder.DisallowUnknownFields` when strict request contracts matter.
- Limit request body sizes with `http.MaxBytesReader` or upstream limits.
- Return structured JSON errors with stable codes/messages; do not expose internal errors.
- Set server timeouts (`ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`).
- Keep domain errors framework-independent and map them in handlers.

## Testing

Use `httptest` for handlers and servers. Avoid fixed ports and live network dependencies.
Assert status code, headers when meaningful, JSON body shape, validation failures, auth
hooks, context cancellation, and side effects through isolated stores.

## Workflow

1. Define route, method, schema, status codes, errors, auth, and compatibility needs.
2. Choose stdlib mux or chi based on concrete routing needs.
3. Implement thin handlers over services/stores.
4. Add middleware for request IDs, logging, recovery, auth, and timeouts only when needed.
5. Add handler/service tests for success, validation, auth, errors, and cancellation.
6. Run targeted tests, `go test ./...`, race checks when concurrency is involved, lint, and
   `just check`.

## Antipatterns

- Business logic embedded in handlers.
- Starting servers at import/init time or in tests with fixed ports.
- Ignoring `r.Context()` for downstream I/O.
- Logging request bodies or auth headers.
- Returning raw `error.Error()` to clients.

## Completion

Report API contract, router/dependency choices, validation and error behavior, auth
assumptions, tests, and validation results.
