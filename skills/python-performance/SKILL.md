---
name: python-performance
description: Python performance workflow for profiling, benchmarking, and optimizing CPU, memory, I/O, async, database, and data-processing hotspots with before/after measurements.
---

# Python Performance

## Rule

Optimize only with evidence. Measure before and after meaningful changes, preserve
correctness, and prefer algorithmic or I/O-boundary improvements over micro-optimization.

Use this skill for performance investigation and optimization, not speculative cleanup.

## Hard Stops

Stop and ask before optimizing when:

- The performance goal, workload, dataset size, latency/throughput target, or resource limit
  is unclear.
- Measurement would require production data, live systems, secrets, or destructive load.
- Proposed changes trade away correctness, security, or public contracts.
- Benchmark results would be dominated by network, database, filesystem, or external service
  noise without an agreed test strategy.
- Adding specialized dependencies or native extensions is being considered without approval.

## Measurement Defaults

- Start with a representative workload and a baseline number.
- Include correctness tests before optimizing non-trivial logic.
- Measure wall time, CPU, memory, allocations, I/O, and query counts as relevant.
- Use `time.perf_counter()` for simple local timing and profilers for deeper analysis.
- Keep benchmarks deterministic enough to compare; document hardware/data caveats.
- Avoid claiming speedups from single noisy runs.

## Optimization Priorities

1. Remove unnecessary work, repeated parsing, redundant I/O, and avoidable allocations.
2. Improve algorithms and data structures.
3. Batch network, filesystem, database, and serialization operations.
4. Use streaming for large data rather than loading everything into memory.
5. For tabular data, consider Polars, PyArrow, or DuckDB when they fit the workload and are
   approved dependencies.
6. Use async/concurrency only for I/O-bound work with clear lifecycle and cancellation rules.
7. Micro-optimize hot loops only after profiling proves they matter.

## Workflow

1. Define the performance target and representative workload.
2. Run existing correctness tests.
3. Capture baseline measurements and profiler output.
4. Identify the bottleneck and choose the smallest safe intervention.
5. Implement the optimization with tests or benchmarks that guard against regression.
6. Measure again under the same conditions.
7. Run repository validation.

## Review Guidance

Flag unmeasured performance claims, benchmark data that does not match production-like
workloads, changes that reduce clarity for negligible gain, hidden memory blowups, N+1 I/O,
missing timeouts, and concurrency that lacks cancellation or cleanup.

## Completion

Report baseline and after measurements, workload used, bottleneck found, optimization made,
correctness tests run, validation commands, and remaining performance risks.
