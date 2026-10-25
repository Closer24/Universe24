"""A FLOAT CHECK (named as such under Addition 3; the integer readings stand beside it in the report): the band's group velocity v(q) = (num / (3 den)) sin q / sin omega(q) with cos omega(q) = (num / (3 den)) (2 + cos q), and the raised cosine envelope's spectral mean of it: the width-2 envelope (1, 2, 1) has the power spectrum cos^4((q - k) / 2), the width-3 envelope (1, 3, 4, 3, 1) the power |4 + 6 cos u + 2 cos 2u|^2, u = q - k; the mean over the 9-torus's modes q = 2 pi m / 9 and over the continuum. Also the velocity at the band's maximum and the fraction of light's long-wavelength speed 1 / sqrt 3."""
import math
den = 1655909141
rows = {'heavy lift (row 2)': 506298091, 'light lift (row 1)': 1655880909, 'light (row 0)': den}
def band(num, q):
    c = (num / (3 * den)) * (2 + math.cos(q)); s = math.sqrt(max(0.0, 1 - c * c))
    return 0.0 if s == 0 else (num / (3 * den)) * math.sin(q) / s
def spectral_mean(num, k, width, L=None):
    if L: qs = [2 * math.pi * m / L for m in range(-(L // 2), L // 2 + 1)]
    else: qs = [-math.pi + 2 * math.pi * (j + 0.5) / 4000 for j in range(4000)]
    w = (lambda u: math.cos(u / 2) ** 4) if width == 2 else (lambda u: (4 + 6 * math.cos(u) + 2 * math.cos(2 * u)) ** 2)
    num_ = sum(w(q - k) * band(num, q) for q in qs); den_ = sum(w(q - k) for q in qs)
    return num_ / den_
ks = {'k = 2 asin(1/4)': 2 * math.asin(0.25), 'k = pi/3': math.pi / 3, 'k = pi/2': math.pi / 2, 'k = pi': math.pi}
for name, num in rows.items():
    vmax = max(band(num, q) for q in [j * math.pi / 4000 for j in range(4001)])
    qmax = max((band(num, q), q) for q in [j * math.pi / 4000 for j in range(4001)])[1]
    print(name, 'num/den', round(num / den, 6), 'v_g max', round(1000 * vmax), 'milli at k', round(qmax, 3), 'rad; light long-wave 1/sqrt3 =', round(1000 / math.sqrt(3)), '; fraction', round(vmax * math.sqrt(3), 3))
    for kn, k in ks.items():
        print('   ', kn, 'plane wave v_g', round(1000 * band(num, k)), '| envelope mean width 2 (9-torus / continuum)', round(1000 * spectral_mean(num, k, 2, 9)), '/', round(1000 * spectral_mean(num, k, 2)), '| width 3', round(1000 * spectral_mean(num, k, 3, 9)), '/', round(1000 * spectral_mean(num, k, 3)))
