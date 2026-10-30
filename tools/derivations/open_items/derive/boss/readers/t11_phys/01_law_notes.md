# Law texts the draft rests on (copied so an interruption loses nothing)

## ALGEBRA.md line 35, item (4) (the law as it stands)
"how the click is computed: the wind of a hand is its stored energy counted in windings, a sum of products of its
gears now and before over the Node-clock and its six neighbours, and the carry is wind + earlier remainder = q x whole
winding + new remainder; with q = 0 there is no click, with q at least 1 the click fires, q whole quanta leaving as
events and the remainder staying, and 'q at least 1' is the quotient itself and no comparison"

## item (5)
"the two kinds of click, and no third: the click of a whole, where one hand holds the whole winding, there is nothing
to choose and the wind decides where the click happens (in nature a quantum given or taken, Planck's E = n h nu, and a
pair set from light or returned to it, E = m c^2); and the click of a split ... the beat (the carry of the clock's
dial) is the clock's own event and no kind of click"
=> THE LAW ITSELF names Planck's E = n h nu as what the whole click is in nature. h universal.

## line 1021
"A click is where the two carry the same signal; its wind is the product of the two directions at the region, the
form D = now^2 - next x before, the now against the future times the past"

## decision 40 (g) (line 35)
"the coupling family's steady count is one quantum per Node-clock, from the law and not from a file (decision 40
(g))" ... "by a steady odd count, such as the coupling family's one quantum per Node-clock of (g), whose kind is to
derive". => (g) is about ONE family (the coupling family) with a STEADY count of ONE quantum at every Node-clock. It
is not "the lay's wind of every train".

## conservation in the clicks (line 35)
"energy, from the time symmetry of every clock winding by one law: the wind, the conserved form, is kept to the
remainders at fixed reads, and at a click the beat before and after is checked; momentum, from the translation
symmetry of the board: the momentum along the click's Mesh is kept to a carried remainder and the transverse through
the gradients; charge, the sum of the senses over the fittings"
=> "at a click the beat before and after is checked" : the law expects the BEAT (frequency) to enter the click's
energy books. The draft's count never reads a beat.

## ARCHITECTURE.md term 11 row (physics column)
"one quantum per mode, E = n h nu; a negative wind is a negative quotient, with no if"

## Solution24 step 5
"Nature reads one quantum: a mass, a rate or a probability is read per quantum"
## step 6
"a conservation kept on the board and lost in the clicks is no solution"
## step 7
"what does not match nature is named, never hidden"

# Engine facts verified by reading src/tensor24
- carry(n, d, r) = ((n + r) // d, (n + r) % d). flip(r, w) = w - 1 - r.
- gear: q, r+ = carry(W (a - b) + push, W, r); a+ = a + q; b+ = a. push = s (F + T_k q_d); the own spring from the
  potential f a.a pushes each leg by -f x the other leg => -2 f a per gear (two legs).
- so a+ - 2 a + b = -(2 f / W) a + remainder effects: cos omega = 1 - f / W; f = W / 800 => omega ~ 0.05, period ~ 125.66.
- mirror: slots swapped, r -> W(b) - 1 - r, rd flipped. untick = mirror tick mirror.
- Animate's world: one Node-clock, nb all itself (no Mesh pull), T1 hands of 3 components x 2 parts = 6 gears each.

# Algebra verified by hand (my own)
- D_gear = a^2 - a+ b = v v+ + a (K a) where v = a - b, v+ = a+ - a, K the (symmetric) spring matrix: the leapfrog's
  exact invariant I = v.v+ + a.K a in exact arithmetic. SUM over all gears of D = I exactly (exact arithmetic).
- For a_t = A cos(omega t + phi): D = A^2 sin^2 omega, phase independent, for ANY harmonic gear (also travelling and
  standing waves on a chain: D per site = A_site^2 sin^2 omega).
- Two-part hand z = re + i im = z+ e^{i w t} + z- e^{-i w t}:
    D = 2 sin^2(omega) (|z+|^2 + |z-|^2)           (the SUM of the two senses, in energy units)
    Omega (area) = W sin(omega) (|z+|^2 - |z-|^2)   (the DIFFERENCE of the senses, in action units)
  Nature's quanta: N = n+ + n- = W sin(omega)(|z+|^2 + |z-|^2) / K_a = W D / (2 sin(omega) K_a). N needs sin omega
  (a root); N^2 = W^4 D^2 / (4 f (2W - f) K_a^2) is a ratio of whole numbers.
- E_act (TERM11) = W^2 D on a circle; E = 2 W sin(omega) Omega on a circle. So D = 2 sin(omega) Omega / W.
  => a fixed key in D is a fixed ENERGY per click, for every frequency. Planck: a fixed ACTION (area) per click.
