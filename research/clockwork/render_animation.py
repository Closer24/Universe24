"""Render saved, exact Universe24 frames as an annotated GIF and poster.

This is an optional read-only presentation tool requiring Pillow. It never
imports the engine or advances/mutates a state. Example from the repository root:

python -m research.clockwork.render_animation \
  runs/clockwork-reviewed/replay_data.json --output runs/animation-new

The output directory must not already exist. All scientific values come from
validated saved frames. Clock hands show counter a to the right and b upward, with
no hand when both counters are zero; remainder gears show the six exact values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

from PIL import Image, ImageChops, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

WIDTH, HEIGHT = 1200, 800
COLORS = {'cream': '#F5F1E8', 'paper': '#FFFEFA', 'navy': '#203641',
          'muted': '#697A7D', 'line': '#D7DED9', 'teal': '#087F82',
          'teal_light': '#D9EFEB', 'coral': '#D85D43', 'coral_light': '#F8E4D8',
          'idle': '#E3E7E2'}
FONT_PATHS = {'sans': Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
              'bold': Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
              'mono': Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')}
FONTS = {}


def font(size, style='sans'):
    key = (size, style)
    if key not in FONTS:
        if not FONT_PATHS[style].is_file():
            raise FileNotFoundError(f'Required font for reproducible layout: {FONT_PATHS[style]}')
        FONTS[key] = ImageFont.truetype(str(FONT_PATHS[style]), size)
    return FONTS[key]


def text(draw, xy, value, size=16, fill='navy', style='sans', anchor=None):
    draw.text(xy, str(value), font=font(size, style), fill=COLORS.get(fill, fill), anchor=anchor)


def panel(draw, box, fill='paper', outline=None, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=COLORS[fill],
                           outline=COLORS[outline] if outline else None, width=1)


def clock(draw, center, radius, triple, color='teal', selected=False):
    x, y = center
    a, b, _ = triple
    ink = COLORS[color]
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=COLORS['paper'],
                 outline=COLORS['navy'] if selected else COLORS['line'], width=3 if selected else 2)
    for angle in range(0, 360, 90):
        theta = math.radians(angle)
        xx, yy = math.cos(theta), math.sin(theta)
        draw.line((x + (radius-3)*xx, y + (radius-3)*yy,
                   x + (radius-6)*xx, y + (radius-6)*yy), fill=COLORS['line'], width=1)
    if a or b:
        norm = math.hypot(a, b)
        dx, dy = (radius-6)*a/norm, -(radius-6)*b/norm
        draw.line((x, y, x+dx, y+dy), fill=ink, width=3 if radius > 16 else 2)
        draw.ellipse((x+dx-2, y+dy-2, x+dx+2, y+dy+2), fill=ink)
    else:
        draw.rectangle((x-2, y-2, x+2, y+2), fill=COLORS['muted'])
    draw.ellipse((x-2, y-2, x+2, y+2), fill=ink if a or b else COLORS['muted'])


def gear(draw, center, radius, remainder, label):
    x, y = center
    points = []
    # Six teeth; contour is stationary. Only the marker tracks retained r.
    for k in range(48):
        angle = 2*math.pi*k/48 - math.pi/2
        rr = radius if k % 8 in (1, 2, 3, 4) else radius-5
        points.append((x+rr*math.cos(angle), y+rr*math.sin(angle)))
    draw.polygon(points, fill=COLORS['teal_light'], outline=COLORS['teal'], width=2)
    draw.ellipse((x-7, y-7, x+7, y+7), fill=COLORS['paper'], outline=COLORS['teal'])
    for r in range(6):
        angle = 2*math.pi*r/6 - math.pi/2
        xx, yy = x + (radius+12)*math.cos(angle), y + (radius+12)*math.sin(angle)
        if r == remainder:
            draw.ellipse((xx-10, yy-10, xx+10, yy+10), fill=COLORS['teal'])
        text(draw, (xx, yy), r, 13, 'paper' if r == remainder else 'muted', anchor='mm')
    angle = 2*math.pi*remainder/6 - math.pi/2
    draw.line((x, y, x+(radius-8)*math.cos(angle), y+(radius-8)*math.sin(angle)),
              fill=COLORS['teal'], width=3)
    text(draw, (x, y+radius+30), label, 13, 'muted', anchor='mm')


def validate(main, control):
    if main['id'] != 'guide_N24' or control['id'] != 'no_source':
        raise ValueError('This registered animation requires guide_N24 and no_source')
    if main['detectors'] != [6, 12] or len(main['sites']) != 25:
        raise ValueError('Expected the registered 25-site guide with detectors 6/12')
    if len(main['frames']) != 57 or len(control['frames']) != 57:
        raise ValueError('Expected every saved integer step t=0,...,56')
    for scenario in (main, control):
        previous_memory = None
        for t, frame in enumerate(scenario['frames']):
            if frame['t'] != t or len(frame['cells']) != 25:
                raise ValueError('Missing, reordered or differently sized frame')
            memory = []
            for pair in frame['cells']:
                if len(pair) != 2:
                    raise ValueError('Expected both retained channels 0 and 14')
                for triple in pair:
                    if len(triple) != 3 or any(type(v) is not int for v in triple) or not 0 <= triple[2] < 6:
                        raise ValueError('Invalid retained triple')
                memory.append(int(pair[0][2] == 0 and pair[1][2] == 4))
            clicks = [] if previous_memory is None else [j for j, value in enumerate(memory) if value and not previous_memory[j]]
            if frame['memory'] != memory or frame['clicks'] != clicks:
                raise ValueError('Readout inconsistent with retained state')
            if not frame['inverse_ok']:
                raise ValueError('Frame lacks successful recorded inverse audit')
            if t:
                if len(frame['transitions']) != 25:
                    raise ValueError('Missing exact incoming transition')
                for j, tr in enumerate(frame['transitions']):
                    if tr['old'] != scenario['frames'][t-1]['cells'][j][0] or tr['next'] != frame['cells'][j][0]:
                        raise ValueError('Transition endpoints disagree with frames')
                    a, b, r = tr['old']; na, nb, nr = tr['next']
                    if 2*tr['u']+r != 6*tr['ell']+nr or na != b or nb != tr['ell']-a:
                        raise ValueError('Rule3 arithmetic mismatch')
            elif frame['transitions']:
                raise ValueError('Synthetic incoming transition at t=0')
            previous_memory = memory
    if any(frame['cells'] != control['frames'][0]['cells'] for frame in control['frames']):
        raise ValueError('No-source displayed projection is not stationary')
    if control['metrics']['checks'].get('entire_board_stationary') is not True:
        raise ValueError('Bundle does not certify no-source full-board stationarity')


def draw_detector(draw, frame, scenario, j, left):
    panel(draw, (left, 379, left+550, 565))
    pair = frame['cells'][j]
    memory = frame['memory'][j]
    clicking = j in frame['clicks']
    text(draw, (left+20, 395), f'Receiver {j:02d}', 21, style='bold')
    panel(draw, (left+445, 392, left+529, 424), 'teal' if memory else 'idle', radius=12)
    text(draw, (left+487, 408), f'M = {memory}', 16, 'paper' if memory else 'navy', style='bold', anchor='mm')
    text(draw, (left+20, 439), f'g0   a={pair[0][0]:+d}  b={pair[0][1]:+d}  r={pair[0][2]}', 16, style='mono')
    text(draw, (left+20, 466), f'g14  a={pair[1][0]:+d}  b={pair[1][1]:+d}  r={pair[1][2]}', 16, style='mono')
    clock(draw, (left+286, 472), 30, pair[0], selected=True)
    text(draw, (left+286, 521), 'a → / b ↑', 12, 'muted', anchor='mm')
    gear(draw, (left+388, 472), 24, pair[0][2], 'r0')
    gear(draw, (left+490, 472), 24, pair[1][2], 'r14')
    prior_click = any(j in row['clicks'] for row in scenario['frames'][:frame['t']])
    if clicking:
        label, color = 'CLICK: internal record 0 -> 1', 'coral'
    elif memory:
        label, color = 'Record retained in the two remainders', 'teal'
    elif prior_click:
        label, color = 'Record reset; full state still reversible', 'coral'
    else:
        label, color = 'Ready: waiting for the arriving influence', 'muted'
    text(draw, (left+20, 538), label, 14, color)


def render_frame(dataset, main, control, t):
    image = Image.new('RGB', (WIDTH, HEIGHT), COLORS['cream'])
    draw = ImageDraw.Draw(image)
    frame, null = main['frames'][t], control['frames'][t]
    text(draw, (38, 25), 'Universe24 / clocks from one rule', 29, style='bold')
    text(draw, (40, 67), 'Exact counter states in a prepared medium: one source starts two finite records.', 16, 'muted')
    panel(draw, (1025, 23, 1161, 80), 'navy', radius=16)
    text(draw, (1093, 45), f't = {t:02d}', 23, 'paper', style='mono', anchor='mm')
    text(draw, (1093, 68), 'saved update', 11, 'paper', anchor='mm')

    panel(draw, (38, 102, 1162, 272))
    text(draw, (58, 119), 'SOURCE PRESENT', 14, 'teal', style='bold')
    text(draw, (1140, 119), '25 sites shown / channels 0 and 14 sampled', 13, 'muted', anchor='ra')
    xs = [64 + j*44.7 for j in range(25)]
    draw.line((xs[0], 185, xs[-1], 185), fill=COLORS['line'], width=2)
    for j, x in enumerate(xs):
        if j in frame['clicks']:
            draw.ellipse((x-21, 164, x+21, 206), fill=COLORS['coral_light'])
        clock(draw, (x, 185), 15, frame['cells'][j][0], color='coral' if j == 0 else 'teal', selected=j in main['detectors'])
        text(draw, (x, 215), 'S' if j == 0 else str(j), 12, 'navy' if j in main['detectors'] else 'muted',
             style='bold' if j in main['detectors'] else 'sans', anchor='mm')
        draw.ellipse((x-4, 234, x+4, 242), fill=COLORS['teal'] if frame['memory'][j] else COLORS['idle'])
    text(draw, (58, 252), 'Hand: a right, b up. Square: zero counters. Dots: internal memory M.', 12, 'muted')

    panel(draw, (38, 284, 1162, 367))
    text(draw, (58, 297), 'MATCHED NO-SOURCE CONTROL', 13, 'muted', style='bold')
    text(draw, (1140, 297), 'same preparation, source omitted: every saved full state is stationary', 12, 'muted', anchor='ra')
    for j, x in enumerate(xs):
        clock(draw, (x, 337), 10, null['cells'][j][0], color='muted')
    for j, left in ((6, 38), (12, 612)):
        draw_detector(draw, frame, main, j, left)

    panel(draw, (38, 578, 1162, 641), 'navy')
    text(draw, (58, 590), 'RULE3 / RECEIVER 6 / CHANNEL 0', 11, 'paper', style='bold')
    if t:
        tr = frame['transitions'][6]
        a, b, r = tr['old']; na, nb, nr = tr['next']
        formula = f"2u + r = 6ell + r'     2({tr['u']}) + {r} = 6({tr['ell']}) + {nr}"
        text(draw, (58, 612), formula, 17, 'paper', style='mono')
        text(draw, (1138, 612), f't{t-1} -> t{t}:  ({a},{b},{r}) -> ({na},{nb},{nr})', 14, 'paper', style='mono', anchor='ra')
    else:
        text(draw, (58, 612), "2u + r = 6ell + r'     a' = b     b' = ell - a", 17, 'paper', style='mono')
        text(draw, (1138, 612), 'Initial preparation; no update yet', 13, 'paper', anchor='ra')

    text(draw, (40, 653), 'FULL RECORDED MEMORY TIMELINE', 12, 'navy', style='bold')
    text(draw, (1160, 653), 'teal: M=1 / coral mark: rising-edge click / cursor: displayed t', 12, 'muted', anchor='ra')
    x0, x1 = 142, 1142
    unit = (x1-x0)/57
    for j, y in ((6, 681), (12, 710)):
        text(draw, (40, y+7), f'Receiver {j}', 13, 'muted', anchor='la')
        for tick, row in enumerate(main['frames']):
            x = x0+tick*unit
            draw.rectangle((x, y, x+unit-1, y+14), fill=COLORS['teal'] if row['memory'][j] else COLORS['idle'])
            if j in row['clicks']:
                draw.rectangle((x, y-4, x+2, y+18), fill=COLORS['coral'])
        current = x0+(t+.5)*unit
        draw.line((current, y-7, current, y+19), fill=COLORS['navy'], width=2)
    for tick in (0, 6, 12, 24, 38, 44, 56):
        text(draw, (x0+(tick+.5)*unit, 738), tick, 11, 'muted', anchor='mm')
    text(draw, (40, 761), 'Source-triggered prepared-medium result; not a free photon. Finite records reset. Replay loops saved frames.', 13, 'muted')
    text(draw, (40, 784), f"Rule3 only / fixed +++ tensor / L={main['side']} / 48 channels per site / engine {dataset['engine_commit'][:12]}", 11, 'muted')
    return image


def main_cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--duration-ms', type=int, default=250)
    parser.add_argument('--poster-step', type=int, default=12)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a new output directory; existing artifacts are never overwritten')
    if not 200 <= args.duration_ms <= 300 or not 0 <= args.poster_step <= 56:
        raise ValueError('Duration must be 200..300 ms; poster step must be 0..56')
    raw = args.dataset.read_bytes()
    dataset = json.loads(raw)
    if dataset['schema_version'] != 'u24-clockwork-v1':
        raise ValueError('Unsupported replay schema')
    scenarios = {scenario['id']: scenario for scenario in dataset['scenarios']}
    guide, control = scenarios['guide_N24'], scenarios['no_source']
    validate(guide, control)
    start = time.process_time()
    images = []
    for t in range(57):
        if time.process_time()-start > 60:
            raise TimeoutError('60 CPU-second rendering budget exceeded')
        images.append(render_frame(dataset, guide, control, t))
    args.output.mkdir(parents=True)
    poster = args.output / 'clockwork-poster.png'
    animation = args.output / 'clockwork-animation.gif'
    images[args.poster_step].save(poster)
    # One common palette avoids arbitrary color shifts between discrete frames.
    palette = images[args.poster_step].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images]
    indexed[0].save(animation, save_all=True, append_images=indexed[1:],
                    duration=args.duration_ms, loop=0, optimize=True, disposal=1)
    elapsed = time.process_time()-start
    if elapsed > 60:
        raise TimeoutError('Render completed outside declared CPU budget; do not accept artifacts')
    with Image.open(animation) as check:
        if check.size != (WIDTH, HEIGHT) or check.n_frames != 57:
            raise ValueError('Encoded GIF geometry/frame count mismatch')
        durations = []
        for t in range(check.n_frames):
            check.seek(t); durations.append(check.info['duration'])
            if ImageChops.difference(check.convert('RGB'), indexed[t].convert('RGB')).getbbox() is not None:
                raise ValueError(f'GIF decoding changed rendered pixels at t={t}')
        if durations != [args.duration_ms]*57:
            raise ValueError('Encoded GIF timing mismatch')
    metadata = {'format': 'u24-clockwork-animation-v1', 'dataset_sha256': hashlib.sha256(raw).hexdigest(),
                'renderer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'protocol_id': dataset['protocol_id'], 'protocol_sha256': dataset['protocol_sha256'],
                'engine_commit': dataset['engine_commit'], 'scenario_id': 'guide_N24',
                'control_scenario_id': 'no_source', 'width': WIDTH, 'height': HEIGHT,
                'frames': 57, 'first_t': 0, 'last_t': 56, 'duration_ms': args.duration_ms,
                'total_duration_ms': args.duration_ms*57, 'poster_t': args.poster_step,
                'pillow_version': PILLOW_VERSION,
                'font_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in FONT_PATHS.values()},
                'artifacts': {p.name: {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
                              for p in (animation, poster)},
                'readout_checked': True, 'incoming_rule3_arithmetic_checked': True,
                'decoded_frames_match_quantized_rendered_frames_exactly': True,
                'control_displayed_projection_stationarity_checked': True,
                'control_full_board_stationarity_reported_by_bundle': True,
                'state_hash_definition': 'Full checkpoint digest including completed_steps; unequal digest alone need not mean different physical state.',
                'state_hashes': [frame['state_hash'] for frame in guide['frames']],
                'budget_cpu_seconds': 60,
                'scope': 'Read-only visualization of saved projected state; source-triggered prepared medium, not a derived photon.'}
    (args.output/'animation-manifest.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps({'output': str(args.output), 'frames': 57, 'size': [WIDTH, HEIGHT],
                      'duration_ms': args.duration_ms*57, 'cpu_seconds': round(elapsed, 3),
                      'artifacts': metadata['artifacts']}, indent=2))


if __name__ == '__main__':
    main_cli()
