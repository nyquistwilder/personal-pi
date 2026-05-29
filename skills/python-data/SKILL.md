---
name: python-data
description: Python data processing workflow for CSV, JSON, Parquet, Polars, PyArrow, DuckDB, schemas, deterministic transformations, malformed data, memory-aware ETL, and reproducible data tests.
---

# Python Data

## Rule

Make data transformations explicit, typed where practical, deterministic, and reproducible.
Prefer small representative fixtures and schema checks over opaque snapshots or large checked
in datasets.

For greenfield data work, prefer Polars for dataframe transformations, PyArrow/Parquet for
columnar interchange, and DuckDB for local analytical SQL when those tools fit the workload
and are approved dependencies.

## Hard Stops

Stop and ask before working with data when:

- Source data ownership, sensitivity, licensing, or retention expectations are unclear.
- Tests or development would require production data, personal data, secrets, or mutable
  external datasets.
- Expected behavior for missing, malformed, duplicate, timezone, encoding, or schema-drift
  cases is unknown.
- Adding heavy data dependencies or changing file formats would affect consumers.
- Outputs may overwrite user data or expensive generated artifacts.

## Data Defaults

- Define input and output schemas explicitly when possible.
- Validate external records with Pydantic or dataframe schema checks before business logic.
- Prefer Parquet for typed intermediate tabular data; use CSV only when it is the external
  contract.
- Use lazy Polars plans for large transformations when it improves memory/performance.
- Use streaming or chunking when data may exceed memory.
- Treat timezone, locale, encoding, decimal precision, nulls, and categorical values as
  explicit design choices.
- Keep raw, intermediate, and output paths separate.

## Workflow

1. Identify input formats, output contracts, schema expectations, and data sensitivity.
2. Create minimal non-sensitive fixtures that represent normal and edge cases.
3. Implement transformations as pure functions where practical, with I/O at the edges.
4. Validate malformed, missing, duplicate, and boundary values deliberately.
5. Add tests for deterministic outputs and schema behavior.
6. Measure memory/performance when workload size matters; use `python-performance` when
   optimization is the primary task.
7. Run focused data tests and repository validation.

## Testing

Use tiny inline data or files under `tests/fixtures/` only when file format behavior matters.
Assert schemas, row counts, key values, ordering when guaranteed, and error behavior. Avoid
large golden files and brittle full-snapshot assertions unless the exact artifact is the
contract.

## Review Guidance

Flag hidden schema assumptions, nondeterministic ordering, accidental production-data use,
large checked-in datasets, lossy type conversions, memory blowups, and transforms that mix
I/O, parsing, business rules, and writing in one hard-to-test function.

## Completion

Report data contracts changed, fixture strategy, malformed-data handling, tools used,
commands run, and any sensitivity or reproducibility concerns.
