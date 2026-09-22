# Generated output retention

Generated simulator output has a default retention period of **24 hours after
its writers finish**. This includes successful and failed run directories,
companion input copies and logs, and generated test reports. Requested HTML/GIF output follows the same policy; retention never
enables visualization. Previously retained traces are temporary evidence under
this policy once they are registered.

The active runner requires a new or empty output directory.
The original initialization file must remain outside the active run output.
CI diagnostic uploads use a
one-day retention setting in [the check workflow](../.github/workflows/check.yml).
The affected-check selector owns only its `artifacts/check-scope.json` report;
its lease is separate from JUnit and run directories. A dry selection creates
neither the report nor a retention registry.

## Ownership and active writes

Cleanup removes only explicitly registered file or directory generations.
Registration records their identity in `.event-universe-retention`; a matching
name or old modification time alone does not establish ownership. A registered
directory owns its generated descendants; unrelated siblings remain untouched.
Keep source trees, tests, reference material, templates and original initialization
files outside owned outputs. Existing generated output must be explicitly enrolled
before this policy can remove it.

An operating-system file lock protects each active writer lease. Runners hold
their output lease through final artifact writing. Cleanup skips active
leases even when a run lasts longer than 24 hours. A companion file (an input
copy or a log registered with `keep_alive_with`) depends on the child output
lease: if its writer dies while the child continues, that active child still
protects the companion file (the local workspace that wrote such files was
deleted on 2026-09-22, record 871; the mechanism stays for any host).

Cleanup counts 24 hours from the latest registered start, recorded completion
or owned content modification time. A later write extends the retention period;
normal finalization records completion after writing ends. If a process terminates
without finalizing, no completion time is invented. Once its own and dependent
writer leases are gone, expiry uses the available start and content modification
times. A surviving child's completion alone does not reset its orphaned companion
files' timer; a later log write does.
Replaced paths, symbolic links and Windows reparse paths are rejected rather than
treated as the registered generation. Cleanup errors are reported.

## When cleanup runs

The runner checks its output parent at startup.

Use the same installed Python environment for an explicit check:

```bash
python -m event_universe.retention --root artifacts --root runs --dry-run
python -m event_universe.retention --root artifacts --root runs
python -m event_universe.retention --root artifacts --root runs --watch
```

Repeat `--root` for separate output roots. Cleanup finds nested registries within
those roots. `--dry-run` reports candidates without deleting them; commands print
JSON reports. `--watch` keeps checking, at intervals of at most one minute.
Only one watcher runs for a normalized set of roots; starting another for the
same set exits successfully. One-shot cleanup exits with status 1 when it reports
errors, while active writers are ordinary skips.

For expiry while the runners are idle, keep the watcher running or schedule
the cleanup command. These commands do not install a background service. Nothing
runs while the computer is off; the next cleanup catches up on expired output.
Save required reproducible configurations and concise acceptance results in their
durable project or review location before generated evidence expires.
