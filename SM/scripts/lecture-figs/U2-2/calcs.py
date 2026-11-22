"""Numbers for lecture-SM-U2-2 figures (2026-11-22 改版); asserts tie to 題解正本."""
import math
d = math.radians
def close(a, b, tol): assert abs(a - b) <= tol, (a, b)
N = {}
# SM-2023-3: layers, Zc = 20D = 10 m, K = 1.0, delta = phi
phis = [(0, 5, 27 + 0.3*12), (5, 15, 27 + 0.3*15), (15, 25, 27 + 0.3*30)]
def sv_true(z):  # 18 above 10 m (water table at 10 m), gamma'=? use solution: 18*5, 20*5 to 10; below WT gamma' from solution figure 343 at 25 -> (343-190)/15
    if z <= 5: return 18*z
    if z <= 10: return 90 + 20*(z - 5)
    return 190 + (343 - 190)/15*(z - 10)
def sv_design(z): return min(sv_true(z), 190.0)
def phi_at(z):
    for a, b, p in phis:
        if a <= z <= b: return p
fsz = lambda z: 1.0*sv_design(z)*math.tan(d(phi_at(z)))
seg = [(0, 5, 45), (5, 10, 140), (10, 15, 190), (15, 25, 190)]
fs_seg = [1.0*s*math.tan(d(phi_at((a+b)/2))) for a, b, s in seg]
close(fs_seg[0], 26.61, 0.02); close(fs_seg[1], 85.79, 0.02); close(fs_seg[2], 116.43, 0.03); close(fs_seg[3], 138.04, 0.03)
Qs = sum(f*math.pi*0.5*(b - a) for f, (a, b, _) in zip(fs_seg, seg))
close(Qs, 3965.5, 0.6)
N['23'] = dict(fs_seg=fs_seg, Qs=Qs)
# SM-2012-3 clay layers
N['12'] = dict(f1=1.0*45, f2=0.75*70, L=15.22)
# SM-2024-4 alpha table and sand tip
ALPHA = [(0.1, 1.0), (0.2, 0.92), (0.3, 0.82), (0.4, 0.74), (0.6, 0.62), (0.8, 0.54), (1.0, 0.48), (1.2, 0.42), (1.4, 0.40),
         (1.6, 0.38), (1.8, 0.36), (2.0, 0.35), (2.4, 0.34), (2.8, 0.34)]
gp = 144.75/15  # gamma' implied by sigma0' = gamma' * 15D, D = 1
ql = 0.5*100*20*math.tan(d(38))
close(ql, 781.3, 0.1); close(144.75*20, 2895, 1e-6)
N['24'] = dict(gp=gp, ql=ql, z_ql=ql/20/gp, Lc=15.0, qLc=144.75*20)
# SM-2005-4 mobilization
As, Ap = math.pi*1.2*12, math.pi/4*1.2**2
def Q(dl): return min(5*dl, 10)*As + min(50*dl, 400)*Ap
close(Q(1), 282.74, 0.01); close(Q(1.5), 424.12, 0.01); close((10*As + 400*Ap)/3, 301.59, 0.01)
N['05'] = dict(Q1=Q(1), Q15=Q(1.5), Qa=(10*As + 400*Ap)/3, share1=5*As/Q(1))
if __name__ == '__main__':
    import json; print(json.dumps(N, indent=1, default=float))
