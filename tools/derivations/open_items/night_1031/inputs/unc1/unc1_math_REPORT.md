<!-- Boss note, 2026-10-31 ~08:5x UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of UNC1 (frozen 2606e2f5), the hostile mathematician (the THIRD pair's mathematician). -->

# The hostile mathematician (THIRD pair) on UNC1 (the uncertainty principle read in the click world), 2026-10-31

The harness refuses report files from this reader, so the whole report is here.

**What I read**
- UNC1.md, whole: 426 lines, sha256 2606e2f55a853f81... All 1,251 sums in FROZEN.sha256 check OK.
- The three probes (unc1_read.py, unc1_twin.py, unc1_toy.py) and their outputs.
- The tree's step.passing, carry, edging and the decoder's sides.py.

**What I ran** (in S/unc1_math/, one process at a time, nice 19, load read before each, the tree read only with -B)
- **Toy, rerun from a copy** (python3 3.13): out/toy.mine.txt is byte for byte the frozen out/toy.a.txt.
- **Record reader, rerun from a copy:** out/read_click200.mine.txt is byte for byte the frozen out/read_click200.a.txt. It needs the live venv's Python 3.14, because the tree's decoder/records.py line 375 uses 3.14-only syntax (`except OSError, ValueError:`), which 3.13 refuses.
- **grain.py (mine):** the passings' grain as fixed by the plan.
- **twin_edge.py (mine):** the twin with the edge's one tooth moved, beside UNC1's one-side twin, half the key, 200 rounds; output in twin_edge_half.txt.

## VERDICT on UNC1: PASSED

Every bound is proved correctly, and each is reached as claimed: U1a to U1f, U2, U3, the coset, and M4's CHSH bound. The measured tables reproduce. There is no BLOCKING item. There are seven MINOR items:
- one naming that overclaims (m1);
- one procedure that makes a record the guard refuses, with its numbers standing (m2);
- one OPEN that I close by derivation (m3);
- four one-line wordings (m4 to m7).

## MINOR

**m1. "This is the counting form of the time-and-energy relation" is named, not derived** (U1d; the Summary's U1 bullet).
- **What is derived:**
  - a q-only reader's band on S_W is exactly 2K - 1 values (K from the birth), so the beat S_W / T lies in an interval of width 2 (K - 1) / T;
  - the whole-number line, T x (2 (K - 1) div T) <= 2 (K - 1) < T x (2 (K - 1) div T + 1), is floor division's definition and carries nothing more.
- **Why it is not the time-and-energy relation:**
  - The "energy" is J's work, the board's passing.
  - The click world's own count Q_W and its own clock's count T are both sharp; only the board's hidden passing is banded.
  - The band vanishes for a reader of the teeth (case ii). It is a counter's plus-or-minus-one-quantum resolution, not a bound on every reader.
- **It clashes with the text itself:** section 4 ends "Nothing above claims ... a time".
- **Fix:** "U1d has the form of a counter's resolution of the board's hidden passing; it is named after the time-and-energy relation by analogy only, OWED as physics".

**m2. The twin moves one side's tooth, not the edge's one tooth** (3.3; unc1_twin.py line 56).
- Only k(13, 0) is moved, and its mirror (17, 0) is not. So the edge's two teeth no longer sum to K - 1, against 0.1's "the edge holds one tooth".
- **MEASURED** (twin_edge.py, half the key, 200 rounds):

  | twin | sides whose clicks differ | the edge's books q(t,u) + q(u,t) not 0 |
  | --- | --- | --- |
  | UNC1's, the side's tooth alone | (13, 0) only | 122 of 200 rounds: a broken mate the sides' guard refuses |
  | the lawful one, the edge's tooth moved (+u on the side, -u on the mirror) | (13, 0) and (17, 0), at 122 rounds each | 0 of 200 rounds |

- The moved side's q is alike in the two twins at 200 of 200 rounds, by the mirror law: carry(-P, K, K - 1 - k) = (-q, K - 1 - k').
- So the text's numbers stand: 122 rounds; every one of the 20,100 windows within one quantum; U1f at 200 of 200.
- **Fix:**
  - move the edge's tooth on both sides;
  - say that the clicks then differ at the edge's two clocks, which bears on the seed test's "only at that clock".

**m3. "That every passing stays a multiple of 3 is not derived here from the plan (OPEN)" (1.1) is derivable.**
- **DERIVED** (grain.py, from the tree's load):
  - Every passing is a whole multiple of G, the gcd of every nonzero edge weight x factor and every Mesh coupling, for every state.
  - On the click world:
    - the values are 288,000 (3 x 96,000), 240,000 (4 x 60,000) and 120,000 (2 x 60,000), with no Mesh couplings;
    - so G = 24,000, gcd(G, K) = 3, the birth is 1 mod 3, and K = 3 x 50,811,429.
  - On the mesh world: G = 30,000 (Mesh couplings +/-750,000) and K = 3 divides it.
- **What follows:**
  - A one-unit move never changes a click on the click world, at any round and on any lay of its files.
  - No move of any tooth ever shows on the mesh world.
  - The measured grains (48,000 over 200 rounds, 30,000 over 125) are multiples of the structural ones.
- **Where the 3 comes from:** kappa/2 = 3 (in K and in the two-leg weight) together with 3 dividing the file's 60,000.

**m4. U1f's "the two lifts kappa = K Q + k differ by u at every round" is exact only when the moved birth does not wrap.**
- In general the lifts differ by u - K [k_0 >= K - u].
- The stated law already carries that second bracket, so only the sentence needs fixing.

**m5. Bell (M4; the Summary; 6.4): the bound covers "the pair's one hand" too.**
- By the text's own proof, a draw reading a shared hand is a local hidden variable and stays within 2, unless:
  - it reads the far setting (an influence across the separation), or
  - the settings depend on it.
- These are exactly the Boss's two roads (07:5x, second part). Fix: say "passing 2 needs the pair's hand to take one of those two roads", rather than listing it as a third.

**m6. Inside a silent gap, "any sub-window's passing is fixed to [-(K - 1), K - 1]" (2.2) is an outer bound.**
- A sub-window that starts or ends at the gap's listed tooth has only K values.

**m7. "The tooth has K / c reachable places" (U1's no) is the coset's size, an upper bound.**
- 283 distinct teeth are written in click200's 200 rounds. Say "at most K / c".

## The press points

**1. Every bound's proof, and whether each is reached: SOUND.**
- **(C):** from the carry, S_W + k_m = K Q_W + k_n, so |K Q_W - S_W| <= K - 1. From the birth, h - k_n lies in [-h, h].
- **Nearest quantum:** Q_n = floor((S_n + h) / K) = j + [r >= h + 1], and r <= h exactly when r < K/2 for an odd K, with no tie because 2S cannot equal (2j + 1)K.
- **Reached over the fiber:** for each tooth path, the passings P_n = K q_n + k_(n+1) - k_n carry to that q-word. So S_W takes all 2K - 1 values (K from the birth).
- **U1e:** K |Q_W - Q'_W| <= 2 (K - 1) < 2K.
- **U3:** adding c' to (q_tu, q_uv, q_vt) leaves every q_t = q_tu - q_vt unchanged (B C = 0).
- **On the record:** the band from the birth is filled to 994 per mille (75,771,435 of 76,217,143), and the q = 1 lines carry 9 passings, 670 per mille of 2 (K - 1). Reproduced to the byte.

**2. The exact law Q'_n - Q_n = [k_n >= K - u] - [k_0 >= K - u]: SOUND.**
- Derivation: kappa_n = k_0 + S_n, the moved lay's kappa'_0 = (k_0 + u) mod K, and Q'_n - Q_n = floor((k_n + u) / K) - [k_0 >= K - u].
- The clicks differ at exactly the rounds where the tooth crosses into or out of the strip [K - u, K - 1].
- MEASURED 200 of 200 (half the key; no wrap at h). The unit move's strip is K - 1 = 2 mod 3, and the down move's is 0, while the tooth stays 1 mod 3 (m3).

**3. "The counting form of the energy-time relation": only named (m1).**

**4. The toy on K = 3, 5, 7: SOUND as checks.**
- It is exhaustive within its boxes: passings in [-2K, 2K]^4 for T1 to T3, and [-K, K]^4 with every pair of births for T4 (21,609, 366,025 and 2,480,625 = K^2 (2K + 1)^4).
- T1 to T3 hold by construction (the carry's bijection), and T4 checks U1e. They can fail only by a fault in the carry, so they are confirmations, not evidence.

**5. The 16 CHSH strategies: SOUND.**
- A(B + B') + A'(B - B') with all four in {+/-1}: one bracket is 0 and the other +/-2, so S is -2 or 2.
- The toy prints the set as [-2, 2], meaning {-2, 2}. Mixtures with settings independent of the state stay within [-2, 2].

## SOUND, with numbers

- **Case (ii) closes the band:** P = K q + k_after - k_before at every listing, and G = k_before(next) - k_after(prev) over every gap. On click200 the gaps run from -37,440,000 to 37,440,000, and adjacent listings agree at 17,982 of 17,982.
- **U2 NOT SHOWN at every listing:** 25,272 and 41,376.
- **U3:** the circulation is not 0 at 4,158 of 4,212 places, and the text names most of these as one edge's quanta.
- **M2:** k_n = (h + S_n) mod K.
- **The decoder:** its click readings read q alone; the teeth appear only in the sides' guard (sided, mirrored) and in docstrings.
- **Standing labels:** the board-check rows are named as board checks; the 27 alike sites are named, so "162 of 162" is "6 of 6"; the thin F2 row is named.
- **The text's question 3:** the owner's seed test (ii) cannot show by one unit on either shipped world with clicks. With m3 this is now DERIVED for every round and every lay of the click world.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED:**
  - U1a to U1f, U2, U3, the coset, M2 and M4;
  - mine: the plan's grain (24,000 and 30,000), the mirror law for the twin, and the unit move's NOT SHOWN for every round.
- **MEASURED:** the two worlds' readings and the twins, reproduced; mine, the lawful twin.
- **OVERCLAIMED:**
  - "This is the counting form of the time-and-energy relation" (m1);
  - "two records alike on the board" for a record pair one of whose members the guard refuses (m2).

## Questions for the Boss

1. Shall the seed test's (ii) be worded as the edge's tooth moved (both sides), with "only at that edge's two clocks"? On the click world one unit never shows, by structure (m3), so the move must be at least two units, or the owner's lay must make gcd(G, K) = 1.
2. Should the energy-time naming wait for a click-world energy (OWED), given that the click world's own count and own time are both sharp?
3. node-all 9d75a4904's decoder parses only under Python 3.14 (records.py line 375). Should the pairs' "python3" be the live venv's?

## Solution24 (the reader's line)

UNC1 reads the click world's uncertainty honestly as the carry's remainder. The count is the passing to the nearest quantum, the tooth is flat to a reader of q alone, and both close when the record writes the teeth. It is local, so it stays within Bell's 2. Its energy-time name is an analogy; on the click world as laid the one-unit seed move can never show, by the plan's grain.

**Files:** S/unc1_math/grain.py, S/unc1_math/twin_edge.py, S/unc1_math/twin_edge_half.txt, S/unc1_math/copy/out/toy.mine.txt, S/unc1_math/copy/out/read_click200.mine.txt.
