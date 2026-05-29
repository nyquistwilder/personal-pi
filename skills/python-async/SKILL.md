---
name: python-async
description: Python async and concurrency workflow for asyncio, AnyIO, Trio, async clients, cancellation, timeouts, task lifecycle, resource cleanup, and deterministic async tests.
---

# Python Async

## Rule

Write async code with explicit ownership of tasks, timeouts, cancellation, and resources.
Prefer structured concurrency and deterministic tests over background tasks with hidden
lifecycles.

Use this skill for async behavior, concurrency, and event-loop issues.

## Hard Stops

Stop and ask before changing async code when:

- Event-loop ownership, framework runtime, or concurrency library choice is unclear.
- A change may alter cancellation, timeout, retry, ordering, or resource cleanup semantics.
- Tests would depend on sleeps, live services, production queues, or real credentials.
- Blocking synchronous libraries are used in async code and replacing or isolating them would
  require a design decision.
- The task is primarily HTTP API, performance, or test-suite policy rather than async design.

## Async Defaults

- Prefer `async with` for clients, connections, streams, locks, and task groups.
- Use explicit timeouts around network and queue operations.
- Avoid `asyncio.create_task()` without storing, supervising, and cancelling the task.
- Prefer AnyIO task groups when the project already uses AnyIO or framework support makes it
  natural; otherwise preserve the existing async framework.
- Do not call blocking I/O, CPU-heavy functions, or synchronous clients directly from async
  request paths.
- Treat cancellation as normal control flow. Use `finally` blocks for cleanup and avoid
  swallowing `CancelledError`.
- Use `httpx.AsyncClient` with explicit timeout and lifecycle management for async HTTP.

## Workflow

1. Inspect framework, event-loop entry points, async tests, clients, and resource lifecycles.
2. Identify tasks, queues, locks, streams, timeouts, and cancellation boundaries.
3. Reproduce failures or define expected ordering/concurrency behavior.
4. Implement with structured lifecycle management and minimal shared mutable state.
5. Add deterministic tests using existing async test tooling. Ask before adding AnyIO or
   pytest-asyncio.
6. Run narrow async tests and repository validation.

## Testing

Avoid sleeps as proof of correctness. Prefer events, barriers, fake clocks, bounded queues,
mock transports, and explicit synchronization. Test timeout and cancellation paths when they
are part of the contract.

Do not leak tasks across tests. Ensure clients, servers, streams, and temporary resources are
closed.

## Review Guidance

Flag orphaned tasks, missing timeouts, blocking calls in async paths, unsafe shared state,
resource leaks, swallowed cancellation, tests that rely on timing luck, and unclear event-loop
ownership.

## Completion

Report async boundaries changed, timeout/cancellation behavior, resource lifecycle handling,
tests run, and remaining concurrency assumptions.
