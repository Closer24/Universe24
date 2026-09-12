---
name: visualization-check
description: Validate or repair Universe24 HTML and animation output so displayed fields, motion and labels faithfully describe recorded simulation state.
---

# Visualization check

Read [the shared workflow](../workflow.md) and the display contract in
[definitions](../../SIMULATOR_DEFINITIONS.md). Input is recorded state, model and
the output change; output is an inspected artifact and scoped visual findings.
Use the existing frame, HTML/GIF and image-inspection tools.

Visualization is opt-in. Apply this workflow to requested visual output; do not
turn a headless simulation or ordinary test run into a rendering run. Use
`pytest --visualize-runs` only when visual checks were requested. Headless output
contracts are checked through metadata and event traces without frame capture.

Rendering reads copied state only. Keep physical changes with the field/engine
owner. Inspect actual saved frames and HTML, not merely plotting code or a tool's
success message. Check the relevant initial, event/failure and final frames.

Verify labels, scales, geometry, particle identities, visibility and playback.
For historical particle views, velocity arrows must use the selected model's
mass/momentum scale. Generic disturbance views must label configured fields
without inferring physical meaning from names. Periodic seams,
sampled-frame displacement and actual multi-hop movement are different facts;
show the recorded distinction rather than interpolating it away. The animation
must follow the current end-of-playback contract.

For initialization-defined topology, read the saved immutable port offsets and
site residues. Do not reconstruct directions from `port // 2` or draw excluded
sites as nodes. Check diagonal transfers, actual neighbor links, periodic seam
splitting and collapsed layers in a projection. Receiver labels must use the
receiving port's offset while preserving the local observer's recorded receipt
prefix; opening an observer view must not initialize a global audit view. Older
recordings without topology metadata retain the six cardinal directions. See
[the observer contract](../../docs/LOCAL_OBSERVER.md) and its topology playback
tests for the current interfaces.

A stream population sum is not scalar phi. Label the displayed quantity and any
visual transfer explicitly; do not invent per-source attribution from a combined
field. Ensure metadata and legend describe the actual model and view.

Test only meaningful rendering contracts affected by the change and reuse existing
run evidence. Hand presentation-only fixes to the assigned renderer owner, physical
anomalies to simulation/physics review, and inspected output to Boss. Do not mark
motion physically correct from its appearance alone.

For renderer optimizations, follow the shared workflow's
[performance procedure](../workflow.md#performance-work). Compare saved frame
count, dimensions, duration, playback and representative decoded images in
addition to the unchanged physical trace.
Historical live previews remain explicit opt-ins. Do not apply their scalar and
particle display semantics to initialization-defined fields in the active runner.
