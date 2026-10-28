import sys
L = open(sys.argv[1], encoding='utf-8').read().split('\n')
Q = {92: ["a Node-clock reads itself and its six Meshes and nothing else, forward and backward"],
     94: ["the step commutes with each of the cube's 24 turns, bit for bit, the click included"],
     721: ["the charge density at a Node-clock is the booking W_i = re_now x im_before - im_now x re_before",
           "exactly invariant in the rationals at rates fixed in time", "1 / p_i^2"],
     785: ["no quadratic form of the notches and the remainders is conserved exactly by the integer step, the Wronskian included",
           "the exact invariant of the integer step being the state itself through the back step"],
     803: ["two solutions u, v of one line conserve Omega(u, v) = SUM_i (u_now v_before - v_now u_before) / p_i^2",
           "exactly in the rationals at fixed rates, in integers to the carried remainders", "W = Omega(re, im)"],
     805: ["no rounding with one integer of memory per Node-clock conserves the form", "Rule3 unchanged", "no second carried integer", "2026-10-19"],
     1539: ["the odd gear on the axis a is sourced by J_a, the sign's own current"],
     1602: ["where they differ the neighbour's plane value is read conjugated and its K negated",
            "the Wronskian's flux through a Mesh is one number read from both ends in the frame every hand was born in",
            "39 to 75 notches", "owed by name", "every charge conjugated (the Wronskian odd under the swap)",
            "the step's output discarded", "at the state it started from",
            "the swap of the post-state in place of the pre-state locks the great clock in a two-cycle at its top, refuted and shown",
            "(M z)* = M* z*"]}
for n, qs in Q.items():
    for q in qs:
        found = q in L[n - 1]
        where = [i + 1 for i, l in enumerate(L) if q in l][:4]
        print(f"L{n}: {'FOUND' if found else 'MISSING'}  {q[:70]!r}  (lines holding it: {where})")
