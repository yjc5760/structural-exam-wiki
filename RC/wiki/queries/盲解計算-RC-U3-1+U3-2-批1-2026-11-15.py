# -*- coding: utf-8 -*-
"""RC-U3-1（撓度、裂縫）／RC-U3-2（樓版、基腳）批 1 盲解計算（2026-11-15）
現行台灣規範：建築物混凝土結構設計規範（內政部 2023 年版，ACI 318-19 世代），kgf-cm 制。
本檔在打開任何舊解析之前寫定。

共同設定（考卷未給時的假設）：
  Ec = 15000√f'c（主線，與本庫前批一致）；考卷給 n 時 Ec = Es/n；敏感度另列 12000√f'c
  fr = 2.0λ√f'c
  有效慣性矩（現行規範，ACI 318-19 表 24.2.3.5）：
     Ma ≤ (2/3)Mcr → Ie = Ig；否則 Ie = Icr / [1 − ((2/3)Mcr/Ma)²(1 − Icr/Ig)]
     對照：舊式 Branson Ie = (Mcr/Ma)³Ig + [1 − (Mcr/Ma)³]Icr ≤ Ig
  長期撓度 λΔ = ξ/(1+50ρ')，ξ：3 月 1.0、6 月 1.2、1 年 1.4、5 年以上 2.0
  單向剪力（無 Av,min，如基腳）：Vc = 2.12 λs λ ρw^(1/3) √f'c bw d；λs = √(2/(1+0.04d)) ≤ 1（d 以 cm 計）
  雙向剪力：vc = λs λ√f'c × min(1.06, 0.53(1+2/β) , 0.265(2+αs d/bo))；有閉合箍筋時 vc = 0.53λsλ√f'c、Vn ≤ 1.59√f'c bo d
  φ：剪力 0.75；撓曲依 εt（≥ εty+0.003 為 0.90）
  載重組合 1.2D+1.6L（並核 1.4D）
"""
from math import sqrt, pi

Es = 2.04e6
def P(*a):
    print(*a)

def lam_s(d):
    return min(1.0, sqrt(2 / (1 + 0.04 * d)))

def ie_bischoff(Ma, Mcr, Ig, Icr):
    if Ma <= 2 / 3 * Mcr:
        return Ig
    return Icr / (1 - ((2 / 3) * Mcr / Ma) ** 2 * (1 - Icr / Ig))

def ie_branson(Ma, Mcr, Ig, Icr):
    if Ma <= Mcr:
        return Ig
    r = (Mcr / Ma) ** 3
    return min(Ig, r * Ig + (1 - r) * Icr)

def cracked(b, n, tens, comp=(), comp_factor=None):
    """開裂換算斷面：tens=[(As,d)...]，comp=[(As',d')...]（壓力筋以 (n-1)As'）。回傳 (kd, Icr)"""
    nc = (n - 1) if comp_factor is None else comp_factor
    lo, hi = 0.01, max(d for _, d in tens)
    for _ in range(200):
        x = (lo + hi) / 2
        f = b * x * x / 2 + sum(nc * A * (x - dd) for A, dd in comp) - sum(n * A * (dd - x) for A, dd in tens)
        if f > 0: hi = x
        else: lo = x
    x = (lo + hi) / 2
    I = b * x ** 3 / 3 + sum(nc * A * (x - dd) ** 2 for A, dd in comp) + sum(n * A * (dd - x) ** 2 for A, dd in tens)
    return x, I

# ============================================================ RC-2005-4
P("=== RC-2005-4 素混凝土柱潛變")
fc = 280; L = 150; A = 25 * 35; Pk = 15000; Cc = 3.0
for name, Ec in [("15000√f'c", 15000 * sqrt(fc)), ("12000√f'c", 12000 * sqrt(fc))]:
    di = Pk * L / (A * Ec)
    P(f"  [{name}] Ec={Ec:.0f}  σ={Pk/A:.2f} kgf/cm²  δi={di:.5f} cm  δcreep={Cc*di:.5f}  δtotal={(1+Cc)*di:.5f} cm")

# ============================================================ RC-2006-3
P("=== RC-2006-3 簡支梁 PL 增加之即時撓度")
fc = 280; n = 8; Ec = Es / n; b = 30; h = 50; L = 800
Ab = 6.47; tens = [(3 * Ab, 42.0), (2 * Ab, 34.0)]
fr = 2.0 * sqrt(fc); Ig = b * h ** 3 / 12; Mcr = fr * Ig / (h / 2)
kd, Icr = cracked(b, n, tens)
kd1, Icr1 = cracked(b, n, [(5 * Ab, 50 - 11.2)])
MD = 0.8 * 10 * L ** 2 / 8 / 1e3 * 1e3  # kgf-cm: w=0.8 tf/m = 8 kgf/cm
MD = 8.0 * L ** 2 / 8
ML = 5000 * L / 4
MT = MD + ML
P(f"  Ec={Ec:.0f} fr={fr:.2f} Ig={Ig:.0f} Mcr={Mcr/1e5:.3f} tf-m  kd={kd:.3f} Icr={Icr:.0f} (形心法 kd={kd1:.3f} Icr={Icr1:.0f})")
P(f"  MD={MD/1e5:.2f}  MD+L={MT/1e5:.2f} tf-m")
def d_ss(w, Pc, I):
    return 5 * w * L ** 4 / (384 * Ec * I) + Pc * L ** 3 / (48 * Ec * I)
res = {}
for name, fn in [("Bischoff(現行)", ie_bischoff), ("Branson(舊)", ie_branson)]:
    IeD = fn(MD, Mcr, Ig, Icr); IeT = fn(MT, Mcr, Ig, Icr)
    dD = d_ss(8.0, 0, IeD); dT = d_ss(8.0, 5000, IeT)
    res[name] = dT - dD
    P(f"  [{name}] IeD={IeD:.0f} IeD+L={IeT:.0f}  ΔD={dD:.4f}  ΔD+L={dT:.4f}  ΔL增量={dT-dD:.4f} cm")
P(f"  [全開裂 Icr] ΔL={d_ss(0,5000,Icr):.4f} cm")

# ============================================================ RC-2007-2
P("=== RC-2007-2 簡支梁即時與長期撓度")
fc = 280; b = 30; h = 60; L = 800
Ec = 15000 * sqrt(fc); n = Es / Ec
# 假設：淨保護層 4 cm、D13 箍筋、兩排 D25 淨距 2.5 cm
d1 = 60 - 4 - 1.27 - 2.54 / 2; d2 = d1 - 2.54 - 2.5
tens = [(40.56 / 2, d1), (40.56 / 2, d2)]; dbar = (d1 + d2) / 2
comp = [(8.55, 6.5)]
fr = 2.0 * sqrt(fc); Ig = b * h ** 3 / 12; Mcr = fr * Ig / 30
kd, Icr = cracked(b, n, tens, comp)
wD = 0.30 * 0.60 * 2.4 * 10 + 1.0     # kgf/cm（0.432+0.1 tf/m）
wL = 20.0; wS = wD + 0.2 * wL; wT = wD + wL
M = lambda w: w * L ** 2 / 8
rho_p = 8.55 / (b * dbar)
P(f"  d1={d1:.2f} d2={d2:.2f} d={dbar:.2f}  Ec={Ec:.0f} n={n:.3f} Mcr={Mcr/1e5:.3f}  kd={kd:.3f} Icr={Icr:.0f} Ig={Ig:.0f}")
P(f"  wD={wD/10:.3f} wS={wS/10:.3f} wT={wT/10:.3f} tf/m;  MD={M(wD)/1e5:.3f} MS={M(wS)/1e5:.3f} MT={M(wT)/1e5:.3f} tf-m;  ρ'={rho_p:.5f}")
def d5(w, I, Ecc=None):
    return 5 * w * L ** 4 / (384 * (Ecc or Ec) * I)
for name, fn in [("Bischoff(現行)", ie_bischoff), ("Branson(舊)", ie_branson)]:
    IeD, IeS, IeT = (fn(M(w), Mcr, Ig, Icr) for w in (wD, wS, wT))
    dD = d5(wD, IeD); dS = d5(wS, IeS); dT = d5(wT, IeT)
    out = {}
    for yrs, xi in [("1年", 1.4), ("5年", 2.0)]:
        lam = xi / (1 + 50 * rho_p)
        out[yrs] = (lam, dT + lam * dS)
    P(f"  [{name}] IeD={IeD:.0f} IeS={IeS:.0f} IeT={IeT:.0f}")
    P(f"     ㈠(Δi)d={dD:.3f}  ㈡(Δi)sus 總(D+0.2L)={dS:.3f}／其中0.2L增量={dS-dD:.3f}  ㈢(Δi)l=ΔT−ΔD={dT-dD:.3f}  (ΔT={dT:.3f}) cm")
    for k, (lam, tot) in out.items():
        P(f"     ㈣㈤ {k}: λΔ={lam:.3f}  長期增量={lam*dS:.3f}  總位移=ΔT+λΔ·ΔS={tot:.3f} cm")
for dd in (50.0, 52.0):
    kd_, Icr_ = cracked(b, n, [(40.56, dd)], comp)
    IeT_ = ie_bischoff(M(wT), Mcr, Ig, Icr_)
    P(f"  敏感度 d={dd}: Icr={Icr_:.0f} ΔT={d5(wT, IeT_):.3f}")

# ============================================================ RC-2008-1
P("=== RC-2008-1 懸臂梁一年後撓度")
fc = 280; n = 8; Ec = Es / n; b = 40; h = 70; L = 500
tens = [(50.0, 60.0)]; comp = [(20.0, 10.0)]
fr = 2.0 * sqrt(fc); Ig = b * h ** 3 / 12; Mcr = fr * Ig / 35
kd, Icr = cracked(b, n, tens, comp)
w = 0.40 * 0.70 * 2.4 * 10   # kgf/cm（假設 2.4 tf/m³）
Pp = 2000
Ma = Pp * L + w * L ** 2 / 2
rho_p = 20 / (b * 60)
for name, fn in [("Bischoff(現行)", ie_bischoff), ("Branson(舊)", ie_branson)]:
    Ie = fn(Ma, Mcr, Ig, Icr)
    di = Pp * L ** 3 / (3 * Ec * Ie) + w * L ** 4 / (8 * Ec * Ie)
    lam = 1.4 / (1 + 50 * rho_p)
    P(f"  [{name}] Mcr={Mcr/1e5:.3f} Ma={Ma/1e5:.3f} tf-m kd={kd:.3f} Icr={Icr:.0f} Ig={Ig:.0f} Ie={Ie:.0f}")
    P(f"     Δi={di:.4f} cm  λΔ={lam:.4f}  Δ長期={lam*di:.4f}  Δ總={di*(1+lam):.4f} cm")

# ============================================================ RC-2009-2
P("=== RC-2009-2 懸臂梁降伏彎矩時自由端撓度")
fc = 210; fy = 2800; b = 35; h = 60; d = 50; As = 10.13; L = 400
Ec = 15000 * sqrt(fc); n = Es / Ec; fr = 2.0 * sqrt(fc)
Ig = b * h ** 3 / 12; Mcr = fr * Ig / 30
kd, Icr = cracked(b, n, [(As, d)])
ey = fy / Es
fc_top = ey * Ec * kd / (d - kd)
My = As * fy * (d - kd / 3)
Py = My / L
P(f"  Ec={Ec:.0f} n={n:.3f} kd={kd:.3f} Icr={Icr:.0f} Ig={Ig:.0f} Mcr={Mcr/1e5:.3f}  fc,top={fc_top:.1f}({fc_top/fc:.2f}f'c)")
P(f"  My={My/1e5:.3f} tf-m  P={Py/1e3:.3f} tf")
for name, fn in [("Bischoff(現行)", ie_bischoff), ("Branson(舊)", ie_branson)]:
    Ie = fn(My, Mcr, Ig, Icr)
    P(f"  [{name}] Ie={Ie:.0f}  Δ=PL³/3EIe={Py*L**3/(3*Ec*Ie):.4f} cm")
xcr = Mcr / Py
dex = Py / Ec * (xcr ** 3 / 3 / Ig + (L ** 3 - xcr ** 3) / 3 / Icr)
P(f"  [分段積分：x<{xcr:.1f} cm 未開裂 Ig，其餘 Icr] Δ={dex:.4f} cm;  [全段 Icr] Δ={Py*L**3/(3*Ec*Icr):.4f}")
# 曲率法交叉：φy = εy/(d−kd)，Δ ≈ φy L²/3（全段開裂線性曲率）
phiy = ey / (d - kd)
P(f"  交叉：φy={phiy:.4e}  φyL²/3={phiy*L*L/3:.4f} cm（應=全段 Icr 值）")

# ============================================================ RC-2018-3
P("=== RC-2018-3 T 梁負彎矩裂縫控制")
fy = 4200; fs = 2 / 3 * fy; db = 2.54; dst = 1.27; cov = 4.0
cc = cov + dst
s1 = 38 * (2800 / fs) - 2.5 * cc; s2 = 30 * (2800 / fs)
smax = min(s1, s2)
bw = 40; hf = 15; ln = 1200; sw = 300 - 40
be = bw + 2 * min(8 * hf, sw / 2, ln / 8)
wdist = min(be, ln / 10)
P(f"  fs={fs:.0f} cc={cc:.2f}  s≤{s1:.2f} 且 ≤{s2:.1f} → smax={smax:.2f} cm")
P(f"  有效翼寬 be={be:.0f} cm；ℓn/10={ln/10:.0f} → 分布寬 {wdist:.0f} cm（be>ℓn/10，外側翼版另配縱向筋）")
P(f"  12-D25 均分於 {wdist:.0f} cm：中心距 ≈ {wdist/12:.1f}（每根代表寬）～{(wdist-0)/11:.1f} cm（端筋在帶寬邊緣）；淨距 ≥ max(db,2.5) OK")
As = 12 * 5.07; jd = 0.9 * 113
P(f"  若 120 tf-m 為使用彎矩：fs≈M/(As·0.9d)={120e5/(As*jd):.0f} kgf/cm²（< 2/3fy，取 2/3fy 偏保守）")
P(f"  表層筋：h=120>90 → 自受拉面（頂面）起 h/2=60 cm 範圍兩側面（版底 15 cm 以下即 15～60 cm 段）；間距 ≤ {smax:.1f} cm")

# ============================================================ RC-2007-3 / RC-2025-1 基腳
def footing(tag, B, c, D, Lv, d, As, fc, fy, depth, gc, gs, qa, h_assume, one_way=True):
    P(f"=== {tag}")
    soil = depth - h_assume / 100
    qnet = qa - (h_assume / 100 * gc + soil * gs)
    Areq = (D + Lv) / qnet
    P(f"  假設全厚 h={h_assume}；覆土 {soil:.2f} m；q淨容許={qnet:.2f} tf/m² → 需 {Areq:.2f} m² vs {B*B:.2f}")
    Pu = max(1.2 * D + 1.6 * Lv, 1.4 * D); qu = Pu / B ** 2
    sq = sqrt(fc); lsd = lam_s(d)
    # 撓曲
    l = (B * 100 - c) / 2
    Mu = qu * B * (l / 100) ** 2 / 2
    a = As * fy / (0.85 * fc * B * 100); cN = a / 0.85; et = 0.003 * (d - cN) / cN
    Mn = As * fy * (d - a / 2) / 1e5
    Asmin = 0.0018 * B * 100 * h_assume
    P(f"  Pu={Pu:.1f} tf qu={qu:.3f} tf/m²  懸臂 {l:.1f} cm  Mu={Mu:.2f} tf-m  a={a:.3f} εt={et:.4f} φMn={0.9*Mn:.2f} tf-m → {'OK' if 0.9*Mn>=Mu else 'NG'}；As,min=0.0018bh={Asmin:.1f} ≤ {As}")
    # 單向剪力
    if one_way:
        x = l - d
        Vu = qu * B * x / 100
        rho = As / (B * 100 * d)
        Vc_new = min(2.12 * lsd * rho ** (1 / 3) * sq, 1.33 * sq) * B * 100 * d / 1e3
        Vc_old = 0.53 * sq * B * 100 * d / 1e3
        P(f"  單向剪力：Vu={Vu:.2f} tf；λs={lsd:.4f} ρw={rho:.5f}  現行 φVc={0.75*Vc_new:.2f} → {'OK' if 0.75*Vc_new>=Vu else 'NG'}；舊 0.53√f'c φVc={0.75*Vc_old:.2f} → {'OK' if 0.75*Vc_old>=Vu else 'NG'}")
    # 穿孔
    bo = 4 * (c + d); Vu2 = qu * (B ** 2 - ((c + d) / 100) ** 2)
    k = min(1.06, 0.53 * (1 + 2 / 1.0), 0.265 * (2 + 40 * d / bo))
    Vc2 = k * lsd * sq * bo * d / 1e3; Vc2o = k * sq * bo * d / 1e3
    P(f"  穿孔：bo={bo} Vu={Vu2:.2f} tf；係數 {k:.3f}；現行(λs) φVc={0.75*Vc2:.2f} → {'OK' if 0.75*Vc2>=Vu2 else 'NG'}（比值 {Vu2/(0.75*Vc2):.3f}）；無 λs φVc={0.75*Vc2o:.2f} → {'OK' if 0.75*Vc2o>=Vu2 else 'NG'}")
    return dict(Pu=Pu, qu=qu, Mu=Mu, phiMn=0.9 * Mn)

footing("RC-2007-3 獨立基腳（彎矩、單向與穿孔剪力）", 3.0, 45, 100, 80, 50, 50, 280, 4200, 1.5, 2.4, 2.0, 25, 60)
footing("RC-2025-1 獨立基腳（彎矩、穿孔剪力）", 3.0, 40, 80, 75, 50, 50, 280, 4200, 1.5, 2.4, 2.0, 25, 60)

# ============================================================ RC-2017-3
P("=== RC-2017-3 獨立基腳 4×4（設計彎矩筋、檢核剪力）")
B = 4.0; c = 45; D = 180; Lv = 120; h = 80; fc = 210; fy = 4200; qa = 30; gs = 1.9; gc = 2.4
d = 80 - 7.5 - 2.54   # 假設：保護層 7.5、D25 兩向平均 d
sq = sqrt(fc); lsd = lam_s(d)
qnet = qa - (h / 100 * gc + 1.0 * gs); Areq = (D + Lv) / qnet
Pu = max(1.2 * D + 1.6 * Lv, 1.4 * D); qu = Pu / B ** 2
l = (B * 100 - c) / 2; Mu = qu * B * (l / 100) ** 2 / 2
bb = B * 100
Rn = Mu * 1e5 / (0.9 * bb * d ** 2)
rho = 0.85 * fc / fy * (1 - sqrt(1 - 2 * Rn / (0.85 * fc)))
Asreq = rho * bb * d; Asmin = 0.0018 * bb * h
Asd = max(Asreq, Asmin)
a = Asd * fy / (0.85 * fc * bb); b1 = 0.85; cN = a / b1; et = 0.003 * (d - cN) / cN
P(f"  d={d:.2f} λs={lsd:.4f}  q淨={qnet:.2f} 需面積 {Areq:.2f} ≤ 16")
P(f"  Pu={Pu:.0f} qu={qu:.3f}  Mu={Mu:.2f} tf-m  As,req={Asreq:.2f}  As,min={Asmin:.1f} → As={Asd:.2f} cm²（每向）  εt={et:.4f}")
nbar = Asd / 5.07
P(f"  例：D25 {nbar:.1f}→{int(-(-nbar//1))} 根（{int(-(-nbar//1))*5.07:.1f} cm²）；間距 ≈ {(bb-15)/(int(-(-nbar//1))-1):.1f} cm（≤ 3h、45 OK）")
x = l - d; Vu1 = qu * B * x / 100
for Asp in (Asd, 12 * 5.07):
    r = Asp / (bb * d)
    Vc1 = min(2.12 * lsd * r ** (1 / 3) * sq, 1.33 * sq) * bb * d / 1e3
    P(f"  單向剪力 Vu={Vu1:.2f}；As={Asp:.1f} ρw={r:.5f} 現行 φVc={0.75*Vc1:.2f} → {'OK' if 0.75*Vc1>=Vu1 else 'NG'}")
Vc1o = 0.53 * sq * bb * d / 1e3
P(f"  單向剪力 舊 0.53√f'c φVc={0.75*Vc1o:.2f} → {'OK' if 0.75*Vc1o>=Vu1 else 'NG'}")
need = Vu1 / 0.75 * 1e3 / (2.12 * lsd * sq * bb * d)
P(f"  現行式要單向剪力 OK 需 ρw^(1/3)={need:.4f} → ρw={need**3:.4f}（As={need**3*bb*d:.0f} cm²，不實際）→ 須加厚")
bo = 4 * (c + d); Vu2 = qu * (B ** 2 - ((c + d) / 100) ** 2)
k = min(1.06, 1.59, 0.265 * (2 + 40 * d / bo))
Vc2 = k * lsd * sq * bo * d / 1e3; Vc2o = k * sq * bo * d / 1e3
P(f"  穿孔 bo={bo:.1f} Vu={Vu2:.2f}；現行 φVc={0.75*Vc2:.2f} → {'OK' if 0.75*Vc2>=Vu2 else 'NG'}；無 λs φVc={0.75*Vc2o:.2f} → {'OK' if 0.75*Vc2o>=Vu2 else 'NG'}")
for dd in (72.5, 71.23, 68.69):
    bo_ = 4 * (c + dd); Vu_ = qu * (B ** 2 - ((c + dd) / 100) ** 2)
    k_ = min(1.06, 1.59, 0.265 * (2 + 40 * dd / bo_))
    P(f"    敏感度 d={dd}: 穿孔 Vu={Vu_:.2f} 無λs φVc={0.75*k_*sq*bo_*dd/1e3:.2f}  現行 φVc={0.75*k_*lam_s(dd)*sq*bo_*dd/1e3:.2f}")
# 求現行規範要穿孔與單向剪力都 OK 的最小厚度（As=As,min 隨 h）
for hh in range(80, 141, 5):
    dd = hh - 10.0
    q2 = qu
    Vu_1 = q2 * B * (l - dd) / 100
    As_ = max(0.0018 * bb * hh, Asreq)
    r = As_ / (bb * dd)
    V1 = 0.75 * min(2.12 * lam_s(dd) * r ** (1 / 3), 1.33) * sq * bb * dd / 1e3
    bo_ = 4 * (c + dd); Vu_2 = q2 * (B ** 2 - ((c + dd) / 100) ** 2)
    V2 = 0.75 * min(1.06, 0.265 * (2 + 40 * dd / bo_)) * lam_s(dd) * sq * bo_ * dd / 1e3
    if V1 >= Vu_1 and V2 >= Vu_2:
        P(f"  參考：現行規範（As=0.0018bh）兩種剪力皆 OK 約需 h≈{hh} cm（d={dd}）")
        break
# 柱底承壓（參考）
A1 = c * c; A2 = min(400, c + 2 * 2 * (h - 0)) ** 2
P(f"  柱底承壓（參考）：柱 φ0.85f'c A1={0.65*0.85*350*A1/1e3:.0f} tf；基腳 min(√(A2/A1),2)=2 → {0.65*0.85*210*A1*2/1e3:.0f} tf ≥ Pu={Pu:.0f}")

# ============================================================ RC-2013-1
P("=== RC-2013-1 連續單向版：版厚與外支承負彎矩筋")
lc = 480; bw = 30; ln = lc - bw; fc = 280; fy = 4200
h_min_ext = lc / 24; h_min_int = lc / 28
h = 20.0
wD = 0.1 + h / 100 * 2.4; wL = 0.6
wu = max(1.2 * wD + 1.6 * wL, 1.4 * wD)
Mu = wu * (ln / 100) ** 2 / 24
d = h - 2.0 - 1.27 / 2
Rn = Mu * 1e5 / (0.9 * 100 * d ** 2)
rho = 0.85 * fc / fy * (1 - sqrt(1 - 2 * Rn / (0.85 * fc)))
Asreq = rho * 100 * d; Asmin = 0.0018 * 100 * h
smax_crack = min(38 * (2800 / (2 / 3 * fy)) - 2.5 * 2.0, 30)
smax = min(3 * h, 45, smax_crack)
P(f"  最小厚度：一端連續 ℓ/24={h_min_ext:.2f}、兩端連續 ℓ/28={h_min_int:.2f}（ℓ=480 中心距；若用 ℓn=450：{450/24:.2f}）→ 取 h={h}")
P(f"  wD={wD:.3f} wL={wL} wu={wu:.3f} tf/m²；ACI 係數法外支承與邊梁一體 Mu=wuℓn²/24={Mu:.3f} tf-m/m（若為柱支承 /16={wu*(ln/100)**2/16:.3f}）")
P(f"  d={d:.3f} Rn={Rn:.2f} As,req={Asreq:.3f} cm²/m；As,min=0.0018bh={Asmin:.2f} → 控制 {max(Asreq,Asmin):.2f}")
P(f"  間距上限：3h、45、裂縫 {smax_crack:.1f} → {smax:.1f} cm；D13@30 → {1.27/0.30:.2f} cm²/m OK；D10@19 → {0.71/0.19:.2f}")
P(f"  L/D={wL/wD:.2f} ≤ 3 → 係數法適用")

# ============================================================ RC-2020-3
P("=== RC-2020-3 無梁版內柱穿孔剪力與剪力筋間距")
wu = 4.6; d = 35; c = 100; fc = 280; fyt = 4200; sq = sqrt(fc); lsd = lam_s(d)
bo = 4 * (c + d); Vu = wu * (8 * 9 - ((c + d) / 100) ** 2)
k = min(1.06, 0.265 * (2 + 4 / 1.0), 0.265 * (2 + 40 * d / bo))
Vc_new = k * lsd * sq * bo * d / 1e3; Vc_old = k * sq * bo * d / 1e3
P(f"  bo={bo} Vu={Vu:.2f} tf；三式係數 1.06 / {0.265*6:.3f} / {0.265*(2+40*d/bo):.3f} → {k}；λs={lsd:.4f}")
P(f"  ㈠ 現行 φVc={0.75*Vc_new:.2f}（Vc={Vc_new:.2f}）→ {'OK' if 0.75*Vc_new>=Vu else '不足'}；照考卷式 φVc={0.75*Vc_old:.2f} → {'OK' if 0.75*Vc_old>=Vu else '不足'}")
Av = 4 * 2 * 1.267
Vnmax = 1.59 * sq * bo * d / 1e3
for name, vc in [("現行 0.53λs√f'c", 0.53 * lsd * sq), ("照考卷 0.53√f'c", 0.53 * sq)]:
    Vc = vc * bo * d / 1e3
    Vs = Vu / 0.75 - Vc
    s = Av * fyt * d / (Vs * 1e3)
    P(f"  ㈡ [{name}] Vc={Vc:.2f} Vs需={Vs:.2f} tf；Av(4 支×雙肢)={Av:.3f} cm² → s={s:.2f} cm（≤ d/2={d/2}）；φVn,max={0.75*Vnmax:.1f} ≥ Vu")
# 交叉：每一支（單向、2 肢）分擔 Vs/4
P(f"  交叉：每一方向一支雙肢 Av=2.534，分擔 Vs/4 → 同上 s")

# ============================================================ RC-2021-3
P("=== RC-2021-3 四樁樁帽最大容許偏心距")
Pu = 100.0; x = 90.0; Pc = 40.0; Pt = -10.0; d = 55 - 10; fc = 280; sq = sqrt(fc); lsd = lam_s(d)
sx2 = 4 * x * x
k_e = Pu * x / sx2   # tf/cm
e_comp = (Pc - Pu / 4) / k_e
e_ten = (Pu / 4 - Pt) / k_e
P(f"  樁力 = 25 ± {k_e:.4f}·e；壓 ≤40 → e≤{e_comp:.2f} cm；拉 ≥−10 → e≤{e_ten:.2f} cm")
# 柱周雙向
c = 50; b1 = c + d; bo = 4 * b1
k = min(1.06, 0.265 * 6, 0.265 * (2 + 40 * d / bo))
Vc = k * lsd * sq * bo * d / 1e3
P(f"  柱周：臨界邊 {b1} cm 距中心 {b1/2}，樁緣最近 {x-15} cm → 4 樁全在外，Vu=Pu=100 tf；係數 {k}；λs={lsd:.4f} φVc={0.75*Vc:.1f}（無λs {0.75*k*sq*bo*d/1e3:.1f}）")
gv = 1 - 1 / (1 + 2 / 3)
Jc = d * b1 ** 3 / 6 + b1 * d ** 3 / 6 + d * b1 * b1 ** 2 / 2
for e in (e_comp,):
    vu = Pu * 1e3 / (bo * d) + gv * Pu * 1e3 * e * (b1 / 2) / Jc
    P(f"  含不平衡彎矩轉移(γv={gv:.2f})，e={e:.1f}: vu={vu:.2f} vs φvc={0.75*k*lsd*sq:.2f} kgf/cm² → {'OK' if vu<=0.75*k*lsd*sq else 'NG'}")
emax_v = (0.75 * k * lsd * sq - Pu * 1e3 / (bo * d)) / (gv * Pu * 1e3 * (b1 / 2) / Jc)
P(f"  （彎矩轉移限制 e≤{emax_v:.1f} cm，不控制）")
# 角隅基樁穿孔
r = 15 + d / 2
bo_c = 2 * 40 + pi * r / 2
bo_full = 2 * pi * r
kc = min(1.06, 0.265 * 6, 0.265 * (2 + 20 * d / bo_c))
Vcc = kc * lsd * sq * bo_c * d / 1e3
P(f"  角隅樁：臨界半徑 {r}（< 距邊 40，整圓 {bo_full:.1f} 亦在帽內）；角隅型周長 2×40+πr/2={bo_c:.1f}；係數 {kc}；φVc={0.75*Vcc:.1f} tf ≥ 樁力上限 40 → 不控制（無λs {0.75*kc*sq*bo_c*d/1e3:.1f}）")
# 單向剪力（題目未要求，參考）
xs = c / 2 + d
P(f"  參考單向剪力：臨界面距中心 {xs}，樁心 {x}（距面 {x-xs} ≥ 半徑 15 → 全計）；Vu=2(25+{k_e:.4f}e)；")
Vc1 = 0.53 * sq * 260 * d / 1e3
e1 = (0.75 * Vc1 / 2 - 25) / k_e
P(f"     若以 0.53√f'c：φVc={0.75*Vc1:.2f} → e≤{e1:.2f} cm；現行式需 ρw（考卷未給樁帽筋）")

P("完")
