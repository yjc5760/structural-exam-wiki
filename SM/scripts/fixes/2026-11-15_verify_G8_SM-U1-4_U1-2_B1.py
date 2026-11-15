# -*- coding: utf-8 -*-
"""G8 勘誤獨立重算：SM-2011-2、SM-2018-3、SM-2020-1、SM-2025-4（由題目正本給定量出發）"""
import math
mm = []
def chk(name, val, ref, tol=0.006):
    ok = abs(val - ref) <= tol * max(1, abs(ref)) if ref != 0 else abs(val) < 1e-9
    print("%-28s %12.5g  ref %12.5g  %s" % (name, val, ref, "ok" if ok else "MISMATCH"))
    if not ok: mm.append(name)
gw = 9.81
# ---- SM-2011-2 ----
th = math.atan2(4, 3); s = math.sin(th)
z = dict(a=8, b=0, c=2, d=3, e=5)
hb, hd = 8.0, 6.0                    # b: 水壓計; d: 圍堰內水位(地表 6 m)
L = (z['d'] - z['b']) / s            # 3.75
i = (hb - hd) / L
h = dict(a=8, b=hb, c=hb - i * (z['c'] / s), d=hd, e=6.0)
hp = {k: h[k] - z[k] for k in h}
chk("2011-2 L_bd", L, 3.75); chk("2011-2 i_bd", i, 0.5333)
chk("2011-2 h_c", h['c'], 6.667); chk("2011-2 hp_c", hp['c'], 4.667)
chk("2011-2 hp_d", hp['d'], 3.0); chk("2011-2 hp_e", hp['e'], 1.0); chk("2011-2 hp_b", hp['b'], 8.0)
k = 0.005e-2; A = 2 * 2
Q = k * i * A; chk("2011-2 Q m3/s", Q, 1.0667e-4); chk("2011-2 Q m3/day", Q * 86400, 9.22)
# 第二路徑：流網 Nf=2（1 m 流槽）、Nd=3.75（1 m 方格），寬 2 m
Q2 = k * (hb - hd) * 2 / L * 2 * 86400; chk("2011-2 Q flownet", Q2, 9.22)
# 第二路徑：c 以高程線性內插
chk("2011-2 h_c by z", hb - (hb - hd) * z['c'] / z['d'], 6.667)
# 對照（§5）
chk("2011-2 old Q", k * (3 / 6.25) * 3.2 * 86400, 6.64)
chk("2011-2 alt L=3 Q", k * (2 / 3) * 4 * 86400, 11.52)
chk("2011-2 alt dry i", (8 - 3) / 3.75, 1.333)
# ---- SM-2018-3 ----
H, Nf, Nd, kk = 6.3, 3, 10, 3.5e-6
q = kk * H * Nf / Nd; chk("2018-3 q m3/s/m", q, 6.615e-6); chk("2018-3 q m3/day/m", q * 86400, 0.5715)
dh = H / Nd; chk("2018-3 dh", dh, 0.63)
U = {}
for p, n in dict(a=4.5, b=5, c=6, d=7, e=8).items():
    hh = H - n * dh; hpp = hh + 1.6; U[p] = gw * hpp
ref = dict(a=49.69, b=46.60, c=40.42, d=34.24, e=28.06)
for p in ref: chk("2018-3 u_" + p, U[p], ref[p], 0.002)
# 第二路徑：以壩底為基準 z=0，上游總水頭 7.9、下游 1.6，損失 6.3
for p, n in dict(a=4.5, e=8).items():
    chk("2018-3 u_%s (base datum)" % p, gw * (7.9 - n * 0.63 - 0), ref[p], 0.002)
chk("2018-3 u_a n=4", gw * (H - 4 * dh + 1.6), 52.78, 0.002)
chk("2018-3 gw10 u_e", 10 * (H - 8 * dh + 1.6), 28.6, 0.002)
chk("2018-3 gw10 u_a", 10 * (H - 4.5 * dh + 1.6), 50.65, 0.002)
# 對照：Nd=9
q9 = kk * H * 3 / 9; chk("2018-3 alt Nd9 q", q9, 7.35e-6)
for p, n, r in (("b", 5, 43.16), ("e", 8, 22.56), ("a", 4.5, 46.60)):
    chk("2018-3 alt Nd9 u_" + p, gw * (H - n * 0.7 + 1.6), r, 0.002)
# 對照：舊讀法
chk("2018-3 old q", kk * 7.9 * 0.4, 1.106e-5, 0.002)
# ---- SM-2020-1（數值不變，只核對分布描述用的值）----
gd = 2.65 / 1.5 * gw; gm = (2.65 + 0.25) / 1.5 * gw; e3 = 0.42 * 2.71; gs = (2.71 + e3) / (1 + e3) * gw
sB = gd * 2.1; sC = sB + gm * 0.9; sD = sC + gs * 1.9; uB = -0.5 * gw * 0.9; uD = gw * 1.9
chk("2020-1 sigma_B", sB, 36.39, 0.002); chk("2020-1 u_B", uB, -4.41, 0.002)
chk("2020-1 sig'_B cap", sB - uB, 40.80, 0.002); chk("2020-1 sig'_B dry", sB, 36.39, 0.002)
chk("2020-1 sigma_C", sC, 53.46, 0.002); chk("2020-1 sigma_D", sD, 87.00, 0.002); chk("2020-1 sig'_D", sD - uD, 68.36, 0.002)
chk("2020-1 slope sig' BC", (sC - (sB - uB)) / 0.9, 14.07, 0.003)
chk("2020-1 slope sig' CD", ((sD - uD) - sC) / 1.9, 7.84, 0.003)
# ---- SM-2025-4（數值不變；凸出部寬直接為 40 m）----
def Ic(m, n):
    a = m*m + n*n + 1; b = m*m*n*n
    t1 = 2*m*n*math.sqrt(a)/(a + b) * (a + 1)/a
    x = 2*m*n*math.sqrt(a)/(a - b)
    t2 = math.atan(x) + (math.pi if a - b < 0 else 0)
    return (t1 + t2) / (4*math.pi)
I = Ic(1, 1) * 2 + Ic(2, 1)
chk("2025-4 I(1,1)", Ic(1, 1), 0.1752, 0.002); chk("2025-4 I(2,1)", Ic(2, 1), 0.1999, 0.002)
chk("2025-4 dsig", 200 * I, 110.06, 0.002)
chk("2025-4 left gap", 120 - 40 - 40, 40)
print("MISMATCHES:", len(mm), mm)
