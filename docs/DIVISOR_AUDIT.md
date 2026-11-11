# Migration to the fixed divisor six

The active scalar recurrence is now

```python
quotient, remainder = divmod(2 * input_sum + remainder, 6)
previous, current = current, quotient - previous
```

The former adjustable divisor scale has been removed from the active model.
It is not renamed, transferred into another global knob, or chosen per gear.
The six-state remainder alphabet is part of the elementary state definition.

This is a deliberate model migration. Older constructions used a larger
remainder alphabet and integer coefficient calibrations tied to it. Changing
only their divisor would change their histories, and dividing arbitrary old
coefficients would generally produce nonintegers. Those old physical and
numerical claims cannot be inherited by the current model.

The already-fixed-six pp-wave and integer-clock examples keep their arithmetic
law. Their current tensor, seed and complete-state checks determine whether
a refactor preserves the earlier history. Other builders must be reconstructed
with explicit integer coefficients, or remain unavailable. Passing an import
or renaming a parameter is not a mathematical reconstruction.

The engine's retained inverse remains

    old_b = new_a,
    old_r = (new_r - 2*old_input) mod 6,
    old_a = (2*old_input + old_r - new_r)//6 - new_b.

The old input is evaluated in the declared inverse dependency order. No
information is discarded inside this inverse. Migrating an old seed with a
larger remainder alphabet is a different operation and must not be disguised
as an invertible state conversion.

The former analysis explaining when a larger scale can be canceled is a
historical statement about a different family of models. It no longer defines
an active parameter or a supported resolution-lifting workflow.

See [the current algebra](MODEL.md) and [validation scope](VALIDATION.md).
