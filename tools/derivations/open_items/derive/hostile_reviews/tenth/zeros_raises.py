"""What np.zeros((rows, sites), dtype=object) raises for huge sites: the lay's guard catches ValueError and MemoryError.
usage: python -I zeros_raises.py"""
import numpy as np

print("numpy", np.__version__)
for rows in (1, 3, 1 << 20):
    for e in (31, 32, 40, 48, 59, 60, 61, 62, 63, 64, 65, 100, 1000):
        for delta in (-1, 0, 1):
            sites = (1 << e) + delta
            try:
                z = np.zeros((rows, sites), dtype=object)
                print(rows, f"2^{e}{delta:+d}", "made", z.shape)
                del z
            except (ValueError, MemoryError) as error:
                print(rows, f"2^{e}{delta:+d}", "caught", type(error).__name__, str(error)[:70])
            except BaseException as error:  # noqa: BLE001
                print(rows, f"2^{e}{delta:+d}", "ESCAPES", type(error).__name__, str(error)[:70])
