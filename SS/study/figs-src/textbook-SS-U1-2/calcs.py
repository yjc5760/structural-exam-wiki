# -*- coding: utf-8 -*-
"""教科書講義 SS-U1-2 梁桿件 的所有數值（圖與內文共用，先算再寫）。單位 tf、cm（SS-2012-1 保留原題 SI）。

python3 calcs.py  → 印出全部數值，與內文逐一對帳。
"""
import math

E = 2040.0      # tf/cm²
G = 790.0       # tf/cm²
NU = 0.3
PHI_B = 0.90


# ───────────────────────── 通用：板斷面（矩形條）組成的斷面 ─────────────────────────
# 斷面用一串矩形 (b, h, y_bot) 表示，y 自底緣量起。

def props(rects):
    A = sum(b * h for b, h, y in rects)
    ybar = sum(b * h * (y + h / 2) for b, h, y in rects) / A
    I = sum(b * h ** 3 / 12 + b * h * (y + h / 2 - ybar) ** 2 for b, h, y in rects)
    top = max(y + h for b, h, y in rects)
    ct, cb = top - ybar, ybar
    # PNA：由底往上累加面積到 A/2
    target = A / 2
    yp = None
    for b, h, y in sorted(rects, key=lambda r: r[2]):
        a = b * h
        if a >= target:
            yp = y + target / b
            break
        target -= a
    Z = 0.0
    for b, h, y in rects:   # 對 PNA 取 |一次矩|，跨 PNA 的矩形切兩段
        lo, hi = y, y + h
        if hi <= yp:
            Z += b * h * (yp - (lo + hi) / 2)
        elif lo >= yp:
            Z += b * h * ((lo + hi) / 2 - yp)
        else:
            Z += b * (yp - lo) ** 2 / 2 + b * (hi - yp) ** 2 / 2
    return dict(A=A, ybar=ybar, I=I, ct=ct, cb=cb, St=I / ct, Sb=I / cb,
                Smin=min(I / ct, I / cb), yp=yp, Z=Z, top=top)


def H_rects(d, bf, tw, tf, bf2=None, tf2=None):
    """對稱或非對稱 H：上翼 bf×tf、下翼 bf2×tf2、腹板 tw×(d−tf−tf2)。"""
    bf2 = bf if bf2 is None else bf2
    tf2 = tf if tf2 is None else tf2
    hw = d - tf - tf2
    return [(bf2, tf2, 0.0), (tw, hw, tf2), (bf, tf, tf2 + hw)]


def M_phi(rects, Fy, phi_ratio, n=4000):
    """彈性–完全塑性材料，對稱斷面的 M(φ)/My 曲線（φ_ratio = φ/φy）。數值積分。"""
    p = props(rects)
    c = p['ct']
    M = 0.0
    for b, h, y in rects:
        for i in range(n):
            yy = y + (i + 0.5) * h / n - p['ybar']     # 距中性軸
            eps_ratio = phi_ratio * yy / c            # ε/εy
            s = max(-1.0, min(1.0, eps_ratio)) * Fy
            M += s * b * h / n * yy
    return M / (Fy * p['St'])


def rect_Mphi(phi_ratio):
    """矩形斷面解析式：M/My = 1.5(1 − (φy/φ)²/3)，φ ≥ φy。"""
    if phi_ratio <= 1:
        return phi_ratio
    return 1.5 * (1 - 1 / (3 * phi_ratio ** 2))


# ───────────────────────── 局部挫屈：板的「推歪＝拉回」 ─────────────────────────

def plate_coef(k):
    """Fcr = Fy 時的 b/t ÷ √(E/Fy) = √(kπ²/(12(1−ν²)))"""
    return math.sqrt(k * math.pi ** 2 / (12 * (1 - NU ** 2)))


K_PLATE = {   # 彈性板挫屈係數（材料力學／板理論的標準值）
    '一邊自由（懸臂翼板）': 0.425,
    '兩邊簡支、均勻受壓（柱腹板）': 4.0,
    '兩邊簡支、純彎曲（梁腹板）': 23.9,
}

LIM = dict(fp=17.0, fr=25.0, wp=170.0, wr=260.0, cwr=68.0)   # ×1/√Fy（tf/cm²）


def lim_coef(c):        # 把 17/√Fy 換成 □√(E/Fy) 的 □
    return c / math.sqrt(E)


def asd_flb(lam, Fy):
    """ASD 非結實翼板（台灣 ASD 對應式）：0.66Fy 與 0.60Fy 之間的直線。"""
    lp, lr = LIM['fp'] / math.sqrt(Fy), LIM['fr'] / math.sqrt(Fy)
    if lam <= lp:
        return 0.66 * Fy
    if lam >= lr:
        return 0.60 * Fy
    return 0.66 * Fy - 0.06 * Fy * (lam - lp) / (lr - lp)


def asd_flb_code(lam, Fy):
    return Fy * (0.79 - 0.0076 * lam * math.sqrt(Fy))


# ───────────────────────── 貫穿範例：SS-2007-3 H700×200×12×25 ─────────────────────────
EX = dict(d=70.0, bf=20.0, tw=1.2, tf=2.5, Fy=3.5, Fr=1.16,
          # 題給斷面性質
          A=178.0, ry=4.33, Zx=4642.5, Sx=4040.6, Ix=141421.0, Iy=3343.0,
          J=245.77, Cw=3807536.63)


def example():
    d = dict(EX)
    r = H_rects(d['d'], d['bf'], d['tw'], d['tf'])
    p = props(r)
    d['Zx_calc'] = p['Z']; d['Ix_calc'] = p['I']; d['Sx_calc'] = p['St']
    d['h'] = d['d'] - 2 * d['tf']
    d['Zf'] = d['bf'] * d['tf'] * (d['d'] - d['tf'])          # 兩翼板
    d['Zw'] = d['tw'] * d['h'] ** 2 / 4                       # 腹板
    d['f'] = d['Zx'] / d['Sx']
    d['Mp'] = d['Fy'] * d['Zx']
    d['My'] = d['Fy'] * d['Sx']
    d['Mr'] = (d['Fy'] - d['Fr']) * d['Sx']
    d['phiMp'] = PHI_B * d['Mp']
    d['lf'] = d['bf'] / (2 * d['tf']); d['lpf'] = 17 / math.sqrt(d['Fy']); d['lrf'] = 25 / math.sqrt(d['Fy'])
    d['lw'] = d['h'] / d['tw']; d['lpw'] = 170 / math.sqrt(d['Fy']); d['lrw'] = 260 / math.sqrt(d['Fy'])
    d['lpw_pd'] = 138 / math.sqrt(d['Fy'])                   # 考卷 96 年印的耐震值（fa=0）
    d['Ma_asd'] = 0.66 * d['Fy'] * d['Sx']
    d['asd_ratio'] = (d['phiMp'] / 1.5) / d['Ma_asd']
    # LTB（第 4 章用；先算好）
    FL = d['Fy'] - d['Fr']; d['FL'] = FL
    d['X1'] = math.pi / d['Sx'] * math.sqrt(E * G * d['J'] * d['A'] / 2)
    d['X2'] = 4 * d['Cw'] / d['Iy'] * (d['Sx'] / (G * d['J'])) ** 2
    d['Lp'] = 80 * d['ry'] / math.sqrt(d['Fy'])
    d['Lr'] = d['ry'] * d['X1'] / FL * math.sqrt(1 + math.sqrt(1 + d['X2'] * FL ** 2))
    Lb = 500.0
    d['Mn5'] = d['Mp'] - (d['Mp'] - d['Mr']) * (Lb - d['Lp']) / (d['Lr'] - d['Lp'])
    Lb = 800.0; s = Lb / d['ry']
    d['Mcr8_cb1'] = d['Sx'] * d['X1'] * math.sqrt(2) / s * math.sqrt(1 + d['X1'] ** 2 * d['X2'] / (2 * s ** 2))
    d['Mn8'] = min(1.7 * d['Mcr8_cb1'], d['Mp'])
    return d


# ───────────────────────── 其他範例 ─────────────────────────

def ex_2025_1():
    """SS-2025-1 銲接 H：bf30 tf1.5 hw42 tw1.5，Fy=2.5，完全側撐。"""
    bf, tf, hw, tw, Fy = 30.0, 1.5, 42.0, 1.5, 2.5
    d = hw + 2 * tf
    p = props(H_rects(d, bf, tw, tf))
    o = dict(bf=bf, tf=tf, hw=hw, tw=tw, Fy=Fy, d=d, A=p['A'])
    o['Zf'] = 2 * bf * tf * (hw / 2 + tf / 2)
    o['Zw'] = 2 * (hw / 2) * tw * (hw / 4)
    o['Zx'] = o['Zf'] + o['Zw']
    o['Zx_check'] = p['Z']
    o['Ix'] = p['I']; o['Sx'] = p['St']
    o['f'] = o['Zx'] / o['Sx']
    o['My'] = Fy * o['Sx']; o['Mp'] = Fy * o['Zx']; o['phiMp'] = PHI_B * o['Mp']
    o['lf'] = bf / (2 * tf); o['lpf'] = 17 / math.sqrt(Fy)
    o['lw'] = hw / tw; o['lpw'] = 170 / math.sqrt(Fy)
    o['Ma_asd'] = 0.66 * Fy * o['Sx']
    return o


def ex_2023_3():
    """SS-2023-3 非對稱 I：上翼 50×5、腹 100×2、下翼 30×5，Fy=2.5。"""
    r = [(30.0, 5.0, 0.0), (2.0, 100.0, 5.0), (50.0, 5.0, 105.0)]
    p = props(r)
    o = dict(p)
    o['Fy'] = 2.5
    o['My'] = o['Fy'] * p['Smin']; o['Mp'] = o['Fy'] * p['Z']; o['f'] = o['Mp'] / o['My']
    # 半面積法：A/2 × (壓側形心距 + 拉側形心距)
    yp = p['yp']
    up = [(250.0, 107.5), (2.0 * (105 - yp), (yp + 105) / 2)]
    lo = [(150.0, 2.5), (2.0 * (yp - 5), (yp + 5) / 2)]
    o['yc'] = sum(a * (y - yp) for a, y in up) / sum(a for a, y in up)
    o['yt'] = sum(a * (yp - y) for a, y in lo) / sum(a for a, y in lo)
    o['Z_half'] = p['A'] / 2 * (o['yc'] + o['yt'])
    o['gap'] = yp - p['ybar']
    return o


def ex_2012_1():
    """SS-2012-1 W14×90，A572 Gr.50（SI，原題單位）：非結實翼板 FLB。"""
    Fy, Fr = 350.0, 69.0
    Sx, Zx = 2343350.0, 2572769.0          # mm³
    bf, tf = 368.0, 18.0
    lp, lr = 9.19, 22.3                     # 題給
    o = dict(Fy=Fy, Fr=Fr, Sx=Sx, Zx=Zx, bf=bf, tf=tf, lp=lp, lr=lr)
    o['Mp'] = Fy * Zx / 1e6; o['Mr'] = (Fy - Fr) * Sx / 1e6        # kN·m
    o['lf'] = bf / (2 * tf)
    o['ratio'] = (o['lf'] - lp) / (lr - lp)
    o['Mn'] = o['Mp'] - (o['Mp'] - o['Mr']) * o['ratio']
    o['phiMn'] = PHI_B * o['Mn']
    o['drop'] = 1 - o['Mn'] / o['Mp']
    return o


def ex_rect():
    p = props([(10.0, 20.0, 0.0)])
    return dict(S=p['St'], Z=p['Z'], f=p['Z'] / p['St'])


def kratio():
    """SS-2016-1：梁腹板 vs 柱腹板 λr 的比，彈性板理論 vs 規範。"""
    th = math.sqrt(K_PLATE['兩邊簡支、純彎曲（梁腹板）'] / K_PLATE['兩邊簡支、均勻受壓（柱腹板）'])
    code = LIM['wr'] / LIM['cwr']
    return th, code


# ═════════════════════════ 第 3～7 章：LTB、Cb、ASD ═════════════════════════

def mcr_basic(Lb, Iy, J, Cw, Cb=1.0, Eval=E, Gval=G):
    """彈性 LTB 臨界彎矩（教科書形式）：Mcr = Cb (π/Lb)√(E Iy G J + (πE/Lb)² Iy Cw)。"""
    sv = Eval * Iy * Gval * J                       # 聖維南扭轉項
    wp = (math.pi * Eval / Lb) ** 2 * Iy * Cw        # 翹曲項
    return Cb * math.pi / Lb * math.sqrt(sv + wp), Cb * math.pi / Lb * math.sqrt(sv), Cb * math.pi / Lb * math.sqrt(wp)


def mcr_x(Lb, Sx, X1, X2, ry, Cb=1.0):
    s = Lb / ry
    return Cb * Sx * X1 * math.sqrt(2) / s * math.sqrt(1 + X1 ** 2 * X2 / (2 * s ** 2))


def mn_ltb(Lb, Mp, Mr, Lp, Lr, Sx, X1, X2, ry, Cb=1.0):
    if Lb <= Lp:
        return Mp
    if Lb <= Lr:
        return min(Mp, Cb * (Mp - (Mp - Mr) * (Lb - Lp) / (Lr - Lp)))
    return min(Mp, mcr_x(Lb, Sx, X1, X2, ry, Cb))


def ex_ltb():
    d = example()
    o = dict(d)
    m, sv, wp = mcr_basic(800.0, d['Iy'], d['J'], d['Cw'])
    o['Mcr8_basic'], o['Mcr8_sv'], o['Mcr8_wp'] = m, sv, wp
    o['Mcr8_x'] = mcr_x(800.0, d['Sx'], d['X1'], d['X2'], d['ry'])
    o['ratio5'] = (500 - d['Lp']) / (d['Lr'] - d['Lp'])
    o['Lp_coef'] = 80 / math.sqrt(E)                 # 80/√Fy = c·√(E/Fy) 的 c
    o['Mcr_at_Lr'] = mcr_x(d['Lr'], d['Sx'], d['X1'], d['X2'], d['ry'])   # 應等於 Mr
    o['Mn8_cb1'] = mcr_x(800.0, d['Sx'], d['X1'], d['X2'], d['ry'])
    o['wrong5'] = d['Mp'] - (d['Mp'] - d['Mr']) * (500 - d['Lp']) / (d['Lr'] - 500)   # 分母印錯
    return o


def ex_2008_3():
    E8, G8 = 2100.0, 840.0
    Sx, Zx, ry, A, Iy, J, Cw, Fy, Fr = 2802.0, 3212.0, 4.65, 156.77, 3388.0, 181.0, 2317464.0, 3.5, 0.69
    X1 = math.pi / Sx * math.sqrt(E8 * G8 * J * A / 2)
    X2 = 4 * Cw / Iy * (Sx / (G8 * J)) ** 2
    FL = Fy - Fr
    Lp = 80 * ry / math.sqrt(Fy)
    Lr = ry * X1 / FL * math.sqrt(1 + math.sqrt(1 + X2 * FL ** 2))
    Mcr = mcr_x(600.0, Sx, X1, X2, ry)
    o = dict(Mp=Fy * Zx, Mr=FL * Sx, X1=X1, X2=X2, Lp=Lp, Lr=Lr, Mcr=Mcr, Cb=1.0)
    o['phiMn'] = PHI_B * Mcr
    o['w'] = o['phiMn'] / 100 / 18          # 18w = M_max（t·m）
    return o


def ex_2024_3():
    Mp, Mr, Lp, Lr = 7285.0, 4608.0, 374.0, 1168.0
    Cb = cb_quarter(42, 21, 42, 21)
    raw = Cb * (Mp - (Mp - Mr) * (600 - Lp) / (Lr - Lp))
    o = dict(Mp=Mp, Mr=Mr, Lp=Lp, Lr=Lr, Cb=Cb, raw=raw, Mn=min(raw, Mp))
    o['phiMn'] = PHI_B * o['Mn'] / 100
    o['Mny'] = min(2.35 * 823.7, 1.5 * 2.35 * 540.3)
    o['phiMny'] = PHI_B * o['Mny'] / 100
    o['Mu'] = 42.0
    return o


EX25_3 = dict(Mp=21871.0, Mr=15760.0, Lp=340.0, Lr=1050.0, Lb=300.0)


def cb_quarter(Mmax, MA, MB, MC):
    return min(3.0, 12.5 * Mmax / (2.5 * Mmax + 3 * MA + 4 * MB + 3 * MC))


def cb_from_fn(mfun):
    """mfun(t), t∈[0,1] 為無側撐段內的彎矩分布；取絕對值。"""
    xs = [i / 400 for i in range(401)]
    Mmax = max(abs(mfun(t)) for t in xs)
    return cb_quarter(Mmax, abs(mfun(0.25)), abs(mfun(0.5)), abs(mfun(0.75)))


CB_CASES = [
    ('均勻彎矩', lambda t: 1.0),
    ('簡支均佈', lambda t: 4 * t * (1 - t)),
    ('簡支跨中集中', lambda t: 1 - abs(2 * t - 1)),
    ('一端彎矩、一端 0', lambda t: 1 - t),
    ('兩端等值反向（雙曲率）', lambda t: 1 - 2 * t),
]


def cb_old(r):
    """舊版三項式，r = M1/M2（同曲率為負）。"""
    return min(2.3, 1.75 + 1.05 * r + 0.3 * r ** 2)


# ── ASD ──
def rT_of(bf, tf, h, tw):
    """壓翼板＋1/3 受壓腹板（＝h/6 高）組成的 T 形斷面對腹板軸的迴轉半徑。"""
    Af, Aw6 = bf * tf, h / 6 * tw
    I = tf * bf ** 3 / 12 + (h / 6) * tw ** 3 / 12
    return math.sqrt(I / (Af + Aw6))


def asd_fb(Lb, Fy, rT, d_Af, Cb=1.0, compact=True, Lc=None):
    """ASD 容許撓曲應力（tf/cm²）。Lb ≤ Lc → 0.66Fy（結實）；否則三式取大，且 ≤ 0.6Fy。"""
    if Lc is not None and Lb <= Lc and compact:
        return 0.66 * Fy
    lam = Lb / rT
    lo, hi = math.sqrt(7170 * Cb / Fy), math.sqrt(35860 * Cb / Fy)
    if lam <= lo:
        f1 = 0.6 * Fy
    elif lam <= hi:
        f1 = (2 / 3 - Fy * lam ** 2 / (107600 * Cb)) * Fy
    else:
        f1 = 12000 * Cb / lam ** 2
    f3 = 840 * Cb / (Lb * d_Af)
    return min(0.6 * Fy, max(f1, f3))


def ex_asd():
    d = example()
    rT = rT_of(d['bf'], d['tf'], d['h'], d['tw'])
    Af = d['bf'] * d['tf']
    d_Af = d['d'] / Af
    Fy = d['Fy']
    Lc = min(20 * d['bf'] / math.sqrt(Fy), 1400 / (d_Af * Fy))
    Lu_tors = 840 * Af / (0.6 * Fy * d['d'])                 # 840/(Ld/Af)=0.6Fy
    Lu_par = math.sqrt((2 / 3 - 0.6) * 107600 / Fy) * rT     # 拋物線式 = 0.6Fy
    Lu = max(Lu_tors, Lu_par)
    o = dict(rT=rT, Af=Af, d_Af=d_Af, Lc=Lc, Lc1=20 * d['bf'] / math.sqrt(Fy), Lc2=1400 / (d_Af * Fy),
             Lu=Lu, Lu_tors=Lu_tors, Lu_par=Lu_par)
    Lb = 500.0
    lam = Lb / rT
    o['lam5'] = lam
    o['lo'] = math.sqrt(7170 / Fy); o['hi'] = math.sqrt(35860 / Fy)
    o['f_par5'] = (2 / 3 - Fy * lam ** 2 / 107600) * Fy
    o['f_tor5'] = 840 / (Lb * d_Af)
    o['Fb5'] = asd_fb(Lb, Fy, rT, d_Af, 1.0, True, Lc)
    o['Ma5'] = o['Fb5'] * d['Sx']
    o['lrfd5_15'] = PHI_B * d['Mn5'] / 1.5
    o['ratio5'] = o['Ma5'] / o['lrfd5_15']
    o['euler_fs'] = math.pi ** 2 * E / (5 / 3)               # 12000 的由來
    return o


def ex_2002_2():
    Fy, Sx, L, w = 2.5, 1373.0, 14.0, 0.097
    Fb = 0.66 * Fy
    Ma = Fb * Sx / 100                       # tf·m
    P = (Ma - w * L ** 2 / 8) / (L / 4)
    return dict(Fb=Fb, Ma=Ma, Mw=w * L ** 2 / 8, P=P)


# ═════════════════════════ 第 8～13 章 ═════════════════════════

def vn_ratio(hw_tw, kv, Fy):
    """V_n / (0.6 F_y A_w)。"""
    a = 50 * math.sqrt(kv / Fy); b = 62 * math.sqrt(kv / Fy)
    if hw_tw <= a:
        return 1.0
    if hw_tw <= b:
        return a / hw_tw
    return 1860 * kv / hw_tw ** 2 / (0.6 * Fy)


def kv_of(a_h):
    return 5.0 if a_h is None or a_h > 3 else 5 + 5 / a_h ** 2


def ex_shear():
    d = example()
    Aw = d['d'] * d['tw']
    lam = d['h'] / d['tw']
    o = dict(Aw=Aw, lam=lam, lim1=50 * math.sqrt(5 / d['Fy']), lim2=62 * math.sqrt(5 / d['Fy']))
    o['Vn'] = 0.6 * d['Fy'] * Aw * vn_ratio(lam, 5, d['Fy'])
    o['phiVn'] = 0.9 * o['Vn']
    o['tau_coef'] = math.pi ** 2 * E / (12 * (1 - NU ** 2))     # ≈1844 → 規範 1860
    o['ratio_62_50'] = 62 / 50
    # 張力場示例：h/tw=150、Fy=3.5、a/h=1
    kv = kv_of(1.0); Cv = vn_ratio(150, kv, 3.5)
    o['tf_kv'] = kv; o['tf_Cv'] = Cv
    o['tf_ratio'] = Cv + (1 - Cv) / (1.15 * math.sqrt(2))
    return o


def ex_2019_4():
    V, Q, I = 50.0, 1153.5, 75510.0
    q = V * Q / I
    s = 15.0
    Fs = q * s
    te = 0.707 * 0.8
    phiRn = 2 * 0.75 * 0.6 * 4.9 * te
    return dict(q=q, Fs=Fs, te=te, phiRn=phiRn, L=Fs / phiRn)


def ex_defl():
    o = {}
    o['c_uniform'] = 5 / 384
    o['c_center'] = 1 / 48
    o['c_third'] = 23 / 648
    # SS-2015-1：P_L=35 tf 三分點，L=840 cm，I=404,726 cm⁴
    P, L, I = 35.0, 840.0, 404726.0
    o['d2015'] = 23 * P * L ** 3 / (648 * E * I)
    o['lim2015'] = L / 360
    o['use2015'] = o['d2015'] / o['lim2015']
    o['flex2015'] = 230.72 / 233.78
    o['shear2015'] = 82.4 / 224.9
    return o


def ex_weak():
    d = example()
    Zy = 2 * d['tf'] * d['bf'] ** 2 / 4 + d['h'] * d['tw'] ** 2 / 4
    Sy = d['Iy'] / (d['bf'] / 2)
    o = dict(Zy=Zy, Sy=Sy, fy=Zy / Sy, Mpy=d['Fy'] * Zy, cap=1.5 * d['Fy'] * Sy)
    o['Mny'] = min(o['Mpy'], o['cap'])
    o['strong_weak'] = d['Mp'] / o['Mny']
    # SS-2014-3（SI）
    o['i2014'] = 400 / 945.8 + 50 / 171.1
    o['zy_sy_2014'] = 568631 / 362154
    return o


def ex_comp():
    be, ts, fc, Fy = 250.0, 15.0, 0.21, 2.5
    As = 2 * 20 * 1.6 + 46.8 * 1.0
    T = As * Fy
    Cmax = 0.85 * fc * be * ts
    a = T / (0.85 * fc * be)
    arm = ts + 25 - a / 2
    Mn = T * arm
    return dict(As=As, T=T, Cmax=Cmax, a=a, arm=arm, Mn=Mn, phiMn=0.9 * Mn, Ms=None)


def ex_plastic():
    c = 6 + 4 * math.sqrt(2)
    o = dict(c=c, xi=2 - math.sqrt(2))
    o['wu2005'] = c * 1668.6 / 600 ** 2 * 100          # tf/m
    o['wu2020'] = c * 11560.0 / 800 ** 2 * 100
    return o


def wu_curve(xi):
    """一端固定一端簡支，鉸距固定端 ξL：w_u L²/M_p = 2(2−ξ)/(ξ(1−ξ))。"""
    return 2 * (2 - xi) / (xi * (1 - xi))


def ex_synth():
    """上冊綜合重建：H700，Lb = 3 m，Cb = 1.136（簡支均佈）。"""
    d = example(); a = ex_asd()
    Cb = 1.136
    r = (300 - d['Lp']) / (d['Lr'] - d['Lp'])
    raw = Cb * (d['Mp'] - (d['Mp'] - d['Mr']) * r)
    Mn = min(raw, d['Mp'])
    lam = 300 / a['rT']
    fpar = (2 / 3 - d['Fy'] * lam ** 2 / 107600) * d['Fy']
    ftor = 840 / (300 * a['d_Af'])
    Fb = asd_fb(300, d['Fy'], a['rT'], a['d_Af'], 1.0, True, a['Lc'])
    return dict(r=r, raw=raw, Mn=Mn, phiMn=PHI_B * Mn, lam=lam, fpar=fpar, ftor=ftor, Fb=Fb, Ma=Fb * d['Sx'])


def ex_tau():
    """H700：腹板中性軸處 τ = VQ/(I t) 與平均 V/(d t_w) 的比。"""
    d = example()
    Q = d['Zx'] / 2
    return dict(Q=Q, peak=Q / (d['Ix'] * d['tw']), avg=1 / (d['d'] * d['tw']), ratio=Q / (d['Ix'] * d['tw']) * d['d'] * d['tw'])


def ex_synth2():
    """下冊綜合：H700 簡支 10 m、全側撐，w_D = 2、w_L = 3 tf/m。"""
    d = example(); sh = ex_shear()
    L = 10.0
    wu = 1.2 * 2 + 1.6 * 3
    Mu = wu * L ** 2 / 8; Vu = wu * L / 2
    dl = 5 * 0.03 * (L * 100) ** 4 / (384 * E * d['Ix'])
    return dict(wu=wu, Mu=Mu, phiMp=PHI_B * d['Mp'] / 100, uM=Mu / (PHI_B * d['Mp'] / 100), Vu=Vu, phiVn=sh['phiVn'],
                uV=Vu / sh['phiVn'], dl=dl, lim=L * 100 / 360, uD=dl / (L * 100 / 360))


if __name__ == '__main__':
    d = example()
    print('== 貫穿範例 H700×200×12×25 (SS-2007-3)')
    for k in ('Zx_calc', 'Zf', 'Zw', 'Ix_calc', 'Sx_calc', 'f', 'Mp', 'My', 'Mr', 'phiMp', 'lf', 'lpf', 'lrf',
              'h', 'lw', 'lpw', 'lrw', 'lpw_pd', 'Ma_asd', 'asd_ratio', 'X1', 'X2', 'Lp', 'Lr', 'Mn5', 'Mcr8_cb1', 'Mn8'):
        print(f'  {k:10s} {d[k]:.4f}')
    print('  φMn(5m)', PHI_B * d['Mn5'], ' φMn(8m)', PHI_B * d['Mn8'])
    print('== SS-2025-1'); [print(f'  {k:8s} {v:.4f}') for k, v in ex_2025_1().items()]
    print('== SS-2023-3'); [print(f'  {k:8s} {v:.4f}') for k, v in ex_2023_3().items()]
    print('== SS-2012-1'); [print(f'  {k:8s} {v:.4f}') for k, v in ex_2012_1().items()]
    print('== 矩形', ex_rect())
    print('== 板係數'); [print(f'  {k} k={v}  coef={plate_coef(v):.3f}') for k, v in K_PLATE.items()]
    print('  規範係數 ÷√E：', {k: round(lim_coef(v), 3) for k, v in LIM.items()})
    print('  λp/λr 翼', LIM['fp'] / LIM['fr'], ' 腹', LIM['wp'] / LIM['wr'])
    print('  2016-1 比：彈性理論 %.2f  規範 %.2f' % kratio())
    print('== ASD FLB 對照（Fy=3.5）')
    for lam in (9.087, 10.0, 11.5, 13.363):
        print(f'  λ={lam}: 內插 {asd_flb(lam,3.5)/3.5:.4f}Fy  規範式 {asd_flb_code(lam,3.5)/3.5:.4f}Fy')
    r = H_rects(70, 20, 1.2, 2.5)
    print('== M-φ H700:', [round(M_phi(r, 3.5, x), 4) for x in (1, 2, 4, 10)], ' 矩形:', [round(rect_Mphi(x), 4) for x in (1, 2, 4, 10)])
    print('== 第 3～7 章')
    for k, v in ex_ltb().items():
        if k.startswith(('Mcr', 'ratio5', 'Lp_coef', 'Mn8', 'wrong')):
            print(f'  {k:12s} {v:.4f}')
    print('  2008-3', {k: round(v, 4) for k, v in ex_2008_3().items()})
    print('  2024-3', {k: round(v, 4) for k, v in ex_2024_3().items()})
    print('  Cb', [(n, round(cb_from_fn(f), 3)) for n, f in CB_CASES])
    print('  Cb 舊式', [round(cb_old(r), 3) for r in (-1, 0, 1)])
    print('  ASD', {k: round(v, 4) for k, v in ex_asd().items()})
    print('  2002-2', {k: round(v, 4) for k, v in ex_2002_2().items()})
    print('== 第 8～13 章')
    print('  剪力', {k: round(v, 4) for k, v in ex_shear().items()})
    print('  2019-4', {k: round(v, 4) for k, v in ex_2019_4().items()})
    print('  撓度', {k: round(v, 5) for k, v in ex_defl().items()})
    print('  弱軸', {k: round(v, 4) for k, v in ex_weak().items()})
    print('  合成', {k: (round(v, 3) if v else v) for k, v in ex_comp().items()})
    print('  塑性', {k: round(v, 4) for k, v in ex_plastic().items()})
    print('  綜合', {k: round(v, 4) for k, v in ex_synth().items()})
    print('  τ', {k: round(v, 5) for k, v in ex_tau().items()})
    print('  綜合2', {k: round(v, 4) for k, v in ex_synth2().items()})
