# David's step 2 for the Boss's toy: the families' one rule by their exchange (2026-10-27, 07:3x UTC)

On the owner's words of 06:0x UTC (Pauli: every matter family antisymmetric, every non-matter family like light symmetric, able to share one state in the clicks) and of 06:4x UTC, to David: "sync with the Boss toward a full and generic solution". Built in scratch on the Boss's toy boss-toy-1 c389d5580 (the carried paces and the trace 6), measured, not pushed as code; the whole diff beside this file as DAVID-STEP-2_DIFF.txt, to be applied on boss-toy-1 as the toy's step 2 if the Boss takes it.

## 1. The rule: every act of the close chooses by the family's declared exchange, none by a role

Each record row names `exchange` in the universe file beside its shape and pair: +1 symmetric, -1 antisymmetric (the five shipped universes: the plane at (den, den) +1, every gapped plane and the spinor -1). The loader admits the key (loader/world.py ROW_KEYS), the row carries it (rows.Row), and src never asks which family is light.

1. **The refusal (Pauli).** An antisymmetric family's child is refused where its family stands at the end and where two of its children land at one Node in one close: the head's two refusals, now with their reason. A symmetric family's child is never refused (close.refuse).
2. **The lay.** An antisymmetric child is laid by the one lay act at the quarter turn (MS-S1, its own state, A x B = T div 2). A symmetric child joins its family's standing mode by the exact take at -1 on the family's own lines at the end (MG-S1's light lay, merger.light_levels), so the share rises by the child's quantum to the least count and no cross term is made (close.children).
3. **The take.** A symmetric taken family pays by the exact take, one per Node, of its children's walls summed (EX-S1); an antisymmetric taken family is taken whole at each end (MG-S1) (close.births).
4. **The draw.** A symmetric family's meeting draws its children among the antisymmetric families, the draw's modulus their count (pair creation); an antisymmetric family's meeting gives the symmetric family (the merger into light) (close.list_of, draw.read_number).

## 2. The undo: one latent bug of the head, found and mended

A take shared by several children of one close was undone once per child: every child's entry carries the take, and close.click at -1 moved the taken line back for each (close.py, the loop over `entry.get("takes", [entry])`). The head never meets it: 0 births sharing a take on the three committed records and on the toy's two bang worlds. The symmetric admission meets it at once (five children of one light take at one Node on the chiral's interval 12). Mended by undoing a shared take once, the unbooked set guarding the move as it already guards the recoil; and run.birth now logs the exact lay whenever one was made (it logged it for a merger alone, so a symmetric child laid by the exact take at -1 was undone as a quarter-turn child). With both mends the run back is exact on every world below; without them it fails at the first step back.

## 3. Measured, on top of boss-toy-1, the run back of 20 intervals on every world

**Stage (i), the refusal, the lay and the take by exchange, the draw as on the head:** the run back exact 20 of 20 on all four worlds, and light makes light: a light meeting still draws among all the planes, light included, and its light children are no longer refused, so births cascade: the chiral 16 to 3,229, the hole 16 to 2,235 (its widest integer 112 to 3,239 bits), the bang world at 20 60 to 299, at 48 62 to 595 (3,500,112 bits). Nature has no such channel: light makes matter pairs, not light.

**Stage (ii), the rule whole (with the draw by exchange):**

| world | births, toy to step 2 | credits | widest integer (bits) | run back | gates SHOWN / NOT SHOWN / NOT READ |
|---|---|---|---|---|---|
| nature's chiral 60 | 16 to 18 | 2,858 to 3,536 | 112 to 112 | 20 of 20 | 31 / 16 / 24 to 32 / 15 / 24 |
| the hole 60 | 16 to 15 | 2,615 to 2,114 | 112 to 112 | 20 of 20 | 31 / 15 / 24 to 29 / 17 / 24 |
| the bodies 120 | 20 to 20 | 16,905 to 14,348 | 89 to 89 | 20 of 20 | 30 / 17 / 25 to 27 / 20 / 25 |
| the bang world at 20 | 60 to 16 | 14 to 0 | 489 to 213 | 20 of 20 | 28 / 17 / 31 to 22 / 6 / 48 |
| the bang world at 48 | 62 to 16 | 99 to 0 | 18,509 to 213 | 20 of 20 | 36 / 14 / 24 to 22 / 6 / 48 |

The bang world run on to 100 intervals under the rule: the carrier's level bounded at 24 to 131 bits, a two-cycle with the board frozen at every odd interval from 7 (24 bits at the even intervals, 124 to 131 at the odd ones), births at 9 and 11 alone. The runaway of THE-BANG-RUNS-AWAY.md does not occur on this world under the rule.

The kit on nature's chiral 60 (the toy, then step 2): the run back 60 of 60 and 60 of 60; the momentum law 58 of 58 and 58 of 58; the flux 60 of 60 and 60 of 60; the exact take 2,874 of 2,874 and 3,553 of 3,555; the born pair 9 of 16 and 12 of 17; the births' W sum 13 of 16 and 15 of 18; the planes' W at the close 57 of 60 and 40 of 60; the close's book 36 of 60 and 35 of 60; the 48 3 of 48 and 3 of 48.

## 4. The picture

- **Kept:** the run back exact on every world with every counter compared; the momentum law and the flux; Pauli for the matter families as a law and not a letter; light sharing states; no role in the refusal, the take, the lay or the draw; no runaway on the bang world.
- **Found:** the toy's bang world drew its matter and its clicks from light making light (60 births to 16, 14 credits to 0 when the channel closes); under the rule its matter is born once (16 births at 9 and 11) and never clicks. So "after every bang more and more, bodies clicking through detectors" is not on this world under the rule: the bang's births and its clicks need a channel the rule shuts, or a seed that feeds matter by the channel the rule keeps (light meetings drawing matter pairs).
- **Moved the wrong way:** the planes' W at the close 57 to 40 of 60 (the kit's charge book at the close), the hole 2 SHOWN down, the bodies 3; the chiral 1 SHOWN up. Read by the Reader before any word.
- **Left with a role:** close.list_of's `records.index(node.emitter())` (which symmetric family an antisymmetric meeting gives: the one the potential couples to by its pair), the merger's read_ends and takes and the bodies' emitter sites (the same role, the same replacement by exchange, not done here); the emission lay and the potential's pair stay the potential's coupling, a family named by its pair.
- **Not touched:** the runaway's letter on the toy's other worlds (THE-BANG-RUNS-AWAY.md: the owner's word owed between the clause as written and the velocity over the mean wall); Bell (DAVID-ON-THE-TOY.md item 7).
