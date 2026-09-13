# Reuse named fields and disturbances

[definitions.json](definitions.json) is the only owner of this model's two
fields, two disturbance types, defaults and three local exchange rules.
[near.json](near.json) and [shifted.json](shifted.json) place the same types in
different cells of a periodic 7 by 7 by 7 world. Experiments contain no copied
field definitions or physical rules.

The `single channel` disturbance owns `amber inventory`. The `dual channel`
disturbance owns both `amber inventory` and `blue inventory`. Ownership declares
stored values; the three explicit `spatial_couplings` declare their response to
the spatial fields. No behavior is inferred from a name.

For the first tick, the uniform field samples are 3 amber units and 5 blue units.
The configured exchange transfers those amounts from each carrier into the
corresponding spatial inventory. Expected carried values are:

| Type | Initially | After one tick |
| --- | --- | --- |
| `single channel` | amber 10 | amber 7 |
| `dual channel` | amber 20, blue 30 | amber 17, blue 25 |

The dynamic spatial inventory gains 6 amber units and 5 blue units. Combined
carrier and dynamic field totals remain 30 amber units and 30 blue units.
Diagnostics also count the uniform baseline once at each of the 343 cells:
the complete conserved totals stay at 1059 amber units and 1745 blue units.
This finite example uses existing integer local operations; it is not a model
of electrons, photons or a derived electromagnetic law.

From the repository root, resolve either experiment to ordinary initialization
JSON, then use the normal headless runner:

```sh
python -m event_universe.model_definitions --definitions examples/named-definitions/definitions.json --experiment examples/named-definitions/near.json --output-init artifacts/named-near.json
python -m event_universe --init artifacts/named-near.json --output artifacts/named-near
python -m event_universe.model_definitions --definitions examples/named-definitions/definitions.json --experiment examples/named-definitions/shifted.json --output-init artifacts/named-shifted.json
python -m event_universe --init artifacts/named-shifted.json --output artifacts/named-shifted
```

The composer validates every definition and the complete experiment before
writing. It refuses to overwrite an existing output. Resolving JSON does not
compile or change simulator code. The runner preserves its resolved input, so
later edits to the shared definitions do not change that recorded run.

Add or remove types and fields in the definitions file, then update any references
in its rules and in the experiments. A dangling name fails validation; removal
never silently deletes a law. Keep all definitions within the ordinary model
capacities. See the [configuration validation contract](../../docs/CONFIGURATION_VALIDATION.md)
for the distinction between valid input and physical acceptance.
