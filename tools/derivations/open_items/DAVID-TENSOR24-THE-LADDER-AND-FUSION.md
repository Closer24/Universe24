# The ladder of kinds and fusion, on 7a's own act

David, 2026-10-29, 05:0x UTC. It closes steps 2 and 3 of the open steps in my 6488233005, by the owner's word to David of 04:1x UTC (in Hebrew; in translation): "Close every open step. Let it enter the engine if corrections are needed, through the Boss."

Each claim is marked PROVED, CHECKED or OPEN. The probes and their outputs stood in derive/david_open/ladder/; none is in the tree now (l1, f1 and f2 left at 1b6ca0bf9, l2 at the audit of main b1a50bb33):
- l1_ladder_characters.py (.txt): the 24's characters against 7a's 125 tables;
- l2_ladder_on_the_act.py (.txt): the ladder run on 7a's act, turned by the 24, and run back; deleted with its output at the audit of main b1a50bb33 (P2, agreed by both readings), as it declared its three trains and two coupling rows in code on 7a's API, which main no longer has, so section 2 stands as measured on 7a and no probe in the tree reproduces it;
- f1_fusion_split.py (.txt): the joint dial split by 7a's tables, and the composite's whole numbers;
- f2_fusion_on_the_act.py (.txt): two hands bound by coupling rows, run as one clock.

Every probe runs on 7a's engine at tensor24-review 298bec5d8 (its src copied, unchanged): `python -I <probe> <src>`.

## 1. The ladder, from the 24's characters (PROVED and CHECKED, l1)

1. **The 24 and their five kinds** come from 7a's own kinds module, with no table typed: 24 of the 216 matrices whose rows are three Spokes have the determinant 1.
   - The classes, by the order of the turn and their size: (1, 1), (2, 3), (2, 6), (3, 8), (4, 6).
   - The characters, the traces of the kinds' whole matrices, in that order:

     | kind | (1, 1) | (2, 3) | (2, 6) | (3, 8) | (4, 6) |
     | --- | --- | --- | --- | --- | --- |
     | A1 | 1 | 1 | 1 | 1 | 1 |
     | A2 | 1 | 1 | -1 | 1 | -1 |
     | E | 2 | 2 | 0 | -1 | 0 |
     | T1 | 3 | -1 | -1 | 0 | 1 |
     | T2 | 3 | -1 | 1 | 0 | -1 |

   - They are orthonormal over the 24, and 1 + 1 + 4 + 9 + 9 = 24.
2. **Every product of two kinds splits without repeat:** every multiplicity is 0 or 1.
   - A1 x K = K; A2 x A2 = A1, A2 x E = E, A2 x T1 = T2, A2 x T2 = T1;
   - E x E = A1 + A2 + E; E x T1 = E x T2 = T1 + T2;
   - T1 x T1 = T2 x T2 = A1 + E + T1 + T2; T1 x T2 = A2 + E + T1 + T2.

   The triples (i, k -> m) the 24 allow number 43 of 125, which are 7a's 43 tables that are not 0.
3. **The ladder from one A1 train:**
   - **step 1:** its centred differences along the three axes read as T1 (7a's readings);
   - **step 2:** T1 x T1 = A1 + E + T1 + T2. One train's gradient read twice is the symmetric square, A1 + E + T2; the T1 in it, the cross, needs two different T1 readings;
   - **step 3:** T1 x T2 = A2 + E + T1 + T2. One train's gradient read thrice holds A2 as well (Sym^3 T1 = A2 + 2 T1 + T2): the triple product dx a dy a dz a, which turns by the A2 sign under all 24.

   The kinds first stand at step 0 (A1), 1 (T1), 2 (E and T2) and 3 (A2). So all five kinds come from one A1 train within three steps, which is Animate's ladder, all five by the third bang.
4. **7a's tables are exactly the 24's intertwiners:**
   - each is not 0 exactly where the characters put m in i x k;
   - the projector's seeds span, for all 125 triples, a space of the multiplicity's dimension, 0 or 1, so each table is the one intertwiner up to its factor;
   - each table that is not 0 has rank dim m as a map from i x k;
   - each turns as its kind under all 24, C(rho_i u, rho_k v) = rho_m C(u, v), on random whole u and v.

   For example, T1 x T1 -> A1 is the dot, T1 x T1 -> T1 the cross (6 entries), and E x E -> A2 the determinant. T1 x T2 -> A2 is a dot as well, since 7a holds T2 as A2 x T1, each shear on its vector's index.

## 2. The ladder on 7a's act (CHECKED on 7a by l2, whose probe left the tree at the audit of b1a50bb33)

1. **The world:**
   - three trains, a (A1, one gear), t (T2, three gears) and p (A2, one gear), on a board of 5 x 5 x 5;
   - two coupling rows through 7a's own load.plan and tables: J_t = C[T2; T1, T1](grad a, grad a), and J_p = C[A2; T1, T2](grad a, t), 9 terms in all;
   - grips one per Mesh, W = W+ = 6, s = 1, and the drive's teeth 4 on t and p;
   - at the start only a stands, as a bump of seven Node-clocks with no symmetry of its own.
2. **Measured:**
   - t first stands at tick 1 and p at tick 3;
   - p's source is 0 at ticks 1 and 2 and 723 at tick 3. The triple product stands only where the field has spread along all three axes at one Node-clock, which the bump reaches at tick 3.
3. **The 24 on the whole state:** the sites move by the turn about the board's origin, and each train's rows by its kind's matrix. A negated row maps (a, b, r, go, r_d) to (-a, -b, W - 1 - r, 1 - go, T_d - 1 - r_d), the flip. The run of the turned start equals the turned run at every one of 12 ticks and in every slot, for 24 of 24 turns.
4. **The run back** over the 12 ticks returns the start bit for bit.

## 3. Fusion: the composite clock in 7a's terms

### 3.1 Its kind: the product split by the tables (PROVED and CHECKED, f1)
1. **The shares:** for each product i x k, n_m = tr(G_p^-1 C^T G_m C) / dim m from 7a's own table C[i, k -> m]. G is each kind's kept form: the identity on A1, A2, T1 and T2, whose matrices are signed permutations, and [[2, -1], [-1, 2]] on E in its basis e1 - e2, e2 - e3.
   - For T1 x T1: A1 3, E 9, T1 2 and T2 2.
   - For E x E: A1 2, A2 2/3 and E 3.
2. **The fill:** on all 15 products the projectors are idempotent and sum to 1, and SUM_m |C_m x|^2_m / n_m = |x|^2_p holds on 200 of 200 random whole x of the joint dial, products u x v among them. PROVED by Schur; CHECKED exactly.
3. **Equal parts:** under the exchange of the two parts, each table is even or odd.
   - T1 x T1 and T2 x T2: A1, E and T2 even; T1 odd.
   - E x E: A1 and E even; A2 odd.

   So one train's quantum met with itself never reaches an odd kind, as my composite page has it.

### 3.2 Its dial and its binding: the pair runs as one clock (CHECKED, f2)
1. **The world:** two Gaussian hands A and B of one kind, each W = W+ = 1,000, s = 1, its spring D = 30, at one Node-clock (the board 1 x 1 x 1, so no Mesh pulls).
   - A held A1 gear H at 1 (s = 0) stands for the binding's carrier at rest.
   - Coupling rows through 7a's plan, part by part: J_A = g C[K; A1, K](H, B) and J_B = g C[K; A1, K](H, A), with g = 10.
2. **Derived from the act's linear part:** a free hand turns by w with 2 - 2 cos w = s D / W, w0 = 0.173422321 a tick. Bound, the even mode turns by w_S = 0.141539473 (the spring D - g h) and the odd mode by w_O = 0.200334842 (D + g h).
3. **Measured over 2,000 ticks, two A1 hands equal at the start:**
   - free: each hand turns by 0.173422321 and the composite A x B by 0.346844642, which is 2 w0: the beats add;
   - bound: each hand turns by 0.141539473 and the composite by 0.283078947, which is 2 w_S. The binding lowers the pair's turn by 0.063765696 a tick;
   - the two hands stay equal bit for bit at every tick, and the run back is exact.
4. **Two T1 hands, bound:**
   - **equal at the start:** the odd kind T1, the cross, stays 0 at every tick. A1, E and T2 each turn by 0.283078947 = 2 w_S;
   - **unequal at the start:** the odd kind turns by 0.341874316 = w_S + w_O. Each even kind's record is fitted by the two turns 2 w_S and 2 w_O to 1.3e-8 to 3.4e-8 of it, and the odd kind's by the one turn w_S + w_O to 1.3e-8;
   - in both, the fill SUM_m |C_m(A x B)|^2_m / n_m = |A|^2 |B|^2 holds at 2,001 of 2,001 ticks, and the run back is exact.
5. **So the composite's dial is its parts' dials multiplied.** Its beat is the sum of its parts' beats, and the binding is read from the coupling rows, not declared. The even kinds beat at twice each mode, the odd kind at the sum of the two modes.

### 3.3 Its whole numbers (PROVED and CHECKED, f1 item 4, f2 items 3 and 4)
1. **On the parts' own pairs:** the product of two pairs (p + i s) on den's circle lies on den^2's circle, 1,936 of 1,936 at den 5,525. So a free composite's rest beat is the sum of its parts', with its rim den^2 and no new number.
2. **Bound:** the even pair turns by 2 w_S, and 2 - 2 cos 2w = q (4 - q) with q = s (D - g h) / W. So the composite train at W_c = W^2 and s_c = 1 has the whole spring D_c = s (D - g h)(4 W - s (D - g h)) = 79,600. Measured on the act: it turns by 0.283078947 a tick, the bound pair's own turn, and runs back exactly.
3. **The width it costs** at the example universe (den 15,162,856,759,112,389, Gamma 1,000, the width 128):
   - den^2 is 108 bits, so a composite at rim den^2 has T = 6 den^2 Gamma^2 G^2 of 139 bits;
   - a train's W = 2 T is 86 bits, so W_c = W^2 is 171 bits;
   - both pass the width.
4. **Booked at the parts' own teeth instead,** W_c = W and D_c = s (D - g h)(4 W - s (D - g h)) div W, one carry at load, a booking of the law's kind as the rate line's: the composite's turn stands 3.8e-3 of it from the bound pair's at W 1,000, and 6.1e-9 at W 10^9 + 7. That is one tooth in D_c, and no width is added.

### 3.4 How the engine holds it: the law's way
1. **Before a click, the composite is a reading,** with nothing added to the state:
   - the parts' rows and the coupling rows between them carry it: each part moves in the other's field, which is the binding (3.2);
   - its gears are C_K on the parts' gears, the contraction's own gather, product and scattered sum through 7a's tables;
   - so line 98's fixed count holds by itself, and the beats and the binding follow from the act.
2. **At a fusion click, the composite is a train of its kind,** laid in a slot the cap bounds:
   - the click is the split of the joint dial (law 6), drawn by cut 1's one comparison over the shares |C_K x|^2 / n_K;
   - the drawn part is no product of the two parts' states. Over the two parts' components, A1's part has rank 3 in 498 of 498 pairs, T1's rank 2 in 500 of 500, and E's and T2's rank 2 or 3 (f1 item 3). So it cannot be written back into the parts' own rows;
   - it goes into a train of kind K whose rows stand at every Node-clock from the load, at 0 until a click lays them (line 98; Sofer's condition (d));
   - its coefficients come from its parts' and the binding (3.3), booked at the parts' teeth;
   - the click's books move one quantum from each part's train into the composite's train (law 8).
3. **So a fusion is the two kinds of clicks in sequence:** the split click chooses the composite's kind, and the whole click lays its hand.

## 4. What enters the engine, through the Boss
1. **Stage 6's tables:** nothing new, since 7a's tables are the 24's intertwiners exactly (1.4). One test: l1's four checks, and the parity of equal parts (3.1 item 3).
2. **The load (7b or 7c):** the composite trains a universe can form, derived at load from its parts' trains and coupling rows, with no key in any file, booked at the parts' teeth (3.3 item 4).
3. **Stage 9:** the fusion click: the shares n_K read once at load from the tables, the draw, the write into the composite's slot, and its books.
4. **The tests,** to the Boss with the proposal: l2's ladder (the kinds' first ticks, the 24, the run back; its probe since deleted, so such a test would lay its world from files), and f2's pair (the modes, the composite's turn, the odd kind of equal hands at 0, the fill, the written composite's turn, the run back).

## 5. OPEN
1. **The twin kinds** (E1/2, E5/2 and G3/2 of the 24 with the twin's sign) and their multiplicities above one: G3/2 x G3/2 holds T1 twice. This is OPEN 3, as 7a's load names it ("twin kinds wait on OPEN 3").
2. **E as a train:** 7a holds it beside A1 in the tensions (stage 7c), so the ladder's E stands in the tables and the readings, not in a train of its own.
3. **A moving carrier of the binding:** the probe's binding is a held gear. The exchange through a carrier that moves, with its delay, is OPEN beyond the held limit.
4. **The write's size:** the drawn part times sqrt(1 / share) is irrational at most draws (my composite page). The density, or a hand set at its lay to its free size, is decided together with the cap.
5. **The unfusing,** the composite back into its parts, and the run back of a fusion click.
6. **The wind's books for heavy parts:** the beats add, but the wind does not, since sin(w1 + w2) is not sin w1 + sin w2 (my composite page).
7. **The light laying the singlet pair at the bang** (Animate's (b)).
