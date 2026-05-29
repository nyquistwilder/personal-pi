---
name: python-debug
description: Python debugging workflow for reproducing failures, tracing exceptions, isolating root cause, and fixing defects with focused regression tests in uv-managed src/tests projects.
---

# Python Debug

## Rule

Debug from evidence. Reproduce the failure, isolate the root cause, make the smallest
correct fix, and add a regression test when practical.

Do not make speculative changes unrelated to the observed failure.

## Hard Stops

Stop and ask before proceeding when:

- The failure cannot be reproduced and there is no clear expected behavior.
- Reproduction requires production systems, live credentials, mutable user data, or destructive
  operations.
- Logs, traces, crash dumps, or fixtures may contain secrets or sensitive data.
- The likely fix changes public API, persistence schema, CLI/API contracts, or security
  boundaries beyond the reported defect.
- The task is primarily performance tuning, security incident response, or test-suite design;
  use the more specific skill.

## Workflow

1. Capture the exact failing command, traceback, input, environment, and expected behavior.
2. Inspect recent changes, relevant tests, configuration, lockfile, and task wrappers.
3. Reproduce with the narrowest command, preferably through uv.
4. Reduce the failure to the smallest failing test, fixture, or script.
5. Identify root cause before editing. Distinguish symptom, trigger, and underlying defect.
6. Add or update a regression test when practical and safe.
7. Implement a targeted fix.
8. Run the narrow regression test, then related tests, then `just check` or the repository
   validation command.

## Debugging Practices

- Prefer deterministic tests over print-driven debugging.
- Use structured logs, `caplog`, or temporary local instrumentation only when useful; remove
  temporary instrumentation before completion.
- Check import paths, editable install state, uv groups, environment variables, timezones,
  filesystem assumptions, and network/database boundaries.
- For async failures, inspect cancellation, timeout, event-loop ownership, blocking calls,
  and resource cleanup.
- For HTTP failures, capture method, URL shape, timeout, status handling, retry behavior, and
  response parsing without logging secrets.
- For data failures, preserve a minimal non-sensitive fixture that demonstrates malformed,
  missing, or edge-case input.

## Review Guidance

A good bug fix should explain why the failure happened, why the patch fixes that cause, and
how tests prevent recurrence. Flag broad rewrites, swallowed exceptions, missing regression
coverage, and fixes that only satisfy one incidental traceback.

## Completion

Report reproduction steps, root cause, fix summary, regression coverage, commands run, and
any unverified assumptions or remaining risks.
