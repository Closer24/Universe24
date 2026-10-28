# The tie rule: the step's carry odd at every teeth count

The question (TENSOR24.md, section 30, item 2, Rule3's ties; the Boss's #2187 comment 6474542826): the 24's turns negate the T1 and T2 gears, so a gear's step must keep q(-p) = -q(p) bit for bit at every teeth count, at both parities. Rounding half up is not odd.

**The rule:** draft H's going, kept per gear.
- home(w, go) = (w - go) div 2, the 2 being the order of the negation;
- the step: p = W (a - b) + (r - home(W, go)), then (q, r+) = carry(p + push + home(W+, go), W+) and a+ = a + q;
- a gear's negation N: (a, b, r, go) to (-a, -b, w - 1 - r, 1 - go), and the push to its negative.

**PROVED:** home(w, 1 - go) = w - 1 - home(w, go) at both parities, so N maps p to -p exactly. Where u = q w + r' with 0 <= r' < w, the carry of -u + w - 1 at w is (-q, w - 1 - r'). So N commutes with the step, with no tie left and the fine tooth inside [0, w).

**CHECKED** (probe.py, python3 -I probe.py; its output probe_out.txt): W and W+ drawn from 1 to 12, both parities, every r in [0, W):
- the going per gear: N then the step equals the step then N in 200,000 of 200,000 cases;
- a going shared by the Node-clock, where a turn negates one of its two gears: 161,202 of 200,000, since the negated gear's tooth 2 home - r leaves [0, W) at even counts.

Sofer reproduced the going per gear, 200,000 of 200,000, and with the going left unchanged under the negation, 99,385 of 200,000 (#2187 comment 6474681064).

**What it changes:** one going per gear, each gear's own pawl and T's sign on that gear, so the state per Node-clock is 5G + H + 4 integers for the ruling's 4G + H + 5, fixed for the run (line 98).

**What stays struck:** a rule that needs a parity (an odd rounding, every divisor odd, a tie sent to the even quotient). Odd teeth counts are allowed (the owner's word of 10:5x UTC, "Obviously allow odd teeth").

**Words:** Sofer's on the law, passes (6474681064); David's on the formula, owed. In code: algebra/carry.py's home and flip, its law "odd" failing on a home that ignores the going.
