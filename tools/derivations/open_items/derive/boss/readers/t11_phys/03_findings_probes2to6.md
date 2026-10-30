# Findings from probes 2 to 6 (all on the real act; outputs beside them)

## probe2_held.txt (the held quantum)
- (a) Animate's world: the draft's count and the absolute count (D_lay := 0) write the SAME clicks in 6000 of 6000
  rounds (the giver's lay is 7 keys - 5 counts^2, so thresholds coincide). Difference: what each hand READS:
  draft: giver -7..0, taker 0..7, sum -1..0; absolute: giver 0..7, taker 0..7, sum 6..7.
- (d) round 3767: the giver's wind 0 thousandths of a key: the draft reads -7 (a negative occupation), absolute 0;
  the taker 7 in both.
- (b) a FREE hand laid at 6.499 keys: the draft's count 0 clicks (D_lay subtracted); the absolute count flickers 6..7
  in 2893 rounds of 6000 (Rule3's turn 1812 millionths of a key around a threshold). So the D_lay subtraction's real
  job is to put the LAY mid-key. The law's setting lays whole quanta ({"lay": "sea", "quanta": n}), which puts the
  absolute count mid-key too: the protection costs nothing with the law's own lay.
- (c) detuned taker, top 3.588 keys: counts 0..4, 28 click rounds, no flicker (the top stands 88 thousandths above
  the threshold, beyond Rule3's turn). Flicker at a turning point needs the top within ~3 thousandths of a half key:
  probe 2b to do.

## probe3_three.txt (three trains, the wind's count)
- (a) g, g: the counts end (-6, 3, 3); the three counts' sum in -1..1, off 0 in 2954 rounds of 6000 (half the run),
  longest stretch 306 rounds; both takers below half a key in 1526 rounds; clicks' sum not 0 in 89 rounds.
- (b) g, g/2: sum off 0 in 1282 rounds, longest 98; 64 miss rounds.
- the run back: the three winds on the mirrored state equal the forward's 6000 of 6000.
- The bound (n - 1) div 2 = 1 holds. The quantum is "whole on none" for hundreds of rounds at a time: the classical
  split of one quantum into two half shares, and nothing on this board makes it whole again without a push.

## probe4_misses.txt (the misses)
- g = f/10: the 2 misses are rounds 215 and 216: the giver clicks -1 at 215, the taker +1 at 216: a ONE-ROUND TRANSIT
  of one quantum, no loss. D_L + D_M's drift there 489 and -775 millionths of a key. Rule3's turn in one round up to
  3351 millionths of a key; the taker's wind moves up to 10967 millionths per round (3x the turn).
- g = f/100: the taker climbs 0..3 in 6000 rounds; 4 miss rounds (two transits); the pace 2739 millionths/round
  against the turn 3471: still no flicker pair.
- g = f/1000: the pace 202 millionths/round; nothing clicks in 6000 rounds (0.2 key passes at most).
=> a miss is a transit; the sum n_L + n_M returns to its value the next round. Physically: energy conserved to
Rule3's turn (< 2 thousandths of a quantum over 6000 rounds); a quantum "in flight" for one round between two clocks
at one Node-clock. Not a loss, but the clicks' record shows the give and the take one round apart.

## probe5_ring.txt (a ring of 48 Node-clocks with Meshes, the real act)
- (a) c = 1 (G = W): a 3-key binomial packet moves one site a round, exact (no remainder ever). SUM D and SUM P (the
  space Wronskian across the Mesh) both exactly kept; P = E for the right-mover. THE CLICKS' WORLDLINE: every site the
  packet passes clicks +1, +1, +1 then -1, -1, -1 (sites 8, 20, 32 shown; the packet comes round after 48 rounds and
  does it again). FREE PROPAGATION WRITES CLICKS at every Node-clock: 6 clicks per site per pass, 288 per lap, with no
  vertex and nothing given or taken anywhere. Against the law's (5) "a quantum given or taken" and TERM11's "the pull
  of the Meshes moves a train's area from Node-clock to Node-clock, the same train's: that is no take and is not
  counted". The draft's world has no Mesh, so it never saw this.
- (b) two humps with a dip: the wind per Node-clock is NEGATIVE in the dip (-800000, -640000, -800000) while SUM D =
  65760000 > 0: D = now^2 - next x before is not positive site by site (it is positive only where the gear's own
  motion is one beat, A^2 sin^2 omega, or the profile log-concave). With the key a seventh of a hump it would read -1.
- (c) the draft's D_lay on the laid ring: after the packet moves on, the laid sites read (0, 0, -1, -2, -3, -2, -1,
  0, 0) and the new sites (0, 0, 1, 2, 3, 2, 1, 0, 0): the ring's counts sum to 0 while 9 quanta are present. The
  absolute count: 0 where laid, 9 where the packet is.
- (d) c^2 = 1/6 (the engine's grip/teeth ratio): the standing wave A cos(pi x/2) at rest: D >= -425 (Rule3's turn
  on 1.2e9), P = 0 exactly at every round; SUM D kept to 122 millionths over 600 rounds; a moving packet: SUM D kept
  to 34 millionths of itself, SUM P to 15 millionths; D on the mirrored state = forward's at every site, 599 of 599.
  The most negative site wind of the moving packet -874794456 against SUM D 42345300000 (2 per cent).

## probe6_parity.txt
- odd keys 1..39, one birth (key - 1) div 2: 0 misses for every x; even keys: 10 misses in 10 keys of x, at
  x = key/2 mod key; even keys with births key/2 - 1 and key/2: 0 misses. The draft's parity reason carries to the
  state-function count exactly (SOUND).
