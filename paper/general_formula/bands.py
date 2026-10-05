"""Light's and matter's bands along one axis, from the law's line and by no run.

The rotation of a family with the pair [num, den] at the wave vector k is
cos omega = (num / (3 den)) sum_a cos k_a, so along one axis cos omega = (num / (3 den)) (2 + cos k):
at k = 0 the gap cos omega_0 = num / den, at k = pi the band's top cos omega = num / (3 den). Drawn
for the massless pair [1, 1] (light: omega = k / sqrt 3 as k -> 0, the top at arccos(1 / 3) = 1.231)
and the matter pair [2, 3] (omega_0 = 0.841, the inertia m* = 3 tan omega_0 = 3.354 of the parabola
omega_0 + k^2 / (2 m*), the top at arccos(2 / 9) = 1.347); along the cube's diagonal light has
cos omega = cos k exactly. The two slits' wave, k = pi / 4 on light's band, omega = 0.4456.
Every number here is the formula's; nothing is read from a run of the engine.

    python paper/general_formula/bands.py --output paper/general_formula/figures

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
)  # the journal's lettering: 8 pt at the final size, one typeface for the words and the symbols, the figure drawn 1:1 at the page's width of 174 mm at most, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, GREY, LIGHT = "#000000", "#7a7a7a", "#c8c8c8"


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def omega(num: int, den: int, k: float) -> float:
    """The rotation along one axis: cos omega = (num / (3 den)) (2 + cos k)."""
    return math.acos(num / (3 * den) * (2 + math.cos(k)))


def band(ax: Axes) -> None:
    ks = [i * math.pi / 400 for i in range(401)]
    light = [omega(1, 1, k) for k in ks]
    matter = [omega(2, 3, k) for k in ks]
    ax.plot(ks, light, color=INK, lw=1.1, label="light, the pair $[1, 1]$")
    ax.plot(ks, matter, color=INK, lw=1.1, ls=(0, (4, 2)), label="matter, the pair $[2, 3]$")
    # light's speed at long wavelength, the tangent at k = 0
    ax.plot([0, 0.95], [0, 0.95 / math.sqrt(3)], color=GREY, lw=0.6)
    ax.text(
        0.99,
        0.95 / math.sqrt(3) - 0.035,
        "$\\omega = k\\,/\\,3^{1/2}$, light's speed",
        ha="left",
        va="center",
        fontsize=7,
        color=GREY,
    )
    # matter's parabola at the band's bottom: omega_0 + k^2 / (2 m*), m* = 3 tan omega_0
    w0 = math.acos(2 / 3)
    m = 3 * math.tan(w0)
    kp = [i * 1.3 / 100 for i in range(101)]
    ax.plot(kp, [w0 + k * k / (2 * m) for k in kp], color=GREY, lw=0.6)
    ax.text(
        0.12,
        1.14,
        "the parabola $\\omega_0 + k^2 / (2 m^*)$,\n$m^* = 3\\tan\\omega_0 = 3.354$, the inertia",
        ha="left",
        va="bottom",
        fontsize=7,
        color=GREY,
    )
    # the gap, the tops, the two slits' wave
    ax.plot([0], [w0], "o", ms=3.5, color=INK)
    ax.text(
        0.10,
        w0 - 0.11,
        "the gap $\\omega_0 = \\arccos(2 / 3) = 0.841$:\n$E = m^* c_m^2$ exactly, $c_m^2 = \\omega_0 / (3\\tan\\omega_0)$",
        ha="left",
        va="top",
        fontsize=7,
    )
    ax.plot([math.pi], [math.acos(1 / 3)], "o", ms=3.5, color=INK)
    ax.text(
        math.pi - 0.06,
        0.98,
        "light's top along the axis,\n$\\arccos(1 / 3) = 1.231$",
        ha="right",
        va="top",
        fontsize=7,
    )
    ax.plot([math.pi], [math.acos(2 / 9)], "o", ms=3.5, color=INK, markerfacecolor="white")
    ax.text(
        math.pi - 0.06,
        math.acos(2 / 9) + 0.04,
        "matter's top, $\\arccos(2 / 9) = 1.347$",
        ha="right",
        va="bottom",
        fontsize=7,
    )
    k2 = math.pi / 4
    ax.plot([k2], [omega(1, 1, k2)], "s", ms=4, color=INK, markerfacecolor="white")
    ax.text(
        k2 + 0.07,
        omega(1, 1, k2) - 0.01,
        "the two slits' wave,\n$k = \\pi / 4$, $\\lambda = 8$ Links",
        ha="left",
        va="top",
        fontsize=7,
    )
    ax.set_xlim(0, math.pi + 0.05)
    ax.set_ylim(0, 1.6)
    ax.set_xticks([0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi])
    ax.set_xticklabels(["0", "$\\pi / 4$", "$\\pi / 2$", "$3\\pi / 4$", "$\\pi$"])
    ax.set_xlabel("the wave number $k$ along one axis (radians per Link)")
    ax.set_ylabel("the rotation $\\omega$ per interval")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2, labelsize=7)
    ax.legend(loc="lower right", frameon=False, fontsize=7, handlelength=1.8)


def bands_figure(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(4.9, 2.9))
    band(ax)
    fig.subplots_adjust(left=0.11, right=0.995, top=0.98, bottom=0.17)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "bands.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    bands_figure(args.output)


if __name__ == "__main__":
    main()
