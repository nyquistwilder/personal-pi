---
name: python-api
description: Python HTTP API and service workflow for designing, implementing, testing, or reviewing request/response contracts, validation, structured errors, OpenAPI, auth hooks, and FastAPI-style service boundaries.
---

# Python API

## Rule

Build HTTP APIs around explicit contracts. Keep business logic separated from transport
concerns, validate all external input, return structured errors, and test through in-process
clients where practical.

For greenfield personal-baseline services, prefer FastAPI with Pydantic models, typed service
functions, explicit dependency injection, and OpenAPI contracts that match behavior.

## Hard Stops

Stop and ask before changing API behavior when:

- Request/response schemas, status codes, auth requirements, or compatibility expectations
  are unclear.
- A change could break existing clients, documented OpenAPI, webhooks, callbacks, or error
  formats.
- Tests would call live services, production databases, real secrets, or mutable external
  systems.
- Authentication, authorization, rate limiting, CORS, or tenant isolation policy is involved
  but not specified.
- The project already uses a framework pattern and replacing it would be broader than the
  requested task.

## FastAPI Defaults

- Define Pydantic request and response models at the transport boundary.
- Use `response_model` or precise return annotations to keep OpenAPI honest.
- Use `Annotated[...]` for dependencies, headers, query parameters, and validation metadata.
- Keep route functions thin: parse, authorize, call service/domain code, translate result.
- Prefer `HTTPException` or registered exception handlers for transport errors; keep domain
  exceptions framework-independent.
- Use explicit status codes. Return `201` for creates, `204` for no-content deletes, and
  structured 4xx errors for client mistakes.
- Do not perform network/database setup at import time. Use lifespan hooks for app resources.

## HTTP Client Defaults

For outbound HTTP from services, prefer `httpx` with explicit timeouts. Inject clients or
client factories so tests can avoid live network calls. Consider retries only when idempotency
and failure semantics are understood.

## Workflow

1. Inspect framework, app factory, routes, models, tests, OpenAPI expectations, and task
   wrappers.
2. Identify the external contract and compatibility constraints.
3. Keep or introduce a service/domain layer when route logic would otherwise grow.
4. Add or update Pydantic models and structured error handling.
5. Test through the framework's in-process client, normally FastAPI `TestClient` or `httpx`
   ASGI transport patterns already used by the repo.
6. Add regression tests for status codes, response bodies, validation errors, and auth hooks
   when relevant.
7. Run the narrow API tests and repository validation.

## Testing

Do not make live network calls in default tests. Mock outbound HTTP and use isolated test
databases or stores. Assert stable API contracts: status code, media type when relevant,
JSON body shape, important headers, and side effects.

Avoid over-asserting generated OpenAPI unless schema stability is the contract. When OpenAPI
is public, include focused schema assertions for changed endpoints.

## Completion

Report endpoints/contracts changed, validation and error behavior, auth or compatibility
risks, tests run, and any OpenAPI or client-impact notes.
