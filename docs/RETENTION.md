# Generated output retention

Generated simulator output has a default retention period of **24 hours after
its writers finish**. This includes successful and failed run directories,
workspace input copies and logs, exported configurations, and generated test
reports. Requested HTML/GIF output follows the same policy; retention never
enables visualization. Previously retained traces are temporary evidence under
this policy once they are registered.

The active and historical runners require a new or empty output directory.
The original initialization file must remain outside the active run output.
Each workspace run uses a separate output directory. Visual test sessions write
to a unique `artifacts/test-runs/<session-id>` directory and update the generated
`artifacts/test-runs.html` summary. CI diagnostic uploads use a one-day retention
setting in [the check workflow](../.github/workflows/check.yml).
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
their output lease through final artifact writing. The workspace holds its input
and log lease until the child exits and the log closes, including cancellation
and failure. Exports finish their lease after writing. Cleanup skips active
leases even when a run lasts longer than 24 hours. Workspace input copies and
logs also depend on the child output lease: if the workspace process dies while
its child continues, that active child still protects these companion files.

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

Both runners check their output parent at startup. While its server is running,
the workspace checks every 30 seconds and before serving run or export links. It
refreshes job ownership first and removes expired entries from its result lists;
expired links return 404. Opening a result does not renew its retention period.

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

For expiry while the UI and runners are idle, keep the watcher running or schedule
the cleanup command. These commands do not install a background service. Nothing
runs while the computer is off; the next cleanup catches up on expired output.
Save required reproducible configurations and concise acceptance results in their
durable project or review location before generated evidence expires.
