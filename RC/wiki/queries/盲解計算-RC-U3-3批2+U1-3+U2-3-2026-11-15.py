# -*- coding: utf-8 -*-
"""RC-U3-3 批 2＋U1-3＋U2-3 盲解計算（2026-11-15）
現行台灣規範：建築物混凝土結構設計規範（內政部 2023 年版，ACI 318-19 世代）＋耐震第 18 章；kgf-cm 制。
本檔在打開任何舊解析之前寫定。
共同假設：Ec = 15000√f'c（考卷未給時；2016 卷首亦給此式）；Es = 2.04e6；
  耐震 Mpr 用 1.25fy、φ=1.0；重力伴隨地震組合 1.2D+1.0L；
  非側移細長柱：kℓu/r ≤ 34+12(M1/M2) ≤ 40、Cm = 0.6−0.4(M1/M2)（單曲率 M1/M2 為負，ACI 318-14 起無 0.4 下限）、
  δ = Cm/(1−Pu/0.75Pc) ≥ 1、M2,min = Pu(1.5+0.03h) cm。
"""
from math import sqrt, pi

def P(*a): print(*a)
fc = 280.0; sfc = sqrt(fc); Es = 2.04e6; Ec = 15000 * sfc

def mpr(As, fy, b, d, fc=280.0):
    T = 1.25 * fy * As; a = T / (0.85 * fc * b)
    return T, a, T * (d - a / 2)          # kgf, cm, kgf·cm

# ======================= RC-2013-2 柱圍束箍筋
P("=== RC-2013-2")
b = 50; cov = 4; bc = b - 2 * cov; Ag = b * b; Ach = bc * bc; fyt = 2800
r1 = 0.3 * (Ag / Ach - 1) * fc / fyt; r2 = 0.09 * fc / fyt
P(f"bc={bc} Ach={Ach} Ag/Ach-1={Ag/Ach-1:.4f}  0.3(...)f'c/fyt={r1:.5f}  0.09f'c/fyt={r2:.5f}")
req = max(r1, r2) * bc; P(f"Ash/s 需要 = {req:.4f} cm2/cm")
dbh = 1.27; dbl = 3.22
xc = cov + dbh + dbl / 2; sp = (b - 2 * xc) / 4
P(f"主筋心距外緣 {xc:.3f}；同面筋距 {sp:.3f}；淨距 {sp-dbl:.3f}")
for legs, hx in [(3, 2 * sp), (5, sp)]:
    so = min(15, max(10, 10 + (35 - hx) / 3))
    smax = min(b / 4, 6 * dbl, so)
    s_ash = legs * 1.27 / req
    P(f"D13 {legs} 肢：hx={hx:.2f} so={so:.2f} s上限={smax:.2f}  Ash 控制 s={s_ash:.2f}  → 採 s={min(smax, s_ash):.2f}")
P(f"lo ≥ max(h=50, ℓu/6, 45)；lo 外 s ≤ min(6db={6*dbl:.1f}, 15)")
# 高軸壓第三式（Pu>0.3Agf'c 時）示例：kf=f'c/1750+0.6≥1，kn=nl/(nl−2)
kf = max(1.0, fc / 1750 + 0.6); nl = 12  # 若每根皆被支撐 16 根周邊 → nl=16
for nl in (16,):
    kn = nl / (nl - 2)
    for Pu_ratio in (0.4,):
        Pu = Pu_ratio * Ag * fc
        r3 = 0.2 * kf * kn * Pu / (fyt * Ach)
        P(f"[示例] Pu={Pu_ratio}Agf'c={Pu/1000:.0f}tf, nl={nl}: 0.2kfknPu/(fyt Ach)={r3:.5f} → Ash/s={r3*bc:.4f}")

# ======================= RC-2016-2 梁塑鉸區箍筋
P("=== RC-2016-2")
b, d, fy, ln = 35, 63, 4200, 750
Tt, at, Mn_ = mpr(3 * 6.47, fy, b, d); Tb, ab, Mp_ = mpr(3 * 3.87, fy, b, d)
wu = 1.2 * 2 + 1.0 * 1  # tf/m
Vg = wu * ln / 100 / 2; Vsw = (Mn_ + Mp_) / 1e5 / (ln / 100)
Ve = Vsw + Vg
P(f"Mpr-={Mn_/1e5:.2f} (a={at:.2f})  Mpr+={Mp_/1e5:.2f} (a={ab:.2f}) tf·m")
P(f"wu={wu} tf/m  Vg={Vg:.3f}  Vsway={Vsw:.3f}  Ve={Ve:.3f} tf  地震部分/Ve={Vsw/Ve:.4f}")
Vc = 0.53 * sfc * b * d / 1000
Av = 3 * 0.71
for name, vc in [("計Vc", Vc), ("Vc=0", 0)]:
    Vs = Ve / 0.75 - vc; s = Av * 4200 * d / (Vs * 1000)
    P(f"{name}: Vc={vc:.2f} Vs={Vs:.2f} tf → s強度={s:.2f} cm")
P(f"Av,min 檢核: max(0.2√f'c,3.5)bw/fyt = {max(0.2*sfc,3.5)*b/4200:.4f} cm2/cm")
P(f"塑鉸區 s 上限 = min(d/4={d/4:.2f}, 6db(D22)={6*2.22:.2f}, 15) ; 範圍 2h=140 cm；第一支 ≤5 cm")
P(f"(對照 1.2D+0.5L: wu=2.9 → Ve={Vsw+2.9*7.5/2:.3f}, 比={Vsw/(Vsw+2.9*7.5/2):.4f})")

# ======================= RC-2018-2 角柱接頭剪力
P("=== RC-2018-2")
As = 8 * 6.47; b = 50; d = 43; H = 380
T, a, M = mpr(As, 4200, b, d)
Vcol = M / H; Vj = T - Vcol
Aj = 50 * 50
for coef in (5.3, 4.0, 3.2):
    P(f"  係數 {coef}: φVn = {0.85*coef*sfc*Aj/1000:.2f} tf")
phiVn = 0.85 * 3.2 * sfc * Aj / 1000
P(f"T=1.25fyAs={T/1000:.2f} tf a={a:.2f} Mpr={M/1e5:.2f} tf·m Vcol=Mpr/H={Vcol/1000:.2f} Vj={Vj/1000:.2f} tf")
P(f"角柱（柱連續、梁不連續、未圍束）3.2√f'c Aj：Vn={3.2*sfc*Aj/1000:.2f}, φVn={phiVn:.2f} tf → Vj/φVn={Vj/1000/phiVn:.3f}")
ldh = 4200 * 2.87 / (17.2 * sfc); P(f"彎鉤 ldh = fy db/(17.2√f'c) = {ldh:.2f} cm（≥8db={8*2.87:.1f}, 15）")
P(f"梁主筋穿越接頭之柱深 20db = {20*2.87:.1f} cm（角柱梁筋以彎鉤錨定，不適用）")

# ======================= RC-2019-3 橫膈版剪力
P("=== RC-2019-3")
Acv = 500 * 18; phi = 0.6; Vu = 100e3; fy = 2800
Vn_req = Vu / phi; Vc = 0.53 * sfc * Acv
rho = (Vn_req - Vc) / (fy * Acv)
P(f"Vn需={Vn_req/1000:.2f} Vc={Vc/1000:.2f} tf  ρt需={rho:.6f}  Vn上限2.12√f'cAcv={2.12*sfc*Acv/1000:.1f} tf")
Ash = rho * Acv; per_cm = Ash / 500
flex = 2 * 1.27 / 25
P(f"剪力筋 {Ash:.2f} cm2 / 500 cm = {per_cm:.5f} cm2/cm（雙層合計）；撓曲既有 #4@25 雙層 = {flex:.5f}")
tot = flex + per_cm; s = 2 * 1.27 / tot
P(f"相加 {tot:.5f} → 每層 #4 間距 s = {s:.2f} cm → 採 15 cm")
P(f"若不相加：只需 ρt → 每層間距 {2*1.27/per_cm:.1f} cm；既有 #4@25 之 ρt = {2*1.27/(25*18):.5f}")
rho75 = (Vu / 0.75 - Vc) / (fy * Acv)
P(f"[對照 φ=0.75] ρt={rho75:.6f} → 相加後每層間距 s={2*1.27/(flex+rho75*Acv/500):.2f} cm")
P(f"版最少筋 0.0018×18={0.0018*18:.4f} cm2/cm；s上限 min(3h,45)=45")

# ======================= RC-2022-4 韌性需求
P("=== RC-2022-4")
phy = (0.004 + 0.006) / 2; My = (200 + 240) / 2; phu = (0.03 + 0.01) / 2; Mu_ = (230 + 260) / 2
Md = 232.5; phd = phy + (Md - My) / (Mu_ - My) * (phu - phy)
L = 3.2; db = 3.22; fy = 4200
Lp1 = 0.08 * L * 100 + 0.0022 * db * fy; Lp2 = 0.0044 * db * fy; Lp = max(Lp1, Lp2) / 100
dy = phy * L ** 2 / 3; th_y = dy / L
du = Md / My * dy + (phd - phy) * Lp * (L - 0.5 * Lp); th_u = du / L
P(f"內插 φy={phy} My={My} φu={phu} Mu={Mu_}；需求 φd={phd:.5f}  μφ={phd/phy:.3f}")
P(f"Lp: 0.08L+0.0022dbfy={Lp1:.2f} cm, 下限 0.0044dbfy={Lp2:.2f} cm → Lp={Lp*100:.2f} cm")
P(f"δy={dy*100:.4f} cm θy={th_y:.6f}  δu={du*100:.4f} cm θu={th_u:.6f}  μθ={th_u/th_y:.3f} μ={du/dy:.3f}")
# 替代：以極限點
du2 = Mu_ / My * dy + (phu - phy) * Lp * (L - 0.5 * Lp)
P(f"[替代：極限點] μφ={phu/phy:.2f} μ=μθ={du2/dy:.3f}")

# ======================= RC-2025-2 耐震梁剪力筋
P("=== RC-2025-2")
b, d, h, ln = 60, 76, 85, 900
Tt, at, Mn_ = mpr(8 * 8.14, 4200, b, d); Tb, ab, Mp_ = mpr(6 * 8.14, 4200, b, d)
Vsw = (Mn_ + Mp_) / 1e5 / 9; Vg = 2 * 9 / 2; Ve = Vsw + Vg
P(f"Mpr-={Mn_/1e5:.2f} (a={at:.2f}) Mpr+={Mp_/1e5:.2f} (a={ab:.2f}) Vsway={Vsw:.3f} Vg={Vg} Ve={Ve:.3f} 比={Vsw/Ve:.3f}")
Vs = Ve / 0.75; P(f"Vc=0 → Vs={Vs:.2f} tf ; Vs上限 2.12√f'c bw d={2.12*sfc*b*d/1000:.1f} tf")
for legs in (2, 3, 4):
    P(f"  D13 {legs} 肢 s={legs*1.27*2800*d/(Vs*1000):.2f} cm")
P(f"塑鉸區 s 上限 min(d/4={d/4}, 6db={6*3.22:.2f}, 15)=15 ; 範圍 2h={2*h} cm")
P(f"[若 Vc 計入] Vc={0.53*sfc*b*d/1000:.2f} → Vs={Vs-0.53*sfc*b*d/1000:.2f}")

# ======================= RC-2004-4 細長柱設計值
P("=== RC-2004-4")
PD, PL = 200, 100
Pu = 1.2 * PD + 1.6 * PL; P(f"Pu=1.2D+1.6L={Pu} tf (1.4D={1.4*PD})")
MX = dict(top=1.2 * 8 + 1.6 * 9, bot=1.2 * 12 + 1.6 * 8)
MY = dict(top=1.2 * 10 + 1.6 * 12, bot=1.2 * 10 + 1.6 * 6)
P(f"Mux 頂={MX['top']:.2f} 底={MX['bot']:.2f}；Muy 頂={MY['top']:.2f} 底={MY['bot']:.2f}")
bd = 1.2 * PD / Pu
for lu in (530, 600):
    P(f"-- ℓu={lu}, k=1.0, βdns={bd:.3f}")
    for ax, Mm, hdep, bw in (("X(深50)", MX, 50, 70), ("Y(深70)", MY, 70, 50)):
        M1, M2 = min(Mm.values()), max(Mm.values()); ratio = -M1 / M2  # 單曲率為負
        r = 0.3 * hdep; kl = lu / r; lim = min(40, 34 + 12 * ratio)
        Ig = bw * hdep ** 3 / 12; EI = 0.4 * Ec * Ig / (1 + bd)
        Pc = pi ** 2 * EI / lu ** 2 / 1000
        Cm = 0.6 - 0.4 * ratio; dl = max(1.0, Cm / (1 - Pu / (0.75 * Pc)))
        M2min = Pu * (1.5 + 0.03 * hdep) / 100
        Mc = dl * max(M2, M2min)
        if kl > lim:
            P(f"  {ax}: klu/r={kl:.3f} 限值={lim:.3f} 細長  Pc={Pc:.1f} Cm={Cm:.4f} δ={dl:.4f} Mc=δ·M2={Mc:.2f}")
        else:
            P(f"  {ax}: klu/r={kl:.3f} 限值={lim:.3f} 可忽略細長效應 → 不放大（若硬算 δ={dl:.4f}, {Mc:.2f}，僅供參考）")

# ======================= RC-2006-2 放大彎矩
P("=== RC-2006-2")
b = 50; lu = 600; k = 0.9; Pu = 400; bd = 0.3; M1, M2 = 15, 27
r = 0.3 * b; P(f"klu/r={k*lu/r:.2f} 限值={min(40,34-12*M1/M2):.3f}")
Ig = b ** 4 / 12; Ise = 6 * 8.14 * 18 ** 2
EIb = (0.2 * Ec * Ig + Es * Ise) / (1 + bd); EIa = 0.4 * Ec * Ig / (1 + bd)
Cm = 0.6 + 0.4 * M1 / M2
for nm, EI in (("(0.2EcIg+EsIse)/(1+βd)", EIb), ("0.4EcIg/(1+βd)", EIa)):
    Pc = pi ** 2 * EI / (k * lu) ** 2 / 1000; dl = max(1, Cm / (1 - Pu / (0.75 * Pc)))
    P(f"{nm}: EI={EI:.4e} Pc={Pc:.1f} Cm={Cm:.4f} δ={dl:.4f} Mc={dl*M2:.2f} tf·m")
P(f"Ise={Ise:.0f} cm4 Ig={Ig:.0f}；M2min={Pu*(1.5+0.03*b)/100:.1f} tf·m")
Ec2 = 12000 * sfc
EIb2 = (0.2 * Ec2 * Ig + Es * Ise) / (1 + bd); Pc2 = pi ** 2 * EIb2 / (k * lu) ** 2 / 1000
P(f"[敏感度 Ec=12000√f'c] Pc={Pc2:.1f} δ={Cm/(1-Pu/(0.75*Pc2)):.4f} Mc={Cm/(1-Pu/(0.75*Pc2))*M2:.2f}")

# ======================= RC-2016-3
P("=== RC-2016-3")
b = 40; lu = 800; K = 0.9; Pu = 130; M1, M2 = 35, 40
Ig = b ** 4 / 12; EI = 0.25 * Ec * Ig; Pc = pi ** 2 * EI / (K * lu) ** 2 / 1000
r = 0.3 * b; ratio = +M1 / M2  # 雙曲率為正（現行）
P(f"klu/r={K*lu/r:.1f} 限值={min(40,34+12*ratio):.2f}  EI={EI:.4e} Pc={Pc:.2f} tf  Pu/0.75Pc={Pu/(0.75*Pc):.4f}")
for nm, Cm in (("現行 Cm=0.6-0.4M1/M2（無下限）", 0.6 - 0.4 * ratio), ("舊式 Cm≥0.4", max(0.4, 0.6 - 0.4 * ratio))):
    dl_raw = Cm / (1 - Pu / (0.75 * Pc)); dl = max(1, dl_raw)
    P(f"{nm}: Cm={Cm:.3f} δ計={dl_raw:.4f} δ={dl:.4f} Mc={dl*M2:.2f} tf·m")
P(f"M2min={Pu*(1.5+0.03*b)/100:.2f} tf·m")

# ======================= RC-2003-2 柱主筋搭接
P("=== RC-2003-2")
db = 2.87; fy = 4200; cov = 4; dt = 1.27; b = 60
xc = cov + dt + db / 2; sp = (b - 2 * xc) / 4
cb = min(xc, sp / 2); n = 5; Atr = 3 * 1.27; s = 10
Ktr = 40 * Atr / (s * n); ratio = min(2.5, (cb + Ktr) / db)
ld = fy / (3.5 * sfc) * 1.0 / ratio * db
ld_old = 0.28 * db * fy / sfc * 1.0 * db / ((cb + Ktr) if (cb + Ktr) / db < 2.5 else 2.5 * db)
P(f"筋心距面 {xc:.3f}；筋距 {sp:.3f}；cb={cb:.3f}；Ktr=40Atr/(sn)={Ktr:.3f}；(cb+Ktr)/db={(cb+Ktr)/db:.3f}→{ratio}")
P(f"ld(現行 1/3.5)={ld:.2f} cm；ld(考卷 0.28 式)={ld_old:.2f} cm")
P(f"乙級 1.3ld={1.3*ld:.2f} cm（考卷式 {1.3*ld_old:.2f}）；甲級 1.0ld={ld:.2f}")
P(f"柱中央半高範圍：{300/4:.0f}～{300*3/4:.0f} cm；搭接置中 → {150-1.3*ld/2:.1f}～{150+1.3*ld/2:.1f} cm")
P(f"箍筋 s 檢核 min(b/4={b/4}, 6db={6*db:.1f}, so≤15) ≥ 10 OK")
