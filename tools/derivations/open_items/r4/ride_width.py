"""Hand r4 (2026-10-25): the width of the riding line (ALGEBRA.md, The Node: every integer within 128 bits).
The wall w X = 6 den Gamma^2 G^2 X with X = Gamma e^(4 U) (features/volume, d + 1 = 4; the brief's e^(3 U) beside it),
read at U = 2.5 (the record's U) through the engine's own volume_of at the content c = Gamma U, at den 1,021, the 54-bit
candidate 15,162,856,759,112,389 and a den of about 40 bits (2^40 + 1, a magnitude and no circle), with G = 16 and G = 1;
the numerator's width beside it, w X times the amplitude (the sea's v = 189 and a level of 2^31), and the largest den the
riding line admits with w X and w X A within 2^127. Outputs ride_width.json. Integers only."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402

HERE = Path(__file__).resolve().parent
GAMMA, U_TENTHS = 1000, 25  # U = 2.5 as c = Gamma U = 2,500 units of content


def main():
    content = GAMMA * U_TENTHS // 10
    p0 = paces.clock(GAMMA, content)
    x4 = int(volume.volume_of(GAMMA, [content])[0])  # Gamma (Gamma / p_0)^4 to the engine's rounding
    x3 = (GAMMA ** 4 + p0 ** 3 - 1) // p0 ** 3  # Gamma (Gamma / p_0)^3, the brief's form, the same ceiling
    found = {"U": "2.5", "content": content, "p_0": p0, "X_e4U": x4, "X_e3U": x3, "bits_X_e4U": x4.bit_length(), "bits_X_e3U": x3.bit_length(), "dens": {}}
    amplitudes = {"v_189": 189, "level_2^31": 1 << 31}
    for name, den in (("1021", 1021), ("54-bit candidate", 15162856759112389), ("40-bit (2^40 + 1)", (1 << 40) + 1)):
        for unit in (16, 1):
            w = 6 * den * GAMMA * GAMMA * unit * unit
            row = {"den_bits": den.bit_length(), "w": w, "w_bits": w.bit_length()}
            for label, x in (("e4U", x4), ("e3U", x3)):
                wall = w * x
                row[f"wall_bits_{label}"] = wall.bit_length()
                row[f"wall_within_128_{label}"] = wall.bit_length() <= 128
                for aname, amp in amplitudes.items():
                    row[f"numerator_bits_{label}_{aname}"] = (wall * amp).bit_length()
            found["dens"][f"{name}, G {unit}"] = row
    # the largest den with w X < 2^127 and with w X A < 2^127 (A = 2^31) at U 2.5, for G 16 and 1, X = Gamma e^(4 U)
    for unit in (16, 1):
        base = 6 * GAMMA * GAMMA * unit * unit * x4
        found[f"largest_den_bits_wall_within_2^127, G {unit}"] = ((1 << 127) // base).bit_length()
        found[f"largest_den_bits_numerator_2^31_within_2^127, G {unit}"] = ((1 << 127) // (base << 31)).bit_length()
    # the U at which the 54-bit candidate's wall leaves 128 bits, G 16 and G 1 (the content searched by doubling and halving)
    for unit in (16, 1):
        w = 6 * 15162856759112389 * GAMMA * GAMMA * unit * unit
        top = volume.clock_zero(GAMMA) - 1  # the clock's last pace: the volume reading's own top
        low, high = 0, 1
        while high < top and w * int(volume.volume_of(GAMMA, [high])[0]) < (1 << 128):
            high = min(high + high, top)
        while high - low > 1:
            middle = (low + high) // 2
            if w * int(volume.volume_of(GAMMA, [middle])[0]) < (1 << 128):
                low = middle
            else:
                high = middle
        found[f"54-bit candidate: last content with w X within 128 bits, G {unit}"] = {"content": low, "U_thousandths": low * 1000 // GAMMA}
    (HERE / "ride_width.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
