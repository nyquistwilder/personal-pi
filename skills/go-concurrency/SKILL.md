---
name: go-concurrency
description: Go concurrency workflow for goroutines, channels, mutexes, contexts, cancellation, worker pools, pipelines, backpressure, timeouts, lifecycle management, graceful shutdown, and race-free tests.
---

# Go Concurrency

## Rule

Make goroutine ownership, cancellation, backpressure, error propagation, and shutdown
explicit. Use concurrency only when it simplifies I/O or throughput; do not add goroutines
for style.

## Hard Stops

Stop when:

- Runtime ownership, cancellation path, channel close responsibility, or shutdown behavior is
  unclear.
- A design could leak goroutines, block forever, race on shared state, or drop errors.
- The only proof of correctness is `time.Sleep`.
- The change needs unbounded goroutines, unbounded queues, global mutable state, or data-race
  suppression.

## Defaults

- Pass `context.Context` into blocking operations; do not store contexts in structs.
- Prefer simple synchronous code until concurrency is required.
- Use `errgroup` only when already present or approved; otherwise coordinate explicitly with
  `sync.WaitGroup`, channels, and contexts.
- Use bounded channels or semaphores for backpressure.
- Prefer mutexes for shared state and channels for ownership/communication; do not force one
  model everywhere.
- Close channels from the sending side that owns production.
- Handle `os.Signal` shutdown at the application edge.

## Workflow

1. Define the concurrency goal and shared resources.
2. Design ownership: who starts goroutines, who cancels them, who closes channels, who waits.
3. Define error propagation, timeout, retry, and cleanup behavior.
4. Add deterministic tests with explicit synchronization, fake clocks, contexts, or
   controlled channels.
5. Run `go test -race` for touched packages and preferably `go test -race ./...`.
6. Run regular tests, lint, and `just check`.

## Antipatterns

- Fire-and-forget goroutines in libraries.
- Unbounded worker creation per request or input item.
- Closing a channel from receivers or multiple senders without coordination.
- Holding locks while doing network/disk I/O or calling user callbacks.
- Swallowing `ctx.Err()` or converting cancellation into success.
- Sleeps in tests instead of deterministic synchronization.

## Completion

Report lifecycle model, cancellation/backpressure/error choices, race-test results, tests,
and remaining concurrency risks.
