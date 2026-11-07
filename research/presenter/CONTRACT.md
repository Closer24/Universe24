# The Presenter — implementation interface v1

This is a generic read-only viewer for any finite recorded experiment of the current Universe24 reference engine. No experiment IDs, particular channels, guide geometries or expected outcomes may control rendering logic. All UI and documentation are English. The model core is unchanged. Physical clocks are not inferred merely from drawn dials.

## Portable data

Bundle: `{format:'universe24-presenter-v1', title:string, catalog:[coupling,...], experiments:[experiment,...]}`.

Coupling: `{model:'universe24-2O-body-013-v1', body_signs:[sx,sy,sz], directions:[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]], ports:6 arrays of48 integers, weights:6 arrays of48 signs, fingerprint:SHA256}`. This is exactly the fixed engine tensor. Catalog contains all eight existing sign choices to import native checkpoints. An experiment carries its own complete coupling.

Experiment: `{id,title,description,side,background:['0','0',r],coupling,frames,readouts:[],view:{position:[x,y,z],channel:g},provenance:{...}}`.

Frame: `{step:nonnegative safe integer,cells:[[x,y,z,g,a_decimal_string,b_decimal_string,r],...],state_sha256, audit:{forward_equal:boolean|null,inverse_equal:boolean|null}}`. Cells are a complete sparse representation: sorted unique addresses, background triples omitted. Every nonbackground remainder is retained. Missing addresses equal background. Frame steps must be consecutive; a single checkpoint is a valid snapshot with no transition claim. All 48 channels and arbitrary positions must be selectable even if background. Counters use canonical decimal strings for lossless browser BigInt. Hash is SHA256 of compact sorted-key JSON of `{side,background,cells}` (ASCII data only); update index is excluded so physical recurrence is meaningful. Geometry and step indices must be safe integers in browser. Resource limits must be explicit and reject incomplete data rather than silently truncating it.

Optional fixed readout: `{id,label,kind:'all_equal',clauses:[{address:[x,y,z,g],component:'a'|'b'|'r',equals:canonical_decimal_string},...]}`. Readouts are passive declared conjunctions; rising edges are derived from consecutive recorded states. They never modify states, are not universal built-in detector semantics, and remain fixed when navigation changes. Engine arithmetic C0/C1/C2 events are separate and can be computed for any selected completed transition using the unchanged ell!=0 and changed-triple guard.

## Python interface owned by exporter

Module `research.presenter.export` exports:
- `capture(engine, initial, steps, *, id='experiment', title='Experiment', description='', start_step=0, readouts=None, view=None) -> experiment dict`.
- `from_trace(path, *, id='experiment', title='Recorded experiment', description='', readouts=None, view=None) -> experiment dict`; accepts complete native checkpoint JSONL, requires consecutive steps, same fixed coupling/geometry/background, verifies full forward equality and rewind. Single checkpoint handled too.
- `bundle(experiments, *, title='The Presenter') -> bundle dict` (with complete eight-coupling catalog).
- `write_bundle(path, data)` refuses overwrite; canonical decimal codec avoids Python int string limit without disabling the process guard.
- CLI `python -m research.presenter.export (--config FILE | --checkpoint FILE | --trace FILE) [--steps N] --output FILE [--title TEXT]`; initial setup only, Engine.advance is sole forward evolution.
- API arbitrary integer states (including >4300 decimal digits) must export losslessly. Native JSON number input within configured Python limits may be rejected explicitly; support string-counter Presenter data is required and raw configs need not silently disable guards.

## Browser data interface owned by data agent

`research/presenter/data.js` UMD exposes global `PresenterData` and CommonJS `module.exports`. No network, no DOM, no model intervention.
- `parse(text)` strict duplicate-key/nonfinite-rejecting lossless JSON parser; large integer numeric literals are preserved as decimal strings before precision loss.
- `load(text, catalog=[])` async returns normalized bundle; accepts Presenter bundle, native full checkpoint JSON or native checkpoint JSONL. Native imports use supplied fixed coupling catalog. Validate full state and every consecutive transition using independent BigInt arithmetic, reciprocal six-port tensor dimensions, claimed hashes where supplied. No synthetic evolution. Attach `experiment.validation={transitions,hashes_verified,source:'bundle'|'checkpoint'|'trace'}`; single snapshot transitions0.
- `at(experiment, frameIndex, address)` -> `[aBigInt,bBigInt,rNumber]`.
- `transition(experiment, frameIndex, address)` -> null at frame0 else `{old,next,u,ell,numerator,remainder,ok,inputs:[{direction:[dx,dy,dz],address:[x,y,z,g],weight,b,product},...]}` with BigInt arithmetic fields; old/next triples as at().
- `readouts(experiment,frameIndex)` -> `[{id,label,value:boolean,edge:boolean}]` from declared fixed readouts, empty when none.
- `nodes(experiment,frameIndex)` -> sorted `[{position:[x,y,z],stored_channels:number,counter_channels:number,remainder_only_channels:number,channels:[g,...]}]` for all nonbackground nodes.
- `phase(aBigInt,bBigInt)` -> `{x,y,atRest}` normalized display coordinates a right,b up without Number overflow; approximation used for graphics only.
- Optional helpers may be added with early coordination. Frame data stays plain serializable objects; map caches external/WeakMap.

## Generic UI owned by viewer agent

Files `research/presenter/index.html`, `style.css`, `app.js`. index has `<link rel='stylesheet' href='style.css'>`, `<script src='data.js'></script>`, `<script src='app.js'></script>` for repo-local development. Root packager embeds all resources and injects `globalThis.PRESENTER_BUNDLE = ...;` before app.js. App calls `PresenterData.load(JSON.stringify(globalThis.PRESENTER_BUNDLE))`; also handles a blank catalog-enabled bootstrap with no experiments and a file-open control.

Three levels: spatial overview/slices; every node's48 channel dials/gears; selected channel exact algebra and all six signed input neighbors (clickable). Any XYZ/channel can be inspected, including background. Show full arbitrary-size integers as exact text, avoid geometric assumptions and fixed guide layouts. Counter direction alone is not enough: exact a,b plus remainder/retained parity must be accessible. Show motion, remainder-only field and hidden-by-filter counts distinctly. Precomputed replay play/pause/step/scrub/speed; experiment selection and import local files; no external fonts/assets/CDN. Label validation, snapshot-only state, errors and resource limits honestly. Timeline plots/readout annotations are generic; changing the viewport does not change recorded observers.

Responsive at1440,390,360px; keyboard controls, labels and useful empty/error states. Browser tests will load unseen fixtures and exercise channels0..47, arbitrary coordinates, signed neighbors, huge integers, snapshot imports and malformed input rejection.
