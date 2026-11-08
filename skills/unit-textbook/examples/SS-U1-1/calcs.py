# -*- coding: utf-8 -*-
"""教科書講義 SS-U1-1 的所有數值（圖與內文共用，先算再寫）。單位 tf、cm。"""
import math

E = 2040.0
STEELS = {'A36': (2.52, 4.10), 'A572-50': (3.52, 4.57)}


def sq(Fy):            # √(E/Fy)
    return math.sqrt(E / Fy)


def Fe_of(slr):        # Euler 應力
    return math.pi ** 2 * E / slr ** 2


def lam_c(slr, Fy):    # λc
    return slr / math.pi * math.sqrt(Fy / E)


def Fcr_lrfd(lc, Fy):
    return (0.658 ** (lc ** 2)) * Fy if lc <= 1.5 else 0.877 / lc ** 2 * Fy


def Cc_of(Fy):
    return math.sqrt(2 * math.pi ** 2 * E / Fy)


def FS_of(slr, Cc):
    x = min(slr / Cc, 1.0)
    return 5 / 3 + 3 * x / 8 - x ** 3 / 8


def Fa_asd(slr, Fy):
    Cc = Cc_of(Fy)
    if slr <= Cc:
        return (1 - slr ** 2 / (2 * Cc ** 2)) * Fy / FS_of(slr, Cc)
    return 12 * math.pi ** 2 * E / (23 * slr ** 2)


# ---- 範例：H400×400×13×21，A36，柱高 8 m，兩端鉸接，弱軸中央側撐
EX = dict(Ag=218.7, rx=17.45, ry=10.12, L=800.0, Fy=2.52)


def example():
    d = dict(EX)
    d['slx'] = 1.0 * d['L'] / d['rx']
    d['sly'] = 1.0 * (d['L'] / 2) / d['ry']
    s = max(d['slx'], d['sly']); d['sl'] = s
    d['sqEF'] = sq(d['Fy'])
    d['lc'] = lam_c(s, d['Fy']); d['lc2'] = d['lc'] ** 2
    d['Fe'] = Fe_of(s)
    d['ratio'] = 0.658 ** d['lc2']
    d['Fcr'] = Fcr_lrfd(d['lc'], d['Fy'])
    d['phiPn'] = 0.85 * d['Fcr'] * d['Ag']
    d['Cc'] = Cc_of(d['Fy']); d['x'] = s / d['Cc']
    d['par'] = 1 - s ** 2 / (2 * d['Cc'] ** 2)
    d['FS'] = FS_of(s, d['Cc'])
    d['Fa'] = d['par'] * d['Fy'] / d['FS']
    d['Pa'] = d['Fa'] * d['Ag']
    d['LR'] = d['phiPn'] / d['Pa']
    return d


if __name__ == '__main__':
    for k, (Fy, Fu) in STEELS.items():
        print(k, 'sqrt(E/Fy)=%.2f' % sq(Fy), 'Cc=%.1f' % Cc_of(Fy), 'KL/r@lc1.5=%.1f' % (1.5 * math.pi * sq(Fy)),
              'KL/r@lc1=%.1f' % (math.pi * sq(Fy)))
    print('0.877/2.25 =', 0.877 / 2.25, ' root =', (0.877 / 2.25) ** (1 / 2.25), ' e^-0.419=', math.exp(-0.419))
    print('0.658^2.25=', 0.658 ** 2.25)
    print('Cc ↔ λc =', math.sqrt(2))
    print('lc=1.5 -> Fe/Fy=', 1 / 2.25)
    # CRC 拋物線在 Cc 與 Euler 相切
    Fy = 2.52; Cc = Cc_of(Fy)
    print('parab slope at Cc', -Fy / Cc, ' euler slope', -2 * math.pi ** 2 * E / Cc ** 3)
    # LRFD/ASD 比值範圍
    rs = []
    for i in range(1, 300):
        lc = i / 100; s = lc * math.pi * sq(Fy)
        rs.append((0.85 * Fcr_lrfd(lc, Fy) / Fa_asd(s, Fy), lc))
    print('ratio min/max', min(rs), max(rs))
    for lc in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
        s = lc * math.pi * sq(Fy)
        print('lc', lc, 'Fcr/Fy %.3f' % (Fcr_lrfd(lc, Fy) / Fy), 'CRC %.3f' % (1 - lc * lc / 4), 'Euler %.3f' % (1 / lc / lc),
              'ratio %.3f' % (0.85 * Fcr_lrfd(lc, Fy) / Fa_asd(s, Fy)))
    d = example()
    for k, v in d.items():
        print(k, round(v, 4))


# =====================================================================
# 拉力篇（上冊）共用數值
# =====================================================================
# ---- 第 1 章：同一支 H100×100×6×8（A36），當拉桿 vs 當壓桿
H100 = dict(A=21.59, rx=4.18, ry=2.49, Fy=2.52)


def h100_tension():
    return 0.90 * H100['Fy'] * H100['A']


def h100_comp(Lcm, K=1.0):
    slr = K * Lcm / H100['ry']
    lc = lam_c(slr, H100['Fy'])
    return 0.85 * Fcr_lrfd(lc, H100['Fy']) * H100['A'], slr, lc


# ---- 第 2～5 章貫穿範例：L100×100×10 角鋼，A36，單肢 1 排 3 顆 M20 螺栓
TEX = dict(Ag=19.0, t=1.0, xbar=2.82, Fy=2.52, Fu=4.10, db=2.0, dh=2.3, s=7.0, e=3.5, nb=3)


def tension_example():
    d = dict(TEX)
    d['An'] = d['Ag'] - 1 * d['dh'] * d['t']
    d['Lc'] = (d['nb'] - 1) * d['s']                    # 第一顆到最後一顆螺栓
    d['U'] = 1 - d['xbar'] / d['Lc']
    d['Ae'] = d['U'] * d['An']
    d['GSY'] = 0.90 * d['Fy'] * d['Ag']
    d['NSF'] = 0.75 * d['Fu'] * d['Ae']
    d['GSY_a'] = 0.60 * d['Fy'] * d['Ag']               # ASD：Ft = 0.6Fy（毛斷面）
    d['NSF_a'] = 0.50 * d['Fu'] * d['Ae']               # ASD：Ft = 0.5Fu（有效淨斷面）
    d['crit'] = 1.2 * d['Fy'] / d['Fu']                 # Ae/Ag 臨界比
    d['ratio'] = d['Ae'] / d['Ag']
    return d


if __name__ == '__main__':
    print('---- tension')
    print('H100 tension', h100_tension())
    for L_ in (100, 200, 300, 400, 500, 600):
        print('H100 comp L=', L_, ['%.2f' % v for v in h100_comp(L_)])
    for k, v in tension_example().items():
        print(k, round(v, 4) if isinstance(v, float) else v)
    for k, (Fy, Fu) in STEELS.items():
        print(k, 'crit Ae/Ag =', round(1.2 * Fy / Fu, 3))


# ---- 第 3 章：錯列螺栓（板寬 18、三條規線 g=6、s=7、扣除寬 2.3）
STAG = dict(bg=18.0, g=6.0, s=7.0, d=2.3)


def stagger(s=None):
    d = dict(STAG)
    if s is not None:
        d['s'] = s
    d['straight'] = d['bg'] - 2 * d['d']
    d['credit'] = d['s'] ** 2 / (4 * d['g'])
    d['zig'] = d['bg'] - 3 * d['d'] + 2 * d['credit']
    d['s_crit'] = math.sqrt(2 * d['g'] * d['d'])   # 2·s²/4g = d
    return d


# ---- 第 4 章：SS-2025-2（ASD，板厚 2、銲長 l=3、Fy=2.5、Fu=4.1）
def ss2025_2(L):
    l, t, Fy, Fu = 3.0, 2.0, 2.5, 4.1
    if L > l:
        return None
    U = 1.0 if l >= 2 * L else (0.87 if l >= 1.5 * L else 0.75)
    Pgy = 0.6 * Fy * t * L
    Pnsf = 0.5 * Fu * U * t * L
    return dict(U=U, Pgy=Pgy, Pnsf=Pnsf, P=min(Pgy, Pnsf))


def ss2025_2_wrong(L):
    U = 1 - (L / 2) / 3.0
    return min(0.6 * 2.5 * 2 * L, 0.5 * 4.1 * U * 2 * L)


def L_opt(xbar, Fy, Fu, phi=True):
    r = (0.90 * Fy) / (0.75 * Fu) if phi else Fy / Fu
    return xbar / (1 - r)


# ---- 第 5 章：塊狀剪力（同一支角鋼：端距 3.5、s=7、3 顆、拉力面到肢趾 4.5）
def block_shear():
    d = tension_example()
    t, dh = d['t'], d['dh']
    Lv = d['e'] + (d['nb'] - 1) * d['s']
    d['Agv'] = Lv * t
    d['Anv'] = (Lv - (d['nb'] - 0.5) * dh) * t
    d['Agt'] = 4.5 * t
    d['Ant'] = (4.5 - 0.5 * dh) * t
    d['rup'] = 0.6 * d['Fu'] * d['Anv'] + d['Fu'] * d['Ant']
    d['cap'] = 0.6 * d['Fy'] * d['Agv'] + d['Fu'] * d['Ant']
    d['BS'] = 0.75 * min(d['rup'], d['cap'])
    d['BS_a'] = 0.30 * d['Fu'] * d['Anv'] + 0.50 * d['Fu'] * d['Ant']
    return d


if __name__ == '__main__':
    print('---- ch3-5')
    print(stagger())
    for L_ in (1, 1.5, 2, 2.5, 3):
        print('2025-2', L_, ss2025_2(L_), round(ss2025_2_wrong(L_), 3))
    print('Lopt LRFD', L_opt(2.82, 2.52, 4.10), 'nominal', L_opt(2.82, 2.52, 4.10, False))
    print({k: round(v, 3) for k, v in block_shear().items() if isinstance(v, float)})


# =====================================================================
# 壓力篇（下冊）共用數值
# =====================================================================
def K_sway(GA, GB):
    """對位圖（有側移）背後的方程式：GA·GB·(π/K)² − 36) / 6(GA+GB) = (π/K)/tan(π/K)，K ≥ 1。"""
    lo, hi = 1.0000001, 50.0
    def g(K):
        x = math.pi / K
        return (GA * GB * x * x - 36) / (6 * (GA + GB)) - x / math.tan(x)
    for _ in range(200):
        mid = (lo + hi) / 2
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def K_braced(GA, GB):
    """對位圖（無側移）：GA·GB/4·x² + (GA+GB)/2·(1 − x/tan x) + 2tan(x/2)/x − 1 = 0，x = π/K，0.5 ≤ K ≤ 1。"""
    def g(K):
        x = math.pi / K
        return GA * GB / 4 * x * x + (GA + GB) / 2 * (1 - x / math.tan(x)) + 2 * math.tan(x / 2) / x - 1
    lo, hi = 0.5000001, 0.9999999
    for _ in range(200):
        mid = (lo + hi) / 2
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ---- 第 9 章：線性殘留應力（翼板端 0.3Fy 壓 → 翼板中央 0.3Fy 拉；腹板取 0），完全彈塑性
# e = Eε/Fy（外加均勻應變換算的應力），翼板由端部往內降伏
RC = 0.3
AF = 0.8   # 翼板面積占全斷面比例（H400×400 約 0.78）


def yielded_frac(e, rc=RC):
    """每半片翼板由端部降伏的比例 u（0~1）。"""
    if e <= 1 - rc:
        return 0.0
    return min(1.0, (e - (1 - rc)) / (2 * rc))


def f_avg(e, rc=RC, n=400):
    """平均壓應力 P/A ÷ Fy。"""
    fl = sum(min(1.0, e + rc - 2 * rc * (i + 0.5) / n) for i in range(n)) / n
    return AF * fl + (1 - AF) * min(1.0, e)


def Ie_ratio(e, axis='y', rc=RC):
    u = yielded_frac(e, rc)
    return (1 - u) ** 3 if axis == 'y' else (1 - u)


def tm_curve(axis='y', rc=RC, n=400):
    """切線模數柱曲線：平均應力 f = (Ie/I)/λ² → λ = √((Ie/I)/f)。回傳 [(λ, f)]，含彈性段。"""
    pts = []
    for i in range(n + 1):
        e = 0.15 + (1 + rc - 0.15) * i / n
        r = Ie_ratio(e, axis, rc)
        fa = f_avg(e, rc)
        if r <= 1e-9:
            continue
        pts.append((math.sqrt(r / fa), fa))
    pts.append((0.0, 1.0))
    return sorted(pts)


# ---- SS-2024-1（塊狀殘留應力 0.5Fy、RH400×400×13×21、強軸）
SS2024 = dict(Ix=66600.0, dI=8568.0)
SS2024['IeIx'] = (SS2024['Ix'] - 4 * SS2024['dI']) / SS2024['Ix']
SS2024['l1'] = math.sqrt(SS2024['IeIx'])
SS2024['l2'] = math.sqrt(SS2024['IeIx'] / 0.5)
SS2024['l3'] = math.sqrt(2)


def ss2024_curve(l):
    r = SS2024['IeIx']
    if l <= SS2024['l1']:
        return 1.0
    if l <= SS2024['l2']:
        return r / l ** 2
    if l <= SS2024['l3']:
        return 0.5
    return 1 / l ** 2


# ---- 第 11 章：板的挫屈
NU = 0.3


def plate_coef(k):
    """板 Fcr = Fy 時的 (b/t)/√(E/Fy) 理論值 = √(kπ²/12(1−ν²))"""
    return math.sqrt(k * math.pi ** 2 / (12 * (1 - NU ** 2)))


LAMR = [('軋製 I 型鋼翼板 b_f/2t_f', '非加勁', 0.56, 0.425), ('單角鋼肢', '非加勁', 0.45, 0.425),
        ('T 型鋼腹板 d/t', '非加勁', 0.75, None), ('I 型鋼腹板 h/t_w', '加勁', 1.49, 4.0), ('箱型壁 b/t', '加勁', 1.40, 4.0)]


if __name__ == '__main__':
    print('---- compression')
    for G in (0, 0.5, 1, 2, 5, 10):
        print('G', G, 'sway', round(K_sway(max(G, 1e-6), max(G, 1e-6)), 3), 'braced', round(K_braced(max(G, 1e-6), max(G, 1e-6)), 3))
    print('sway G=1,10', K_sway(1, 10), 'braced 1,10', K_braced(1, 10))
    print('Ie y at .85', Ie_ratio(0.85), 'x', Ie_ratio(0.85, 'x'))
    print(SS2024)
    print('plate k=4', plate_coef(4), 'k=.425', plate_coef(0.425))
    ex = example(); print({k: round(v, 3) for k, v in ex.items()})
