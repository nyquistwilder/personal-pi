---
name: rust-performance
description: Rust performance workflow for Criterion benchmarks, hyperfine CLI benchmarks, profiling, allocation analysis, async overhead, CPU/memory optimization, and before/after measurement in greenfield crates.
---

# Rust Performance

## Rule

Measure before optimizing and preserve correctness. Prefer algorithmic improvements and
allocation-aware design over clever unsafe or unreadable micro-optimizations.

## Hard Stops

Stop when:

- No target metric or representative workload exists.
- Correctness tests do not protect the behavior being optimized.
- Optimization requires `unsafe`, public API changes, feature changes, altered semantics,
  custom allocators, or substantially less readable code without approval.
- Benchmark noise makes the conclusion unreliable.

## Defaults

- Use Criterion for in-process benchmarks when approved or already present.
- Use `hyperfine` for CLI/process startup and end-to-end command benchmarks.
- Use `cargo flamegraph`, OS profilers, or sampling profilers for CPU hotspots.
- Use heap/alloc profiling tools appropriate to the platform when allocation behavior is the
  metric.
- Use `tokio-console`/`console-subscriber` during async bottleneck diagnosis when approved.
- Benchmark one change at a time and keep inputs representative.

## Workflow

1. Define metric: latency, throughput, allocations, CPU, memory, binary size, startup, or
   tail behavior.
2. Create or run representative benchmarks and capture baseline.
3. Profile to identify bottlenecks instead of guessing.
4. Make one focused change.
5. Rerun benchmarks enough times to compare reliably.
6. Run correctness tests, Clippy, and `just check`.

## Antipatterns

- Optimizing code outside the measured hot path.
- Adding `unsafe` for avoidable zero-copy tricks.
- Cloning less by making APIs painful or unsound.
- Unbounded concurrency to improve happy-path throughput.
- Choosing Actix/Fiber-style framework equivalents solely from synthetic benchmark charts.

## Completion

Report baseline, profile evidence, measured result, benchmark commands, correctness
validation, and tradeoffs.
