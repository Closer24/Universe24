"""sl2: the algebra's numbers (integers only, every reading a quotient with its remainder): for each lift of the two universe files,
the unit u_s = 3 T s, the default lay's amplitude A (the least A with 12 (2 den - num) A^2 >= 12 u_s, the vacuum's weight), the
quarter-turn child's share 6 den A^2 against its own unit (the whole quantum at both ends) and against the two light quanta's walls
6 den T (the merger's take at one end), MS-S1's child (A B = T div 2) share 3 den (A^2 + B^2) against the same, and the ratio den / s
(the share in the child's own unit under MS-S1, E over m c^2).
Usage: python algebra_sl2.py <universe.json> ..."""
import json
import sys

sys.set_int_max_str_digits(0)


def isqrt_floor(n):
    high = 1
    while high * high <= n:
        high += high
    low = 0
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid <= n:
            low = mid
        else:
            high = mid
    return low


def q_r(a, b):
    return [a // b, a % b]


def main(paths):
    for path in paths:
        u = json.load(open(path))
        den, gamma, T = (int(u["integers"][k]) for k in ("den", "node_clock", "quantum_action"))
        print(f"== {path}: den {den} ({den.bit_length()} bits), Gamma {gamma}, T {T}")
        u_gap0 = 3 * T * den
        walls_light_pair = 2 * u_gap0
        print(f"  the gap-0 unit u_0 = 3 den T = {u_gap0}; the merger's walls (two light quanta) 2 u_0 = {walls_light_pair}")
        a_ms = isqrt_floor(T // 2)
        for row in u["rows"]:
            if row.get("shape") != 2 or row["pair"][0] == row["pair"][1]:
                continue
            num = int(row["pair"][0])
            s = isqrt_floor(den * den - num * num)
            exact = (s * s + num * num == den * den)
            u_s = 3 * T * s
            weight = 12 * (2 * den - num)
            target = 12 * u_s
            A = isqrt_floor(target // weight)
            while weight * A * A < target:
                A += 1
            share_qt = 6 * den * A * A
            print(f"  lift num {num}: s {s} (on den's circle: {exact}); u_s = 3 T s = {u_s}")
            print(f"    default lay A = {A}; child's share 6 den A^2 = {share_qt}")
            print(f"    share / u_s = {q_r(share_qt, u_s)} (quotient, remainder): WHOLE at its own unit where quotient >= 1")
            print(f"    share / (2 u_0) = {q_r(share_qt, walls_light_pair)}: the merger's take at ONE end can pay where quotient >= 1")
            print(f"    2 share / (2 u_0) = {q_r(2 * share_qt, walls_light_pair)}: the two ends summed")
            print(f"    (2 den - num) / s = {q_r(2 * den - num, s)} (the stop's ratio, derived: always above 1)")
            share_ms = 3 * den * (a_ms * a_ms + a_ms * a_ms)
            print(f"    MS-S1 child (A = B = {a_ms}): share 3 den (A^2 + B^2) = {share_ms}; / u_s = {q_r(share_ms, u_s)}; / u_0 = {q_r(share_ms, u_gap0)}; den / s = {q_r(den, s)}")


if __name__ == "__main__":
    main(sys.argv[1:])
