---
name: rust-database
description: Greenfield Rust database workflow for SQLx or project-selected access, migrations, transactions, pooling, query correctness, test databases, and isolation from real data.
---

# Rust Database

## Rule

Make persistence explicit, transactional, context-aware, and isolated from real mutable
systems. Prefer explicit SQL and typed boundaries before ORM-style abstractions.

## Hard Stops

Stop before:

- Touching production or developer databases without explicit approval and backup/safety
  plan.
- Running destructive migrations, changing schema, or changing data retention semantics
  without rollback and compatibility discussion.
- Adding SQLx, Diesel, SeaORM, migration tools, or containers without approval.
- Using real credentials or committing generated secrets.

## Defaults

- Prefer SQLx for async SQL in Tokio services when compile-time query checking or explicit
  SQL fits.
- Use SQLx migrations for straightforward app-owned schemas.
- Use Diesel only when a synchronous, compile-time query-builder/ORM model is explicitly
  desired.
- Use SeaORM only for dynamic/entity-driven CRUD services where that tradeoff is approved.
- Make transactions explicit and keep their scope small.
- Pass pools/connections through application state; avoid global pools.
- Map database errors to domain errors at the data boundary.
- Configure pool size, acquisition timeout, and statement timeouts intentionally.

## Testing

Use isolated temporary databases, test schemas, transaction rollbacks, or approved
`testcontainers` when real database behavior matters. Never point tests at production or a
developer's default database by accident. Test migrations, constraints, not-found behavior,
unique conflicts, rollback, and serialization/deserialization edge cases.

## Workflow

1. Define schema, migrations, queries, transaction boundaries, indexes, and failure behavior.
2. Choose SQLx, Diesel, SeaORM, or existing project access based on approved needs.
3. Implement data access behind small stores/repositories consumed by services.
4. Add isolated tests and fixtures.
5. Run migrations/tests, full tests, Clippy, and `just check`.

## Antipatterns

- String-concatenated SQL with untrusted input.
- Auto-running destructive migrations on every production startup.
- Hiding large workflows in implicit transactions.
- Treating generated ORM entities as domain models by default.
- Tests that require machine-local database state.

## Completion

Report schema/query changes, transaction model, tool choices, test database approach,
commands, and safety boundaries.
