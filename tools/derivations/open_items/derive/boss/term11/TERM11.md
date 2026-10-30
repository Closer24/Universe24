# Term 11, the whole click, in the four layers

The Boss, 2026-10-30, for David's two hostile readers. It rests on Animate's measured form (ANIMATE-CLICK, #2187
6521397023 item 4 (a)). The probe beside this page, `probe.py`, runs on the Node-clock's own act, in whole numbers;
its output is `probe.txt`.

## Clock

- A train at a Node-clock keeps one more tooth: its click tooth, born at the middle of its key.
- Each round the coupling moves some area into the train's hands, or out of them, and the click tooth counts it.
- When the count passes a whole key, the tooth carries one click and keeps the rest.
- A click pushes nothing: the vertex has already moved every bit of area it counts.

## Board

- **The area moved**, read at the now slot from the Node-clock's own gears: tau is the cross of the train's two parts
  with the kick, summed over its rows through the A1 table, tau = SUM C(re, K_im) - C(im, K_re), with K = s T_k q_d.
  A train of one part has no area and never clicks.
- **The carry:** q_c, k+ = carry(tau, key, k), one carry per train and Node-clock. Nothing is written into a, b, r or
  r_d.
- **The run back:** the mirrored state keeps the now slot, so the mirrored tick reads the same tau. The mirror flips the
  click tooth in its key, k to key - 1 - k, as it flips every fine tooth in its teeth. The carry then returns k exactly,
  and no log is read.
- **The birth:** k0 = (key - 1) div 2, with the Spokes along one axis as the divisor. It is the one tooth the flip
  leaves in place, flip(k0) = k0. An odd key has such a tooth; an even key has none.

## Clicks

- A click is one quantum taken (+1) or given back (-1): absorption and emission are one carry's two signs.
- **The books:** a give and a take of the same area are opposite clicks in every round. So conservation holds at every
  click (row 15), both ways of time.
- **Planck's relation per mode:** one key of area carries the key times the mode's own beat (Animate's measure 3),
  E = n h nu with the key as h.
- A free train that no coupling touches moves no area and never clicks (The light no bob, line 148).

## Algebra

- **Forward:** tau + k = q_c key + k+, with 0 <= k+ < key.
- **Back:** tau + (key - 1 - k+) = q_c key + (key - 1 - k), so the mirrored carry gives back key - 1 - k, and the
  mirror turns it into k.
- **Books:** let the key be odd and k0 = (key - 1) / 2. Write A + k0 = q key + r with 0 <= r < key. Then
  -A + k0 = -q key + (key - 1 - r), and 0 <= key - 1 - r < key. So carry(A, key, k0) and carry(-A, key, k0) give
  q and -q, for every whole A.
- **An even key** with k0 = key / 2 misses wherever A + k0 is a multiple of the key: once per key of area.

## Measured (probe.txt)

1. The birth is the one tooth the flip leaves in place.
2. The forward run, 6,000 rounds:
   - the giver's area moved is minus the taker's in every round;
   - the giver's click is minus the taker's in every round;
   - the taker clicks 20 times taken and 14 given back, its count from 0 to 7;
   - key x the count + (the tooth - the birth) equals the area moved in every round.
3. The run back by the act alone, with no log read:
   - gears, click teeth and quotients return in 6,000 rounds of 6,000, both teeth at the birth at the start;
   - **the mutant**, the click teeth not flipped by the mirror: the teeth return in 0 rounds of 6,000.
4. Every area from -3 to 3 keys, at every key from 1 to 40:
   - born at (key - 1) div 2: 0 misses at odd keys and 120 at even ones;
   - born at key div 2 (equal to it at odd keys): 0 at odd keys and 120 at even ones;
   - born at 0: 2,280 and 2,400 misses.
5. Born at 0 on the act (Animate's mutant): the giver's count is not minus the taker's in 5,999 rounds of 6,000.

## Open, so no code starts

- **The key's value:** one number for every train and every mode. Its unit is owed by the train card at G3 (Animate's
  README; TENSOR24_NODE.md 4.5). With no key, no run can click, so term 11 stays OPEN in the architecture document.
- **The key odd:** the books close exactly only for an odd key. Whether the law makes the key odd (den, the seed, is
  odd) is the owner's word and Sofer's law.
- **A train of three parts or more:** the files allow it, and the area is the cross of two parts. Which pairs is OPEN;
  no file lays such a train.
- **The kick's factors:** at s = T_k = T_d = 1 the kick is J, as in Animate's world. With s or T_k above 1 (G3), the
  area moved is the cross with the kick applied, s T_k q_d; this is checked again when G3 lands.
