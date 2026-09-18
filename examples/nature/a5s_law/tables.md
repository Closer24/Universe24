### The books per bit, the rest and the momentum in flight

| World | r | Contents A, B | Ticks | Books per bit balanced | Bodies + shadows in flight = 0 every tick (replay) | Bodies at rest | Shadows at start / at the end | Escaped | First push on B | Runner s |
| --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| `pp_d4_closed` | 4.00 | 2^28, 2^28 | 120 | every tick | not replayed | yes | 75497472 / 75497472 | 0 | 1 | 1152.7 |
| `pp_d6_closed` | 6.00 | 2^28, 2^28 | 120 | every tick | not replayed | yes | 75497472 / 75497472 | 0 | 1 | 1234.4 |
| `pp_d8_closed` | 8.00 | 2^28, 2^28 | 120 | every tick | not replayed | yes | 75497472 / 75497472 | 0 | 1 | 1318.7 |
| `pp_d12_closed` | 12.00 | 2^28, 2^28 | 120 | every tick | not replayed | yes | 75497472 / 75497472 | 0 | 6 | 737.6 |
| `pp_d8_110_closed` | 11.31 | 2^28, 2^28 | 120 | every tick | not replayed | yes | 75497472 / 75497472 | 0 | 6 | 912.7 |
| `pq_d8_closed` | 8.00 | 2^28, 2^27 | 120 | every tick | every tick | yes | 56623104 / 56623104 | 0 | 1 | 724.2 |
| `qq_d8_closed` | 8.00 | 2^27, 2^27 | 120 | every tick | not replayed | yes | 37748736 / 37748736 | 0 | 1 | 702.8 |

### The push per interval on B along the line from A, per window of twenty, the settled push and the standing-set search (every world closed: `boundary` periodic, 120 ticks, `standing_field` on)

| World | r | Contents A, B | Books per bit | Things + in flight + escaped = 0 | At rest | Standing set found | Iterations | Period | Residual (cells, amount) | Push on B, ticks 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 (+- its standard error) | Settled from tick | Push on A, 101-120 | Sign changes | p_B at 120 | p_A at 120 | p_A + p_B at 120 | In flight on the shadows at 120 (replay) | Runner s |
| --- | ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| `pp_d4_closed` | 4.00 | 2^28, 2^28 | every tick | not replayed | yes | False | - | - | 1570754, 92391155 | 42135 | -765 | -3846 | -42680 | -6783 | -13059 +- 8185 | - | 12981 | 51 | -499950 | 487251 | [-12699, 7752, 7127] | None | 1152.7 |
| `pp_d6_closed` | 6.00 | 2^28, 2^28 | every tick | not replayed | yes | False | - | - | 1664493, 92682652 | 7248 | 5964 | -2078 | -12285 | -6432 | 14940 +- 10704 | - | -14622 | 60 | 147139 | -171525 | [-24386, -733, 27134] | None | 1234.4 |
| `pp_d8_closed` | 8.00 | 2^28, 2^28 | every tick | not replayed | yes | False | - | - | 1732076, 93361803 | 2700 | 2689 | 4541 | 14681 | -8918 | -19126 +- 9765 | - | 18291 | 58 | -68674 | 40479 | [-28195, 9445, 1239] | None | 1318.7 |
| `pp_d12_closed` | 12.00 | 2^28, 2^28 | every tick | not replayed | yes | False | - | - | 1864017, 92624819 | 363 | 925 | 5609 | -9163 | -10615 | -4784 +- 4263 | - | 4510 | 54 | -353305 | 372353 | [19048, -3877, -2757] | None | 737.6 |
| `pp_d8_110_closed` | 11.31 | 2^28, 2^28 | every tick | not replayed | yes | False | - | - | 1844529, 93078026 | 8892 | 8872 | 2083 | -8146 | -2999 | -2269 +- 2094 | - | 2258 | 46 | 128655 | -129353 | [-1248, 261, -14532] | None | 912.7 |
| `pq_d8_closed` | 8.00 | 2^28, 2^27 | every tick | every tick | yes | False | - | - | 1583614, 70236352 | 2700 | 2689 | 4539 | 14641 | -9053 | -19147 +- 9765 | - | 9304 | 58 | -72623 | 43116 | [-29507, -1769, -523] | [29507, 1769, 523] | 724.2 |
| `qq_d8_closed` | 8.00 | 2^27, 2^27 | every tick | not replayed | yes | False | - | - | 1437201, 47132707 | 1110 | 1544 | 2424 | 6157 | -4350 | -9359 +- 5566 | - | 9333 | 54 | -49502 | 46785 | [-2717, -4035, -11643] | None | 702.8 |

### The scaling with d (the axis worlds, like contents 2^28), the anisotropy and the product law

| Quantity (the axis worlds) | Slope (log-log over d = 4, 6, 8, 12) | Standard error | Fit at d = 8 | Fit at d = 11.31 | Fit at d = 13.86 |
| --- | ---: | ---: | ---: | ---: | ---: |
| settled push on B, ticks 101-120 | -0.80 | 0.74 | 10302 | 7807 | 6638 |
| push on B, ticks 81-100 | 0.45 | 0.16 | 8558 | 10017 | 10984 |
| settled push on A, ticks 101-120 | -0.85 | 0.73 | 9898 | 7371 | 6203 |
| p_B at 120 | -0.47 | 1.32 | 192224 | 163573 | 148836 |

| World | r | Quantity | Measured | Axis fit | Ratio |
| --- | ---: | --- | ---: | ---: | ---: |
| `pp_d8_110_closed` | 11.31 | settled push on B, ticks 101-120 | -2269 | 7807 | -0.291 |
| `pp_d8_110_closed` | 11.31 | push on B, ticks 81-100 | -2999 | 10017 | -0.299 |
| `pp_d8_110_closed` | 11.31 | settled push on A, ticks 101-120 | 2258 | 7371 | 0.306 |
| `pp_d8_110_closed` | 11.31 | p_B at 120 | 128655 | 163573 | 0.787 |

| World (d = 8) | q_A, q_B | q_A q_B / (3 2^28)^2 | Settled push on B, 101-120 | Ratio to `pp_d8_closed` | 81-100 | Settled push on A, 101-120 | Ratio | Push on A + push on B | p_B at 120 | p_A at 120 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pp_d8_closed` | 3 x 2^28, 3 x 2^28 | 1.0000 | -19126 | 1.000 | -8918 | 18291 | 1.000 | -834 | -68674 | 40479 |
| `pq_d8_closed` | 3 x 2^28, 3 x 2^27 | 0.5000 | -19147 | 1.001 | -9053 | 9304 | 0.509 | -9843 | -72623 | 43116 |
| `qq_d8_closed` | 3 x 2^27, 3 x 2^27 | 0.2500 | -9359 | 0.489 | -4350 | 9333 | 0.510 | -26 | -49502 | 46785 |

### The recoil through the field: `pq_d8_closed` replayed, the momentum in flight from the inventory

| Tick | p_A | p_B | In flight on the shadows | Ledger current | Escaped | Sum |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | [-945, 0, 0] | [1368, 0, 0] | [-423, 0, 0] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 2 | [-1377, 0, 0] | [2043, 0, 0] | [-666, 0, 0] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 3 | [-2304, 0, 0] | [4077, 0, 0] | [-1773, 0, 0] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 5 | [-2070, 18, 0] | [3636, 0, 0] | [-1566, -18, 0] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 10 | [-3843, 9, -27] | [8037, 153, -225] | [-4194, -162, 252] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 20 | [-22455, 540, -54] | [53991, 666, -369] | [-31536, -1206, 423] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 30 | [-32913, 72, 234] | [71703, 135, -450] | [-38790, -207, 216] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 40 | [-53037, 0, 855] | [107766, -729, -720] | [-54729, 729, -135] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 50 | [-63701, -385, 1252] | [127026, -1161, 396] | [-63325, 1546, -1648] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 60 | [-104742, -1626, 379] | [198545, -675, 792] | [-93803, 2301, -1171] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 70 | [-178428, -834, 1547] | [395008, -902, 5767] | [-216580, 1736, -7314] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 80 | [-227588, -705, -3203] | [491373, 4181, 3451] | [-263785, -3476, -248] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 90 | [-150701, -2646, -1134] | [308250, 3842, 2997] | [-157549, -1196, -1863] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 100 | [-142960, -2243, -5826] | [310311, 646, 6854] | [-167351, 1597, -1028] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 110 | [-72995, -3713, -5986] | [141439, 3167, 4841] | [-68444, 546, 1145] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |
| 120 | [43116, -4863, -4619] | [-72623, 3094, 4096] | [29507, 1769, 523] | [0, 0, 0] | [0, 0, 0] | [0, 0, 0] |

The replay's momentum lines equal the record's: True; the two things' momenta plus the momentum in flight on the shadows plus the escaped sum to zero at every tick: True.

