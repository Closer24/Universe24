# Directional transfer comparison

Run from the repository with its Python environment:

```powershell
python examples/directional-delay/observe.py --output C:/temporary/directional-demo
```

Choose a new output directory outside protected checkout ancestors. The recording
and GIF obey the standard 24-hour artifact retention lease. The input is
`initial.json`; display options are `display.json`. No compilation is needed.

The 64-cubed example compares a uniform load (6,0,0), divisor 2, with the same
configuration without the optional timing law. Two particles and a finite pulse
start near the center. Only +X departures receive three extra ticks. The GIF shows
actual saved integer-tick states; orange squares are field stock waiting at its
origin, cyan marks pulse stock or dispatched packets. The load is a uniform
background vector (6,0,0), not an emitted star field or a momentum-changing force.

The observer checks every conserved component including escaped contents on every
tick and writes source identity, initial inputs, events, frames and a summary.
High ordinary budget isolates the directional waiting from arithmetic cost delay.
See [the law and composition limits](../../docs/DIRECTIONAL_DELAY.md).
