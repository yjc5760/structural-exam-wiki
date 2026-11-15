# -*- coding: utf-8 -*-
"""RC-U4-2+U4-3+U4-4 批 1 盲解計算（2026-11-15）
現行台灣規範：建築物混凝土結構設計規範（內政部 2023 年版，ACI 318-19 世代）；kgf-cm 制。
本檔在打開任何舊解析之前寫定。

預力容許應力（kgf/cm² 制係數；SI 係數不可直接代 kgf 制，見 RC-U4-1 批 1 教訓）：
  傳遞階段：壓 0.60f'ci（簡支端部 0.70f'ci）；拉 0.8√f'ci（簡支端部 1.6√f'ci）
  使用階段：壓 0.45f'c（持續載重）、0.60f'c（全部載重）；U 類拉 ft ≤ 2.0√f'c；T 類 2.0～3.2√f'c
共同假設：混凝土單位重 2.4 tf/m³（考卷未給時）；正偏心 e = 形心以下。
"""
from math import sqrt, exp, pi
import numpy as np
from scipy.optimize import linprog

def P(*a): print(*a)

def rect(b, h):
    A = b * h; I = b * h**3 / 12; S = I / (h / 2)
    return A, I, S

def ecc_limits(b, h, L_m, Pi_t, eta, fci_, fc_, wL, gamma=2.4, label=""):
    """簡支矩形梁跨中偏心距上下限（傳遞 Pi＋自重；使用 Pe＋自重＋活載）。單位 kgf, cm"""
    A, I, S = rect(b, h)
    wG = b * h / 1e4 * gamma                      # tf/m
    MG = wG * L_m**2 / 8 * 1e5                    # kgf·cm
    ML = wL * L_m**2 / 8 * 1e5
    Pi = Pi_t * 1e3; Pe = eta * Pi
    fci = 0.60 * fci_; fti = 0.8 * sqrt(fci_)
    fcs_tot = 0.60 * fc_; fcs_sus = 0.45 * fc_; fts = 2.0 * sqrt(fc_)
    k = S / A
    # 傳遞 頂：Pi/A − Pi e/S + MG/S ≥ −fti  → e ≤ ...
    e1 = (Pi / A + fti + MG / S) * S / Pi
    # 傳遞 底：Pi/A + Pi e/S − MG/S ≤ fci → e ≤ ...
    e2 = (fci - Pi / A + MG / S) * S / Pi
    # 使用 頂（全部）：Pe/A − Pe e/S + (MG+ML)/S ≤ fcs → e ≥ ...
    e3 = (Pe / A + (MG + ML) / S - fcs_tot) * S / Pe
    # 使用 頂（持續：只自重）：Pe/A − Pe e/S + MG/S ≤ 0.45f'c → e ≥ ...
    e3s = (Pe / A + MG / S - fcs_sus) * S / Pe
    # 使用 底：Pe/A + Pe e/S − (MG+ML)/S ≥ −fts → e ≥ ...
    e4 = (-fts - Pe / A + (MG + ML) / S) * S / Pe
    P(f"--- {label}  A={A} I={I:.4g} S={S:.4g} kern={k:.2f}  wG={wG:.4f} tf/m")
    P(f"MG={MG/1e5:.3f} ML={ML/1e5:.3f} tf·m  Pi={Pi/1e3:.1f} Pe={Pe/1e3:.1f} tf")
    P(f"容許：fci={fci:.1f} fti={fti:.2f} fcs(全)={fcs_tot:.1f} fcs(持續)={fcs_sus:.1f} fts(U)={fts:.2f}")
    P(f"e ≤ {e1:.2f}（傳遞頂拉）； e ≤ {e2:.2f}（傳遞底壓）")
    P(f"e ≥ {e3:.2f}（使用頂壓 全）； e ≥ {e3s:.2f}（使用頂壓 持續）； e ≥ {e4:.2f}（使用底拉 U 類）")
    lo = max(e3, e3s, e4); hi = min(e1, e2)
    P(f"⇒ {lo:.2f} ≤ e ≤ {hi:.2f} cm（形心以下）；幾何上限 h/2−保護≈{h/2-10:.0f}（cgs 距底 10 cm 假設）")
    return dict(A=A, S=S, MG=MG, ML=ML, lo=lo, hi=hi, e=[e1, e2, e3, e3s, e4])

# ======================= RC-2010-4
P("=== RC-2010-4")
r = ecc_limits(50, 90, 15, 200, 0.85, 280, 350, 1.5, label="㈡ Pi=200 tf")
# 自重 0（只為對照）／單位重 2.5 對照
ecc_limits(50, 90, 15, 200, 0.85, 280, 350, 1.5, gamma=2.5, label="㈡ 對照 γ=2.5")

# ㈠ 直線（等偏心）vs 曲線鋼腱：以 x=Pi、y=Pi·e 線性規劃，求最大可加活載彎矩 ML
def max_ML(curved, b=50, h=90, L=15, eta=0.85, fci_=280, fc_=350, gamma=2.4, emax=None, fix_Pi=None):
    A, I, S = rect(b, h)
    MG = b * h / 1e4 * gamma * L**2 / 8 * 1e5
    fci, fti = 0.6 * fci_, 0.8 * sqrt(fci_)
    fci_end, fti_end = 0.7 * fci_, 1.6 * sqrt(fci_)
    fcs, fcsus, fts = 0.6 * fc_, 0.45 * fc_, 2.0 * sqrt(fc_)
    if emax is None: emax = h / 2 - 10
    # 變數 [x, y, M]，最大化 M → 最小化 −M
    Aub, bub = [], []
    def le(cx, cy, cm, rhs): Aub.append([cx, cy, cm]); bub.append(rhs)
    # 跨中 傳遞
    le(-1 / A, 1 / S, 0, fti + MG / S)            # 頂：x/A − y/S + MG/S ≥ −fti
    le(1 / A, 1 / S, 0, fci + MG / S)             # 底：x/A + y/S − MG/S ≤ fci
    # 跨中 使用
    le(eta / A, -eta / S, 1 / S, fcs - MG / S)    # 頂壓（全部）
    le(eta / A, -eta / S, 0, fcsus - MG / S)      # 頂壓（持續）
    le(-eta / A, -eta / S, 1 / S, fts - MG / S)   # 底拉
    le(-emax, 1, 0, 0)                            # y ≤ emax·x
    if not curved:                                # 直線：端部同偏心、M=0
        le(-1 / A, 1 / S, 0, fti_end)
        le(1 / A, 1 / S, 0, fci_end)
    bounds = [(0, None) if fix_Pi is None else (fix_Pi, fix_Pi), (None, None), (0, None)]
    res = linprog([0, 0, -1], A_ub=Aub, b_ub=bub, bounds=bounds)
    x, y, M = res.x
    return x / 1e3, y / x if x else 0, M / 1e5, MG / 1e5
for emax in (35, 39):
    s = max_ML(False, emax=emax); c = max_ML(True, emax=emax)
    P(f"㈠ 最佳化（Pi、e 皆可選，emax={emax}）：直線 Pi={s[0]:.1f} e={s[1]:.2f} ML={s[2]:.2f}；"
      f"曲線 Pi={c[0]:.1f} e={c[1]:.2f} ML={c[2]:.2f} tf·m；提升 ΔML={c[2]-s[2]:.2f} tf·m"
      f" = Δw {8*(c[2]-s[2])/15**2:.3f} tf/m（直線 {8*s[2]/225:.3f}→曲線 {8*c[2]/225:.3f} tf/m）")
s = max_ML(False, fix_Pi=200e3); c = max_ML(True, fix_Pi=200e3)
P(f"㈠ 固定 Pi=200 tf：直線 e={s[1]:.2f} ML={s[2]:.2f}；曲線 e={c[1]:.2f} ML={c[2]:.2f}；ΔML={c[2]-s[2]:.2f} tf·m"
  f"（η·MG={0.85*s[3]:.2f}）")
P(f"經典式：曲線鋼腱跨中偏心可多 ΔE=MG/Pi → 使用階段多抵 ηMG = {0.85*r['MG']/1e5:.2f} tf·m"
  f" ≈ {8*0.85*r['MG']/1e5/225:.3f} tf/m")
# 對照讀法：直線鋼腱 e=0（純軸壓）
s0 = max_ML(False, emax=1e-9)
P(f"㈠ 對照（直線 e=0）：Pi={s0[0]:.1f} ML={s0[2]:.2f}  vs 曲線 {max_ML(True)[2]:.2f}")

# ======================= RC-2025-4
P("\n=== RC-2025-4")
ecc_limits(40, 120, 12, 200, 0.85, 320, 420, 1.5, label="Pi=200 tf（含自重）")
ecc_limits(40, 120, 12, 200, 0.85, 320, 420, 1.5, gamma=0.0, label="對照：不計自重")

# ======================= RC-2015-4
P("\n=== RC-2015-4")
b, h, L = 30, 50, 12
A, I, S = rect(b, h); wG = b * h / 1e4 * 2.4; MG = wG * L**2 / 8 * 1e5
fca, fta = 140, 0
ML = (fca + fta) * S                         # η=1：頂/底應力範圍 = (fca+fta)
F = (fca + (-fta)) / 2 * A                    # 傳遞：頂 = −fta、底 = fca
Fe = (fca - F / A) * S + MG                   # 傳遞底：F/A + Fe/S − MG/S = fca
e = Fe / F
P(f"A={A} S={S:.0f} wG={wG:.3f} tf/m MG={MG/1e5:.3f} tf·m")
P(f"ML,max={ML/1e5:.3f} tf·m → wL,max={8*ML/1e5/L**2:.4f} tf/m；F={F/1e3:.1f} tf；ep={e:.2f} cm")
for nm, M in (("傳遞", MG), ("全載", MG + ML)):
    P(f"  {nm}：頂 {F/A - F*e/S + M/S:.2f}  底 {F/A + F*e/S - M/S:.2f}")
P(f"  幾何：鋼鍵距底 {h/2-e:.2f} cm；所需 f'ci ≥ {fca/0.6:.0f}（現行 0.6f'ci）；140 = 0.40f'c ≤ 0.45f'c 照用")
P(f"  對照（γ=2.5）：ep={((fca - F/A)*S + MG/2.4*2.5)/F:.2f}")

# ======================= RC-2020-4
P("\n=== RC-2020-4")
w = 1.6; Ls = 15.0; b, h = 50, 90; A, I, S = rect(b, h)
MB = -w * Ls**2 / 8; RA = 3 * w * Ls / 8
Mmid = RA * 7.5 - w * 7.5**2 / 2
Pe = abs(MB) / 0.35
eD = Mmid / Pe
P(f"MB={MB:.2f} tf·m RA={RA:.2f} M(7.5)={Mmid:.2f}；Pe=|MB|/0.35={Pe:.2f} tf；eD=eE={eD*100:.2f} cm")
P(f"均勻壓應力 Pe/A={Pe*1e3/A:.2f} kgf/cm²；跨內最大偏心 {RA**2/(2*w)/Pe*100:.2f} cm @ x={RA/w:.3f} m")
Pi = Pe / 0.8
top = Pi * 1e3 / A + Pi * 1e3 * 35 / S + MB * 1e5 / S
bot = Pi * 1e3 / A - Pi * 1e3 * 35 / S - MB * 1e5 / S
P(f"㈡ Pi={Pi:.2f} tf；B 上緣 {top:.2f}（壓）、下緣 {bot:.2f}（壓） kgf/cm²")

# ======================= RC-2024-4
P("\n=== RC-2024-4")
Pt = 120.0; Lb = 12.0
Mx = np.array([[0, 0, 1], [36, 6, 1], [144, 12, 1]], float)
a_, b_, c_ = np.linalg.solve(Mx, [-25, 15, 0])   # y(x) cm，下為正
P(f"y(x) = {a_:.5f}x² + {b_:.4f}x + {c_:.1f} (cm, x m)；頂點 x={-b_/(2*a_):.3f} m, y={c_-b_**2/(4*a_):.2f} cm")
wup = Pt * (-2 * a_) / 100
P(f"等值載重：向上均佈 {wup:.4f} tf/m；固定端錨碇彎矩 P·0.25={Pt*0.25:.1f} tf·m；端部垂直分力 左 {Pt*b_/100:.3f}、右 {Pt*abs(2*a_*12+b_)/100:.3f} tf")
xs = np.linspace(0, Lb, 120001)
y = a_ * xs**2 + b_ * xs + c_
M1 = -Pt * y / 100                                # tf·m（正＝正彎矩）
R = -3 / Lb**3 * np.trapezoid(M1 * (Lb - xs), xs)  # 輥支承二次反力（向上正）
M2 = R * (Lb - xs)
P(f"二次反力：輥支承 R_B={R:.4f} tf（{'向上' if R>0 else '向下'}）；固定端 V_A={-R:.4f} tf、M_A(二次)={R*Lb:.3f} tf·m")
# 交叉：解析式 R = −3/L³ ∫ M1(L−x)
yc = y - M2 / Pt * 100
P(f"C 線（距形心，下為正）：x=0 {yc[0]:.2f}、x=3 {np.interp(3,xs,yc):.2f}、x=6 {np.interp(6,xs,yc):.2f}、x=9 {np.interp(9,xs,yc):.2f}、x=12 {yc[-1]:.2f} cm")
P(f"總彎矩：x=0 {M1[0]+M2[0]:.3f}、x=6 {np.interp(6,xs,M1+M2):.3f} tf·m；二次彎矩 M2(0)={M2[0]:.3f}, M2(6)={np.interp(6,xs,M2):.3f}")
# 同位鋼腱：保留跨中 15 與輥端 0，改固定端偏心 e0 使 R=0
def R_of(e0):
    a, b, c = np.linalg.solve(Mx, [e0, 15, 0]); yy = a * xs**2 + b * xs + c
    return -3 / Lb**3 * np.trapezoid(-Pt * yy / 100 * (Lb - xs), xs)
from scipy.optimize import brentq
e0c = brentq(R_of, -60, 60)
P(f"同位鋼腱（保留中央 +15、輥端 0 的三點拋物線）：固定端偏心改為 {e0c:.2f} cm（{'形心上方' if e0c<0 else '形心下方'} {abs(e0c):.2f}）")
P(f"或直接把鋼腱放在 C 線上：固定端 {yc[0]:.2f}、中央 {np.interp(6,xs,yc):.2f}、輥端 0（線性轉換，C 線不變）")

# ======================= RC-2002-5
P("\n=== RC-2002-5")
mu, k = 0.4, 0.0026
seg = [("B", 5.35, 0.0), ("C", 7.60, 0.169), ("D", 5.35, 0.0), ("E", 3.20, 0.107)]
Lc = al = 0.0
for nm, l, a in seg:
    Lc += l; al += a; om = k * Lc + mu * al
    P(f"{nm}: Σl={Lc:.2f} m Σα={al:.3f} ω={om:.5f}  F/F1=e^-ω={exp(-om):.4f}  近似 1−ω={1-om:.4f}")
P(f"AE 損失 = {(1-exp(-om))*100:.2f}%（近似式 {om*100:.2f}%）")

# ======================= RC-2016-4
P("\n=== RC-2016-4")
b, h = 20, 60; A, I, S = rect(b, h); e = 15; Aps = 3.95; fpu = 19000; n = 6
fc_ = 350; fci_ = 0.7 * fc_
fpi = 0.7 * fpu; Pi = fpi * Aps
fcgs = Pi / A + Pi * e**2 / I
dES = n * fcgs
dES_x = n * fcgs / (1 + n * Aps * (1 / A + e**2 / I))
P(f"A={A} I={I:.0f} S={S:.0f} fpi={fpi:.0f} Pi={Pi:.0f} kgf")
P(f"fcgs(以 Pi)={fcgs:.2f} → ΔfpES = n·fcgs = {dES:.1f} kgf/cm²（{dES/fpi*100:.2f}%），ΔP={dES*Aps/1e3:.3f} tf")
P(f"精確（轉換斷面／放張後力）ΔfpES={dES_x:.1f}（{dES_x/fpi*100:.2f}%）")
fr = 2 * sqrt(fci_); fti = 0.8 * sqrt(fci_); fti_end = 1.6 * sqrt(fci_)
for nm, d in (("主（以 Pi）", dES), ("精確", dES_x)):
    P0 = (fpi - d) * Aps
    top = P0 / A - P0 * e / S; bot = P0 / A + P0 * e / S
    P(f"{nm}：P0={P0:.0f} kgf；頂 {top:.2f}、底 {bot:.2f} kgf/cm²（不計自重）")
P(f"f'ci={fci_:.0f}；fr=2√f'ci={fr:.2f}；現行傳遞拉 0.8√f'ci={fti:.2f}（端部 1.6√={fti_end:.2f}）；"
  f"壓 0.6f'ci={0.6*fci_:.1f}（端部 0.7f'ci={0.7*fci_:.1f}）")
P(f"對照 n=Es/Eci={2.04e6/(15000*sqrt(fci_)):.2f}（題給 n=6 照用）")

# ======================= RC-2019-4
P("\n=== RC-2019-4")
fc_ = 350; Ec = 15000 * sqrt(fc_); Eps = 1.97e6; n = Eps / Ec
K, mup = 0.0049, 0.25; fpj = 12300; Aps = 30.0; Pj = fpj * Aps
Lt = 36.0; half = Lt / 2
b, h = 40, 180; A, I, S = rect(b, h)
sag = {1: 0.30, 2: 1.05}
ecen = {1: 75, 2: 60}; eend = {1: 45, 2: -45}         # 形心以下為正
Pc = {}
for t in (1, 2):
    alpha = 4 * sag[t] / Lt
    om = K * half + mup * alpha
    Pc[t] = Pj * exp(-om)
    P(f"鋼腱{t}: 矢高 {sag[t]} m，端→中 α={alpha:.5f} rad，ω={om:.5f}，e^-ω={exp(-om):.5f}，P(中,摩擦後)={Pc[t]/1e3:.2f} tf")
P(f"Pj={Pj/1e3:.1f} tf；n=Eps/Ec={n:.4f}（Ec={Ec:.0f}）；A={A} I={I:.4g}")
def fc_at1(P2, e2, e1): return P2 / A + P2 * e2 * e1 / I
dfc_c = fc_at1(Pc[2], ecen[2], ecen[1]); dfc_e = fc_at1(Pj, eend[2], eend[1])
dP_c = n * dfc_c * Aps; dP_e = n * dfc_e * Aps
P(f"鋼腱2 施拉 → 鋼腱1 位置混凝土應力：跨中 {dfc_c:.2f}、端部 {dfc_e:.2f} kgf/cm²")
P(f"鋼腱1 彈性縮短：跨中 ΔP={dP_c/1e3:.3f} tf、端部 ΔP={dP_e/1e3:.3f} tf")
P(f"答（逐斷面）：P1,Cen={(Pc[1]-dP_c)/1e3:.2f}  P2,Cen={Pc[2]/1e3:.2f}  P1,End={(Pj-dP_e)/1e3:.2f}  P2,End={Pj/1e3:.2f} tf")
# 對照：未灌漿鋼腱沿全長平均應變（含鋼腱2 摩擦分布）
xs = np.linspace(-half, half, 36001)
def ecc(t, x): return eend[t] + (ecen[t] - eend[t]) * (1 - (x / half)**2)
def Pfr(t, x):
    alpha = 4 * sag[t] / Lt * (abs(x) / half) * 0 + (4 * sag[t] / Lt) * (half - abs(x)) / half
    return Pj * np.exp(-(K * (half - np.abs(x)) + mup * alpha))
P2x = Pfr(2, xs); fcx = P2x / A + P2x * ecc(2, xs) * ecc(1, xs) / I
avg = np.trapezoid(fcx, xs) / Lt
P(f"對照（平均應變法）：鋼腱1 位置平均 fc={avg:.2f} → ΔP={n*avg*Aps/1e3:.3f} tf（全長均一）")
P(f"   → P1,Cen={(Pc[1]-n*avg*Aps)/1e3:.2f}  P1,End={(Pj-n*avg*Aps)/1e3:.2f} tf")
# 自重彎矩對 fc 的影響不計入鋼腱1 損失（鋼腱1 施拉時自重已作用）

# ======================= RC-2022-3
P("\n=== RC-2022-3")
L = 20.0; gam = 2.4; fc_ = 420; fyt = 2800; Fe = 200e3
Ag = 45 * 20 * 2 + 17.5 * 50
Ig = 2 * (45 * 20**3 / 12 + 900 * 35**2) + 17.5 * 50**3 / 12
WG = Ag / 1e4 * gam; WD = 1.1; WE = 0.25 * (WG + WD); PL = 25.0
bw = 17.5; dp = max(90 - 12, 0.8 * 90); Av = 2 * 0.7133
fpc = Fe / Ag
Vcw = (0.93 * sqrt(fc_) + 0.3 * fpc) * bw * dp / 1e3
P(f"Ag={Ag} Ig={Ig:.1f} WG={WG:.4f} WE={WE:.4f} tf/m；dp={dp}；fpc={fpc:.2f}")
P(f"Vcw=(0.93√f'c+0.3fpc)bw dp + Vp(=0) = {Vcw:.2f} tf")
Vs_max = 2.12 * sqrt(fc_) * bw * dp / 1e3; Vs_half = 1.06 * sqrt(fc_) * bw * dp / 1e3
avmin = max(0.2 * sqrt(fc_), 3.5) * bw / fyt
for xc, nm in ((dp / 100, "x=dp"), (0.45, "x=h/2")):
    for cn, wu, pu in (("1.2D+1.6L", 1.2 * (WG + WD), 1.6 * PL),
                       ("1.2D+1.0E+1.0L", 1.2 * (WG + WD) + 1.0 * WE, 1.0 * PL),
                       ("1.4D", 1.4 * (WG + WD), 0.0),
                       ("(對照) 1.2(D+E)+1.6L", 1.2 * (WG + WD + WE), 1.6 * PL)):
        Vu = wu * (L / 2 - xc) + pu
        Vs = Vu / 0.75 - Vcw
        s = Av * fyt * dp / (Vs * 1e3) if Vs > 0 else float('inf')
        P(f"{nm} {cn}: Vu={Vu:.2f} tf  Vs需={Vs:.2f}  s={s:.2f} cm")
P(f"上限：Vs ≤ 1.06√f'c bw d={Vs_half:.2f} → s ≤ min(0.75h=67.5, 60)；Vs,max(2.12)={Vs_max:.2f}；"
  f"Av,min → s ≤ {Av/avmin:.1f} cm")
Vs15 = Av * fyt * dp / 15 / 1e3
P(f"原設計 D10@15：Vs={Vs15:.2f}，φVn=0.75(Vcw+Vs)={0.75*(Vcw+Vs15):.2f} tf")
