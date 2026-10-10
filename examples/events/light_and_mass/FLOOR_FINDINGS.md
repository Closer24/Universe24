# The floor's bath, the clock's walk and what the paper should say: findings of session universe24-5b (2026-10-10)

Everything here was derived with `tools/derivations/rule3.step` and measured on the engine's own step
(`tools/look/record.py`'s loader, `examples/events/light_and_mass/bath_run.py`). The worlds, their mode files
and the result JSONs sit beside this file on the branch `claude/light-and-mass-worlds`.

## 1. The remainder's walk is harmless; the fast modes' heating is not

Rule3's integer step is the real step plus the remainder term, a_next = a_next* + (r − r′)/w with |ε| < 1 level.
The carried remainder makes ε a *time difference* of a bounded sequence, so for a slow mode (ω ≪ 1) the kicks
average out: the deviation from the exact orbit is a random walk δa ≈ κ√N levels with κ ≈ 0.2 (measured 0.1–0.4
at [2, 3] and [9, 10]). Without the carry there would be a static offset −½/(2 − 2cos ω₀) and a velocity walk
√N/ω₀ (measured: −27,000 against the predicted −25,000 at ω₀ = 0.0045). At nature's numbers (Fermi's Link,
T = Γ²/28, Γ = 2⁹⁴) one quantum's phase walks 2×10⁻¹⁸ rad in a second and 1.4×10⁻⁹ rad in the age of the
universe: no clock sees it. **A derived row, harmless; it also shows nature requires exactly the carry Rule3 declares.**

For a fast mode (ω ~ 1) the difference does not telescope: every unit kick is a delta, white in k and ω, and the
energy per level² there is sin²ω ~ 1. Result: the form (the engine's own, the holder's source) grows at
**1/12 · ⟨sin²ω⟩ level² per Node per interval, independent of amplitude, family, smoothness or geometry.**

Measured on the engine (41×31×1, closed on x and y, the pass_fixed_alone packet, no bodies, held writes off so
the free step is exactly linear and any growth is the floor's):

| run | form, start → end | rate (level² / Node / interval) |
|---|---|---|
| amplitude 1241, 4000 intervals | 14,187,304 → 14,719,867 | 0.103, linear (residual 19k) |
| amplitude 3723, 2000 intervals | 127,656,648 → 127,918,624 | 0.103 (top k-bin), the total masked by a cross term ∝ amplitude |
| quantum ×64 (quantum_action 2²¹, width 127), amplitude 9928 | same rate in level² | 64× fewer quanta, as predicted |

The growth sits in the fast modes (the top |k| bin ×2700), the packet keeps its energy, the number of nonzero
Nodes goes 351 → 1270. In quanta at T = 2¹⁵: 41 fast quanta out of 451 laid, 9 % in 4000 intervals, 0.2 % in
100, so the paper's runs cannot see it. The loader's refusal of an all-even fully periodic board ("Rule3's own
rounding walks the staggered mode without bound") is the special case of this general fact.

## 2. No fix inside the law, the carry or the families

Checked and closed: smooth fields (same rate at A = 2…60), amplitude (same), family (sin²ω only), the carry
(protects k = 0 only: 0.2 against 350), exact integer stencils in 3D (none stable: an integer stencil needs
Σ|c| ≤ 2, i.e. a line), axis-split exact leapfrogs (63 % of the zone unstable, growth ×9.9 per interval), an
exact line with the mass as a carried shrink (stable, heating ∝ S/den, 10¹² short at nature), a narrow band
(gain sin²ω₀ ≈ 10⁻²⁸, 10³⁹ short). Why: a stable integer recurrence with integer coefficients has only the
crystallographic bands (2cos ω ∈ ℤ, periods 1, 2, 3, 4, 6); a light mass and 3D coupling both need a
non-integer coefficient, the 1/3 being Courant's limit on the cube; division forces a floor, a floor is white.

## 3. The one knob is T, and it is tied to α

Heating in quanta is 0.1/T per Node per interval, Γ-independent per read (node-steps per read grow as Γ²
exactly as T does). At nature's T = Γ²/28 ≈ 10⁵⁵: 10⁵⁸ J/m³ per second, a square-metre detector credits ~10²²
quanta of 5×10¹⁰ GeV per second. Needed: T ≳ 10¹¹³ (no read sees a bath quantum), 10¹⁰⁴ (gravity's per-Node
write), 10¹⁴⁰ (created energy below the critical density over the age). Any of these breaks T = Γ²/28, i.e. the
α derivation under k_r = 1 (Supplement line ~530).

**What the paper should say (recommendation):**
- one claims row: *the floor's heating*, derived and measured, lattice; the rate, the conversion to quanta for
  any T, and the long-run test as its check;
- T's status: declared with a lower bound (as den is), the α relation conditional on it, or α kept and the
  heating listed as an open gap with its number. "Derived" alone no longer stands;
- the long-run bath test (thousands of intervals, writes off, the measure the top |k| bin, not the total form)
  among the standing checks;
- **do not** change Rule3, the carry, the engine, or the universe files of existing results; do not add an
  absorbing row (it kills reversibility).

## 4. Open, not resolved by me

- With the held writes **on**, the closed box runs away: the engine refused at interval 3589 (binding 9287 above
  the bound 9266), the form swinging 15.5M → 6.7M and a low-k component growing. Could be the writes in a box
  with no sink, not the floor. Needs the same run with open faces.
- The count read 445 → ~360 at amplitude 1241 within 250 intervals, stable after; 4051 → 4046 at 3723. Looks
  like the per-Node count's reading floor (below one quantum per Node), not a loss. Not proven.

## 5. Other points for the writer

- **Precursors, never "the only":** von Neumann's process 1, GRW (1986) and Bell's "Are there quantum jumps?"
  (1987), Tumulka's flash ontology (2006), Blanchard–Jadczyk's event-enhanced quantum theory (1995), 't Hooft's
  cellular automaton interpretation (2016), Fredkin/Toffoli/Margolus, Zurek (2003), Rovelli (1996). What is
  the paper's own: one integer rule that runs; the click defined operationally (Port inflow, whole quanta at
  the draw, the write back); gravity from the same mechanism (the held row, the exponential metric from the
  composed paces); a body as a record that holds itself in what it writes.
- **Time section:** Ω(k) = ω − kω′ *is* de Broglie's internal clock computed on the lattice band (ω = γω₀,
  k = γω₀v/c² gives ω − kv = ω₀/γ): naming it explains why Lorentz comes out to second order without Lorentz.
  Yilmaz by name with its price (no horizon, the frozen clock, the shadow 2e·m = 5.44m vs 5.20m).
- **Frame dragging / α₁:** separate "derived" from "found against nature" into different sentences; a reader
  sees a self-refutation when both sit in one.
- **First page:** three computed numbers in the second paragraph (two slits vs the band, Bell 2√2, β = γ = 1);
  gloss "fence", "the one assumption", "click" on first use.
- The discreteness a click resolves: one quantum, one interval, half a wavelength; Δt·E ≥ h as a counting fact
  (a quantum is counted once per period on its own clock).
