"""Numbers for lecture-SM-U2-1 figures (2026-11-22 改版)."""
import math
def close(a, b, tol): assert abs(a - b) <= tol, (a, b)
N = {}
# SM-2010-4 gross vs net
qu, q = 439.088, 32.0
N['10_4'] = dict(qu=qu, q=q, qnet=qu - q, qall_gross=qu/3, qall_net=(qu - q)/3 + q)
close(N['10_4']['qall_gross'], 146.363, 0.001); close(N['10_4']['qall_net'], 167.7, 0.01)
# SM-2022-3 three layers (top a -> bottom d), thickness mm and k
H = [50, 100, 50]; k = [1e-2, 1e-1, 1e-3]
R = [h/kk for h, kk in zip(H, k)]
dh_tot = 600.0
dh = [dh_tot*r/sum(R) for r in R]
ha = 600.0; hb = ha - dh[0]; hc = hb - dh[1]; hd = hc - dh[2]
close(hb, 546.43, 0.01); close(hc, 535.71, 0.01); close(hd, 0, 1e-6)
N['22_3'] = dict(H=H, k=k, h=[ha, hb, hc, hd], dh=dh, i=[d/hh for d, hh in zip(dh, H)])
# SM-2015-4
N['15_4'] = dict(sig=(226.0, 216.0), u=(98.1, 73.6), eff=(127.9, 142.4))
close(N['15_4']['sig'][0] - N['15_4']['u'][0], 127.9, 0.01); close(N['15_4']['sig'][1] - N['15_4']['u'][1], 142.4, 0.01)
