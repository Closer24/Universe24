# Odd teeth counts: Sofer's check of the owner's ruling, and the law's lines that leaned on parity

The owner to Sofer, 2026-10-28, 10:59 UTC (in Hebrew, verbatim in translation): "What does odd teeth mean? Why shouldn't they be odd?", with the text of a video on Pauli (amplitudes add; the exchange twice is the identity, so its sign is plus or minus; two identical detectors give A - A = 0; the exchange is the full turn of one particle, which flips the sign of a spin one half), "From here it will be understood how to derive to the board and from it to the click", and "Obviously allow odd teeth." To Animate, the same hour (as Animate relays it, the thread's 6467251813, ledger row 355): "Switch to teeth with no restriction of even or odd." and "Let them check what works out from it." This page is Sofer's check, with its probe (SOFER-ODD-TEETH-1_PROBE.py) and the probe's output (SOFER-ODD-TEETH-1_CHECKS.txt), and the list of the law's lines changed. It is not David's derivation. Each claim is PROVED (with its proof), CHECKED (with its probe's count) or OPEN.

## What odd teeth means, and why the law had them even

1. **The gear:** every gear of a Node-clock has w fine teeth, a remainder r in [0, w), and mid(w) = w div 2. The law's count w = 6 den Gamma^2 G^2 is always even, because 6 is: at w = 10 the half is the tooth 5; an odd count is one like 11, with the middle tooth 5 and five teeth on each side.
2. **The reason it was even:** only the formula. The law said "even at every den, so w div 2 exact": the evenness was a property of 6 den Gamma^2 G^2 that made the half an integer, and was written as if it were a condition. No law line gave a reason from nature for it.

## What the check shows (CHECKED, w from 2 to 40; mutants fail)

| at | even w | odd w |
|---|---|---|
| the one mirror r to (2 mid - r) mod w | an involution; fixes the tooth 0 and the tooth w / 2 | an involution; fixes the mid tooth alone |
| the flip r to w - 1 - r | an involution; fixes no tooth | an involution; fixes the mid tooth alone; **it is the one mirror** |
| the carry's rounding q(p) = (p + mid) div w, q(-p) = -q(p) | fails exactly at the ties p = w / 2 mod w (8 of 65 in -4 w to 4 w at w = 8) | never fails |
| the fold's digit classes min(r, w - 1 - r) | w div 2 | (w + 1) div 2, which is w div 2 at an even w too |
| the stride P under the exchange of the two slots | the flip sends P to -P - 1; the mirror misses -P by w at the tooth 0 | both send P to -P exactly |
| the mean teeth count (w / 2)(X0 + X1) | an integer for every pair of notches | a half where X0 + X1 is odd: the doubled form w (X0 + X1) is the integer at every count |
| the one-gear retrace of a turnover at the weak top (the mathematician's toy, rewritten: w from 8 to 15, D = 3 and 5) | with the mirror 13 to 27 images hit twice at every even w (25 at w = 10); with the flip none | none with either (w = 11: none) |

The mathematician's toy is the Boss's (derive/mathematician/turnover.py on engine-5.0-test 8b657aa57); the probe rewrites it and reproduces his 25 at w = 10 and none at w = 11. Animate's parity probe (reader-5 0d1dbe1d, ANIMATE-PROBES-1/parity.py) gives the same two failures at w from 8 to 15 for the engine's acts.mirror and Rule3's rounding.

**In words, for the owner:** at an even count the dial has two ways to be mirrored and they differ by one tooth: the mirror about the middle (it keeps the setting still, but it fixes two teeth and the step and the turnover can land two states on one image) and the flip (it retraces exactly, but it moves the setting by one). At an odd count the two are one map, the setting is its fixed tooth and the retrace is exact, with no tie in the rounding. An even count needs one of two repairs at the carry (Animate's: the carry kept in the stride; the tie sent to the even quotient); an odd count needs neither. That is the reason to allow both and let the acts hold at both.

## What entered the law (docs/ALGEBRA.md, scribe-5)

The clause **The teeth count has no parity condition**, in the line of **The teeth counts are algebra and not code**, in the owner's words and with the facts above (line numbers unchanged: the clause stands inside the line). Status: decided and unbuilt. The lines that leaned on parity, each changed in place:

| line | before | now |
|---|---|---|
| 100 | "w = 6 den Gamma^2 G^2 even at every den, so w div 2 exact" | the calibre's count, even at every den because of its factor 6, a property of the formula and no condition of the law |
| 110 | Gamma odd for "no tie in the odd rounding, the half teeth counts' div 2 exact through w's own evenness" | Gamma odd for no tie in the odd rounding; the exactness of div 2 is the calibre's even w, which the law does not ask |
| 122 | the fold's digit "over w div 2 classes" | over (w + 1) div 2 classes, w div 2 at an even w |
| 130 | the riders' mean teeth count (w / 2)(X0 + X1), "a product and no division", and the born gears' origin (w / 2) X_before | the same, marked at an even w and owed at an odd w |
| 344 | "the setting's origin at an even half teeth count" | "at the half teeth count of an even teeth count" |
| 559 | "T sends P to -P - 1" | at an even w; to -P at an odd w |
| 622 | the image of the half "one below teeth count div 2 for an even teeth count" | and at teeth count div 2 itself for an odd one |
| 1600 | the shear's term (3 w / 2)(X_ahead - X_behind), the half teeth count's move | the same, marked at an even w and owed at an odd w |

Left as they stand, being records of what a run or a hand measured at the calibre's even counts and scoped by their own words: line 352 (the pair {w / 2 - 1, w / 2}, the half to w / 2 - 1), line 436 (the riders' mean teeth count of David's measure), line 618 (the cube's symmetry: "no fixed point at an even teeth count", "the two's complement at even w, w - 1 - r at odd w").

## What it does not settle (OPEN, David's, with the Boss's property tests at both parities)

1. **The formula of w at an odd count.** The setting's identity SUM R + D = 2 w (**The setting across parts**) ties w to the Spokes' count and the spring's factors (6, 12, 2). Whether a calibre exists at an odd w, and its smallest set, is David's to derive; until then no run at an odd count is claimed and the calibre stands as the one set that loads and runs.
2. **The retrace T S T = S^-1 at any count,** with the mirror about the mid tooth or with the flip (the toy above), and Animate's two candidates for an even count, (i) the mirror with its carry kept in the stride, (ii) the tie sent to the even quotient.
3. **The riders' ride and the shear's term at an odd w:** the mean teeth count and the half teeth count's move, written in the doubled form w (X0 + X1) and 3 w (X_ahead - X_behind) or by another derivation of David's.
4. **The 24 (the cube's turns), the count of quanta and the setting at the mid tooth at an odd count.**

## For the plan

The architect's ask (b), Rule3's ties odd or every divisor odd, is answered by the ruling: no restriction. Every act's probe runs at both parities (the mathematician's toy at w = 10 and 11 and p to -p among them), and carry.py is written only after them (Animate's list, 6467251813).
