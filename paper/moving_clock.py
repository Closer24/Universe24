"""The moving clock's factor from the band, against Lorentz's, by no run.

A packet of a matter family moving at the velocity v = omega'(k) along one axis ticks at the
rotation at its moving centre, Omega(k) = omega(k) - k omega'(k), so its clock's factor is
f = Omega(k) / omega_0 (the paper's Section 8 (e); S.21), with omega(k) from the band
cos omega = (num / (3 den)) (2 + cos k). Drawn exactly from that band for the pairs [2, 3] and
[999, 1000], against Lorentz's factor sqrt(1 - v^2 / c^2) at light's speed c = 1 / sqrt 3 and
at the band's own kinetic scale c_m, c_m^2 = omega_0 / (3 tan omega_0). Every number here is the
formula's; nothing is read from a run of the engine.

    python paper/moving_clock.py --output paper/figures

Needs matplotlib.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
    }
)  # the journal's lettering: 8 pt at the final size, one typeface for the words and the symbols, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, GREY = "#000000", "#7a7a7a"
C = 1 / math.sqrt(3)  # light's speed in Links per interval


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def band(num: int, den: int, k: float) -> float:
    return math.acos(num / (3 * den) * (2 + math.cos(k)))


def moving_clock(num: int, den: int) -> tuple[list[float], list[float]]:
    """The moving clock's factor f = Omega / omega_0 against beta = v / c, up to the band's largest group speed."""
    w0 = band(num, den, 0.0)
    h = 1e-5
    betas, fs = [], []
    last_v = -1.0
    for i in range(1, 3000):
        k = i * math.pi / 3000
        v = (band(num, den, k + h) - band(num, den, k - h)) / (2 * h)
        if v < last_v:
            break  # past the inflection the group speed falls: the band's largest group speed along the axis
        last_v = v
        betas.append(v / C)
        fs.append((band(num, den, k) - k * v) / w0)
    return betas, fs


def figure(ax: Axes) -> None:
    for (num, den), ls, lab in (
        ((2, 3), "-", "the pair $[2, 3]$, from the band exactly"),
        ((999, 1000), (0, (4, 2)), "the pair $[999, 1000]$"),
    ):
        betas, fs = moving_clock(num, den)
        ax.plot(betas, fs, color=INK, lw=1.1, ls=ls, label=lab)
    bs = [i / 400 for i in range(400)]
    ax.plot(
        bs,
        [math.sqrt(1 - b * b) for b in bs],
        color=GREY,
        lw=0.8,
        ls=(0, (1, 1.5)),
        label="Lorentz's $(1 - v^2 / c^2)^{1/2}$ at light's $c$",
    )
    w0 = band(2, 3, 0.0)
    cm = math.sqrt(w0 / (3 * math.tan(w0)))
    bm = [b for b in bs if b * C < cm]
    ax.plot(
        bm,
        [math.sqrt(1 - (b * C / cm) ** 2) for b in bm],
        color=GREY,
        lw=0.8,
        label="Lorentz's at the band's scale $c_m$, $[2, 3]$",
    )
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("the packet's speed over light's, $v / c$")
    ax.set_ylabel("the moving clock's factor $f = \\Omega / \\omega_0$")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2, labelsize=8)
    ax.legend(loc="lower left", frameon=False, fontsize=8, handlelength=1.8)
    b23, f23 = moving_clock(2, 3)
    ax.plot([b23[-1]], [f23[-1]], "o", ms=3.5, color=INK)
    ax.text(
        b23[-1] + 0.02,
        f23[-1],
        "the band's largest group\nspeed along the axis at $[2, 3]$,\n$v$ about $0.2501$ Link per interval",
        ha="left",
        va="center",
        fontsize=8,
    )
    ax.text(
        0.60,
        0.30,
        "$c_m / c = 0.867$ at $[2, 3]$,\n$1$ as the gap closes",
        ha="left",
        va="top",
        fontsize=8,
        color=GREY,
    )


def moving_clock_figure(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.08, 3.0))
    figure(ax)
    fig.subplots_adjust(left=0.12, right=0.975, top=0.98, bottom=0.17)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "moving_clock.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    moving_clock_figure(args.output)


if __name__ == "__main__":
    main()
