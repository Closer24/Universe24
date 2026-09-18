### The books per bit

| World | Ticks | World line balanced | Real line | Shadow line | `real_conserved` | Shadows at start | At tick 40 | Escaped | Runner s |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `pulse` | 40 | every tick | every tick | every tick | every tick | 3145728 | 3145728 | 0 | 210.9 |
| `standing` | 40 | every tick | every tick | every tick | every tick | 37748736 | 19372497 | 18376239 | 114.3 |
| `probe_axis_r4` | 40 | every tick | every tick | every tick | every tick | 37733842 | 19453575 | 18280267 | 1250.8 |
| `probe_axis_r8` | 40 | every tick | every tick | every tick | every tick | 37748734 | 19392959 | 18355775 | 494.4 |
| `probe_axis_r12` | 40 | every tick | every tick | every tick | every tick | 37748736 | 19383998 | 18364738 | 278.7 |
| `probe_110_m3` | 40 | every tick | every tick | every tick | every tick | 37716989 | 19517291 | 18199698 | 1328.7 |
| `probe_110_m6` | 40 | every tick | every tick | every tick | every tick | 37748736 | 19457929 | 18290807 | 594.2 |
| `probe_110_m9` | 40 | every tick | every tick | every tick | every tick | 37748736 | 19402443 | 18346293 | 265.4 |

### The test things: the pushed amount per interval and the inventory's J at the same Node

| Probe | r | Cumulative radial push at 40 | At 30 | Mean per interval, ticks 2-21 | 2-11 | 12-21 | 22-31 | 32-40 | Inventory J_r, mean 2-21 (`standing`) | Content per Node at 2 / 21 / 40 | Intervals waited | Body's momentum at 40 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `axis_r4` | 4.00 | 115328 | 115787 | 5868.1 | 8538.1 | 3198.1 | -107.9 | -106.1 | - | - / - / - | 39 | [-1587, 6, 5] |
| `axis_r8` | 8.00 | 17204 | 9190 | 392.0 | 153.9 | 630.1 | 399.9 | 596.1 | - | - / - / - | 39 | [0, 0, 0] |
| `axis_r12` | 12.00 | 6572 | 6295 | 101.0 | 30.1 | 171.8 | 431.9 | 26.0 | - | - / - / - | 37 | [0, 0, 0] |
| `110_m3` | 4.24 | 235703 | 234571 | 11527.1 | 16474.5 | 6579.8 | 395.0 | 134.5 | - | - / - / - | 39 | [-6044, -5618, -2] |
| `110_m6` | 8.49 | 69914 | 68845 | 2879.9 | 1350.7 | 4409.2 | 1190.7 | 45.3 | - | - / - / - | 39 | [-449, -391, -3] |
| `110_m9` | 12.73 | 15481 | 11006 | 306.6 | 125.7 | 487.4 | 602.9 | 369.0 | - | - / - / - | 35 | [0, 0, 0] |

### The 1/r^2 fit per direction and the anisotropy

| Direction | Quantity | Slope (log-log over three radii) | Standard error | Value at r = 8 | At r = 12 |
| --- | --- | ---: | ---: | ---: | ---: |
| axis | cumulative_push_at_40 | -2.62 | 0.10 | 18303.5 | 6320.1 |
| axis | mean_push_2_21 | -3.72 | 0.15 | 430.2 | 95.2 |
| 110 | cumulative_push_at_40 | -2.40 | 0.52 | 58031.5 | 21926.2 |
| 110 | mean_push_2_21 | -3.16 | 0.93 | 1927.8 | 535.0 |

| Quantity | Axis / (111) at r = 8 | At r = 12 | Axis / (110) at r = 8 | At r = 12 |
| --- | ---: | ---: | ---: | ---: |
| cumulative_push_at_40 | - | - | 0.315 | 0.288 |
| mean_push_2_21 | - | - | 0.223 | 0.178 |
| inventory_j_2_21 | - | - | - | - |
