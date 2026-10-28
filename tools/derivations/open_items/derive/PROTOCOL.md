# The derivation protocol (the owner's word of 2026-10-28, 09:3x UTC: every derivation with a second hand, or a way that ensures no errors, no hallucinations and no fakes)

Every derivation for Tensor24's owed list goes through six steps before it enters section 19:

1. **The formula in the three operations alone:** integer multiplication, addition and Rule3 (n + r = q d + r', 0 <= r' < d). Each term is named with its clock word (docs/CLOCK_WORDS.md). No number beyond 0 and 1 except the lattice's counts read from the piece's shape (2 the sides of a Spoke, 3 the axes, 6 the Spokes). No float, root, cosine, angle, table, clamp (min, max, abs, where), loop that makes a formula, branch on a train's identity, or rule written for the phenomenon it makes.
2. **An algebraic proof** of every property claimed: what is conserved, the exact rewind, the 24's symmetry, the count of quanta kept, what it reduces to on the head.
3. **An executable probe that can fail:** integers only (python3 -I), run against the head's code where the head holds no fake (bit for bit), or as exhaustive or random property tests. The probe and its output are kept with the derivation.
4. **What it replaces and what it changes:** the fake it removes by its label (E, R, F, A, G), the rows it should move, and any contradiction with nature it leaves.
5. **A second, independent hand:** a verifier who did not write it re-derives it or attacks it (counterexamples; the edge cases 0, sign, the largest integers, the rewind), runs the probe, and reports CONFIRMED or REFUTED with its reasons.
6. **Sofer's law check** (no number, no closed form, no rule written for the phenomenon, no fitted constant), then **David's sign-off** as the derivations' owner.

Every claim is marked PROVED (with its proof), CHECKED (with its probe's count) or OPEN. Nothing is claimed that is neither proved nor checked.
