### The books per bit

| World | Board | Ticks | World line balanced | Real line | Shadow line | `real_conserved` | Shadows at start | At the end | Escaped | Runner s | Source |
| --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `pulse` | open | 40 | every tick | every tick | every tick | every tick | 3145728 | 3145728 | 0 | 210.9 | `6fef7cc0` |
| `standing` | open | 40 | every tick | every tick | every tick | every tick | 37748736 | 19372497 | 18376239 | 114.3 | `6fef7cc0` |
| `standing_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 479.0 | `051d7168` |
| `probe_axis_r4` | open | 40 | every tick | every tick | every tick | every tick | 37733842 | 19453575 | 18280267 | 1250.8 | `6fef7cc0` |
| `probe_axis_r8` | open | 40 | every tick | every tick | every tick | every tick | 37748734 | 19392959 | 18355775 | 494.4 | `6fef7cc0` |
| `probe_axis_r12` | open | 40 | every tick | every tick | every tick | every tick | 37748736 | 19383998 | 18364738 | 278.7 | `6fef7cc0` |
| `probe_110_m3` | open | 40 | every tick | every tick | every tick | every tick | 37716989 | 19517291 | 18199698 | 1328.7 | `6fef7cc0` |
| `probe_110_m6` | open | 40 | every tick | every tick | every tick | every tick | 37748736 | 19457929 | 18290807 | 594.2 | `6fef7cc0` |
| `probe_110_m9` | open | 40 | every tick | every tick | every tick | every tick | 37748736 | 19402443 | 18346293 | 265.4 | `6fef7cc0` |
| `probe_axis_r4_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37733842 | 37733842 | 0 | 559.5 | `051d7168` |
| `probe_axis_r8_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748734 | 37748734 | 0 | 580.9 | `051d7168` |
| `probe_axis_r12_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 550.3 | `051d7168` |
| `probe_110_m3_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37716989 | 37716989 | 0 | 921.9 | `051d7168` |
| `probe_110_m6_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 1004.9 | `051d7168` |
| `probe_110_m9_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 1000.8 | `051d7168` |
| `probe_111_m2_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37514574 | 37514574 | 0 | 1016.2 | `051d7168` |
| `probe_111_m5_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 636.0 | `051d7168` |
| `probe_111_m7_closed` | periodic | 120 | every tick | every tick | every tick | every tick | 37748736 | 37748736 | 0 | 552.5 | `051d7168` |

### The standing world (`standing_closed`): the field of the thing at rest on the closed board, `boundary` periodic, 120 ticks, `standing_field` on

The runner's standing-set search: fixed point or cycle found False, iterations to the repeat None, period None, residual at the last comparison 622389 cells and 46597043 quanta, ticks kept fixed 0, fallback None. Shadows on the board at every tick: 37748736 (escaped 0). Off the planes, mean of the last twenty ticks: 0.860. The replay identical to the record tick by tick (shadows on the board, escapes, the body's momentum, the books): True.

| k (L1) | Nodes | Content per Node, ticks 81-100 | 101-120 | J_r per Node, 81-100 | 101-120 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 21213 | 8661 | 0 | 0 |
| 1 | 6 | 8263 | 2759 | 1430 | 879 |
| 2 | 18 | 4419 | 1537 | 65 | 179 |
| 3 | 38 | 3758 | 1338 | -55 | 63 |
| 4 | 66 | 3663 | 1332 | 116 | 55 |
| 5 | 102 | 3646 | 1273 | -0 | 150 |
| 6 | 146 | 3291 | 1203 | -37 | 128 |
| 7 | 198 | 2929 | 1173 | -31 | 152 |
| 8 | 258 | 2777 | 1207 | -6 | 133 |
| 9 | 326 | 2669 | 1280 | 43 | 196 |
| 10 | 402 | 2464 | 1315 | 43 | 281 |
| 11 | 486 | 2204 | 1278 | 18 | 235 |
| 12 | 578 | 1973 | 1246 | -24 | 207 |
| 13 | 678 | 1768 | 1263 | -30 | 223 |
| 14 | 786 | 1675 | 1218 | -29 | 236 |
| 15 | 902 | 1680 | 1133 | -50 | 226 |
| 16 | 1026 | 1685 | 1109 | -32 | 191 |

| Read Node (free field) | r | Content, ticks 81-100 | 101-120 | Settled from tick | J_r, 81-100 | 101-120 | Amplitude, 81-100 | 101-120 | Settled from tick | Wave fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| axis_r4 | 4.00 | 9833 | 2603 | - | -424.0 | 92.5 | 179.2 | 86.0 | - | 1.136 |
| axis_r8 | 8.00 | 5997 | 3038 | - | -497.1 | 33.3 | 130.7 | 73.3 | - | 0.793 |
| axis_r12 | 12.00 | 5804 | 3059 | - | 61.9 | 934.3 | 127.0 | 97.1 | - | 1.180 |
| 110_m3 | 4.24 | 3952 | 2219 | - | 242.3 | 278.9 | 107.4 | 63.4 | - | 0.773 |
| 110_m6 | 8.49 | 1652 | 2563 | - | 311.7 | 778.0 | 48.7 | 85.5 | - | 1.130 |
| 110_m9 | 12.73 | 1924 | 2384 | - | 264.1 | 92.0 | 70.8 | 84.4 | - | 1.199 |
| 111_m2 | 3.46 | 7726 | 1254 | - | 258.2 | 255.4 | 164.5 | 47.2 | - | 1.152 |
| 111_m5 | 8.66 | 2033 | 867 | - | -288.1 | 167.9 | 80.7 | 54.9 | - | 1.427 |
| 111_m7 | 12.12 | 2521 | 4653 | - | 498.1 | 1486.9 | 92.9 | 126.6 | - | 1.671 |

| t | On the board | Content per Node at k = 4 | 8 | 12 | J_r per Node at k = 4 | 8 | 12 | Off the planes | Parked | Step s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 37748736 | 40312 | 14116 | 802 | 18700 | 8924 | 513 | 0.491 | 0.000 | 3.202 |
| 5 | 37748736 | 47936 | 12646 | 4537 | 23592 | 6661 | 2780 | 0.832 | 0.000 | 3.836 |
| 10 | 37748736 | 9140 | 8122 | 6885 | 1806 | 3454 | 3796 | 0.791 | 0.001 | 3.832 |
| 20 | 37748736 | 1684 | 1796 | 1708 | 187 | 410 | 594 | 0.868 | 0.002 | 3.597 |
| 30 | 37748736 | 613 | 606 | 657 | 51 | 85 | 157 | 0.910 | 0.002 | 3.823 |
| 40 | 37748736 | 295 | 305 | 339 | 13 | 17 | 37 | 0.938 | 0.003 | 3.97 |
| 50 | 37748736 | 219 | 222 | 285 | 14 | 2 | -1 | 0.955 | 0.003 | 3.662 |
| 60 | 37748736 | 239 | 278 | 349 | -17 | -31 | -47 | 0.958 | 0.003 | 3.762 |
| 70 | 37748736 | 581 | 995 | 950 | -240 | -311 | -243 | 0.919 | 0.003 | 3.698 |
| 80 | 37748736 | 1220 | 2018 | 1783 | -261 | -274 | -226 | 0.843 | 0.003 | 3.768 |
| 90 | 37748736 | 4860 | 3692 | 1620 | -17 | -527 | 85 | 0.802 | 0.003 | 3.369 |
| 100 | 37748736 | 2342 | 2716 | 2064 | 726 | 85 | 320 | 0.838 | 0.003 | 3.217 |
| 110 | 37748736 | 816 | 1033 | 1169 | 112 | -55 | 251 | 0.844 | 0.003 | 3.343 |
| 120 | 37748736 | 459 | 773 | 741 | 47 | 136 | 40 | 0.890 | 0.003 | 3.274 |

### The test things (the nine closed probe worlds): the push per interval per window of twenty, the settled push and the amplitude at the thing's Node

| Probe | r | Ticks 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 (+- its standard error) | Settled from tick | Sign changes | Amplitude at the Node, 81-100 | 101-120 | Arrived per interval, 101-120 | Wave fraction | Free-field amplitude (`standing_closed`), 101-120 | Intervals waited | Cumulative push at 120 | Body's momentum at 120 | Recoil home | In flight on the shadows at 120 (replay) | Probe + shadows + body = 0 every tick (replay) | Standing-set search |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- |
| `axis_r4_closed` | 4.00 | 5863.9 | -98.2 | 28.9 | 44.5 | 1915.6 | 637.2 +- 588 | - | 58 | 259.2 | 264.2 | 14200 | 1.754 | - | 119 | 167837 | [-3284, -22, -58] | 2.0 % | [-164553, 244, 1939] | True | False, iterations None, residual 46861051 |
| `axis_r8_closed` | 8.00 | 425.9 | 430.9 | 120.2 | 343.1 | 1344.0 | 1155.1 +- 685 | - | 44 | 191.3 | 172.3 | 12360 | 0.915 | - | 119 | 76386 | [-257, -29, 14] | 0.3 % | [-76129, -1144, -1577] | True | False, iterations None, residual 46785415 |
| `axis_r12_closed` | 12.00 | 59.2 | 273.0 | 192.6 | 343.2 | 1939.3 | 1845.7 +- 621 | - | 36 | 143.1 | 103.4 | 2589 | 1.602 | - | 117 | 93060 | [-58, -17, 2] | 0.1 % | [-93002, -659, 292] | True | False, iterations None, residual 46774502 |
| `110_m3_closed` | 4.24 | 11608.0 | 175.8 | 44.4 | -71.9 | 1348.4 | 1064.5 +- 542 | - | 66 | 192.0 | 214.1 | 8595 | 1.886 | - | 119 | 283383 | [-8575, -8167, -42] | 4.2 % | [-212166, -171856, 51] | True | False, iterations None, residual 46993502 |
| `110_m6_closed` | 8.49 | 2473.3 | 1024.0 | 46.1 | 206.2 | 222.9 | 409.0 +- 883 | - | 39 | 90.6 | 191.9 | 8488 | 1.697 | - | 119 | 87629 | [-751, -667, -3] | 1.1 % | not read | not read | False, iterations None, residual 46792815 |
| `110_m9_closed` | 12.73 | 270.1 | 506.5 | 66.3 | 118.7 | -122.6 | 452.8 +- 252 | - | 48 | 73.3 | 85.0 | 2371 | 1.239 | - | 115 | 25835 | [-34, -73, 4] | 0.3 % | not read | not read | False, iterations None, residual 46753318 |
| `111_m2_closed` | 3.46 | 15259.6 | 1092.6 | 5.2 | -949.5 | -340.7 | 443.9 +- 827 | - | 49 | 345.7 | 392.9 | 18704 | 2.763 | - | 119 | 310224 | [-29934, -30205, -32802] | 17.3 % | not read | not read | False, iterations None, residual 46671324 |
| `111_m5_closed` | 8.66 | 5440.5 | 297.7 | 6.4 | -13.3 | 266.6 | 562.1 +- 403 | - | 46 | 99.0 | 53.3 | 870 | 1.189 | - | 118 | 131203 | [-3894, -3932, -1740] | 4.2 % | not read | not read | False, iterations None, residual 46980039 |
| `111_m7_closed` | 12.12 | 1748.7 | 1044.2 | 33.4 | -280.8 | 317.3 | 318.7 +- 219 | - | 41 | 94.3 | 127.0 | 4319 | 1.724 | - | 115 | 63629 | [-743, -751, -213] | 1.5 % | not read | not read | False, iterations None, residual 46834595 |

### The 1/r^2 fit per direction and the anisotropy (closed board)

| Direction | Quantity | Slope (log-log over three radii) | Standard error | Value at r = 8 | At r = 12 | Signs |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| axis | settled_push_101_120 | 0.96 | 0.08 | 1213.9 | 1788.7 | [1, 1, 1] |
| axis | push_81_100 | -0.05 | 0.37 | 1701.8 | 1671.0 | [1, 1, 1] |
| axis | amplitude_at_probe_101_120 | -0.83 | 0.17 | 154.8 | 110.6 | [1, 1, 1] |
| axis | free_amplitude_101_120 | 0.07 | 0.24 | 85.5 | 88.1 | [1, 1, 1] |
| axis | free_j_101_120 | 1.72 | 2.55 | 167.7 | 336.9 | [1, 1, 1] |
| axis | free_content_101_120 | 0.16 | 0.05 | 2935.3 | 3125.8 | [1, 1, 1] |
| 110 | settled_push_101_120 | -0.84 | 0.43 | 564.1 | 400.8 | [1, 1, 1] |
| 110 | push_81_100 | -2.23 | 0.30 | 306.4 | 124.2 | [1, 1, -1] |
| 110 | amplitude_at_probe_101_120 | -0.77 | 0.49 | 147.4 | 108.0 | [1, 1, 1] |
| 110 | free_amplitude_101_120 | 0.28 | 0.12 | 77.9 | 87.2 | [1, 1, 1] |
| 110 | free_j_101_120 | -0.74 | 1.77 | 264.0 | 195.4 | [1, 1, 1] |
| 110 | free_content_101_120 | 0.08 | 0.10 | 2391.8 | 2471.4 | [1, 1, 1] |
| 111 | settled_push_101_120 | -0.15 | 0.41 | 422.5 | 396.8 | [1, 1, 1] |
| 111 | push_81_100 | -0.10 | 0.17 | 303.1 | 290.9 | [-1, 1, 1] |
| 111 | amplitude_at_probe_101_120 | -1.17 | 1.01 | 121.3 | 75.5 | [1, 1, 1] |
| 111 | free_amplitude_101_120 | 0.66 | 0.49 | 74.3 | 97.0 | [1, 1, 1] |
| 111 | free_j_101_120 | 1.01 | 1.47 | 448.4 | 676.3 | [1, 1, 1] |
| 111 | free_content_101_120 | 0.74 | 1.14 | 1868.0 | 2522.9 | [1, 1, 1] |

| Quantity | Axis / (111) at r = 8 | At r = 12 | Axis / (110) at r = 8 | At r = 12 |
| --- | ---: | ---: | ---: | ---: |
| amplitude_at_probe_101_120 | 1.276 | 1.466 | 1.050 | 1.024 |
| free_amplitude_101_120 | 1.151 | 0.909 | 1.099 | 1.011 |
| free_content_101_120 | 1.571 | 1.239 | 1.227 | 1.265 |
| free_j_101_120 | 0.374 | 0.498 | 0.635 | 1.724 |
| push_81_100 | 5.615 | 5.745 | 5.553 | 13.452 |
| settled_push_101_120 | 2.873 | 4.507 | 2.152 | 4.463 |

## The open board, measured earlier (recorded; not the series)

The eight open-board records below were made before the model owner's decision that only closed worlds are tested (Highlights 5.4, "The board of a run is closed"); they are kept as recorded and stand outside the series' reading.


### The test things on the open board: the pushed amount per interval and the inventory's J at the same Node

| Probe | r | Cumulative radial push at 40 | At 30 | Mean per interval, ticks 2-21 | 2-11 | 12-21 | 22-31 | 32-40 | Sign changes | Inventory J_r, mean 2-21 (`standing`) | Content per Node at 2 / 21 / 40 | Intervals waited | Body's momentum at 40 | Recoil home | Ledger momentum lines at 40 (current, returned, escaped) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- | --- |
| `axis_r4` | 4.00 | 115328 | 115787 | 5868.1 | 8538.1 | 3198.1 | -107.9 | -106.1 | 18 | 4274.9 | 22653 / 2634 / 388 | 39 | [-1587, 6, 5] | 1.4 % | {'current': [1760, -13, 1], 'returned': [-1587, 6, 5], 'escaped': [-173, 7, -6]} |
| `axis_r8` | 8.00 | 17204 | 9190 | 392.0 | 153.9 | 630.1 | 399.9 | 596.1 | 12 | 606.4 | 841 / 1674 / 501 | 39 | [0, 0, 0] | -0.0 % | {'current': [119, 8, 10], 'returned': [0, 0, 0], 'escaped': [-119, -8, -10]} |
| `axis_r12` | 12.00 | 6572 | 6295 | 101.0 | 30.1 | 171.8 | 431.9 | 26.0 | 10 | 163.8 | 0 / 1072 / 228 | 37 | [0, 0, 0] | -0.0 % | {'current': [63, 3, -5], 'returned': [0, 0, 0], 'escaped': [-63, -3, 5]} |
| `110_m3` | 4.24 | 235703 | 234571 | 11527.1 | 16474.5 | 6579.8 | 395.0 | 134.5 | 20 | 12227.5 | 85833 / 2410 / 295 | 39 | [-6044, -5618, -2] | 3.5 % | {'current': [6326, 5927, 2], 'returned': [-6044, -5618, -2], 'escaped': [-282, -309, 0]} |
| `110_m6` | 8.49 | 69914 | 68845 | 2879.9 | 1350.7 | 4409.2 | 1190.7 | 45.3 | 9 | 3929.1 | 976 / 6515 / 79 | 39 | [-449, -391, -3] | 0.8 % | {'current': [640, 566, 18], 'returned': [-449, -391, -3], 'escaped': [-191, -175, -15]} |
| `110_m9` | 12.73 | 15481 | 11006 | 306.6 | 125.7 | 487.4 | 602.9 | 369.0 | 10 | 1251.5 | 0 / 12242 / 151 | 35 | [0, 0, 0] | -0.0 % | {'current': [8, 204, 6], 'returned': [0, 0, 0], 'escaped': [-8, -204, -6]} |

### The pulse (open board, measured earlier): the front per direction and the release off the planes

| Read Node | r | sqrt 3 r | First arrival (tick) | Peak (tick) | Peak content |
| --- | ---: | ---: | ---: | ---: | ---: |
| axis_r4 | 4.00 | 6.9 | 3 | 9 | 7385 |
| axis_r8 | 8.00 | 13.9 | 11 | 29 | 827 |
| axis_r12 | 12.00 | 20.8 | 19 | 37 | 241 |
| 110_m3 | 4.24 | 7.3 | 5 | 9 | 19854 |
| 110_m6 | 8.49 | 14.7 | 13 | 19 | 4062 |
| 110_m9 | 12.73 | 22.0 | 21 | 29 | 1542 |
| 111_m2 | 3.46 | 6.0 | 5 | 7 | 59187 |
| 111_m5 | 8.66 | 15.0 | 14 | 16 | 13893 |
| 111_m7 | 12.12 | 21.0 | 20 | 22 | 7786 |

| t | On the board | Escaped | On the axes | On the planes off the axes | Off the planes | Parked |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3145728 | 0 | 0.556 | 0.444 | 0.000 | 0.000 |
| 2 | 3145728 | 0 | 0.556 | 0.247 | 0.198 | 0.000 |
| 3 | 3145728 | 0 | 0.106 | 0.598 | 0.296 | 0.000 |
| 5 | 3145728 | 0 | 0.007 | 0.182 | 0.811 | 0.000 |
| 10 | 3145728 | 0 | 0.034 | 0.281 | 0.684 | 0.001 |
| 20 | 3145728 | 0 | 0.008 | 0.148 | 0.837 | 0.007 |
| 30 | 3145728 | 0 | 0.003 | 0.086 | 0.891 | 0.020 |
| 40 | 3145728 | 0 | 0.001 | 0.053 | 0.907 | 0.038 |

### The field of the thing at rest on the open board (measured earlier), shell by shell (L1 shells; content per Node / J_r per Node)

| k | Nodes | t = 1 | t = 5 | t = 10 | t = 20 | t = 30 | t = 40 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1462250 / 0 | 19210 / 0 | 21746 / 0 | 4638 / 0 | 956 / 0 | 395 / 0 |
| 1 | 6 | 313379 / 178614 | 10153 / 2233 | 10946 / 216 | 2288 / 76 | 780 / 32 | 360 / 12 |
| 2 | 18 | 326632 / 210417 | 42046 / 5450 | 9622 / 1570 | 1877 / 217 | 672 / 58 | 287 / 10 |
| 3 | 38 | 155616 / 99772 | 36850 / 7414 | 11819 / 2508 | 1890 / 151 | 653 / 26 | 297 / 12 |
| 4 | 66 | 40312 / 18700 | 47936 / 23592 | 9140 / 1806 | 1684 / 187 | 613 / 51 | 284 / 17 |
| 5 | 102 | 28688 / 14126 | 30024 / 14173 | 11471 / 3960 | 1961 / 370 | 665 / 71 | 299 / 18 |
| 6 | 146 | 26824 / 14981 | 33872 / 19932 | 8694 / 2762 | 1725 / 254 | 602 / 57 | 281 / 15 |
| 7 | 198 | 18284 / 10111 | 23858 / 13648 | 10173 / 4141 | 2075 / 536 | 664 / 136 | 300 / 48 |
| 8 | 258 | 14116 / 8924 | 12646 / 6661 | 8122 / 3454 | 1796 / 410 | 606 / 85 | 282 / 28 |
| 9 | 326 | 10138 / 6345 | 10001 / 5370 | 9584 / 4757 | 2052 / 563 | 706 / 146 | 324 / 52 |
| 10 | 402 | 2125 / 1314 | 7698 / 4309 | 7854 / 3938 | 1789 / 542 | 632 / 138 | 291 / 47 |
| 11 | 486 | 1665 / 1031 | 6095 / 3431 | 8422 / 4660 | 1963 / 660 | 709 / 160 | 317 / 54 |
| 12 | 578 | 802 / 513 | 4537 / 2780 | 6885 / 3796 | 1708 / 594 | 650 / 162 | 306 / 54 |
| 13 | 678 | 615 / 392 | 3631 / 2215 | 4118 / 2252 | 1896 / 746 | 705 / 188 | 332 / 63 |
| 14 | 786 | 0 / 0 | 859 / 530 | 3391 / 1854 | 1683 / 671 | 641 / 178 | 317 / 65 |
| 15 | 902 | 0 / 0 | 700 / 431 | 2682 / 1528 | 1915 / 847 | 694 / 218 | 342 / 82 |
| 16 | 1026 | 0 / 0 | 332 / 207 | 2240 / 1277 | 1712 / 766 | 633 / 211 | 318 / 70 |

| t | On the board | Escaped | J_r per Node at k = 4 | 8 | 12 | Off the planes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 37748736 | 0 | 18700 | 8924 | 513 | 0.491 |
| 2 | 37748736 | 0 | 54232 | 7296 | 815 | 0.580 |
| 3 | 37748736 | 0 | 54358 | 7285 | 816 | 0.681 |
| 5 | 37748736 | 0 | 23592 | 6661 | 2780 | 0.832 |
| 10 | 37748736 | 0 | 1806 | 3454 | 3796 | 0.791 |
| 15 | 37748736 | 0 | 429 | 1285 | 1736 | 0.923 |
| 20 | 37606136 | 142600 | 187 | 410 | 594 | 0.869 |
| 25 | 36908514 | 840222 | 50 | 249 | 326 | 0.944 |
| 30 | 34801662 | 2947074 | 51 | 85 | 162 | 0.909 |
| 35 | 28765664 | 8983072 | 7 | 81 | 97 | 0.948 |
| 40 | 19372497 | 18376239 | 17 | 28 | 54 | 0.926 |

### The 1/r^2 fit per direction and the anisotropy (open board)

| Direction | Quantity | Slope (log-log over three radii) | Standard error | Value at r = 8 | At r = 12 | Signs |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| axis | cumulative_push_at_40 | -2.62 | 0.10 | 18303.5 | 6320.1 | [1, 1, 1] |
| axis | mean_push_2_21 | -3.72 | 0.15 | 430.2 | 95.2 | [1, 1, 1] |
| axis | inventory_j_2_21 | -2.95 | 0.11 | 566.2 | 171.0 | [1, 1, 1] |
| 110 | cumulative_push_at_40 | -2.40 | 0.52 | 58031.5 | 21926.2 | [1, 1, 1] |
| 110 | mean_push_2_21 | -3.16 | 0.93 | 1927.8 | 535.0 | [1, 1, 1] |
| 110 | inventory_j_2_21 | -2.03 | 0.31 | 3634.4 | 1597.3 | [1, 1, 1] |
| 111 | inventory_j_2_21 | -1.25 | 0.47 | 5626.1 | 3383.2 | [1, 1, 1] |

| Quantity | Axis / (111) at r = 8 | At r = 12 | Axis / (110) at r = 8 | At r = 12 |
| --- | ---: | ---: | ---: | ---: |
| cumulative_push_at_40 | - | - | 0.315 | 0.288 |
| inventory_j_2_21 | 0.101 | 0.051 | 0.156 | 0.107 |
| mean_push_2_21 | - | - | 0.223 | 0.178 |
