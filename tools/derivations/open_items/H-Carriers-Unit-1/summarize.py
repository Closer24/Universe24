"""pm1's summary of the records under out/: per record the counts, the bits, the content, the run back, the exact take (taken >= booked), the charge at the births (the two children's W opposite and equal), the credits' senses, the first body click, the first Link at the wall and the first frozen Node. Integers only. Usage: python summarize.py <name> [<name> ...]"""
import json, os, sys
sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
for name in sys.argv[1:]:
    path = os.path.join(HERE, 'out', name + '.json')
    if not os.path.exists(path):
        print(name, 'MISSING'); continue
    r = json.load(open(path))
    last = r['rows'][-1]
    log = r['log']
    births = [e for e in log if e['event'] == 'birth']
    credits = [e for e in log if e['event'] == 'credit']
    charge_ok = sum(1 for e in births if e['W_children'][0] == -e['W_children'][1])
    taken, booked = int(r['counts']['taken']), int(r['counts']['booked'])
    senses = sum(e['sense'] for e in credits)
    first_credit = credits[0]['i'] if credits else None
    held = [n['i'] for n in r['nodes'] if n['held']]
    frozen = [n['i'] for n in r['nodes'] if n['frozen']]
    rows_clicked = {}
    for e in credits:
        rows_clicked[e['line']] = rows_clicked.get(e['line'], 0) + 1
    credit_contents = [e['content'] for e in credits]
    print(json.dumps({
        'record': name, 'weight': r.get('pm1_weight', 'engine'), 'intervals': r['intervals'],
        'births': r['counts']['births'], 'body_clicks': r['counts']['body_clicks'], 'clicks_by_row': rows_clicked,
        'first_credit': first_credit, 'credit_content_min_max': [min(credit_contents), max(credit_contents)] if credits else None,
        'credit_senses_sum': senses, 'credits_plus_minus': [sum(1 for e in credits if e['sense'] > 0), sum(1 for e in credits if e['sense'] < 0)],
        'turns': r['counts']['turns'], 'refused_stop': r['counts']['refused_stop'], 'refused_lay': r['counts']['refused_lay'],
        'taken_ge_booked': taken >= booked, 'taken_over_booked_per_mille': (taken * 1000) // booked if booked else None,
        'charge_0_at_births': [charge_ok, len(births)],
        'content_min_mean_max': last['content min/mean/max'], 'volume_mean': last['volume mean'],
        'state_bits': last['max bits'], 'transient_bits': last['max transient bits'], 'integers': last['integers'],
        'links_at_wall_end': last['links at the wall'], 'first_held_interval': held[0] if held else None, 'first_frozen_interval': frozen[0] if frozen else None,
        'run_back': r['run_back'], 'W_total': last['W total'],
    }))
