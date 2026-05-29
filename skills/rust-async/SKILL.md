---
name: rust-async
description: Async Rust workflow for Tokio, futures, cancellation, timeouts, task lifecycle, channels, streams, Send/Sync boundaries, graceful shutdown, backpressure, and deterministic async tests.
---

# Rust Async

## Rule

Make task ownership, cancellation, timeouts, backpressure, and shutdown explicit. Use async
only when it solves real I/O concurrency needs.

## Hard Stops

Stop when:

- Runtime ownership, cancellation, task supervision, or shutdown behavior is unclear.
- Blocking work is inside async tasks without `spawn_blocking` or isolation.
- `Send`/`Sync` constraints are bypassed without understanding.
- Tests rely on sleeps rather than deterministic synchronization or paused time.
- A library tries to create or own a global Tokio runtime without approval.

## Defaults

- Use Tokio for greenfield async apps when approved.
- Libraries should expose async APIs without owning the runtime.
- Use `tokio::time::timeout`, cancellation tokens or context-like shutdown channels, and
  explicit `JoinHandle` ownership.
- Prefer bounded `tokio::sync::mpsc` channels for backpressure.
- Use `select!` carefully and handle cancellation safety.
- Use `tracing` spans for long-lived tasks and I/O boundaries when observability is in
  scope.
- Use `tokio::test(start_paused = true)` where time control is needed.

## Workflow

1. Define concurrency goal, runtime ownership, shared state, and task lifecycle.
2. Design cancellation, timeouts, backpressure, error propagation, and cleanup.
3. Avoid holding mutex guards across `.await` unless using async-aware locks and justified.
4. Add deterministic async tests with paused time, controlled channels, or explicit
   synchronization.
5. Run async tests, full tests, Clippy, and `just check`.

## Antipatterns

- Fire-and-forget tasks with dropped `JoinHandle`s.
- Unbounded channels or task spawning per request/item without limits.
- Blocking filesystem/CPU work on the async runtime.
- `Arc<Mutex<_>>` shared state with lock guards crossing awaits.
- Treating cancellation as success without cleanup.

## Completion

Report runtime model, task lifecycle, cancellation/backpressure choices, tests, and risks.
