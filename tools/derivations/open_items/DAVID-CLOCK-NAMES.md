# The clock-and-gear names

David, 2026-10-27, 11:2x UTC, for the Boss (his task of 10:5x UTC).

## The word

The owner's word of 2026-10-27, 10:5x UTC, relayed by the Boss, in translation: "Replace, in the code and in every place, with clock words only... the documents too. The system is in fact one big clock with many gears."

## 1. The core table

These are the roots; section 3 derives every name from them.

| the law's name | clock name | what the code does |
|---|---|---|
| **The gear (a line)** |  |  |
| line | gear | one number on two wheels: the coarse wheel's notch and the fine wheel of `teeth` teeth |
| level | notch | the coarse wheel's position; `now` and `before` are its last two readings |
| remainder (rem, r) | fine (the fine tooth) | the fine wheel's tooth, 0 to teeth - 1: the fraction of the gear's stride |
| wall (w) | teeth | the fine wheel's teeth per notch |
| the carried division (divide) | carry | V = teeth (now - before) + fine, V' = V + pull; the next stride is V' div teeth and the fine tooth V' mod teeth |
| quotient | carries | the full turns of a total over the teeth |
| born (the half wall) | mid | the fine wheel set at its middle tooth: born at rest |
| mirror (w - 1 - r) | flip | the fine wheel read from its other end (the rewind's one rule) |
| exchange | reverse | a train's two readings exchanged and its hand reflected: the gears run backward |
| lay | advance | a count of notches added to a gear |
| write; the write remainder and wall | drive; drive fine and drive teeth | a source carried into a gear through its own drive wheel |
| direction | going | +1 forward, -1 backward |
| **The hand (a plane) and its train** |  |  |
| row | train | one family's gears at every clock, stepped by one gearing |
| shape (of a row) | gears | a train's count of gears |
| plane | hand | a train of two gears: one hand's two shadows |
| re, im | three, twelve | the hand's shadow on the three-o'clock line and on the twelve-o'clock line |
| pair (num, den) | ratio (pinion, rim) | the train's rest rate, cos omega_0 = pinion / rim |
| den | rim | the rim's teeth, the one denominator of every ratio |
| family | train | the law's word for a row's kind |
| the gap; gapped | the spring; sprung | a hand with a rest rate of its own |
| mass (D) | spring | the hairspring's stiffness, 12 (rim - pinion) rate^2 G^2 |
| emitter; light (the plane at the gap 0) | unsprung | the hand with no spring: no rest rate |
| carrier (shape 10) | regulator | the train whose time gear counts the clock's own ticks and rulers per great tick (its stretch), and so sets every rate at the clock |
| potential (shape 4) | offset | the train whose time gear and three odd gears set the offsets between neighbouring clocks |
| the walled row (shape 1, its own wall) | ratchet | the clock's offset count; its fine tooth at two teeth is the pawl |
| frame bit; frame sign | pawl | the ratchet's fine tooth: which way the clock's time runs; two clocks whose pawls differ read each other reflected |
| Rule (S, R, w, D) | gearing (hold, grips, teeth, spring) | Rule3's integers at a clock |
| reach R_ij | grip | how strongly a mesh grips: 2 pinion mesh_rate^2 Q |
| self coefficient S | hold | the gear's hold on its own notch |
| force F; arrivals | pull; pulls | what the meshes and the spring pull on a gear |
| current | lead | how far one clock's gear leads its neighbour's across a mesh |
| charge W (the Wronskian) | sweep | the area a hand's tick spans, signed by its sense |
| momentum | push | the leads summed over the great clock; what an unwind or an advance books |
| kick | impulse | the stride read at the mean teeth and impelled by the pull |
| share | wind | the hand's stored energy, counted in windings |
| unit; quantum | winding | the wind of one quantum, 3 key s |
| quantum_action (T) | key | one turn of the winding key: the quantum of action |
| take | unwind | the hand shortened by the least count whose wind falls by the windings tallied |
| the take's remainder (take_rem) | slack | the wind left at a clock after an unwind |
| booked; owed | tallied; due | the windings tallied for the fitted hands; what an end owes after its slack |
| draw | vernier | the fine teeth of the clock and its six neighbours read as digits |
| **The great clock** |  |  |
| board | great clock | the whole lattice of clocks |
| Node | clock | one small clock: its trains, its rate, its dial |
| Link | mesh | the meshing of two neighbouring clocks |
| Port | spoke | one of a clock's six meshing sides |
| interval | tick | the great clock's one tick |
| pace p_0 | rate | the clock's beats per tick, at or below the full rate |
| the Link's pace | mesh rate | the rate twice: the ruler |
| node_clock (Gamma) | full rate | the rate at the vacuum |
| content | load | the count of 1 / full-rate slowings on the clock's rate |
| volume X | stretch | how many of the clock's own ticks and rulers one great tick holds |
| proper count | dial | the clock's own dial: its rate summed over the ticks |
| frozen | stopped | a clock whose mesh rate rounds to 0 |
| horizon | standstill | the stopped clocks |
| the swap at the top | the turnover | a clock's gears reversed at its stretch's top |
| the bang | the swing | every clock's stretch at its top at once; the great clock runs back to its setting |
| the run back | the rewind | every gear run backward |
| the phase line | the standard | the reference clock: a hand turning 1 / full rate per act |
| amplitude X | standard length | the standard's hand length |
| orbit | circuit | the standard's turn, tabled |
| the Link's phase | offset | the angle between two clocks' offset counts, read on the standard |
| universe file | calibre | the clock's design: its integers and trains |
| world file | piece | one built clock: its calibre, its size, its ticks, its setting |
| seed | setting | the hands set at the start |
| record (the run's file) | chart | what the run writes |
| the close | the striking | the work after each tick: engagements, fittings and chimes |
| click (the act, and any of its events) | strike | the striking's act; any event it makes |
| meet | engage | two neighbouring clocks each holding a whole winding |
| birth | fitting | two new hands fitted at a mesh's two ends |
| child | fitted (hand) | a hand fitted at a birth |
| body | bob | a sprung hand standing at a clock |
| credit | chime | a bob that held a whole winding through one beat chimes; the unsprung hand pays one winding |
| the credit's frame | face | what the clock's face showed at the chime |
| the run back's frame | rewind note | what the striking keeps so the rewind can undo it |
| refused | jammed | an advance, an unwind or an engagement the law refuses by name |
| standing | wound | ticks a hand has held a whole winding |
| decoder | reckoner | the reader of a chime's face |
| merger | unspringing | two sprung hands at rest into unsprung windings |
| beat; the reader; carry | kept | already clock words |
| Rule3 | Rule3 (kept) | the owner's name; the rule of three is the arithmetic of gear ratios |

## 2. The picture, one correction, and the rules

### The picture

The great clock is the board, and its tick is the interval. Its clocks are the Nodes, each with its own rate (the pace) and its own dial (the proper count). A mesh is a Link between two neighbouring clocks. A train is a row: one family's gears at every clock, stepped by one gearing. A gear is a line. A hand is a plane: two gears, the hand's three-o'clock and twelve-o'clock shadows.

### One correction to the Boss's reading

The fine wheel's full turn does not carry the coarse wheel one step of position. It carries one notch into the coarse wheel's **stride**, its notches per tick:

- each tick, the coarse wheel repeats its last stride;
- the pull, counted in fine teeth, turns the fine wheel;
- each full turn of the fine wheel adds one notch to the stride.

In symbols: V = teeth (now - before) + fine, then V' = V + pull; the next stride is V' div teeth and the fine tooth is V' mod teeth (DAVID-CLOCKS.md section 1, checked there on 200,000 steps). So a gear is a flywheel with a carry, and Rule3 is the carry of a gear that keeps its stride.

### Rule3

I agree with the Boss: keep "Rule3". It is the owner's own name, and the rule of three is the arithmetic of gear ratios.

### The rules

- **One name per meaning.** A compound name is built from the roots: `link_pace_of` becomes `mesh_rate_of`, `refused_lay` becomes `jammed_advance`. Where one old word carries two meanings, each meaning gets its own name:
  - the calibre's rows become trains, while the reader's rows stay `rows` (a table's rows);
  - a Link's phase becomes an offset, while a packet's phase in the setting becomes an angle;
  - the moving packet's `wave` field becomes `stride`, while the light's wave form becomes `cycle`;
  - `frame` becomes `face` for a chime's frame, `pawl` for the frame bit, and `rewind_note` for the run back's frame;
  - the chart's `remainder` and `remainder_was` (the take's account) become `slack`, while a gear's remainder becomes `fine`;
  - the chart's `carry` (the drive's fine wheels) becomes `drive_fine`, while the rate table's `carry` stays (it is a carry);
  - handedness ("hand" in hand_of_birth, hands_of and one_hand) becomes `twist`, the engine's own word for it, so that "hand" means a plane alone.
- **Kept, with my judgment for the owner's word:**
  - plain words a clock does: now, before, start, top, count, run, read, state, time, beat, carry, recoil, tension, weight, drift, the reader;
  - mathematics: cosine, sine, angle, gradient, matrix, cross, dot, form, odd, even;
  - letters and counts: A, B, G, the axes, the sides;
  - Python's own names;
  - nature's names for the phenomena the gates read: light, charge, mass, energy, momentum, the horizon, the Aharonov-Bohm phase, force, velocity, CPT, the black body. A clock does not do the photoelectric effect; renamed, a gate would no longer say what it tests.
  - the law's clause tags (W-S3, G-S2, BH-S1 and so on): codes the thread's history cites.

  If the owner wants even these in clock words, they go last, with his word.
- **The same name on two objects with one meaning:** `w` on the clock and the chart, and `wall` on a gear and a gearing, all become `teeth`. No object holds both.

## 3. The full tables

There are 843 names: 35 modules, 9 classes, 291 module functions, 51 methods, 65 module constants and type aliases, 111 attributes, 174 keys of the chart, 28 keys of the files and 79 gates. The law's recurring titles follow them. They are read from the tree of f9e9b0d05 (ddb4ed84) and its three committed charts. "kept" means the name is unchanged.

### 3.1 Modules

| module | clock module |
|---|---|
| `__init__.py` | kept |
| `bangs.py` | `swings.py` |
| `board.py` | `great_clock.py` |
| `bodies.py` | `bobs.py` |
| `circle.py` | `rim.py` |
| `clicks.py` | `strikes.py` |
| `close.py` | `striking.py` |
| `decoder.py` | `reckoner.py` |
| `draw.py` | kept |
| `events.py` | kept |
| `gates.py` | kept |
| `gram.py` | `hands.py` |
| `interval.py` | `tick.py` |
| `links.py` | `meshes.py` |
| `merger.py` | `unspring.py` |
| `metric.py` | `regulation.py` |
| `node.py` | `clock.py` |
| `predicates.py` | kept |
| `readings.py` | kept |
| `rows.py` | `trains.py` |
| `run.py` | kept |
| `symmetries.py` | kept |
| `take.py` | `unwind.py` |
| `features/__init__.py` | kept |
| `features/volume/__init__.py` | `features/stretch/__init__.py` |
| `features/phase/__init__.py` | `features/standard/__init__.py` |
| `core/__init__.py` | kept |
| `core/acts.py` | kept |
| `core/paces.py` | `core/rates.py` |
| `core/ports.py` | `core/spokes.py` |
| `core/rule3.py` | kept |
| `loader/__init__.py` | `assembly/__init__.py` |
| `loader/seed.py` | `assembly/setting.py` |
| `loader/wave.py` | `assembly/cycle.py` |
| `loader/world.py` | `assembly/piece.py` |

### 3.2 Classes

| class | clock class |
|---|---|
| `Birth (close.py)` | `Fitting` |
| `Record (decoder.py)` | `Chart` |
| `Interval (interval.py)` | `Tick` |
| `Link (links.py)` | `Mesh` |
| `Node (node.py)` | `Clock` |
| `Row (rows.py)` | `Train` |
| `Line (rows.py)` | `Gear` |
| `Side (core/paces.py)` | `Side` |
| `Rule (core/rule3.py)` | `Gearing` |

### 3.3 Module functions, by module

**bangs.py**

| function | clock name |
|---|---|
| `marks` | kept |
| `returns_of` | kept |
| `volumes` | `stretches` |
| `bottoms_of` | kept |
| `tops_of` | kept |
| `state_of` | kept |
| `at_resolution` | kept |
| `exact_of` | kept |
| `recurring_bang` | `recurring_swing` |
| `tops` | kept |
| `returns` | kept |

**board.py**

| function | clock name |
|---|---|
| `contraction` | kept |
| `shortening` | kept |
| `lift_of` | kept |
| `acceleration` | kept |
| `era` | kept |
| `horizon` | `standstill` |
| `stopped_clock` | kept |
| `same_gates` | kept |
| `neighbours` | kept |
| `maxwell` | kept |
| `well` | kept |

**bodies.py**

| function | clock name |
|---|---|
| `bodies` | `bobs` |
| `frame_of` | `face_of` |

**circle.py**

| function | clock name |
|---|---|
| `witnesses` | kept |
| `is_prime` | kept |
| `divisor_of` | kept |
| `circle_of` | `rim_of` |

**clicks.py**

| function | clock name |
|---|---|
| `solved` | `reckoned` |
| `tracks_of` | kept |
| `species_track` | kept |
| `families` | kept |
| `leg_of` | kept |
| `mass_ratios` | kept |
| `one_click_floor` | `one_strike_floor` |
| `charge` | kept |
| `conservation_at_click` | `conservation_at_strike` |
| `halves` | kept |
| `dilation` | kept |
| `lengthening` | kept |
| `merger` | `unspring` |
| `horizon_radiates` | kept |

**close.py**

| function | clock name |
|---|---|
| `list_of` | kept |
| `meet` | `engage` |
| `refuse` | `jam` |
| `births` | `fittings` |
| `children` | `fitted` |
| `click` | `strike` |

**core/acts.py**

| function | clock name |
|---|---|
| `mirror` | `flip` |
| `born` | `mid` |
| `divide` | `carry` |
| `exchange` | `reverse` |
| `lay` | `advance` |

**core/paces.py**

| function | clock name |
|---|---|
| `rounded` | kept |
| `sine_den` | `sine_rim` |
| `sides` | kept |
| `certified` | kept |
| `side_of` | kept |
| `clock` | `rate` |
| `link_pace` | `mesh_rate` |
| `frozen_content` | `stopped_load` |
| `looked_up` | kept |
| `clock_of` | `rate_of` |
| `link_pace_of` | `mesh_rate_of` |

**core/ports.py**

| function | clock name |
|---|---|
| `shifted` | kept |
| `port_of` | `spoke_of` |
| `transverse` | kept |
| `wrap` | kept |
| `across` | kept |

**core/rule3.py**

| function | clock name |
|---|---|
| `wall_of` | `teeth_of` |
| `mass` | `spring` |
| `rule_integers` | `gearing` |
| `link_factor` | `mesh_factor` |
| `least_at` | kept |
| `flux_total` | `pull_total` |
| `rule3` | kept |
| `link_unit_of` | `mesh_unit_of` |
| `held_wall` | `held_teeth` |
| `held_numerator` | kept |
| `unit_of` | `winding_of` |
| `signed_quotient` | `signed_carries` |
| `half` | kept |
| `odd` | kept |
| `share_weight` | `wind_weight` |
| `quotient` | `carries` |
| `remainder` | kept |
| `lattice` | `pitch` |
| `balanced_pair` | `balanced_notches` |
| `largest_below` | kept |

**decoder.py**

| function | clock name |
|---|---|
| `kind_of` | kept |
| `cause_of` | kept |
| `unread_words` | kept |
| `shown` | kept |
| `quot` | `carries` |
| `cmp_rat` | kept |
| `carrier_levels` | `regulator_notches` |
| `solve` | `reckon` |
| `nearest` | kept |
| `middle` | kept |
| `decoded_credits` | `reckoned_chimes` |

**draw.py**

| function | clock name |
|---|---|
| `read_number` | `vernier` |

**events.py**

| function | clock name |
|---|---|
| `names_of` | kept |
| `label_of` | kept |
| `phenomenon_of` | kept |
| `eras_of` | kept |
| `first_interval` | `first_tick` |
| `first_shown` | kept |
| `wave_lay` | `cycle_setting` |
| `no_wave` | kept |
| `no_field` | kept |
| `no_conversion` | kept |
| `stub` | kept |
| `eighths_of` | kept |
| `era_row` | kept |
| `fast_expansion` | kept |
| `deceleration` | kept |
| `acceleration_in_clicks` | `acceleration_in_strikes` |

**features/phase/__init__.py**

| function | clock name |
|---|---|
| `unit` | `standard_rate` |
| `D` | `standard_teeth` |
| `K0` | `standard_pinion` |
| `half_wall` | `mid` |
| `seed` | `first_pair` |
| `act` | kept |
| `deviation` | kept |
| `floor` | `shortest_hand` |
| `carried` | kept |

**features/volume/__init__.py**

| function | clock name |
|---|---|
| `clock_zero` | `rate_zero` |
| `volume_of` | `stretch_of` |
| `level_of` | `load_of` |
| `searched_levels` | `searched_loads` |

**gates.py**

| function | clock name |
|---|---|
| `approach` | kept |
| `collisions` | kept |
| `free_fall` | kept |
| `light` | kept |
| `redshift` | kept |
| `delay` | kept |
| `arrow` | kept |
| `recoil` | kept |
| `constants` | kept |
| `conservations` | kept |
| `entropy` | kept |
| `restated` | kept |
| `verdicts` | kept |
| `gates` | kept |
| `main` | kept |

**gram.py**

| function | clock name |
|---|---|
| `identity` | kept |
| `rotation` | `quarter` |
| `conjugation` | `reflection` |
| `matvec` | kept |
| `products` | kept |
| `dot` | kept |
| `weighted` | kept |
| `form` | kept |
| `charge` | `sweep` |
| `conjugated` | `reflected` |
| `current` | `lead` |
| `share` | `wind` |
| `moving` | kept |
| `rest` | kept |
| `cosine_count` | kept |

**interval.py**

| function | clock name |
|---|---|
| `laid_on` | `advanced_on` |
| `run` | kept |

**links.py**

| function | clock name |
|---|---|
| `coupling_of` | kept |
| `cross` | kept |
| `even` | kept |
| `odd_sum` | kept |
| `frame` | `pawl` |
| `turn_pair` | `offset_pair` |
| `factors` | kept |
| `frames` | `pawls` |
| `centred_count` | kept |
| `phases` | `offsets` |
| `links_of` | `meshes_of` |
| `folded` | `skewed` |
| `link_wall` | `mesh_teeth` |
| `turned` | `through_mesh` |
| `gradient` | kept |
| `link_current` | `mesh_lead` |
| `row_current` | `train_lead` |
| `row_twist` | `train_twist` |
| `net_current` | `net_lead` |

**loader/seed.py**

| function | clock name |
|---|---|
| `lay_world` | `set_piece` |
| `raised_cosine` | kept |
| `offsets` | `places` |
| `envelope_of` | kept |
| `circle_point` | `rim_point` |
| `axis_pairs` | kept |
| `phase_of` | `angle_of` |
| `phases_of` | `angles_of` |
| `running_rotation` | kept |
| `rest_record` | `rest_hand` |
| `uniform_levels` | `even_notches` |
| `share_at_node` | `wind_at_clock` |
| `lay_uniform` | `set_even` |
| `packet_share` | `packet_wind` |
| `fitted` | kept |
| `wave_of` | `stride_of` |
| `lay_packet` | `set_packet` |

**loader/wave.py**

| function | clock name |
|---|---|
| `cycle_phases` | `cycle_angles` |
| `cycle_levels` | `cycle_notches` |
| `lay_cycle` | `set_cycle` |

**loader/world.py**

| function | clock name |
|---|---|
| `refused_keys` | kept |
| `read_world` | `check_piece` |
| `load_world` | `read_piece` |

**merger.py**

| function | clock name |
|---|---|
| `child_levels` | `fitted_notches` |
| `children_laid` | `fitted_advanced` |
| `light_levels` | `unsprung_notches` |
| `momentum_per_line` | `push_per_gear` |
| `walls_of` | `fitted_windings_of` |
| `share_fall` | `wind_fall` |
| `levels_at` | `notches_at` |
| `read_ends` | kept |
| `write_ends` | `unwind_ends` |
| `takes` | `unwinds` |
| `summed` | kept |
| `stood_at` | kept |
| `senses_at` | kept |

**metric.py**

| function | clock name |
|---|---|
| `stress_parts` | kept |
| `shear_parts` | kept |
| `tensor_parts` | kept |
| `net_flux` | `net_flow` |
| `rotation_of` | `rest_rate_of` |

**predicates.py**

| function | clock name |
|---|---|
| `unread` | kept |
| `hand_of_birth` | `twist_of_fitting` |
| `coulomb` | kept |
| `lifts` | kept |
| `confinement` | kept |
| `photoelectric` | kept |
| `exclusion` | kept |
| `exact_take` | `exact_unwind` |
| `decay` | kept |
| `two_slits` | kept |
| `bell` | kept |
| `ghz` | kept |
| `arrow_of_time` | kept |

**readings.py**

| function | clock name |
|---|---|
| `paces_of` | `rates_of` |
| `frozen_of` | `stopped_of` |
| `content` | `load` |
| `pair_angle` | `standard_angle` |
| `rule` | `gearing` |
| `rule_of` | `gearing_of` |
| `mean_wall` | `mean_teeth` |
| `floor` | `bottom` |

**rows.py**

| function | clock name |
|---|---|
| `zeros` | kept |
| `write_walls` | `drive_teeth` |
| `lines_of` | `gears_of` |
| `order_key` | kept |
| `rows_of` | `trains_of` |
| `row_of` | `train_of` |
| `walled_of` | `ratchet_of` |
| `records_of` | `hands_of` |

**run.py**

| function | clock name |
|---|---|
| `entry` | kept |
| `logged` | kept |
| `refused` | `jammed` |
| `birth` | `fitting` |
| `credit` | `chime` |
| `frame` | `rewind_note` |
| `bits_of` | kept |
| `arrays` | kept |
| `state` | kept |
| `census` | kept |
| `state_text` | kept |
| `state_hash` | kept |
| `ints` | kept |
| `packets_of` | kept |
| `reading` | kept |
| `node_lines` | `clock_lines` |
| `run_back` | `rewind` |
| `forward` | kept |
| `record` | `chart` |
| `main` | kept |

**symmetries.py**

| function | clock name |
|---|---|
| `region` | kept |
| `uniformity` | kept |
| `dark_matter` | kept |
| `lepton_number` | kept |
| `energy` | kept |
| `cpt` | kept |
| `hands_of` | `twists_of` |
| `matter_against_antimatter` | kept |
| `one_hand` | `one_twist` |
| `baryon_number` | kept |
| `bookings_of` | `tallies_of` |
| `momentum_booked` | kept |

**take.py**

| function | clock name |
|---|---|
| `neighbour` | kept |
| `frame_nodes` | `window_clocks` |
| `at_node` | `at_clock` |
| `fall_of` | kept |
| `lay` | `advance` |
| `momentum_of` | `push_of` |
| `move` | kept |
| `recoil` | kept |

### 3.4 Methods

| method | clock name |
|---|---|
| `Record.__init__ (decoder.py)` | `Chart.__init__` |
| `Record.to (decoder.py)` | `Chart.to` |
| `Record.index (decoder.py)` | `Chart.index` |
| `Record.node (decoder.py)` | `Chart.clock` |
| `Record.distance (decoder.py)` | `Chart.distance` |
| `Record.bodies_of (decoder.py)` | `Chart.bobs_of` |
| `Record.first_frozen (decoder.py)` | `Chart.first_stopped` |
| `Record.charges_of (decoder.py)` | `Chart.sweeps_of` |
| `Record.signs_of (decoder.py)` | `Chart.signs_of` |
| `Record.takes_of (decoder.py)` | `Chart.unwinds_of` |
| `Record.born_of (decoder.py)` | `Chart.fitted_of` |
| `Record.laid_at_nothing (decoder.py)` | `Chart.advanced_at_nothing` |
| `Record.circle (decoder.py)` | `Chart.rim` |
| `Interval.__init__ (interval.py)` | `Tick.__init__` |
| `Interval.at (interval.py)` | `Tick.at` |
| `Interval.lines (interval.py)` | `Tick.gears` |
| `Interval.ends (interval.py)` | `Tick.ends` |
| `Interval.readings (interval.py)` | `Tick.readings` |
| `Interval.kick (interval.py)` | `Tick.impulse` |
| `Interval.division (interval.py)` | `Tick.carry` |
| `Interval.lays (interval.py)` | `Tick.advances` |
| `Interval.swap (interval.py)` | `Tick.turnover` |
| `Interval.close (interval.py)` | `Tick.strike` |
| `Link.__init__ (links.py)` | `Mesh.__init__` |
| `Node.__init__ (node.py)` | `Clock.__init__` |
| `Node.start_state (node.py)` | `Clock.start_state` |
| `Node.ride_walls (node.py)` | `Clock.driven_teeth` |
| `Node.node_of (node.py)` | `Clock.clock_of` |
| `Node.row (node.py)` | `Clock.train` |
| `Node.emitter (node.py)` | `Clock.unsprung` |
| `Node.records (node.py)` | `Clock.hands` |
| `Node.turned_arrival (node.py)` | `Clock.offset_pull` |
| `Node.arrivals (node.py)` | `Clock.pulls` |
| `Node.rotate (node.py)` | `Clock.turn` |
| `Node.write (node.py)` | `Clock.drive` |
| `Node.act (node.py)` | `Clock.act` |
| `Node.restore (node.py)` | `Clock.restore` |
| `Node.rows (node.py)` | `Clock.trains` |
| `Node.set_rows (node.py)` | `Clock.set_trains` |
| `Node.all_lines (node.py)` | `Clock.all_gears` |
| `Node.exchange (node.py)` | `Clock.reverse` |
| `Node.swap (node.py)` | `Clock.turnover` |
| `Node.read_lines (node.py)` | `Clock.read_gears` |
| `Node.click (node.py)` | `Clock.strike` |
| `Node.step (node.py)` | `Clock.tick` |
| `Row.__init__ (rows.py)` | `Train.__init__` |
| `Row.gap (rows.py)` | `Train.spring` |
| `Line.__init__ (rows.py)` | `Gear.__init__` |
| `Line.copy (rows.py)` | `Gear.copy` |
| `Side.reach (core/paces.py)` | `Side.fill_to` |
| `Side.undecided (core/paces.py)` | `Side.undecided` |

### 3.5 Module constants and type aliases

| name | clock name |
|---|---|
| `BIRTHS (bangs.py)` | `FITTINGS` |
| `PULL (board.py)` | `LOAD_PULL` |
| `EVEN (circle.py)` | `EVEN` |
| `GAUSS (circle.py)` | `GAUSS` |
| `Decoded (clicks.py)` | `Reckoned` |
| `MIL (decoder.py)` | `MIL` |
| `HUNDRED (decoder.py)` | `HUNDRED` |
| `THOUSAND (decoder.py)` | `THOUSAND` |
| `FEW (decoder.py)` | `FEW` |
| `SPANS (decoder.py)` | `SPANS` |
| `HALF (decoder.py)` | `HALF` |
| `PAIR (decoder.py)` | `RATIO` |
| `THIRDS (decoder.py)` | `THIRDS` |
| `QUARTERS (decoder.py)` | `QUARTERS` |
| `LIFTS (decoder.py)` | `LIFTS` |
| `LISTED (decoder.py)` | `LISTED` |
| `SHORT_LIST (decoder.py)` | `SHORT_LIST` |
| `FOUR_LISTED (decoder.py)` | `FOUR_LISTED` |
| `MAX (decoder.py)` | `MAX` |
| `LEVELS_BACK (decoder.py)` | `NOTCHES_BACK` |
| `Rational (decoder.py)` | `Rational` |
| `NOT (decoder.py)` | `NOT` |
| `KINDS (decoder.py)` | `KINDS` |
| `RESTATED (decoder.py)` | `RESTATED` |
| `NAMES (events.py)` | `NAMES` |
| `UNREAD (events.py)` | `UNREAD` |
| `Row (gates.py)` | `Train` |
| `UNREAD_LIGHT (gates.py)` | `UNREAD_UNSPRUNG` |
| `RESTATED (gates.py)` | `RESTATED` |
| `TABLE (gates.py)` | `TABLE` |
| `Matrix (gram.py)` | `Matrix` |
| `Sources (metric.py)` | `Sources` |
| `COUNTS (node.py)` | `COUNTS` |
| `SETTINGS (predicates.py)` | `DIALS` |
| `CARRIER (rows.py)` | `REGULATOR` |
| `POTENTIAL (rows.py)` | `OFFSET` |
| `PLANE (rows.py)` | `HAND` |
| `POWER_TIME (rows.py)` | `POWER_TIME` |
| `POWER_AXIS (rows.py)` | `POWER_AXIS` |
| `MARKS (run.py)` | `MARKS` |
| `EARLY (run.py)` | `EARLY` |
| `REGIONS (symmetries.py)` | `REGIONS` |
| `EXPONENT (features/volume/__init__.py)` | `EXPONENT` |
| `LOW (features/volume/__init__.py)` | `LOW` |
| `LEVELS (features/volume/__init__.py)` | `LOADS` |
| `Line (features/phase/__init__.py)` | `Gear` |
| `Pair (features/phase/__init__.py)` | `Ratio` |
| `FLOORS (features/phase/__init__.py)` | `SHORTEST_HANDS` |
| `AXES (core/ports.py)` | `AXES` |
| `SIDES (core/ports.py)` | `SIDES` |
| `PORTS (core/ports.py)` | `SPOKES` |
| `PORT_SIDES (core/ports.py)` | `SPOKE_SIDES` |
| `arrival (core/ports.py)` | `pull` |
| `Reads (core/rule3.py)` | `Grips` |
| `HELD_WRITE_WEIGHT (core/rule3.py)` | `HELD_DRIVE_WEIGHT` |
| `UNIT_WEIGHT (core/rule3.py)` | `WINDING_WEIGHT` |
| `HALF_SPANS (loader/seed.py)` | `HALF_SPANS` |
| `FIELDS (loader/seed.py)` | `FIELDS` |
| `Pair (loader/seed.py)` | `Ratio` |
| `TURNS (loader/wave.py)` | `QUARTERS` |
| `QUARTER (loader/wave.py)` | `QUARTER` |
| `WORLD_KEYS (loader/world.py)` | `PIECE_KEYS` |
| `UNIVERSE_KEYS (loader/world.py)` | `CALIBRE_KEYS` |
| `INTEGERS (loader/world.py)` | `INTEGERS` |
| `ROW_KEYS (loader/world.py)` | `TRAIN_KEYS` |

### 3.6 Attributes (of the clock, the tick, the gear, the gearing, the chart, the side)

| attribute | clock name |
|---|---|
| `A` | kept |
| `B` | kept |
| `G` | kept |
| `NAMES` | kept |
| `NL` | kept |
| `T` | `key` |
| `X` | `standard_length` |
| `__dict__` | kept |
| `__slots__` | kept |
| `action` | kept |
| `beats` | kept |
| `before` | kept |
| `before_swap` | `before_turnover` |
| `bookings` | `tallies` |
| `by_index` | kept |
| `c` | `load` |
| `carrier` | `regulator` |
| `carry` | kept |
| `clocks` | `rates` |
| `closes` | `strikes` |
| `cosine` | kept |
| `count_max` | kept |
| `counts` | kept |
| `cphi` | `clocked_offset` |
| `credits` | `chimes` |
| `crossed` | kept |
| `cube` | kept |
| `den` | `rim` |
| `direction` | `going` |
| `drawn` | `vernier_read` |
| `drift` | kept |
| `emission` | `release` |
| `factor` | kept |
| `flux` | `flow` |
| `flux_lines` | `flow_gears` |
| `fold` | `skew` |
| `force` | `pull` |
| `forms` | kept |
| `frozen` | `stopped` |
| `gamma` | `full_rate` |
| `gapped` | `sprung` |
| `held` | kept |
| `interval` | `tick` |
| `intervals` | `ticks` |
| `kept` | kept |
| `kicked` | `impelled` |
| `last_dp` | `last_push` |
| `last_recoil` | kept |
| `lattices` | `pitches` |
| `line_name` | `gear_name` |
| `line_num` | `gear_pinion` |
| `line_pair` | `gear_ratio` |
| `links` | `meshes` |
| `links_at` | `meshes_at` |
| `log` | kept |
| `max_transient` | kept |
| `memo` | kept |
| `minus` | kept |
| `nodes` | `clocks` |
| `now` | kept |
| `orbit` | `circuit` |
| `orbit_half` | `circuit_half` |
| `orbit_lines` | `circuit_gears` |
| `out` | kept |
| `p0` | `rate` |
| `pair` | `ratio` |
| `pi` | `mesh_rate` |
| `plane_starts` | `hand_starts` |
| `planes` | `hands` |
| `plus` | kept |
| `potential` | `offset` |
| `proper` | `dial` |
| `reaches` | `grips` |
| `rec` | kept |
| `rem` | `fine` |
| `riders` | `driven` |
| `room` | kept |
| `rotations` | `rest_rates` |
| `rows_` | `trains_` |
| `scaled` | kept |
| `self_coefficient` | `hold` |
| `shape` | `gears` |
| `shear` | kept |
| `sine` | kept |
| `stack` | kept |
| `standing` | `wound` |
| `start_clock` | `start_rate` |
| `start_content` | `start_load` |
| `start_factors` | kept |
| `start_frames` | `start_pawls` |
| `start_lines` | `start_gears` |
| `start_odd` | kept |
| `start_phases` | `start_offsets` |
| `start_x` | `start_stretch` |
| `starts` | kept |
| `still` | kept |
| `take_rem` | `slack` |
| `top` | kept |
| `trace` | kept |
| `traceless` | kept |
| `turns` | `turnovers` |
| `unit_emitter` | `winding_unsprung` |
| `units` | `windings` |
| `w` | `teeth` |
| `wall` | `teeth` |
| `walled` | `ratchet` |
| `walls` | `train_teeth` |
| `where` | kept |
| `wr` | `dfine` |
| `wwall` | `dteeth` |
| `x_now` | `stretch_now` |

### 3.7 The chart's keys (the record)

**the chart's top keys**

| key | clock key |
|---|---|
| `G` | kept |
| `T` | `key` |
| `counts` | kept |
| `cube` | kept |
| `den` | `rim` |
| `gamma` | `full_rate` |
| `gapped` | `sprung` |
| `intervals` | `ticks` |
| `log` | kept |
| `nodes` | `clocks` |
| `planes` | `hands` |
| `rows` | kept |
| `run_back` | `rewind` |
| `turns` | `turnovers` |
| `universe` | `calibre` |
| `world` | `piece` |

**the counts**

| key | clock key |
|---|---|
| `births` | `fittings` |
| `body_clicks` | `bob_chimes` |
| `booked` | `tallied` |
| `laid` | `advanced` |
| `laid_back` | `returned` |
| `laid_nodes` | `advanced_clocks` |
| `met` | `engaged` |
| `refused_lay` | `jammed_advance` |
| `refused_orientation` | `jammed_orientation` |
| `refused_origin` | `jammed_origin` |
| `refused_sense` | `jammed_sense` |
| `refused_stop` | `jammed_stop` |
| `refused_twist` | `jammed_twist` |
| `taken` | `unwound` |
| `turns` | `turnovers` |

**a clock line (the record's Node line)**

| key | clock key |
|---|---|
| `X` | `stretch` |
| `content` | `load` |
| `current` | `lead` |
| `frozen` | `stopped` |
| `held` | kept |
| `i` | kept |
| `turned` | `turned_over` |

**the reader's rows (kept as rows: a table's rows)**

| key | clock key |
|---|---|
| `W abs sum` | `sweep abs sum` |
| `W total` | `sweep total` |
| `births` | `fittings` |
| `body_clicks` | `bob_chimes` |
| `content min/mean/max` | `load min/mean/max` |
| `gap-0 W abs max` | `unsprung sweep abs max` |
| `gap-0 velocity max` | `unsprung stride max` |
| `i` | kept |
| `integers` | kept |
| `link count max` | `mesh count max` |
| `links at the wall` | `meshes disengaged` |
| `max bits` | kept |
| `max transient bits` | kept |
| `milliseconds` | kept |
| `odd max bits` | kept |
| `orbit table` | `circuit table` |
| `packets (reader)` | kept |
| `planes energy bits` | `hands wind bits` |
| `refused` | `jammed` |
| `refused_lay` | `jammed_advance` |
| `refused_orientation` | `jammed_orientation` |
| `sign level max` | `sign notch max` |
| `tension min/max` | kept |
| `turns` | `turnovers` |
| `volume mean` | `stretch mean` |

**the rewind**

| key | clock key |
|---|---|
| `exact` | kept |
| `intervals` | `ticks` |

**the events**

| key | clock key |
|---|---|
| `refused` | `jammed` |
| `birth` | `fitting` |
| `credit` | `chime` |
| `lay` | `set` |

**the fields of the `refused` event**

| key | clock key |
|---|---|
| `cause` | kept |
| `charges` | `sweeps` |
| `children_at_one_node` | `fitted_at_one_clock` |
| `event` | kept |
| `fall` | kept |
| `i` | kept |
| `link` | `mesh` |
| `node` | `clock` |
| `owed` | `due` |
| `row` | `train` |
| `standing` | `wound` |
| `unit` | `winding` |
| `walls` | `teeth` |

**the fields of the `birth` event**

| key | clock key |
|---|---|
| `W_children` | `sweep_fitted` |
| `amplitude` | `hand_length` |
| `booked` | `tallied` |
| `carry` | `drive_fine` |
| `carry_ends` | `drive_fine_ends` |
| `carry_was` | `drive_fine_was` |
| `carry_was_ends` | `drive_fine_was_ends` |
| `children_at_node` | `fitted_at_clock` |
| `clock` | `rate` |
| `clock_ends` | `rate_ends` |
| `content` | `load` |
| `cross` | kept |
| `dP_lay` | `push_advance` |
| `dP_lay_ends` | `push_advance_ends` |
| `dP_take` | `push_unwind` |
| `event` | kept |
| `exact_lay` | `exact_advance` |
| `i` | kept |
| `levels` | `notches` |
| `line_pair` | `hand_ratio` |
| `minus` | kept |
| `node` | `clock` |
| `owed` | `due` |
| `plus` | kept |
| `proper` | `dial` |
| `recoil` | kept |
| `recoil_ends` | kept |
| `remainder` | `slack` |
| `remainder_was` | `slack_was` |
| `room` | kept |
| `senses` | kept |
| `stood` | kept |
| `taken` | `unwound` |
| `taken_line` | `unwound_gear` |
| `taken_now_was` | `unwound_now_was` |
| `taken_row` | `unwound_train` |
| `taker` | `unwinder` |
| `takes` | `unwinds` |

**the fields of the `credit` event**

| key | clock key |
|---|---|
| `beat` | kept |
| `booked` | `tallied` |
| `carry` | `drive_fine` |
| `carry_was` | `drive_fine_was` |
| `clock` | `rate` |
| `closes` | `strikes` |
| `content` | `load` |
| `dP_take` | `push_unwind` |
| `event` | kept |
| `frame` | `face` |
| `i` | kept |
| `levels` | `notches` |
| `line` | `gear` |
| `node` | `clock` |
| `owed` | `due` |
| `proper` | `dial` |
| `recoil` | kept |
| `remainder` | `slack` |
| `remainder_was` | `slack_was` |
| `sense` | kept |
| `sign_level` | `sign_notch` |
| `taken` | `unwound` |
| `taken_line` | `unwound_gear` |
| `taken_now_was` | `unwound_now_was` |
| `taker` | `unwinder` |
| `turned` | `turned_over` |

**the fields of the `lay` event**

| key | clock key |
|---|---|
| `amplitude` | `hand_length` |
| `event` | kept |
| `i` | kept |
| `line_pair` | `hand_ratio` |
| `node` | `clock` |
| `nodes` | `clocks` |
| `quanta` | `windings` |
| `sense` | kept |
| `share` | `wind` |
| `unit` | `winding` |
| `width` | kept |

**a chime's face (the credit's frame)**

| key | clock key |
|---|---|
| `X` | `stretch` |
| `factors` | kept |
| `frames` | `pawls` |
| `im_before` | `twelve_before` |
| `im_before_swap` | `twelve_before_turnover` |
| `im_neighbours_start` | `twelve_neighbours_start` |
| `im_now` | `twelve_now` |
| `im_start_before` | `twelve_start_before` |
| `im_start_now` | `twelve_start_now` |
| `odd` | kept |
| `phases` | `offsets` |
| `re_before` | `three_before` |
| `re_before_swap` | `three_before_turnover` |
| `re_neighbours_start` | `three_neighbours_start` |
| `re_now` | `three_now` |
| `re_start_before` | `three_start_before` |
| `re_start_now` | `three_start_now` |

### 3.8 The files' keys (the calibre and the piece; the setting's forms and fields)

| key | clock key |
|---|---|
| `amplitude` | `standard_length` |
| `at` | kept |
| `centre` | kept |
| `cz` | kept |
| `den` | `rim` |
| `hole` | `unfilled` |
| `integers` | kept |
| `intervals` | `ticks` |
| `lay` | `set` |
| `mirror` | `flip` |
| `node_clock` | `full_rate` |
| `p1` | kept |
| `pair` | `ratio` |
| `quanta` | `windings` |
| `quantum_action` | `key` |
| `row` | `train` |
| `rows` | `trains` |
| `sea` | `filled` |
| `seed` | `setting` |
| `sense` | kept |
| `shape` | `gears (a train) / size (the piece)` |
| `top` | kept |
| `trace` | kept |
| `universe` | `calibre` |
| `wall` | `teeth` |
| `wave` | `cycle (the form) / stride (a packet's field)` |
| `width` | kept |
| `world` | `piece` |

### 3.9 The gates of UNIVERSE24.md (nature's names for the phenomena kept)

| gate | clock name |
|---|---|
| `1 recurring bangs` | `1 recurring swings` |
| `1b the board tops, every Node turning at once` | `1b the great clock tops, every clock turning at once` |
| `1c the board returns to the seed` | `1c the great clock returns to the setting` |
| `2 the Links lengthening in the clicks` | `2 the meshes lengthening in the strikes` |
| `3 shortening then lengthening` | kept |
| `4 an era of matter` | kept |
| `5 acceleration (the lengthening quickens)` | kept |
| `6 contraction (the board, the reader's view)` | `6 contraction (the great clock, the reader's view)` |
| `7 light present and absorbed` | kept |
| `8 families forming (whole view)` | kept |
| `8b species over the track (one-place view: the middle solve of the body's track)` | `8b species over the track (one-place view: the middle reckoning of the bob's track)` |
| `9 collisions` | kept |
| `10 gravitational time dilation` | kept |
| `11 gravitational redshift` | kept |
| `12 light's delay or deflection` | kept |
| `13 free fall` | kept |
| `14 the horizon` | kept |
| `15 conservation at the click` | `15 conservation at the strike` |
| `16 uncertainty floor (one click)` | `16 uncertainty floor (one strike)` |
| `17 charge conservation` | kept |
| `18 the arrow of time` | kept |
| `19 mass ratios (parts per million)` | kept |
| `20 the twist's 24 and 24` | kept |
| `21 the C of the birth` | `21 the C of the fitting` |
| `22 Coulomb's sign` | kept |
| `23 the momentum across the click` | `23 the momentum across the strike` |
| `24 the merger (a pair into light)` | `24 the unspringing (a pair into light)` |
| `25 the entropy of the clicks rising` | `25 the entropy of the strikes rising` |
| `26 the three lifts born and their beats' ratios` | kept |
| `27 confinement (no third alone)` | kept |
| `28 the conversion list` | kept |
| `29 the redshift of light` | kept |
| `30 the dilation` | kept |
| `31 the deflection and the Shapiro delay` | kept |
| `32 the perihelion` | kept |
| `33 free fall by the tail` | kept |
| `34 the horizon and the stopped clock` | kept |
| `35 frame dragging for matter, light not dragged` | kept |
| `36 the shears as waves` | kept |
| `37 Maxwell's one Link per interval` | `37 Maxwell's one mesh per tick` |
| `38 the Aharonov-Bohm phase` | kept |
| `39 the Zeeman and Stark shifts` | kept |
| `40 the photoelectric click` | `40 the photoelectric strike` |
| `41 the spinor's two beats` | kept |
| `42 the split along the gradient (Stern-Gerlach)` | kept |
| `43 the exclusion` | kept |
| `44 the moving lay's velocity against k` | `44 the moving setting's velocity against k` |
| `45 the bodies' well, binding and collapse` | `45 the bobs' well, binding and collapse` |
| `46 the bangs recurring with the same gates` | `46 the swings recurring with the same gates` |
| `47 the exact take` | `47 the exact unwind` |
| `48 the black body` | kept |
| `49 the exponential decay` | kept |
| `50 light on light` | kept |
| `51 the Casimir force and the running alpha` | kept |
| `52 the neutrino` | kept |
| `53 a fast packet binds at its lay` | `53 a fast packet binds at its setting` |
| `54 scattering, two packets through each other` | kept |
| `55 the two slits` | kept |
| `56 Bell` | kept |
| `57 GHZ` | kept |
| `58 the fast expansion after the bang` | `58 the fast expansion after the swing` |
| `59 the deceleration in the clicks` | `59 the deceleration in the strikes` |
| `60 the acceleration in the clicks` | `60 the acceleration in the strikes` |
| `61 the horizon radiates` | kept |
| `62 the arrow of time in the clicks` | `62 the arrow of time in the strikes` |
| `63 the uniformity in the clicks` | `63 the uniformity in the strikes` |
| `64 dark matter in kind` | kept |
| `65 the lepton number` | kept |
| `66 the energy in the clicks` | `66 the energy in the strikes` |
| `67 CPT in the clicks` | `67 CPT in the strikes` |
| `68 matter against antimatter` | kept |
| `69 the neutrino's one hand` | kept |
| `70 the baryon number` | kept |
| `71 the momentum booked on the Link` | `71 the momentum tallied on the mesh` |
| `the conservations in the clicks` | `the conservations in the strikes` |
| `the three constants` | kept |
| `the decoder` | `the reckoner` |
| `events` | kept |
| `the eras` | kept |

### 3.10 The law's recurring titles (ALGEBRA.md, cited twice or more)

| title | clock title |
|---|---|
| `Alignment, 2026-10-25` | kept |
| `The click writes on the lattice` | `The strike writes on the lattice` |
| `The Node` | `The Clock` |
| `The paces compose` | `The rates compose` |
| `The two rows` | `The two trains` |
| `The nuclear holder` | kept |
| `The law's alpha is a coefficient of the file` | kept |
| `The conversion` | kept |
| `Every row reads the content` | `Every train reads the load` |
| `The same clock and the same ruler for every act` | kept |
| `The conventions and the units` | kept |
| `The clock family on the Ports` | `The clock train on the Ports` |
| `The carried momentum` | kept |
| `A body and the light it reads keep one energy` | `A bob and the light it reads keep one energy` |
| `The atom is a bound body of the holder of the sign` | `The atom is a bound bob of the holder of the sign` |
| `The sign holder rotates the two-part record` | `The sign holder rotates the two-part hand` |
| `The clock is the Node's, the tension is the Link's` | `The clock is the Clock's, the tension is the Mesh's` |
| `The write per proper volume and per proper interval` | `The drive per proper volume and per proper tick` |
| `The tension` | kept |
| `The two branches` | kept |
| `The vacuum content` | `The vacuum load` |
| `The clusters' cosmology` | kept |
| `The odd line's source is the sign's own current` | `The odd gear's source is the sign's own current` |
| `The compact pixel under the composed paces` | `The compact pixel under the composed rates` |
| `Only clicks against clicks` | `Only strikes against strikes` |
| `The units are the electron's and the share's ceiling is the highest photon energy` | `The units are the electron's and the wind's ceiling is the highest photon energy` |
| `The sign is the rotation sense` | kept |
| `The seed is a list of lays` | `The setting is a list of settings` |
| `Matter's birth from light` | `Matter's fitting from light` |
| `The three shapes` | kept |
| `The two-mode line` | `The two-mode gear` |
| `The stress's trace is the time line's` | `The stress's trace is the time gear's` |
| `The click's read of the board` | `The strike's read of the great clock` |
| `The nucleus` | kept |
| `The integer budget of a derived row` | `The integer budget of a derived train` |
| `The mass is one integer` | kept |
| `Every family has a dimension` | `Every train has a dimension` |
| `The strong force` | kept |
| `The final unification` | kept |
| `What a body reads` | `What a bob reads` |
| `The three masses of a body` | `The three masses of a bob` |
| `No click names a Node` | `No strike names a Clock` |
| `The board's interval is no observable` | `The great clock's tick is no observable` |
| `The cube's symmetry` | kept |
| `The swap at the top` | kept |
| `The guard` | kept |
| `The bound body is one Node` | `The bound bob is one Clock` |
| `The turn per proper interval` | `The turn per proper tick` |
| `The interval's dependency radius is one Link` | `The tick's dependency radius is one Mesh` |
| `The vacuum's row steps at the divisor 1` | `The vacuum's train steps at the divisor 1` |
| `The click is the detector's report` | `The strike is the detector's report` |
| `Only local` | kept |
| `The inverse` | kept |
| `Light is born by the write` | `Light is born by the drive` |
| `Spin, closed for the paper as a route` | kept |
| `The click's unit: the whole of a click is the detector's own transition` | `The strike's unit: the whole of a strike is the detector's own transition` |
| `The share's change is the currents` | `The wind's change is the currents` |
| `The pair family and Bell's gate` | `The pair train and Bell's gate` |
| `Locality is never broken` | kept |
| `Gamma is not constant` | kept |
| `No family is declared` | `No train is declared` |
| `The closed lattice has no rest` | kept |
| `The frozen Node has no share` | `The frozen Clock has no wind` |
| `The lattice's frame is read by gravity alone, and its carrier is a pair of Links` | `The lattice's frame is read by gravity alone, and its regulator is a pair of Meshes` |
| `A family's write is one act` | `A train's drive is one act` |
| `The lattice constants` | kept |
| `No record reads its own write of the sign` | `No hand reads its own drive of the sign` |
| `Nature's numbers enter the board only as clicks` | `Nature's numbers enter the great clock only as strikes` |
| `The wall is one` | `The teeth is one` |
| `The way to a solution` | kept |
| `One function steps a line` | `One function steps a gear` |
| `The holders are derived` | kept |
| `The charge of a plane is bounded by its share` | `The charge of a plane is bounded by its wind` |
| `The decay is the click forward` | `The decay is the strike forward` |
| `The count is the record's share` | `The count is the hand's wind` |
| `The click's algebra beyond the law` | `The strike's algebra beyond the law` |
| `The lattice momentum` | kept |
| `Every body is bound; records may be free` | `Every bob is bound; records may be free` |
| `The mean's velocity is the content's` | `The mean's velocity is the load's` |
| `The motion of gravity's row is a hill at the symmetry's weight` | `The motion of gravity's train is a hill at the symmetry's weight` |
| `What the lattice conserves` | kept |
| `The click is the meeting of the future with the past` | `The strike is the meeting of the future with the past` |
| `Proof` | kept |
| `The start` | kept |
| `The band at a pace` | `The band at a rate` |
| `The share's sign and the credit's floor` | `The wind's sign and the credit's floor` |
| `The meeting's identity` | kept |
| `The lay is a standing state of the step` | `The setting is a standing state of the step` |
| `The click's parity` | `The strike's parity` |
| `The third and the colours, closed as absent` | kept |
| `The reads are derived` | kept |
| `The one form` | kept |
| `The uniform mode carried by Rule3's own k = 0 line` | `The uniform mode carried by Rule3's own k = 0 gear` |
| `The form's own clock` | kept |
| `The GHZ gate` | kept |
| `The floor` | kept |
| `The NodeDetector is one declaration kind for every world` | kept |
| `Computed` | kept |
| `The remainders' walk accumulates on a bounded board` | `The remainders' walk accumulates on a bounded great clock` |
| `The click's algebraic definition` | `The strike's algebraic definition` |
| `The record's parts are its particles` | `The hand's parts are its particles` |
| `The exact bands` | kept |
| `The click joins and parts` | `The strike joins and parts` |
| `The hierarchy is recursive` | kept |
| `The fork, decided` | kept |
| `No write from outside Rule3 wakes either double root of the massless row` | `No drive from outside Rule3 wakes either double root of the massless train` |
| `The share and the wall` | `The wind and the teeth` |
| `The nucleon is a compact body of its family` | `The nucleon is a compact bob of its train` |
| `Nothing that is not Rule3 remains` | kept |
| `The dense record's absorption is read in the books` | `The dense hand's absorption is read in the books` |
| `The meeting's reading` | kept |
| `The algebra of the exclusivity` | kept |
| `Rule3 is not changed; it is used to solve problems` | kept |
| `Every Node's remainder is born at the half wall` | `Every Clock's fine tooth is born at the half teeth` |
| `The width is derived` | kept |
| `The Lorentz form on the sign holder's four lines` | `The Lorentz form on the sign holder's four gears` |
| `The volume holder is massless, derived from den` | kept |
| `Confinement is the click's` | `Confinement is the strike's` |
| `The rule's own universe` | kept |
| `The board reads itself` | `The great clock reads itself` |
| `The fine structure is Klein-Gordon's` | kept |
| `Dark matter in kind is a theorem of the lines` | `Dark matter in kind is a theorem of the gears` |
| `The algebra of clusters` | kept |
| `The three roots of the gaps` | kept |
| `The one Node` | `The one Clock` |
| `The flux form of Rule3` | kept |
| `The Link is twice` | `The Mesh is twice` |
| `Theorem` | kept |
| `The mass defect is the form's fall at a kept count` | kept |
| `What a click reads of a quantum` | `What a strike reads of a quantum` |
| `The questions on the law's own formulas, with their answers` | kept |
| `The one universe file since the merge of 2026-10-24` | kept |
| `The universe holds the lines' pairs as numbers` | kept |
| `The families from the rule` | kept |
| `The volume holder's rest is the clock's one level` | `The volume holder's rest is the clock's one notch` |
| `The symmetric hill` | kept |
| `The off-diagonal parts where declared` | kept |
| `The generations` | kept |
| `The mass read at the content` | `The mass read at the load` |
| `The lightest point is derived` | kept |
| `The one universe` | kept |
| `The board is a torus` | `The great clock is a torus` |
| `What nature splits is a body` | `What nature splits is a bob` |
| `The nucleus's reading, the more generic: the law's five lines` | `The nucleus's reading, the more generic: the law's five gears` |
| `The factor carried` | kept |
| `The 2 Larmor fork under the Lorentz form` | kept |
| `Clicks go only forward; the backward run is exact` | `Strikes go only forward; the backward run is exact` |
| `The clock near matter` | kept |
| `The cube's slowing and the tick's bound` | kept |
| `The static frame and the two gauges` | kept |
| `The flux form on a turned or folded Link` | `The flux form on a turned or folded Mesh` |
| `Gravity's flux and the enclosed write` | `Gravity's flux and the enclosed drive` |
| `The emission of a bound record is the click's act of the taker` | `The emission of a bound hand is the strike's act of the taker` |
| `The uncertainty relation is the detector's three declarations` | kept |
| `The count's unit` | kept |
| `What produces a click is not known` | `What produces a strike is not known` |
| `The births' book` | kept |
| `The NodeDetector in six steps` | kept |
| `What clicks` | `What strikes` |
| `The click formulas` | `The strike formulas` |
| `The stress is the Links'` | kept |
| `The traceless tension` | kept |
| `The fall` | kept |
| `The reach of a held family is its pair` | `The reach of a held train is its pair` |
| `The law's own formulas` | kept |
| `No free number but the mass` | kept |
| `Enter them carefully, as derived hypotheses` | kept |
| `The two kinds of act` | kept |
| `Tsirelson's bound is a theorem of the credit's form` | kept |
| `The constants of the universe` | kept |
| `The law in one line` | `The law in one gear` |
| `The click is the meeting` | `The strike is the meeting` |
| `A body is laid over its packet` | `A bob is laid over its packet` |
| `The unbounded board` | `The unbounded great clock` |
| `The uniform seed is a lay` | `The uniform setting is a setting` |
| `The birth's selector is the lifts' draw within the energy` | `The fitting's selector is the lifts' draw within the energy` |
| `The line of a record` | `The gear of a hand` |
| `A pair's numerator may be negative` | kept |
| `The lay across parts` | `The setting across parts` |
| `The bilinears of one pair` | kept |
| `The constants` | kept |
| `The den enlarged as content` | `The den enlarged as load` |
| `The click's momentum on the board` | `The strike's momentum on the great clock` |
| `The presence effect of the click as defined` | `The presence effect of the strike as defined` |
| `The share rule` | `The wind rule` |
| `One world, defined to the bit, compared clicks to clicks` | `One world, defined to the bit, compared strikes to strikes` |
| `The properties of the lattice` | kept |
| `The pixel's representation` | kept |
| `The observer is a cluster` | kept |
| `The count is read through both holders` | kept |
| `The count is the baryon number` | kept |
| `Light is born by the write; no quantum changes family at a crossing` | `Light is born by the drive; no quantum changes train at a crossing` |
| `At a Node there is Rule3 and nothing else; nothing on the board draws` | `At a Clock there is Rule3 and nothing else; nothing on the great clock draws` |
| `A static sign row is the electric potential in the temporal gauge` | `A static sign train is the electric potential in the temporal gauge` |
| `The shear's momentum is carried at the volume's wall` | `The shear's momentum is carried at the volume's teeth` |
| `The moving pattern's clock` | kept |
| `The clocks shift alike` | kept |
| `The digits' budget` | kept |
| `A collapse ends in a frozen clock` | kept |
| `The two-way reading` | kept |
| `The anti-body` | `The anti-bob` |
| `The count on the board` | `The count on the great clock` |
| `The paces' own change moves the share with no current` | `The paces' own change moves the wind with no current` |
| `The dark board and the standing body` | `The dark great clock and the standing bob` |
| `The Ports' three readings` | kept |
| `The two slits' variants under the click's read` | `The two slits' variants under the strike's read` |
| `No act and no reading of the Node names a row` | `No act and no reading of the Clock names a train` |
| `Derived` | kept |
| `The start's source is the form the held write writes` | `The start's source is the form the held drive writes` |
| `The binding energy gravitates` | kept |
| `The four lines of the body` | `The four gears of the bob` |
| `The cooling` | kept |
| `The calibration series` | kept |
| `The two columns of the potential` | kept |
| `The count's line and the sense's line leave the law` | `The count's gear and the sense's gear leave the law` |
| `The Node steps on its own clock; the board at equal ticks is one` | `The Clock steps on its own clock; the great clock at equal ticks is one` |
| `The swap keeps the charge` | kept |
| `SL-S2, the merger is the birth read at -1` | `SL-S2, the unspringing is the fitting read at -1` |
| `SL-S3, light laid into light` | kept |
| `One point and one beat` | kept |
| `CS6-S1, the retrace theorem` | kept |
| `The den of the record` | `The den of the hand` |
| `The exact bands are exact only in the vacuum` | kept |
| `The colours are the three axes` | kept |
| `The tail of a body` | `The tail of a bob` |
| `What is open` | kept |
| `The staggering is exact` | kept |
| `The screen is a cluster` | kept |
| `The three distances are the rule's` | kept |
| `The couplings are at the edge` | kept |
| `The wavelength is the giver's beat` | kept |
| `The hill's weight is the write's mix` | `The hill's weight is the drive's mix` |
| `The sign side of the exponent` | kept |
| `The width bounds A by the least of the two` | kept |
| `The electron needs no band of its own` | kept |
| `The electron is one quantum` | kept |
| `The generator is Rule3` | kept |
| `Pauli at the lay without a weight` | `Pauli at the setting without a weight` |
| `The points of the lattice are the Node and the Event` | `The points of the lattice are the Clock and the Event` |
| `The free part` | kept |
| `The tick is the count of rounds` | kept |
| `The clock once and the Link twice` | `The clock once and the Mesh twice` |
| `The fork of 46 is decided` | kept |
| `The bound` | kept |
| `The redshift` | kept |
| `Einstein lives in the clicks of bound bodies, and the board is never measured` | `Einstein lives in the strikes of bound bobs, and the great clock is never measured` |
| `The charge is the record's, not the count's` | `The charge is the hand's, not the count's` |
| `The second level's amplitude is a count of its own` | `The second notch's amplitude is a count of its own` |
| `The push on a moving record` | `The push on a moving hand` |
| `The mass is the well` | kept |
| `The uncertainty relation is the taker's three readings` | kept |
| `The uncertainty principle is the record's and the click's` | `The uncertainty principle is the hand's and the strike's` |
| `The forces as the law holds them` | kept |
| `The booking is the frame's` | kept |
| `The digits' base and a total's factors` | kept |
| `Every formula is fenced` | kept |
| `A pixel` | kept |
| `The cloud look` | kept |
| `The lay and the wall` | `The setting and the teeth` |
| `The hill holds the body` | `The hill holds the bob` |
| `The photon channel is the write` | `The photon channel is the drive` |
| `The number of quanta a cloud gives to settle` | kept |
| `The field at rest, the start of a world` | kept |
| `The packet lay` | `The packet setting` |
| `The lay's before level is the band's own` | `The setting's before notch is the band's own` |
| `The law changes and the engine does not` | kept |
| `The integer-exact constructions are the preferred ones` | kept |
| `Gamma and T` | kept |
| `The measured speed` | kept |
| `No waves on the event board` | `No waves on the event great clock` |
| `One test world and one gate` | kept |
| `There is no sense` | kept |
| `The lattice's frame, the second residue` | kept |
| `The moving clock` | kept |
| `The pair of two bound records` | kept |
| `Only a click moves a quantum between families` | `Only a strike moves a quantum between families` |
| `The rotation's first-order line` | `The rotation's first-order gear` |
| `The pressure's write in the time line` | `The pressure's drive in the time gear` |
| `The horizon` | kept |
| `The charge written is the Wronskian over T div 2 for every reader` | kept |
| `The exact answer on the clock` | kept |
| `The universe expands` | kept |
| `Go for it: the principle C` | kept |

## 4. The checks

- Across the 843 names, no two collide inside one module, one class or one section of the chart.
- None is a Python keyword, soft keyword or builtin; `orbit`, whose first clock word was a builtin, became `circuit`.
- The one name shared across objects is `teeth`, for one meaning: `w` and `wall`.
- The rename changes no number. Every integer of the state, the charts' values, the run back and the gates' verdicts stand. Only names move.

## 5. The stages of the build

Each stage is bit for bit in physics.

### (1) The identifiers and docstrings of src

Rename the identifiers and docstrings of src, together with every test and tool that names them, and leave the chart's keys untouched: the writer keeps emitting the old keys through one key table in run.py.

The checks:

- the three committed charts regenerate SAME, key by key, with their hashes;
- the readings stay byte for byte;
- the run back is 20 of 20;
- the full check exits 0.

One risk: longer names can re-wrap lines, and a file of src beyond the code shape's limits may not grow in lines. Where a file is at its limit, keep the new name no longer than the old one, or give that file room by name.

### (2) The chart's and the files' keys, with the readers

Rename the chart's keys and the files' keys (section 3.7 and 3.8), together with every reader: the gates, the reckoner, the events, the predicates, the symmetries, the great clock's gates, the strikes, the swings, and the tools.

- The committed charts are regenerated.
- The world and universe files are converted.
- One converter takes an old chart to a new one, with section 3.7 as its map, for the Reader's folders.

The check: the converter applied to every old committed chart equals the new chart, key by key and value by value.

### (3) The documents and the law's text, by the Scribe

ENGINE.md, UNIVERSE24.md (section 3.9), ALGEBRA.md (section 3.10 and the core table for the rest) and the CHANGELOG are re-cut on the owner's word, which is given. A history clause that quotes an old name keeps the quote and dates it.

A document alone: no code and no test change.
