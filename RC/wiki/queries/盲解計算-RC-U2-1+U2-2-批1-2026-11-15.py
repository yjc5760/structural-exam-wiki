# -*- coding: utf-8 -*-
"""RC-U2-1／U2-2 批 1 盲解計算（2026-11-15）
現行台灣規範：建築物混凝土結構設計規範（內政部 2023 年版，ACI 318-19 世代），kgf-cm 制。
所用條文（kgf/cm² 換算係數）：
  Vc（Av≥Av,min）= [0.53λ√fc' + Nu/(6Ag)] bw d  或 [2.1λρw^(1/3)√fc' + Nu/(6Ag)] bw d；≤1.33λ√fc' bw d；Nu/(6Ag)≤0.05fc'
  Vs ≤ 2.12√fc' bw d；Vs>1.06√fc' bw d 時 s≤d/4、30；否則 s≤d/2、60
  Av,min/s = max(0.2√fc', 3.5) bw / fyt
  Tth = 0.27λ√fc' Acp²/pcp；Tcr = 4Tth；Tu<φTth 可忽略扭力
  Tn = 2 Ao At fyt cotθ / s，Ao = 0.85 Aoh，θ=45°
  斷面上限 √[(Vu/bwd)² + (Tu ph/1.7Aoh²)²] ≤ φ(Vc/bwd + 2.12√fc')
  Aℓ = (At/s) ph (fyt/fy) cot²θ；Aℓ,min = 較小者 {1.33√fc'Acp/fy − (At/s)ph fyt/fy, 1.33√fc'Acp/fy − (1.75bw/fyt)ph fyt/fy}
  (Av+2At)/s ≥ max(0.2√fc', 3.5) bw/fyt；s ≤ min(ph/8, 30)
  φ：剪力、扭力 0.75；撓曲 φ 依 εt（εty=fy/Es，壓力控制 ≤εty，拉力控制 ≥εty+0.003）
"""
from math import sqrt, atan, degrees, sin, cos, radians
import numpy as np

out = {}
def P(*a):
    print(*a)

# ---------------------------------------------------------------- RC-2006-1
P("=== RC-2006-1")
b, d, dp, As, Asp, fc, fy, Es = 30, 45, 8, 40, 24, 280, 4200, 2.04e6
b1 = 0.85; ecu = 0.003; ety = fy / Es
def forces(c):
    a = b1 * c
    esp = ecu * (c - dp) / c
    fsp = max(min(esp * Es, fy), -fy)
    Cc = 0.85 * fc * a * b
    Cs = Asp * (fsp - 0.85 * fc)            # 扣除被鋼筋取代的混凝土
    T = As * fy
    return Cc + Cs - T, a, fsp, Cc, Cs
lo, hi = 1, d
for _ in range(200):
    m = (lo + hi) / 2
    if forces(m)[0] > 0: hi = m
    else: lo = m
c = (lo + hi) / 2
_, a, fsp, Cc, Cs = forces(c)
Mn = Cc * (d - a / 2) + Cs * (d - dp)
et = ecu * (d - c) / c
phi_f = 0.65 if et <= ety else (0.90 if et >= ety + 0.003 else 0.65 + 0.25 * (et - ety) / 0.003)
phiMn = phi_f * Mn
L = 450
wu = 2 * phiMn / L**2           # kgf/cm
Vu_d = wu * (L - d); Vu_face = wu * L
lam = 1.0; sq = sqrt(fc)
Vc = 0.53 * sq * b * d
Av = 2 * 0.71
def s_req(Vu):
    Vs = Vu / 0.75 - Vc
    s = Av * fy * d / Vs
    smax = d / 4 if Vs > 1.06 * sq * b * d else d / 2
    return Vs, s, min(s, smax, Av * fy / (max(0.2 * sq, 3.5) * b))
P(f"c={c:.2f} a={a:.2f} fs'={fsp:.0f} Mn={Mn/1e5:.2f} tf-m εt={et:.5f} φ={phi_f:.3f} φMn={phiMn/1e5:.2f}")
P(f"wu={wu*100/1000:.3f} tf/m  Vu(d)={Vu_d/1000:.2f}  Vu(face)={Vu_face/1000:.2f}  Vc={Vc/1000:.2f}")
for lab, Vu in [("d", Vu_d), ("face", Vu_face)]:
    Vs, s, sg = s_req(Vu); P(f"  [{lab}] Vs={Vs/1000:.2f} s={s:.2f} 控制={sg:.2f}")
# 照考卷 φ=0.9 對照
wu9 = 2 * 0.9 * Mn / L**2
for lab, Vu in [("d", wu9 * (L - d)), ("face", wu9 * L)]:
    Vs, s, sg = s_req(Vu); P(f"  [φ=0.9 {lab}] Vu={Vu/1000:.2f} Vs={Vs/1000:.2f} s={s:.2f}")
# Vc 用 (b) 式對照
rw = As / (b * d); Vcb = 2.1 * rw**(1/3) * sq * b * d
P(f"  ρw={rw:.4f} Vc(b)={Vcb/1000:.2f}; s(d, Vc(b)) = {Av*fy*d/(Vu_d/0.75 - Vcb):.2f}")

# ---------------------------------------------------------------- RC-2009-3
P("=== RC-2009-3  STM")
fc = 250; b = 20; fy = 4200; Ast = 6 * 2.87
jd = 70 - 10 - 10; a_sh = 50
th = atan(jd / a_sh); P(f"θ={degrees(th):.2f}°")
# 每個 P 的分量：P/2 為支承反力
T_cap = Ast * fy                               # 拉桿
Pt = 2 * T_cap * jd / a_sh                     # T = (P/2)(a/jd)
fce = lambda bs, bn=None: 0.85 * (bs if bn is None else bn) * fc
# 水平壓桿（邊界壓桿 βs=1.0），寬 20
Ph = 2 * fce(1.0) * 20 * b * jd / a_sh
# 斜壓桿（內部壓桿、配置分布鋼筋 βs=0.75）
ws_sup = 20 * sin(th) + 20 * cos(th)           # 支承節點：承壓鈑 20、拉桿帶高 20
ws_load = 20 * sin(th) + 20 * cos(th)          # 載重節點：承壓鈑 20、水平壓桿 20
Fstrut = lambda P_: (P_ / 2) / sin(th)
Pd = 2 * sin(th) * fce(0.75) * min(ws_sup, ws_load) * b
# 節點面：支承 CCT βn=0.8；載重 CCC βn=1.0
Pn_sup_bear = 2 * fce(0, 0.8) * 20 * b
Pn_sup_tie = 2 * fce(0, 0.8) * 20 * b * jd / a_sh
Pn_load_bear = 2 * fce(0, 1.0) * 20 * b
Pn_sup_strut = 2 * sin(th) * fce(0, 0.8) * ws_sup * b
# 深梁尺寸上限（9.9.2.1）Vn ≤ 2.65√fc' bw d（不乘 φ），d=60
P_dim = 2 * 2.65 * sqrt(fc) * b * 60
for k, v in [("拉桿", Pt), ("水平壓桿", Ph), ("斜壓桿 βs=0.75", Pd), ("支承承壓面 βn=0.8", Pn_sup_bear),
             ("支承拉桿面", Pn_sup_tie), ("支承斜壓桿面 βn=0.8", Pn_sup_strut), ("載重承壓面 βn=1.0", Pn_load_bear),
             ("9.9.2.1 尺寸上限", P_dim)]:
    P(f"  {k}: P={v/1000:.1f} tf")
P(f"  ws={ws_sup:.2f} cm, fce斜={fce(0.75):.1f}")

# ---------------------------------------------------------------- RC-2010-3
P("=== RC-2010-3")
fc = 280; sq = sqrt(fc); b, d, h = 40, 52, 60; Ag = b * h
for lab, Nu in [("a 無軸力", 0), ("b 軸壓30", 30000), ("c 軸拉30", -30000)]:
    t = min(Nu / (6 * Ag), 0.05 * fc)
    Vc = max((0.53 * sq + t) * b * d, 0); Vc = min(Vc, 1.33 * sq * b * d)
    P(f"  {lab}: Nu/6Ag={t:.3f}  Vc={Vc/1000:.2f}  φVc={0.75*Vc/1000:.2f}")
# 舊規範簡化式對照
Vc0 = 0.53 * sq * b * d
P(f"  舊式：無 {0.75*Vc0/1000:.2f}；壓 {0.75*Vc0*(1+30000/(140*Ag))/1000:.2f}；拉 {0.75*Vc0*(1-30000/(35*Ag))/1000:.2f}"
  f"（φ=0.85：{0.85*Vc0/1000:.2f}／{0.85*Vc0*(1+30000/(140*Ag))/1000:.2f}／{0.85*Vc0*(1-30000/(35*Ag))/1000:.2f}）")

# ---------------------------------------------------------------- RC-2014-3
P("=== RC-2014-3")
b, d, h = 30, 60, 70; Ag = b * h; As = 24.42; L = 500; w = 50  # kgf/cm
x = d; Vu = w * (L / 2 - x); Mu = w * x * (L - x) / 2
rw = As / (b * d)
P(f"  Vu={Vu/1000:.2f} tf Mu={Mu/1e5:.3f} tf-m ρw={rw:.5f}")
for lab, Nu in [("無", 0), ("壓25", 25000), ("拉25", -25000)]:
    t = min(Nu / (6 * Ag), 0.05 * fc)
    Va = (0.53 * sq + t) * b * d; Vb = (2.1 * rw**(1/3) * sq + t) * b * d
    Vc = min(max(Va, Vb, 0), 1.33 * sq * b * d)
    P(f"  {lab}: (a)={Va/1000:.2f} (b)={Vb/1000:.2f} → Vc={Vc/1000:.2f}")
# 照考卷印出的 401-100 式子
r = min(Vu * d / Mu, 1)
V0 = min((0.5 * sq + 175 * rw * r) * b * d, 0.93 * sq * b * d)
Mm = Mu - 25000 * (4 * h - d) / 8
Vcomp_cap = 0.93 * sq * b * d * sqrt(1 + 25000 / (35 * Ag))
Vten = 0.53 * (1 - 25000 / (35 * Ag)) * sq * b * d
P(f"  401-100：無 {V0/1000:.2f}；Mm={Mm/1e5:.3f}（<0 取上限）壓 {Vcomp_cap/1000:.2f}；拉 {Vten/1000:.2f}；簡化無 {0.53*sq*b*d/1000:.2f}")

# ---------------------------------------------------------------- RC-2017-2
P("=== RC-2017-2")
fc = 210; fy = 4200; Es = 2.04e6; Ab = 5.067; bcol = 40; H = 70
def conc_stress(e):
    if e <= 0: return 0
    if e <= 0.002: return fc * e / 0.002
    return fc * (1 - 0.2 * (e - 0.002) / 0.001)
def run(old_cover):
    bars = [(6.5, 4)] + [(15 + old_cover, 3), (35, 2), (55 - old_cover, 3)] + [(63.5, 4)]
    def section(c, n=2000):
        # 壓力側在 x=0；中性軸 x=c
        xs = (np.arange(n) + 0.5) * min(c, H) / n
        dx = min(c, H) / n
        eps = 0.003 * (c - xs) / c
        sc = np.array([conc_stress(e) for e in eps])
        Cc = np.sum(sc) * dx * bcol
        Mc = np.sum(sc * (H / 2 - xs)) * dx * bcol
        # 新混凝土條帶 0–15 cm
        msk = xs <= 15
        Cstrip = np.sum(sc[msk]) * dx * bcol
        N = Cc; M = Mc; bar_info = []
        for xb, nb in bars:
            e = 0.003 * (c - xb) / c
            fs = max(min(e * Es, fy), -fy)
            fnet = fs - (conc_stress(e) if e > 0 else 0)
            F = nb * Ab * fnet
            N += F; M += F * (H / 2 - xb); bar_info.append((xb, nb, fs, F))
        return N, M, Cstrip, bar_info
    best = None
    for c in np.arange(10, 70, 0.02):
        N, M, Cs_, bi = section(c, 600)
        if best is None or M > best[1]: best = (c, M, N)
    c = best[0]
    N, M, Cstrip, bi = section(c, 4000)
    comp_bars = bi[0]; ten_bars = bi[-1]
    Vint_c = Cstrip + comp_bars[3]
    Vint_t = -ten_bars[3]
    return c, N, M, Cstrip, comp_bars, ten_bars, Vint_c, Vint_t
for oc in (6.5, 8.6):
    c, N, M, Cstrip, cb, tb, Vc_, Vt_ = run(oc)
    P(f"  原柱筋距原柱面 {oc}: c={c:.2f} Pn={N/1000:.1f} tf Mn,max={M/1e5:.2f} tf-m | 壓側條帶混凝土 {Cstrip/1000:.2f}"
      f" + 4根 fs={cb[2]:.0f} → {cb[3]/1000:.2f}；壓側介面合計 {Vc_/1000:.2f} tf；拉側 4根 fs={tb[2]:.0f} → {Vt_/1000:.2f} tf")
    Ab19 = 3.871; mu = 1.0
    for V in (Vc_, Vt_):
        n1 = V / (0.75 * mu * fy * Ab19); n0 = V / (mu * fy * Ab19); n287 = V / (0.75 * mu * fy * 2.87)
        P(f"     V={V/1000:.2f}: 植筋根數 φ=0.75 → {n1:.2f}；不乘 φ → {n0:.2f}；若 Ab=2.87 φ=0.75 → {n287:.2f}")

# ---------------------------------------------------------------- RC-2020-2
P("=== RC-2020-2")
fc = 280; sq = sqrt(fc); bw = 35; d = 64; fy = 4200; Av = 2 * 1.267
Vu = 15 * 8 / 2 * 1000
Vc = 0.53 * sq * bw * d; Vs = Vu / 0.75 - Vc
s = Av * fy * d / Vs; smax = d / 4 if Vs > 1.06 * sq * bw * d else d / 2
Vsmax = 2.12 * sq * bw * d
P(f"  Vu={Vu/1000:.1f} Vc={Vc/1000:.2f} Vs={Vs/1000:.2f} 1.06界={1.06*sq*bw*d/1000:.2f} Vsmax={Vsmax/1000:.2f} s={s:.2f} smax={smax:.1f}")
P(f"  ㈢ φ(Vc+Vsmax)={0.75*(Vc+Vsmax)/1000:.2f} tf")
hang = 150 / (0.75 * fy)
P(f"  吊筋 Ah/s={hang:.4f}；剪力 Av/s={Vs/(fy*d):.4f}；合計 s={Av/(hang+Vs/(fy*d)):.2f}")
# 若取 d 處（對照）
Vud = (15 * 4 - 15 * 0.64) * 1000
P(f"  對照 Vu(d)={Vud/1000:.2f} → s={Av*fy*d/(Vud/0.75-Vc):.2f}")

# ---------------------------------------------------------------- RC-2023-3
P("=== RC-2023-3")
b, h, d, L, Wu = 35, 60, 53, 350, 25.0  # kgf/cm
Vu = Wu * (L - d); Acp = b * h; pcp = 2 * (b + h)
Tth = 0.27 * sq * Acp**2 / pcp
e = 0.75 * Tth / (Wu * (L - d))
P(f"  Vu(d)={Vu/1000:.3f} tf  Tth={Tth/1e5:.4f} φTth={0.75*Tth/1e5:.4f} tf-m  e={e:.2f} cm")
P(f"  對照 φ=0.85/舊門檻 0.265? ： e(φ=0.75, 固定端 L)={0.75*Tth/(Wu*L):.2f} cm")
# 斷面剪力上限（另一讀法，對照）
P(f"  對照 φ(Vc+2.12√fc'bwd)={0.75*(0.53+2.12)*sq*b*d/1000:.2f} tf")

# ---------------------------------------------------------------- RC-2002-3
P("=== RC-2002-3")
fc = 210; sq2 = sqrt(fc); b, h, d = 36, 50, 45; Wu = 20.0; L = 800
Acp = b * h; pcp = 2 * (b + h); Tth = 0.27 * sq2 * Acp**2 / pcp
for lab, Lt in [("距支承面 d", L - d), ("支承處", L)]:
    for ph_ in (0.75, 0.85):
        P(f"  {lab} φ={ph_}: e={ph_*Tth/(Wu*Lt):.2f} cm")
P(f"  Tth={Tth/1e5:.4f} φTth={0.75*Tth/1e5:.4f} tf-m")
P(f"  兩端皆拘束（對照）：e={0.75*Tth/(Wu*(L/2-d)):.2f} cm")

# ---------------------------------------------------------------- 扭力共用
def tors_geom(b, h, cover, ds):
    x1 = b - 2 * cover - ds; y1 = h - 2 * cover - ds
    Aoh = x1 * y1; ph = 2 * (x1 + y1); return x1, y1, Aoh, ph, 0.85 * Aoh

P("=== RC-2008-3")
fc = 280; sq = sqrt(fc); b, h = 30, 60; fy = fyt = 2800; Tu = 3.0e5
x1, y1, Aoh, ph, Ao = tors_geom(b, h, 4, 1.27)
Acp = b * h; pcp = 2 * (b + h); Tth = 0.27 * sq * Acp**2 / pcp
lhs = Tu * ph / (1.7 * Aoh**2); rhs = 0.75 * (0.53 + 2.12) * sq
At_s = Tu / (0.75 * 2 * Ao * fyt)
prov = 1.27 / 15
Al = At_s * ph * fyt / fy
Almin = min(1.33 * sq * Acp / fy - At_s * ph * fyt / fy, 1.33 * sq * Acp / fy - 1.75 * b / fyt * ph * fyt / fy)
minAv = max(0.2 * sq, 3.5) * b / fyt
Tmax = rhs * 1.7 * Aoh**2 / ph
P(f"  x1={x1:.2f} y1={y1:.2f} Aoh={Aoh:.1f} ph={ph:.2f} Ao={Ao:.1f}  φTth={0.75*Tth/1e5:.3f}")
P(f"  ㈠ {lhs:.2f} ≤ {rhs:.2f}?  Tu,max={Tmax/1e5:.2f} tf-m")
P(f"  ㈡ At/s 需={At_s:.4f} 供={prov:.4f}；2At/s={2*prov:.4f} ≥ {minAv:.4f}；s≤{min(ph/8,30):.2f}")
P(f"     Aℓ={Al:.2f} Aℓ,min={Almin:.2f} 供 6#4={6*1.27:.2f}；以供給 At/s 計 Aℓ={prov*ph:.2f}")
P(f"     θ 可取 30–60°：Aℓ 隨 cot²θ；若 θ=60° 由箍筋供給反推  At/s需(60°)={Tu/(0.75*2*Ao*fyt/np.tan(radians(60))):.4f}")
# θ 調整：讓箍筋與縱筋都足夠的 θ 範圍
for thd in (45, 50, 55, 60):
    tt = radians(thd); ats = Tu / (0.75 * 2 * Ao * fyt / np.tan(tt)); al = ats * ph / np.tan(tt)**2
    P(f"     θ={thd}: At/s需={ats:.4f}（供 {prov:.4f}）Aℓ需={al:.2f}（供 7.62）")

P("=== RC-2011-4")
b, h, d = 35, 60, 53; fyt = 2800
x1, y1, Aoh, ph, Ao = tors_geom(b, h, 4, 1.27)
Acp = b * h; pcp = 2 * (b + h); Tcr = 1.06 * sq * Acp**2 / pcp
At_s = Tcr / (0.75 * 2 * Ao * fyt); leg = 1.267 / 8
Av_s = 2 * (leg - At_s); Vs = Av_s * fyt * d; Vc = 0.53 * sq * b * d
Vu1 = 0.75 * (Vc + Vs)
t = Tcr * ph / (1.7 * Aoh**2); R = 0.75 * (Vc / (b * d) + 2.12 * sq)
Vu2 = sqrt(R**2 - t**2) * b * d
P(f"  Aoh={Aoh:.1f} ph={ph:.2f} Ao={Ao:.1f} Tcr={Tcr/1e5:.3f} tf-m At/s={At_s:.5f} 每肢供={leg:.5f}")
P(f"  Av/s={Av_s:.5f} Vs={Vs/1000:.2f} Vc={Vc/1000:.2f} → Vu(箍筋)={Vu1/1000:.2f}；斷面上限 Vu={Vu2/1000:.2f}")
P(f"  檢核 Vs≤2.12√fc'bwd={2.12*sq*b*d/1000:.1f}；s=8≤ph/8={ph/8:.1f}、d/2={d/2}")
# 對照：Tcr 舊式（ACI 318-14 同 4Tth；舊 φ=0.85）
At85 = Tcr / (0.85 * 2 * Ao * fyt); Vs85 = 2 * (leg - At85) * fyt * d
P(f"  對照 φ=0.85：Vu={0.85*(Vc+Vs85)/1000:.2f}；若 Tu=φTcr：At/s={0.75*Tcr/(0.75*2*Ao*fyt):.5f}")

P("=== RC-2013-3")
b, h = 30, 50; fy = fyt = 2800; Tu = 1.5e5
x1, y1 = 20 - 0.96, 40 - 0.96; Aoh = x1 * y1; ph = 2 * (x1 + y1); Ao = 0.85 * Aoh
Acp = b * h; pcp = 2 * (b + h); Tth = 0.27 * sq * Acp**2 / pcp
lhs = Tu * ph / (1.7 * Aoh**2)
At_s = Tu / (0.75 * 2 * Ao * fyt); s = 0.71 / At_s
Al = At_s * ph
Almin = min(1.33 * sq * Acp / fy - At_s * ph, 1.33 * sq * Acp / fy - 1.75 * b / fyt * ph)
P(f"  Aoh={Aoh:.1f} ph={ph:.2f} Ao={Ao:.1f} φTth={0.75*Tth/1e5:.3f}  斷面 {lhs:.2f} ≤ {rhs:.2f}")
P(f"  At/s={At_s:.5f} s={s:.2f} smax={min(ph/8,30):.2f}  2At/s={2*At_s:.4f}≥{max(0.2*sq,3.5)*b/fyt:.4f}")
P(f"  Aℓ={Al:.2f} Aℓ,min={Almin:.2f} 供 4-D13={4*1.27:.2f}；6-D13={6*1.27:.2f}；縱筋垂直淨距中心 {y1:.2f}>30")
print("  對照 中心線 20×40：", end="")
Aoh2 = 800; ph2 = 120; at2 = Tu / (0.75 * 2 * 0.85 * Aoh2 * fyt); print(f"At/s={at2:.5f} s={0.71/at2:.2f} Aℓ={at2*ph2:.2f}")

P("=== RC-2018-1")
b = h = 50; d = 43; fyt = 2800; Tu = 4e5; Vu = 20e3; Ab = 1.27
x1, y1, Aoh, ph, Ao = tors_geom(b, h, 4, 1.27)
Acp = b * h; pcp = 2 * (b + h); Tth = 0.27 * sq * Acp**2 / pcp
Vc = 0.53 * sq * b * d
v = Vu / (b * d); t = Tu * ph / (1.7 * Aoh**2); R = 0.75 * (Vc / (b * d) + 2.12 * sq)
At_s = Tu / (0.75 * 2 * Ao * fyt)
Vs = max(Vu / 0.75 - Vc, 0); Av_s = Vs / (fyt * d)
s4 = Ab / (At_s + Av_s / 4); s2 = Ab / (At_s + Av_s / 2)
smax = min(ph / 8, 30, d / 2 if Vs <= 1.06 * sq * b * d else d / 4)
P(f"  Aoh={Aoh:.1f} ph={ph:.2f} Ao={Ao:.1f} φTth={0.75*Tth/1e5:.3f}  斷面 √({v:.2f}²+{t:.2f}²)={sqrt(v*v+t*t):.2f} ≤ {R:.2f}")
P(f"  At/s={At_s:.5f} Vc={Vc/1000:.2f} Vs={Vs/1000:.2f} Av/s={Av_s:.5f}")
P(f"  外圍肢需 {At_s+Av_s/4:.5f} → s(4肢抗剪)={s4:.2f}；s(外圍2肢抗剪)={s2:.2f}；smax={smax:.2f}")
P(f"  (Av+2At)/s={Av_s+2*At_s:.4f} ≥ {max(0.2*sq,3.5)*b/fyt:.4f}")

P("=== RC-2025-3")
b, h = 40, 70; fyt = 2800
x1, y1, Aoh, ph, Ao = tors_geom(b, h, 4, 1.27)
Tn = 2 * Ao * 1.27 * fyt / 15
Tumax = 0.75 * (0.53 + 2.12) * sq * 1.7 * Aoh**2 / ph
P(f"  x1={x1:.2f} y1={y1:.2f} Aoh={Aoh:.1f} ph={ph:.2f} Ao={Ao:.1f}  Tn={Tn/1e5:.3f} tf-m φTn={0.75*Tn/1e5:.3f}；斷面上限 Tn={Tumax/0.75/1e5:.2f}；s≤{ph/8:.1f}")
P(f"  對照 Ao=Aoh：Tn={2*Aoh*1.27*fyt/15/1e5:.3f}；用 1.267：{2*Ao*1.267*fyt/15/1e5:.3f}")
