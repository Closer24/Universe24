# The closed list: the engine written with the carry, addition and multiplication

The owner's word (2026-10-28, 15:3x UTC, Hebrew, translated): "The node does very simple things, right? In the main it does Rule3, addition and multiplication; that is also what the laws approve, I think. So make sure the engine can really be written with these."

**The answer: CHECKED.** probe.py (python3 -I probe.py; its output probe_out.txt) holds a whole number Z that allows addition and multiplication alone, a product by -1 included. Every comparison, truth test, division, remainder, power, shift, bit operation, abs, int, index and hash raises, and so does any plain number beyond 0 and 1. carry() is the one place a division is written. On Z the probe writes the engine's 29 acts:
- the whether, the choice, min, max and equality, from the carry's quotient: nonneg(n) = 1 + n div (n n + 1);
- the Gaussian product, its dot and cross (conj(z) w), the norm and i z; the twin hands' T (T T = -1) and Lagrange's identity;
- the 24 from the six Spokes alone: 24 found, with no table typed;
- the contraction T1 x T1 -> A1 + T1 + E + T2 (the dot, the cross, the stress), its tables made from the Spokes, and the outer product read back from the nine parts, every quotient exact;
- the step of a gear (p+ = p + s F + K, with F = sum_j g_j (U_j a_j - a) - D a + J, then the carry) and its exact inverse;
- the whole click; the split click with the draw, one part picked by the cumulative quotients, with no sort and no if; the draw's digits in order as a fixed network of min and max; the turnover at the top by the time gear's carry; the beat by the rate dial's carry.

Every act matches its plain reference on random cases (2,000 to 4,000 each, 0 failures). The scan of the 29 acts' code finds no if, conditional expression, comparison, while, and/or, try, raise or assert. Each of the 12 mutants (one term changed) fails its check, its count printed in probe_out.txt.

**What it does not show:**
- **The one promise:** every divisor must be a teeth count of at least 1. Two divisors do not keep it: light's winding w_c = 0 in the whole click (M2), and W+ <= 0 in the step (M1). Both close before the first cut.
- **Reading and holding are no operations:** a Node-clock reads its own gears and its six Meshes' by the layout's fixed tables, and holds a fixed count of integers (lines 92 and 98). The probe's loops run over the layout (the six Meshes, the 216 candidates, the 3 x 3 tables), never over the state; in the engine they are array operations.
- **Outside the Node-clock:** loading the files, the runner's rounds and its rewind check, and the decoder loop and compare by design (derive/architecture/ARCHITECTURE.md, section 4).
- **The twin hands beyond the half turns** (M5, M6): over Z[i] only the half turns are exact. That is the ring's question, not the operations'.
- **The draw's fairness** (item 6) is no question of the operations.

**For Sofer's meeting point** (SOFER-ARCHITECTURE-1.md, section 6, item 3): law 9's "digits in the order of their values" stays inside the closed list as a fixed network of min and max (sort4 here). An order-free composition is shorter; the choice is the architect's.

This is a probe, not the engine: nothing is built before the owner's approval.
