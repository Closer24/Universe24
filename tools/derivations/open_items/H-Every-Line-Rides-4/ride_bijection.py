"""Hand r4 (2026-10-25): the riding line's act and its inverse, measured in integers (ALGEBRA.md, The line; The direction; The wall is one; The inverse).

The line: w [X_now (a_next - a_now) - X_before (a_now - a_before)] + r' - r = X_now (SUM_j R_ij (m_j - a_now) - D a_now),
one carried division at the wall w X_now forward; the inverse one carried division at the wall w X_before, the wall the
carried remainder r was born under. Part A checks the bijection on random states (growing and shrinking volumes), the
engine's carried_division at -1 among them; part B the two variants that move the remainder to the new wall (rescaled;
folded) and counts their failures; part C the joint map of one Node (the torus of extent one, flux 0) with the volume's
own line and its write sourced by the light's form, enumerated whole at tiny integers: the collisions of the whole map,
the failures of the inverse taken in the engine's order (the post-state's volumes in place of the start's), and the
joint inverse as a search over the previous volume.
Outputs ride_bijection.json beside it. Integers only; no float anywhere."""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from event_universe.core.rule3 import carried_division  # noqa: E402

HERE = Path(__file__).resolve().parent


MOVE = 0  # 1: the half wall's move (w (X_now - X_before)) div 2 in the numerator, the law's clause of the shear's momentum


def ride_forward(flux, mass, w, a_now, a_before, r, x_now, x_before):
    numerator = x_now * (flux - mass * a_now) + w * x_now * a_now + w * x_before * (a_now - a_before) + r
    numerator += MOVE * ((w * (x_now - x_before)) // 2)
    wall = w * x_now
    a_next = numerator // wall
    return a_next, numerator - wall * a_next


def ride_back(flux, mass, w, a_now, a_next, r_after, x_now, x_before):
    """w X_before a_before - r = V, 0 <= r < w X_before: a_before = ceil(V / (w X_before)), r = w X_before a_before - V."""
    v = x_now * (flux - mass * a_now) + w * x_now * a_now + w * x_before * a_now - w * x_now * a_next - r_after
    v += MOVE * ((w * (x_now - x_before)) // 2)
    wall = w * x_before
    a_before = -((-v) // wall)
    return a_before, wall * a_before - v


def ride_back_engine(flux, mass, w, a_now, a_next, r_after, x_now, x_before):
    """The same inverse through the engine's carried_division at direction -1, the wall w X_before."""
    total = x_now * (flux - mass * a_now) + w * x_now * a_now + w * x_before * a_now - w * x_now * a_next
    total += MOVE * ((w * (x_now - x_before)) // 2)
    return carried_division(total, w * x_before, r_after, -1)


def part_a(cases, seed):
    draw = random.Random(seed)
    w = 6 * 1021 * 1000 * 1000 * 256
    exact, exact_engine, shrinking, growing, out_of_new_wall = 0, 0, 0, 0, 0
    for _ in range(cases):
        x_now, x_before = draw.randint(1, 1 << 20), draw.randint(1, 1 << 20)
        a_now, a_before = draw.randint(-(1 << 30), 1 << 30), draw.randint(-(1 << 30), 1 << 30)
        flux = draw.randint(-(1 << 60), 1 << 60)
        mass = draw.choice((0, 0, draw.randint(0, 1 << 40)))
        r = draw.randint(0, w * x_before - 1)
        if r >= w * x_now:
            out_of_new_wall += 1  # the carried remainder stands at or above the new wall: admitted, no fold
        a_next, r_after = ride_forward(flux, mass, w, a_now, a_before, r, x_now, x_before)
        assert 0 <= r_after < w * x_now
        back = ride_back(flux, mass, w, a_now, a_next, r_after, x_now, x_before)
        exact += back == (a_before, r)
        exact_engine += ride_back_engine(flux, mass, w, a_now, a_next, r_after, x_now, x_before) == (a_before, r)
        shrinking += x_now < x_before
        growing += x_now > x_before
    return {
        "cases": cases,
        "exact_ceil_form": exact,
        "exact_engine_carried_division_minus_one": exact_engine,
        "cases_volume_shrinking": shrinking,
        "cases_volume_growing": growing,
        "cases_remainder_at_or_above_new_wall": out_of_new_wall,
        "wall_w": w,
    }


def part_b(cases, seed):
    """Two variants that move r to the new wall before the division: rescaled r_s = (r X_now) div X_before, and folded
    r_f = r mod (w X_now); each run forward from random states and inverted at the new wall; the failures counted, and the
    collisions (two states with the same image) counted on a small exhaustive box."""
    draw = random.Random(seed)
    w = 6
    fail_rescaled, fail_folded = 0, 0
    for _ in range(cases):
        x_now, x_before = draw.randint(1, 64), draw.randint(1, 64)
        a_now, a_before = draw.randint(-50, 50), draw.randint(-50, 50)
        flux = draw.randint(-500, 500)
        r = draw.randint(0, w * x_before - 1)
        r_s = (r * x_now) // x_before
        a_next, r_after = ride_forward(flux, 0, w, a_now, a_before, r_s, x_now, x_now)  # the velocity term at X_now too
        back = ride_back(flux, 0, w, a_now, a_next, r_after, x_now, x_now)
        r_back = (back[1] * x_before + x_now - 1) // x_now if back[0] == a_before else None
        fail_rescaled += back[0] != a_before or r_back != r
        r_f = r % (w * x_now)
        a_next, r_after = ride_forward(flux, 0, w, a_now, a_before, r_f, x_now, x_before)
        back = ride_back(flux, 0, w, a_now, a_next, r_after, x_now, x_now)
        fail_folded += back != (a_before, r)
    # exhaustive collisions of the rescaled variant: (a_before, r) -> (a_next, r') at fixed (a_now, flux, X_now, X_before)
    collisions = {}
    for x_now, x_before in ((2, 5), (5, 2), (3, 7), (7, 3)):
        images = {}
        for a_before in range(-20, 21):
            for r in range(0, w * x_before):
                r_s = (r * x_now) // x_before
                key = ride_forward(0, 0, w, 0, a_before, r_s, x_now, x_now)
                images[key] = images.get(key, 0) + 1
        domain = 41 * w * x_before
        collisions[f"X_now {x_now}, X_before {x_before}"] = {
            "domain": domain,
            "distinct_images": len(images),
            "states_lost": domain - len(images),
        }
    return {"cases": cases, "failures_rescaled": fail_rescaled, "failures_folded": fail_folded, "collisions_rescaled": collisions}


def one_node_forward(state, w, w_t, mass_t, write_wall, exponent):
    """One Node of the torus of extent one: the light's riding line (flux 0, massless), the volume's own plain line
    (Rule3 with its mass, flux 0) and its write ((d + 1) X_now c + r_w) div W, c the light's form now^2 - next x before."""
    a, b, r_l, x, x_b, r_t, r_w = state
    a_next, r_l2 = ride_forward(0, 0, w, a, b, r_l, x, x_b)
    total_t = w_t * (x + x - x_b) - mass_t * x
    x_tilde, r_t2 = carried_division(total_t, w_t, r_t, 1)
    c = a * a - a_next * b
    q, r_w2 = carried_division(exponent * x * c, write_wall, r_w, 1)
    return (a_next, a, r_l2, x_tilde + q, x, r_t2, r_w2)


def part_c():
    w, w_t, mass_t, write_wall, exponent = 6, 6, 2, 5, 4
    levels, x_max = 3, 4
    images, pre_states = {}, []
    for a in range(-levels, levels + 1):
        for b in range(-levels, levels + 1):
            for x in range(1, x_max + 1):
                for x_b in range(1, x_max + 1):
                    for r_l in range(0, w * x_b):
                        for r_t in range(0, w_t):
                            for r_w in range(0, write_wall):
                                state = (a, b, r_l, x, x_b, r_t, r_w)
                                post = one_node_forward(state, w, w_t, mass_t, write_wall, exponent)
                                if post[3] < 1:
                                    continue  # the volume at most 0: the floor's domain, refused by name
                                pre_states.append((state, post))
                                images.setdefault(post, []).append(state)
    collisions = sum(len(v) - 1 for v in images.values() if len(v) > 1)
    # the inverse in the engine's order: the light's line back first, with the volumes the post-state holds,
    # (X_now, X_before) read as (post.before, post.now) = (X_k, X_{k+1})
    engine_order_failures, law_order_needs_search, search_unique = 0, 0, 0
    for state, post in pre_states:
        a_next, a, r_l2, x_next, x_k, r_t2, r_w2 = post
        back = ride_back(0, 0, w, a, a_next, r_l2, x_k, x_next)
        engine_order_failures += back != (state[1], state[2])
        # the joint inverse: X_{k-1} unknown; every candidate tried, the consistent ones counted
        found = []
        for x_b in range(1, x_max + 1):
            b, r_l = ride_back(0, 0, w, a, a_next, r_l2, x_k, x_b)
            if not (0 <= r_l < w * x_b):
                continue
            c = a * a - a_next * b
            # the write back: X_tilde = X_next - q with q from (exponent X_k c + r_w) div W: r_w unknown too, every r_w tried
            for r_w in range(0, write_wall):
                q, r_w_after = carried_division(exponent * x_k * c, write_wall, r_w, 1)
                if r_w_after != r_w2:
                    continue
                x_tilde = x_next - q
                total_t = w_t * (x_k + x_k) - mass_t * x_k  # minus w_t X_{k-1}: the volume's own line back
                x_b_found, r_t = carried_division(total_t - w_t * 0, w_t, r_t2, -1)  # placeholder, replaced below
                # the exact inverse of the volume's plain line: w_t X_tilde + r_t2 = w_t (2 X_k - X_b) - mass X_k + r_t
                r_t = w_t * x_tilde + r_t2 - (w_t * (x_k + x_k - x_b) - mass_t * x_k)
                if 0 <= r_t < w_t:
                    found.append((a, b, r_l, x_k, x_b, r_t, r_w))
        law_order_needs_search += len(found) > 1 or len(found) == 0
        search_unique += len(found) == 1 and found[0] == state
    return {
        "parameters": {"w": w, "w_t": w_t, "mass_t": mass_t, "write_wall": write_wall, "exponent": exponent, "levels": levels, "x_max": x_max},
        "pre_states_in_domain": len(pre_states),
        "distinct_post_states": len(images),
        "collisions_of_the_whole_map": collisions,
        "failures_of_the_light_inverse_in_the_engine_order": engine_order_failures,
        "joint_inverse_unique_and_right": search_unique,
        "joint_inverse_not_unique_or_missing": law_order_needs_search,
    }


def part_d():
    """The third level on the time line (X two intervals back) at the one Node of part C: the forward map does not read it,
    so every post-state has one pre-image per value of the dropped level; the light's inverse with the held level is exact
    for the one step (counted), and the pre-state's own third level is not in the post-state (the pre-images per post-state)."""
    w, w_t, mass_t, write_wall, exponent = 6, 6, 2, 5, 4
    levels, x_max = 3, 4
    images, one_step_exact, total = {}, 0, 0
    for a in range(-levels, levels + 1):
        for b in range(-levels, levels + 1):
            for x in range(1, x_max + 1):
                for x_b in range(1, x_max + 1):
                    for x_bb in range(1, x_max + 1):  # the third level, two intervals back
                        for r_l in range(0, w * x_b):
                            for r_t in range(0, w_t):
                                r_w = 2
                                state = (a, b, r_l, x, x_b, r_t, r_w)
                                post = one_node_forward(state, w, w_t, mass_t, write_wall, exponent)
                                if post[3] < 1:
                                    continue
                                total += 1
                                extended = (*post, x_b)  # the post-state with its third level, X_{k-1}
                                images.setdefault(extended, []).append((*state, x_bb))
                                a_next, a_now, r_l2, x_next, x_k, r_t2, r_w2 = post
                                back = ride_back(0, 0, w, a_now, a_next, r_l2, x_k, x_b)
                                one_step_exact += back == (b, r_l)
    per_image = sorted(set(len(v) for v in images.values()))
    return {
        "pre_states": total, "distinct_extended_post_states": len(images), "pre_images_per_post_state": per_image,
        "light_inverse_exact_one_step_with_held_level": one_step_exact,
        "integers_added_per_node": 1, "dropped_by_the_forward_map": "X two intervals back (one pre-image per value)",
    }


if __name__ == "__main__":
    found = {"A_no_move": part_a(20000, 4)}
    MOVE = 1
    found["A_half_wall_move"] = part_a(20000, 4)
    MOVE = 0
    found.update({"B": part_b(20000, 5), "C": part_c(), "D": part_d()})
    (HERE / "ride_bijection.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    print(json.dumps(found, indent=1))
