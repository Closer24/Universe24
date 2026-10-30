# The order-free strike, spelled

David, 2026-10-28, 02:3x UTC, for the Boss (his asks of 02:1x UTC: the jam's decision on the start board, and where two writes that both pass on the start board but over-draw a shared light book put the excess; the owner's word of 02:0x UTC through the Boss: "the 24 is the target"). Read on 97e5b3fd6's striking.py, unspring.py and bobs.py, with each count a harness (DAVID-THE-ORDER-FREE-STRIKE_CHECKS.txt). No src touched.

## Where the strike reads the live board

1. **The jam already reads the start board.** The lay's check reads the start winds (the fitted hand standing at the - end, its twin at the + end), and the crowd is a count over every kept fitting. Neither reads an order.
2. **The unwind reads the live board.** The light's take picks its gear, its count and its stop on the window's wind and the slack as the earlier unwinds of the striking left them (fall_of, read_ends). A sprung end re-reads its winds after every unspringing's write. The unspringing's draw is read between its reads and its writes, and its push cross term is the live push less the start's. The lay's cross term reads the board after the lay.
3. **The fittings run in the clocks' sorted order and the chimes in the index order**, so each read takes in the writes before it. On the bang's first 100 ticks, 5,319 of 17,156 end reads see a window an earlier unwind of the same striking wrote, and 1,012 of the 6,853 stops fall on such a window (52 and 267 stops on the chiral and the hole settings).

## The letter

1. **Every read on the start board:** each take's gear (the largest now^2 - before^2), its count (the least that pays its due over its window), its stop (the full move paying less), each sprung end's fall, the draw, and each due with the slack at the tick's start.
2. **One take per clock and unwound hand:** the dues at one clock are summed into one take. The birth's case already does this for every fitting at one clock; it extends to the chimes of several hands at one clock.
3. **Any other two writes of one gear at one clock jam by name, all of them:** two fitted children of one hand at one clock (the crowd, as built), and two unwinds of one child (two unspringings at one end).
4. **A clock fitted in the striking does not chime** (as built), and the fitted set is read from 1 to 3.
5. **Every write lands on its own gear:** each take moves its own clock's gear by the count it read, and each lay advances its own ends. So the writes commute.
6. **Each act reads its own cross terms on the start board with its own writes alone:** the unspringing's two ends (wind_cross), its push with its own other end unwound (at the fitting's own clock, as e910698f9 books it), and the lay's two windows.

## The book of two writes over one window

1. **Two takes cannot over-draw a gear.** Takes at two clocks move two gears, and two at one clock are one take. Each count stays within its gear's distance to its before, read on the start board.
2. **What they share is the wind of the clocks between them.** A take's window is its clock and six neighbours. At a clock inside both windows, the board's fall differs from the two falls read alone by their cross term.
3. **Each clock books its own part of that cross term, signed, in its remainder:** the fall the board shows there, less the falls the takes read alone there. Nothing is refused or undone.
4. **The book closes exactly.** The light's whole fall equals the windings tallied plus the remainders' rise, since each take's remainder already holds its own fall less its due.
5. **A negative remainder is the light's debt at that clock.** The next due there (the windings less the remainder) pays it first.
6. **The lays' and the sprung ends' writes are booked the same way:** their cross terms with their neighbours' writes go to the remainders of the clocks where they arise.

## The competitions at one clock

| the competition | the order-free reading |
|---|---|
| two takes of the light at one clock (births, or chimes of two hands) | one take, the dues summed |
| two fitted children of one hand at one clock | all jam by name (the crowd, as built) |
| two unwinds of one child | all jam by name |
| a birth against a chime at one clock | the birth: the fitted clock does not chime (as built) |
| a lay at an end where its hand stands at the tick's start | the lay jams (as built) |

Each reading reads the set of acts and the start board, never their order, so each is its own image under every rotation and translation. The Boss's tick-25 part on the hole (a birth in the setting, a chime at its clock in the image) has the shape of a stop read on a window an earlier take had moved; read on the start board, both runs would decide alike (the hole seed 57/58 is T4's, unread here).

## For the Boss

1. **The jam already decides on the start board.** The letter moves the stop, the count and the draw there.
2. **Two writes over one window book their cross term clock by clock in the remainders**, signed, and the book closes exactly.
3. **No competition is left to an order:** one take per clock and hand, a crowd jammed whole, and the fitted clock silent.
