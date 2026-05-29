---
name: go-database
description: Greenfield Go database workflow for database/sql, pgx, migrations, transactions, pooling, query correctness, test databases, and safe data boundaries.
---

# Go Database

## Rule

Make persistence explicit, transactional, context-aware, and isolated from real mutable
systems. Keep SQL close enough to review and data access behind small boundaries.

## Hard Stops

Stop before:

- Touching production or developer databases without explicit approval and backup/safety
  plan.
- Running destructive migrations, changing schema, or changing data retention semantics
  without rollback and compatibility discussion.
- Adding an ORM, query generator, migration tool, or container dependency without approval.
- Using real credentials or committing generated secrets.

## Defaults

- Use `database/sql` for generic SQL access and `jackc/pgx/v5` for PostgreSQL driver/pool
  needs.
- Prefer explicit SQL and small repository/store types over full ORMs in greenfield Go.
- Use `golang-migrate/migrate/v4` for versioned SQL migrations when migration tooling is
  needed.
- Pass contexts into queries and transactions.
- Make transaction boundaries explicit; do not hide large workflows in auto-transactions.
- Map database errors to domain errors at the data boundary.
- Configure pool limits and timeouts intentionally.

## Testing

Use isolated test databases, transaction rollbacks, temporary schemas, or approved
`testcontainers-go` when real database behavior matters. Do not use production-like shared
state by default. Test migrations up/down when the tool supports it, constraints, not-found
behavior, uniqueness conflicts, and transaction rollback.

## Workflow

1. Define schema, migrations, queries, transaction boundaries, indexes, and failure behavior.
2. Choose stdlib `database/sql`, pgx, or project-approved tool based on needs.
3. Implement data access behind a small interface or concrete store consumed by services.
4. Add isolated tests and fixtures.
5. Run migrations/tests, `go test ./...`, race tests for concurrent DB use, lint, and
   `just check`.

## Antipatterns

- Building SQL with string concatenation and untrusted input.
- Global DB handles hidden in packages.
- Ignoring `rows.Err()` or leaking `Rows`/transactions.
- N+1 queries without measurement or accepted tradeoff.
- Tests that depend on a developer's local database.

## Completion

Report schema/query changes, transaction model, tool choices, test database approach,
commands, and safety boundaries.
