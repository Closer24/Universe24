<!-- rendered by tools/render_documents.py from the tree; do not edit by hand -->

# The run's files, key by key

The kinds are the frame's schemas (`src/event_universe/loader/frame.py`) and the folders' cards; a key the frame does not name and no card declares is refused by name. The rules between keys (a key admitted only with another) stay in the loader's prose (docs/ENGINE.md, section 4).

## The world file

| key | required | kind |
| --- | --- | --- |
| `shape` | required | a list of 3, each an integer from 1 |
| `boundary` | required | one of `open` or an object with `x` (one of `open`, `periodic`, `closed`, optional), `y` (one of `open`, `periodic`, `closed`, optional), `z` (one of `open`, `periodic`, `closed`, optional) |
| `ticks` | required | an integer from 0 |
| `engine` | required | a word |
| `stamp` | optional | an object with `hash` (a word) |
| `face_depth` | optional | an integer from 1 |
| `age_bound` | required | an integer from 1 |
| `probes` | optional | a list, each a list of 3, each an integer from 0 |
| `mode_axis` | optional | one of `x`, `y`, `z` |
| `amplitude_bound` | optional | an integer from 1 |
| `node_clock` | optional | an integer from 1 |
| `momentum_unit` | optional | an integer from 1 |
| `N` | required | an integer from 2 |
| `clock_stamp` | required | true or false |
| `massive_record` | required | true or false |
| `body_record` | required | true or false |


Handed on as written to their readers, once the world's own keys are checked:

| key | required | what it holds |
| --- | --- | --- |
| `universe` | required | the repository path of the universe file |
| `measured` | required | the bodies, each in one of the two forms below |
| `detectors` | required | the detectors, below |
| `readings` | optional | the readings, below |
| `twist_table` | optional | an inline world's twist table, the universe file's form |


### A body by its position (today's form)

| key | required | kind |
| --- | --- | --- |
| `position` | required | a list of 3, each an integer from 0 |
| `family` | required | a family's name |
| `amount` | required | an integer from 1 |
| `momentum` | required | a list of 3, each an integer |
| `stocks` | required | an object mapping a family's name to an integer from 1 |
| `fixed` | required | true or false |
| `kind` | optional | a list of 2, each an integer from 1 |
| `q` | optional | an integer |
| `spin` | optional | a list of 3, each an integer |
| `moment` | optional | a list of 3, each an integer |
| `twist` | optional | an integer from 0 |
| `side` | optional | an integer from 1 |
| `extents` | optional | a list of 3, each an integer from 1 |
| `pair` | optional | a list of 2, each an integer from 1 |
| `seed` | optional | an integer from 0 or a list, each an integer |
| `clock` | optional | a list of 2, each an integer from 1 |
| `proper_clock` | optional | a list, each a list of 2, each an integer from 1 |
| `ramp` | optional | an integer from 0 |
| `start` | optional | an integer from 0 |
| `margin` | optional | a word |
| `emitter` | optional | an object with `family` (a family's name), `receiver` (a word or a list, each a word, optional), `period` (an integer from 1, optional), `norm` (an integer from 1, optional), `weight` (an integer from 1, optional), `norm_denominator` (an integer from 1, optional), `window_read` (an integer, optional), `clock` (an integer from 1 or a list of 2, each an integer from 1, optional), `pair` (an integer from 1 or a list of 2, each an integer from 1, optional), `twist` (an integer from 0) |
| `receiver` | optional | a word |
| `stock` | optional | an integer from 1 |


### A body's emitter

| key | required | kind |
| --- | --- | --- |
| `family` | required | a family's name |
| `receiver` | optional | a word or a list, each a word |
| `period` | optional | an integer from 1 |
| `norm` | optional | an integer from 1 |
| `weight` | optional | an integer from 1 |
| `norm_denominator` | optional | an integer from 1 |
| `window_read` | optional | an integer |
| `clock` | optional | an integer from 1 or a list of 2, each an integer from 1 |
| `pair` | optional | an integer from 1 or a list of 2, each an integer from 1 |
| `twist` | required | an integer from 0 |


### A body by its Nodes (the law's form)

| key | required | kind |
| --- | --- | --- |
| `family` | required | a family's name |
| `nodes` | required | a list, each an object with `node` (a list of 3, each an integer from 0), `count` (an integer from 1) |
| `momentum` | required | a list of 3, each an integer |
| `spin` | optional | a list of 3, each an integer |
| `moment` | optional | a list of 3, each an integer |


### A detector

| key | required | kind |
| --- | --- | --- |
| `name` | required | a word |
| `positions` | optional | a list, each a list of 3, each an integer from 0 |
| `block` | optional | an integer from 0 |


### A reading

Every reading has a `name` and a `kind`; the kind takes its own keys (`src/event_universe/core/readings.py`).

| kind | label | its keys |
| --- | --- | --- |
| `clicks` | DETECTOR | `detector` |
| `level` | GAMEBOARD | `family`, `node`, `every` |
| `support` | GAMEBOARD | `family`, `every` |
| `total` | GAMEBOARD | `family`, `every` |
| `centre` | GAMEBOARD | `body`, `every` |
| `alive` | HOST | `every` |


## The universe file

Two keys: `integers`, `families`.


### The integers

| key | required | kind |
| --- | --- | --- |
| `node_clock` | required | an integer from 1 |
| `amplitude_bound` | required | an integer from 1 |
| `Lambda` | required | an integer from 1 |
| `momentum_unit` | required | an integer from 1 |
| `twist_table` | required | an object with `unit` (an integer from 1), `fine` (a list, each a list of 3, each an integer), `coarse` (a list, each a list of 3, each an integer) |


### A family's entry

Each key beyond the frame's is one folder's, declared on its card.

| key | required | kind | declared by |
| --- | --- | --- | --- |
| `name` | required | a word | the frame |
| `clock` | optional | a list of 2, each an integer from 0 | the frame |
| `spins_step` | optional | an object with `curl` (a list of 2, each an integer from 1), `tidal` (a list of 2, each an integer from 1) | the spin's step |
| `clicks` | optional | an object with `gives` (true or false), `takes` (true or false), `quantum` (an integer from 1) | the clicks |
| `parts` | required | a list, each an integer from 1 | the degree |
| `held` | optional | an object with `count` (one of `content`, `sign`), `factors` (a list, each an integer from 1), `dipole` (one of `spin`, `moment`, optional), `dipole_div` (an integer from 1, optional) | the hold |
| `pair` | required | a list of 2, each an integer from 1 or one of `body` | the pair |
| `phase` | required | one of `1`, `2` | the phase |
| `self_source` | required | an object with `unit` (an integer from 0) | the self-source |
| `sign` | required | one of `-1`, `0`, `1` | the signed read |
| `reads` | required | a list, each an object with `family` (a family's name), `weight` (an integer from 1 or the name of one of the universe's integers), `twist` (an integer from 0 or one of `own`), `by` (one of `1`, `q`) | the signed read |
| `sourced` | optional | an object with `of` (a family's name), `weight` (an integer), `scale` (an integer from 1), `cap` (an integer from 1, optional) | the source |


## The start file

| key | required | kind |
| --- | --- | --- |
| `mode` | required | one of `check`, `pin` |


## The step file

`law/step.json`: an object with the one key `interval`, a list of acts, each `[place, name]` or `[place, name, words]`, a primitive's name at its declared place with the words of its call; a name has one place; no act twice. The acts as the file lists them today are in STATUS.md.


## The pins file

An object keyed by the input's file stem; each pin has a `detector`, one of `count`, `first_click` or `mean_interval`, and a `band`; passed to `tools/run_inputs.py` with `--pins`, refused under the mode `check`, required under `pin`.


## The output file

One file per world, `<name>.output.json`, as `examples/events/massive_record/light_clock.output.json` shows it (4800 intervals, the verdict `LAWFUL`).

| key | in the shipped output |
| --- | --- |
| `clicks` | a list of 167 |
| `counts` | an object with `at_well` |
| `format` | `one-command-output-v1` |
| `input` | `light_clock.json` |
| `mode` | `check` |
| `name` | `light_clock` |
| `pins` | an empty list |
| `readings` | an empty list |
| `records_alive` | the integer 18 |
| `stamp` | an object with `hash` |
| `step` | an object with `hash` |
| `ticks` | the integer 4800 |
| `verdict` | `LAWFUL` |

Each click:

| key | in the first click |
| --- | --- |
| `detector` | `at_well` |
| `giving` | the integer 27 |
| `interval` | the integer 268 |
| `record` | the integer 2 |
