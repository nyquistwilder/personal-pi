---
name: python-database
description: Python database workflow for SQLModel/SQLAlchemy-style persistence, transactions, sessions, migrations, query correctness, connection management, and isolated database tests.
---

# Python Database

## Rule

Make persistence boundaries explicit. Manage sessions, transactions, migrations, and test
data deliberately, and never let default tests touch developer or production databases.

For greenfield personal-baseline apps, prefer SQLModel for typed relational models when it
fits the domain, with Alembic-style migrations when schema evolution is required.

## Hard Stops

Stop and ask before changing database code when:

- The target database, schema ownership, migration policy, or transaction boundary is unclear.
- Work could read, write, migrate, truncate, or seed developer, staging, or production data.
- Connection strings, credentials, or dumps may contain secrets or sensitive data.
- A model/schema change may break existing data, downstream queries, or API contracts.
- Adding an ORM, migration tool, or database dependency would change architecture.

## Database Defaults

- Keep persistence models and domain logic separate when practical.
- Use parameterized queries or ORM expressions; never build SQL with untrusted string
  interpolation.
- Make transaction boundaries explicit at service or unit-of-work boundaries.
- Use context managers for sessions/connections.
- Configure pools, timeouts, and pragmas deliberately; avoid hidden module-level connections.
- For local analytics or embedded workloads, consider DuckDB when it fits and is approved.
- For tabular interchange, prefer Parquet/Arrow-compatible paths when appropriate.

## SQLModel Guidance

- Define primary keys, indexes, nullability, and relationships explicitly.
- Keep Pydantic/API schemas separate from table models when external contracts diverge from
  persistence shape.
- Avoid import cycles between models, repositories, and services.
- Use migrations for persistent schema changes; `create_all()` is acceptable only for simple
  tests or explicitly ephemeral databases.

## Workflow

1. Inspect database configuration, models, migrations, repositories, tests, and task wrappers.
2. Identify the data contract, transaction scope, and migration expectations.
3. Create or update isolated tests using in-memory, temporary, containerized, or
   transaction-rolled-back databases according to project convention.
4. Implement query/model/session changes with explicit error and transaction handling.
5. Add migrations when persistent schema changes require them.
6. Run focused database tests and repository validation.

## Testing

Tests must not use production or developer databases by accident. Use temporary database
URLs, fixtures, transactions, or test containers with explicit opt-in. Keep fixtures small
and assert persisted state, rollback behavior, and query edge cases.

## Completion

Report schema/model/query changes, transaction boundaries, migration status, database safety
measures, tests run, and any manual migration or data-backfill steps.
