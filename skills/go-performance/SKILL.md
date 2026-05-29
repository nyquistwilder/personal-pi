---
name: go-performance
description: Go performance workflow for benchmarking, profiling, pprof, trace, allocation analysis, CPU/memory/latency/throughput optimization, and before/after measurement in greenfield modules.
---

# Go Performance

## Rule

Measure before optimizing and preserve correctness. Prefer algorithmic improvements,
allocation-aware data flow, and bounded concurrency over clever micro-optimizations.

## Hard Stops

Stop when:

- No target metric or representative workload exists.
- Correctness tests do not protect the behavior being optimized.
- The optimization requires public API changes, semantics changes, `unsafe`, cgo, or
  unreadable code without approval.
- Benchmark results are too noisy to support the conclusion.

## Defaults

- Use `testing.B` benchmarks for package-level performance.
- Use `benchstat` to compare before/after results when available.
- Use pprof for CPU/heap/mutex/block profiles and `go test -trace` or runtime trace for
  scheduler/concurrency issues.
- Inspect allocations with `go test -bench ... -benchmem` and escape analysis with
  `go test -gcflags=-m` when useful.
- Optimize one thing at a time and keep benchmark inputs realistic.

## Workflow

1. Define metric: latency, throughput, allocations, CPU, memory, binary size, startup, or
   tail behavior.
2. Create or run a representative benchmark and capture baseline.
3. Profile to identify the bottleneck instead of guessing.
4. Make one focused change.
5. Rerun benchmarks multiple times and compare with `benchstat` when possible.
6. Run correctness tests, race tests for concurrency changes, and `just check`.

## Antipatterns

- Optimizing code outside the measured hot path.
- Trading clear code for tiny unproven wins.
- Unbounded goroutines or caches to improve happy-path throughput.
- Pooling small objects without allocation evidence.
- Using `unsafe` for avoidable conversions or premature zero-copy tricks.

## Completion

Report baseline, profile evidence, change made, before/after results, benchmark commands,
correctness validation, and tradeoffs.
