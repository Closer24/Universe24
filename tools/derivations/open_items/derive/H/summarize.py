import json, sys
for line in open(sys.argv[1]):
    d = json.loads(line)
    v = d['variant counted']; h = d['head counted']
    print(d['variant'], d['world'], d['ticks'], '| differ', d['ticks differing from the head'], 'first', d['first tick differing'], '| stopped', d['variant stopped at tick'], d['error'])
    print('   counts head', d['head counts'], 'var', d['variant counts'], '| bits', d['head widest transient (bits)'], d['variant widest transient (bits)'], '| rewind', d['rewind exact of 20'])
    print('   pinned head/var', h.get('pinned (turned two ticks running)'), v.get('pinned (turned two ticks running)'), '| loads<0 head/var', h.get('tick-start loads below 0'), v.get('tick-start loads below 0'),
          '| X+<=0 not turned', v.get('outputs X+ <= 0 at a clock not turned'), '| W+<=0 head/var', h.get('end teeth at or below 0'), v.get('end teeth at or below 0'), '| not turned', h.get('end teeth at or below 0 at a clock not turned'), v.get('end teeth at or below 0 at a clock not turned'))
    print('   cone past head/var', h.get('clock-gearings past the light-cone edge'), v.get('clock-gearings past the light-cone edge'), 'of', v.get('clock-gearings read'), '| tensions <0/>G head', h.get('tensions below 0'), h.get('tensions above Gamma'), 'of', h.get('tensions read'))
    t = {k.split('),')[-1] if '),' in k else k[-12:]: h[k] for k in h if 'ties' in k}
    print('   ties head', t)
