"""THE SURPLUS LEAVES, checked algebraically (COMPUTED, no run of the engine): Rule3's line a_next = M(t) a_now - a_before
on a chain of Nodes in an external well, in floats (the identities are exact in integers up to the remainder).

(A) THE FORM UNDER A CHANGING WELL: the exact identity D(t + 1) - D(t) = <a_{t+1}, (M_t - M_{t+1}) a_t> for the total form
    D = |a_t|^2 - <a_{t+1}, a_{t-1}>; a well deepening slowly lowers the form of the standing mode while the adiabatic
    invariant A^2 sin omega stands: the count (flux alone, no flux at rest) stays, the form falls: the mass defect.
(B) THE FREE PART: at a Node the local rotation 2 cos omega_i = (next_i + before_i) / now_i against the band's top at the
    Node's pace; the standing mode has no free Node; a cloud twice too wide has free Nodes at its outskirts.
(C) THE SETTLING IS THE OPEN FACES': the same cloud on a chain with open faces (what leaves does not return: a sponge at the
    faces) against a closed chain (periodic); the width over time, the form kept inside the body, the free Nodes.
"""

import numpy as np

NUM, DEN, GAMMA = 4000, 6000, 6000
N = 400


def coefficients(p):
    """S / w and R / w at the pace p, the transverse arrivals equal to the level (a chain: the y and z Links flat)."""
    S = 2 * (1 - p * p / GAMMA**2)
    R = NUM * p * p / (3 * DEN * GAMMA**2)
    return S, R


def operator(p):
    S, R = coefficients(p)
    M = np.diag(S + 4 * R)  # the four flat transverse arrivals at the level itself
    bond = (
        NUM * p[:-1] * p[1:] / (3 * DEN * GAMMA**2)
    )  # the Link's bond num p_i p_j / (3 den Gamma^2), symmetric
    M += np.diag(bond, 1) + np.diag(bond, -1)
    return M


def top_of_band(p):
    S, R = coefficients(p)
    return S + 6 * R


def ground_mode(M):
    val, vec = np.linalg.eigh(M)
    v = vec[:, -1]
    return val[-1], v * np.sign(v[np.argmax(np.abs(v))])


x = np.arange(N) - N // 2


def well(depth, width):
    return depth * np.exp(-(x**2) / (2 * width**2))


# (A) the form under a deepening well
depth0, depth1, width = 300.0, 600.0, 6.0
p = GAMMA - well(depth0, width)
M = operator(p)
lam, phi = ground_mode(M)
omega = np.arccos(lam / 2)
a_before = phi * np.cos(-omega)
a_now = phi.copy()
steps = 4000
forms, invariant, identity_error = [], [], 0.0
for t in range(steps):
    depth = depth0 + (depth1 - depth0) * t / steps
    M_next = operator(GAMMA - well(depth, width))
    a_next = M @ a_now - a_before
    D = a_now @ a_now - a_next @ a_before
    a_next2 = M_next @ a_next - a_now
    D_next = a_next @ a_next - a_next2 @ a_now
    identity_error = max(identity_error, abs((D_next - D) - a_next @ ((M - M_next) @ a_now)))
    forms.append(D)
    lam_t = ground_mode(M_next)[0] if t % 500 == 0 else None
    if lam_t is not None:
        w_t = np.arccos(lam_t / 2)
        amp2 = (a_now @ a_now + a_next @ a_next - lam_t * (a_now @ a_next)) / np.sin(
            w_t
        ) ** 2  # A^2 of the mode
        invariant.append((t, depth, D, amp2 * np.sin(w_t), w_t))
    a_before, a_now, M = a_now, a_next, M_next
print(
    "(A) the identity D(t+1) - D(t) = <a_{t+1}, (M_t - M_{t+1}) a_t>: the largest error over 4000 intervals",
    f"{identity_error:.1e}",
)
print(
    "    the well deepening from 300 to 600: t, depth, the form D (the count stays: no flux at rest), the adiabatic invariant A^2 sin omega, omega_b"
)
for t, depth, D, inv, w in invariant:
    print(f"    {t:>5} {depth:6.0f}  D {D:9.6f}  A^2 sin omega {inv:9.6f}  omega_b {w:.4f}")
print(
    f"    the form fell by {100 * (1 - forms[-1] / forms[0]):.1f} percent at a kept count: the mass defect, the fields lighter by the binding"
)


# (B) the free part
def free_nodes(a_before, a_now, a_next, p):
    top = top_of_band(p)
    with np.errstate(divide="ignore", invalid="ignore"):
        bound = a_now * (a_next + a_before) > a_now * a_now * top
    return (~bound) & (np.abs(a_now) > 1e-9 * np.abs(a_now).max())


p = GAMMA - well(600.0, 6.0)
M = operator(p)
lam, phi = ground_mode(M)
omega = np.arccos(lam / 2)
a_b, a_n = phi * np.cos(-omega), phi.copy()
a_x = M @ a_n - a_b
print(
    "(B) the standing mode in the well of 600: free Nodes",
    int(free_nodes(a_b, a_n, a_x, p).sum()),
    "of",
    N,
)
sigma = np.sqrt((x**2 * phi**2).sum() / (phi**2).sum())
cloud = np.exp(-(x**2) / (2 * (2 * sigma) ** 2))
cloud /= np.linalg.norm(cloud) / np.linalg.norm(phi)
a_b, a_n = cloud * np.cos(-omega), cloud.copy()
a_x = M @ a_n - a_b
print(
    f"    a cloud twice too wide (width {2 * sigma:.1f} against {sigma:.1f}): free Nodes at the start",
    int(free_nodes(a_b, a_n, a_x, p).sum()),
)


# (C) open against closed faces
def run(open_faces, steps=6000, report=1000):
    a_b, a_n = cloud * np.cos(-omega), cloud.copy()
    sponge = np.ones(N)
    if open_faces:
        edge = 40
        ramp = np.linspace(1, 0, edge)
        sponge[:edge] = ramp[::-1] ** 2
        sponge[-edge:] = ramp**2
    M_local = M
    body = np.abs(x) <= 3 * sigma
    out = []
    for t in range(steps + 1):
        a_x = M_local @ a_n - a_b
        if t % report == 0:
            D_node = a_n * a_n - a_x * a_b
            D_in = D_node[body].sum()
            w = np.sqrt((x**2 * D_node.clip(0)).sum() / D_node.clip(0).sum())
            out.append((t, w, D_in, int(free_nodes(a_b, a_n, a_x, p).sum())))
        a_b, a_n = a_n * sponge, a_x * sponge
    return out


for open_faces in (True, False):
    print(
        f"(C) the chain with {'OPEN' if open_faces else 'CLOSED'} faces: t, the width, the form inside the body (3 sigma), free Nodes; the standing mode's width {sigma:.1f}"
    )
    for t, w, D_in, nf in run(open_faces):
        print(f"    {t:>5}  width {w:6.2f}  form inside {D_in:9.6f}  free Nodes {nf:3d}")


# (D) THE OUTWARD CURRENT AT THE SHELL: the count's line's own flux F through the Link at the body's edge, quadratic in the
#     record (the form's flux), for the standing mode against the cloud; its swing is the beat of the bound modes


def current_trace(start, steps=3000):
    a_b, a_n = start * np.cos(-omega), start.copy()
    i = N // 2 + int(2 * sigma) + 1
    trace = []
    for _t in range(steps):
        a_x = M @ a_n - a_b
        D = a_n * a_n - a_x * a_b
        trace.append(D[i])
        a_b, a_n = a_n, a_x
    trace = np.array(trace)
    return trace.mean(), trace.std(), trace.max() - trace.min()


print(
    "(D) the form at the shell Node (its flux is the count's line's current): the mean, the swing (its standard deviation) and the range over 3000 intervals"
)
for name, start in (("the standing mode", phi), ("the cloud twice too wide", cloud)):
    m, sd, rng_ = current_trace(start)
    print(f"    {name:26}: mean {m:9.6f}  swing {sd:9.6f}  range {rng_:9.6f}")
