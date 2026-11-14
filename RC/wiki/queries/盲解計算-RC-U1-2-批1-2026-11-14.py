# -*- coding: utf-8 -*-
"""盲解計算 — RC-U1-2 批1（2026-11-14）
單位：kgf、cm；輸出 tf、tf·m
規範：建築物混凝土結構設計規範（2023，對應 ACI 318-19）
  εcu=0.003；Es=2.04e6；β1=0.85-0.05(f'c-280)/70，0.65~0.85
  φ：壓力控制 εt≤εty → 0.65（箍筋）／0.75（螺筋）；拉力控制 εt≥εty+0.003 → 0.90；其間線性
  Pn,max=0.80Po（箍筋）／0.85Po（螺筋）
"""
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

Es = 2.04e6
ecu = 0.003


def beta1(fc):
    return min(0.85, max(0.65, 0.85 - 0.05 * (fc - 280) / 70))


def phi_tied(et, fy, spiral=False):
    ety = fy / Es
    lo = 0.75 if spiral else 0.65
    if et <= ety:
        return lo
    if et >= ety + 0.003:
        return 0.90
    return lo + (0.90 - lo) * (et - ety) / 0.003


def whitney(c, h, b, fc, fy, layers, xref):
    """layers: [(dist from compression face, As)]；回傳 Pn, Mn(對 xref，自壓力緣量), εt"""
    b1 = beta1(fc)
    a = min(b1 * c, h)
    Cc = 0.85 * fc * a * b
    P = Cc
    M = Cc * (xref - a / 2)
    for d, As in layers:
        es = ecu * (c - d) / c
        fs = max(-fy, min(fy, Es * es))
        if d < a and fs > 0:
            fs -= 0.85 * fc  # 扣除被鋼筋佔據的混凝土
        F = fs * As
        P += F
        M += F * (xref - d)
    dt = max(d for d, _ in layers)
    et = ecu * (dt - c) / c
    return P, M, et


def show(tag, P, M):
    print(f"  {tag}: Pn={P/1000:.2f} tf, Mn={M/1e5:.2f} tf-m")


print("=" * 70)
print("RC-2002-2  40(彎曲向)x30，3-#9@7、3-#9@33，e=10 cm，f'c=280")
A9 = 6.47
L = [(7, 3 * A9), (33, 3 * A9)]
h, b, fc, fy = 40, 30, 280, 4200
f = lambda c: whitney(c, h, b, fc, fy, L, 20)[1] - 10 * whitney(c, h, b, fc, fy, L, 20)[0]
c = brentq(f, 5, 200)
P, M, et = whitney(c, h, b, fc, fy, L, 20)
print(f"  c={c:.3f} cm, a={beta1(fc)*c:.3f}, εs(拉側)={et:.5f}")
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}, fs={max(-fy,min(fy,Es*es)):.0f}")
show("結果", P, M)
P_2002 = (P, M)
# 對照：不扣除位移混凝土
def whitney_nodisp(c, h, b, fc, fy, layers, xref):
    b1 = beta1(fc); a = min(b1 * c, h); Cc = 0.85 * fc * a * b; P = Cc; M = Cc * (xref - a / 2)
    for d, As in layers:
        fs = max(-fy, min(fy, Es * ecu * (c - d) / c)); P += fs * As; M += fs * As * (xref - d)
    return P, M
c2 = brentq(lambda c: whitney_nodisp(c, h, b, fc, fy, L, 20)[1] - 10 * whitney_nodisp(c, h, b, fc, fy, L, 20)[0], 5, 200)
P2, M2 = whitney_nodisp(c2, h, b, fc, fy, L, 20)
print(f"  對照（不扣位移混凝土）c={c2:.3f} Pn={P2/1000:.2f} Mn={M2/1e5:.2f}")

print("=" * 70)
print("RC-2005-1  60(彎曲向)x50，#8 三層 3/2/3 @7/30/53，Pn=90 t，f'c=280")
A8 = 5.067
L = [(7, 3 * A8), (30, 2 * A8), (53, 3 * A8)]
h, b, fc, fy = 60, 50, 280, 4200
Pt = 90e3
c = brentq(lambda c: whitney(c, h, b, fc, fy, L, 30)[0] - Pt, 1, 60)
P, M, et = whitney(c, h, b, fc, fy, L, 30)
print(f"  c={c:.3f}, a={0.85*c:.3f}, εt={et:.5f}")
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}")
show("極限", P, M)
phiu = ecu / c
print(f"  φu=0.003/c={phiu:.4e} 1/cm")

# 降伏曲率：最外拉力筋 εs=εy，同 P=90 t
ey = fy / Es


def section_fiber(phi_curv, eps_top, h, b, fc, layers, model="hognestad", Ec=None, n=400):
    """以壓力緣應變 eps_top、曲率 phi 積分；回傳 P, M(對 h/2)"""
    y = (np.arange(n) + 0.5) * h / n  # 自壓力緣
    eps = eps_top - phi_curv * y
    e0 = 0.002
    if model == "hognestad":
        fcs = np.where(eps > 0, fc * (2 * eps / e0 - (eps / e0) ** 2), 0.0)
        fcs = np.where(eps > e0, fc * (1 - 0.15 * (eps - e0) / (0.0038 - e0)), fcs)
    elif model == "linear":
        fcs = np.where(eps > 0, Ec * eps, 0.0)
    elif model == "fig2017":
        fcs = np.where(eps > 0, np.where(eps <= 0.002, fc * eps / 0.002, fc * (1 - 0.2 * (eps - 0.002) / 0.001)), 0.0)
    dA = b * h / n
    P = np.sum(fcs * dA)
    M = np.sum(fcs * dA * (h / 2 - y))
    for d, As in layers:
        es = eps_top - phi_curv * d
        fs = max(-4200, min(4200, Es * es))
        ec = eps_top - phi_curv * d
        # 扣除鋼筋位置混凝土
        if model == "hognestad":
            fcd = fc * (2 * ec / e0 - (ec / e0) ** 2) if 0 < ec <= e0 else (fc * (1 - 0.15 * (ec - e0) / 0.0018) if ec > e0 else 0)
        elif model == "linear":
            fcd = Ec * ec if ec > 0 else 0
        else:
            fcd = (fc * ec / 0.002 if ec <= 0.002 else fc * (1 - 0.2 * (ec - 0.002) / 0.001)) if ec > 0 else 0
        F = (fs - fcd) * As
        P += F
        M += F * (h / 2 - d)
    return P, M


def yield_curv(h, b, fc, layers, Ptarget, model="hognestad", Ec=None):
    dt = max(d for d, _ in layers)

    def g(c):
        phi_c = ey / (dt - c)
        return section_fiber(phi_c, phi_c * c, h, b, fc, layers, model, Ec)[0] - Ptarget
    grid = np.linspace(0.5, dt - 0.5, 400)
    vals = [g(x) for x in grid]
    i = next(k for k in range(len(grid) - 1) if vals[k] < 0 <= vals[k + 1])
    c = brentq(g, grid[i], grid[i + 1])
    phi_c = ey / (dt - c)
    P, M = section_fiber(phi_c, phi_c * c, h, b, fc, layers, model, Ec)
    return c, phi_c, phi_c * c, M


for model, Ec in [("hognestad", None), ("linear", 15000 * math.sqrt(fc)), ("linear", 12000 * math.sqrt(fc))]:
    cy, phiy, etop, My = yield_curv(h, b, fc, L, Pt, model, Ec)
    print(f"  降伏[{model}{'' if Ec is None else ' Ec=%.0f'%Ec}]: c_y={cy:.3f}, εc,top={etop:.5f}, φy={phiy:.4e}, My={My/1e5:.2f} → μφ={phiu/phiy:.2f}")

print("=" * 70)
print("RC-2008-2  56x40，c=48（自右緣），f'c=350，對幾何中心取矩")
h, b, fc, fy = 56, 40, 350, 4200
L = [(8, 4 * A8), (28, 2 * 5.07), (48, 2 * 5.07)]
L = [(8, 4 * 5.07), (28, 2 * 5.07), (48, 2 * 5.07)]
c = 48
P, M, et = whitney(c, h, b, fc, fy, L, 28)
print(f"  β1={beta1(fc)}, a={beta1(fc)*c:.2f}")
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}, fs={max(-fy,min(fy,Es*es)):.0f}")
show("對幾何中心", P, M)
print(f"  e=M/P={M/P:.3f} cm")
# 塑性中心對照
P0c = 0.85 * fc * (h * b - 8 * 5.07)
xpc = (0.85 * fc * h * b * 28 + sum((fy - 0.85 * fc) * As * d for d, As in L)) / (0.85 * fc * h * b + sum((fy - 0.85 * fc) * As for d, As in L))
print(f"  塑性中心距右緣 {xpc:.3f}；對塑性中心 Mn={(M + P*(xpc-28))/1e5:.2f}")
_, Mn_nd = whitney_nodisp(c, h, b, fc, fy, L, 28)
print(f"  對照（不扣位移混凝土）Pn={whitney_nodisp(c,h,b,fc,fy,L,28)[0]/1000:.2f} Mn={Mn_nd/1e5:.2f}")

print("=" * 70)
print("RC-2010-1  圓柱 D=75，Dc=68，12-#10，#4 螺筋，f'c=350")
fc, fy = 350, 4200
D, Dc = 75, 68
Ag = math.pi * D ** 2 / 4
Ach = math.pi * Dc ** 2 / 4
Ast = 12 * 8.17
Py = 0.85 * fc * (Ag - Ast) + fy * Ast
print(f"  Ag={Ag:.1f}, Ach={Ach:.1f}, Ast={Ast:.2f}")
print(f"  Py=Po=0.85f'c(Ag-Ast)+fyAst={Py/1000:.1f} tf")
rs_min = 0.45 * (Ag / Ach - 1) * fc / fy
Asp, dbs = 1.27, 1.27
s_req = 4 * Asp / (Dc * rs_min)
s_clear_max = 7.5 + dbs
print(f"  ρs,min={rs_min:.5f} → s≤{s_req:.2f} cm；淨距≤7.5 → s≤{s_clear_max:.2f}")
core_loss = 0.85 * fc * (Ag - Ach)
for lab, rs in [("ρs=ρs,min", rs_min), ("s=8 cm", 4 * Asp / (Dc * 8)), ("s=7.5 cm", 4 * Asp / (Dc * 7.5))]:
    Pu = 0.85 * fc * (Ach - Ast) + fy * Ast + 2 * rs * Ach * fy
    Pu2 = 0.85 * fc * (Ach - Ast) + fy * Ast + 2.05 * rs * Ach * fy
    print(f"  {lab}: ρs={rs:.5f}, 螺筋貢獻 2ρsAchfy={2*rs*Ach*fy/1000:.1f} tf → Pu={Pu/1000:.1f} tf（4.1f2 式 {Pu2/1000:.1f}）")
print(f"  保護層損失 0.85f'c(Ag-Ach)={core_loss/1000:.1f} tf")
print(f"  讀法② φPn,max=0.75×0.85×Po={0.75*0.85*Py/1000:.1f} tf")

print("=" * 70)
print("RC-2011-3  60(彎曲)x40，3-#10@6、3-#10@54，f'c=350，Pn=0.9Pb")
h, b, fc, fy = 60, 40, 350, 4200
A10 = 8.143
L = [(6, 3 * A10), (54, 3 * A10)]
cb = ecu / (ecu + fy / Es) * 54
Pb, Mb, _ = whitney(cb, h, b, fc, fy, L, 30)
print(f"  cb={cb:.3f}, Pb={Pb/1000:.2f}, Mb={Mb/1e5:.2f}")
for lab, Pt in [("讀法② Pn=0.9Pb", 0.9 * Pb)]:
    c = brentq(lambda c: whitney(c, h, b, fc, fy, L, 30)[0] - Pt, 1, cb)
    P, M, et = whitney(c, h, b, fc, fy, L, 30)
    ph = phi_tied(et, fy)
    print(f"  {lab}: c={c:.3f}, εt={et:.5f}, φ={ph:.4f}, Mn={M/1e5:.2f}, φMn={ph*M/1e5:.2f}, φPn={ph*P/1000:.2f}")
    c_u = c
    Pn_i = P
# 讀法①對照
def g1(c):
    P, M, et = whitney(c, h, b, fc, fy, L, 30)
    return phi_tied(et, fy) * P - 0.9 * Pb
c1 = brentq(g1, 5, 200)
P1, M1, et1 = whitney(c1, h, b, fc, fy, L, 30)
print(f"  讀法①對照 φPn=0.9Pb: c={c1:.3f}, εt={et1:.5f}, φ={phi_tied(et1,fy):.3f}, Pn={P1/1000:.1f}, φMn={phi_tied(et1,fy)*M1/1e5:.2f}")
phiu = ecu / c_u
print(f"  ㈡ φu(Pn=0.9Pb)={phiu:.4e}")
for lab, Pt_y in [("φy 在 P=0.9Pb/1.3", 0.9 * Pb / 1.3), ("φy 在 P=0.9Pb", 0.9 * Pb)]:
    for model, Ec in [("hognestad", None), ("linear", 15000 * math.sqrt(fc))]:
        try:
            cy, phiy, etop, My = yield_curv(h, b, fc, L, Pt_y, model, Ec)
            print(f"   {lab} [{model}]: c_y={cy:.2f}, εc,top={etop:.5f}, φy={phiy:.4e} → μφ={phiu/phiy:.2f}")
        except Exception as ex:
            print(lab, model, ex)
# φu 也在 0.9Pb/1.3
Ps = 0.9 * Pb / 1.3
cs = brentq(lambda c: whitney(c, h, b, fc, fy, L, 30)[0] - Ps, 1, 60)
cy, phiy, etop, My = yield_curv(h, b, fc, L, Ps, "hognestad")
print(f"   全在 P=0.9Pb/1.3：c_u={cs:.3f}, φu={ecu/cs:.4e}, φy={phiy:.4e} → μφ={ecu/cs/phiy:.2f}")

print("=" * 70)
print("RC-2015-1  60x60，4-#10 上下 @8/52，f'c=350，最大 φMn")
h, b, fc, fy = 60, 60, 350, 4200
L = [(8, 4 * A10), (52, 4 * A10)]
Ag, Ast = 3600, 8 * A10
Po = 0.85 * fc * (Ag - Ast) + fy * Ast
cs = np.linspace(3, 80, 77001)
best = None
bestn = None
for c in cs:
    P, M, et = whitney(c, h, b, fc, fy, L, 30)
    ph = phi_tied(et, fy)
    if ph * P > 0.8 * 0.65 * Po:
        continue
    if best is None or ph * M > best[0]:
        best = (ph * M, c, P, M, et, ph)
    if bestn is None or M > bestn[0]:
        bestn = (M, c, P, et)
print(f"  Po={Po/1000:.1f}, φPn,max={0.52*Po/1000:.1f}")
print(f"  max φMn={best[0]/1e5:.2f} tf-m at c={best[1]:.3f}, φPn={best[5]*best[2]/1000:.2f}, Pn={best[2]/1000:.2f}, Mn={best[3]/1e5:.2f}, εt={best[4]:.5f}, φ={best[5]:.4f}")
print(f"  max Mn(標稱)={bestn[0]/1e5:.2f} at c={bestn[1]:.3f}, Pn={bestn[2]/1000:.2f}, εt={bestn[3]:.5f}")
cb = ecu / (ecu + fy / Es) * 52
Pb_, Mb_, _ = whitney(cb, h, b, fc, fy, L, 30)
print(f"  平衡點 cb={cb:.3f}: Pb={Pb_/1000:.2f}, Mb={Mb_/1e5:.2f}, φMb={0.65*Mb_/1e5:.2f}")
# 舊規範 0.005 對照
def phi_old(et):
    return 0.65 if et <= 0.002 else (0.9 if et >= 0.005 else 0.65 + 0.25 * (et - 0.002) / 0.003)
bo = max((phi_old(whitney(c, h, b, fc, fy, L, 30)[2]) * whitney(c, h, b, fc, fy, L, 30)[1], c) for c in np.linspace(3, 60, 5701))
print(f"  對照 φ(0.002/0.005 舊過渡區): max φMn={bo[0]/1e5:.2f} at c={bo[1]:.2f}")
# 純彎
c0 = brentq(lambda c: whitney(c, h, b, fc, fy, L, 30)[0], 1, 30)
P0_, M0_, et0 = whitney(c0, h, b, fc, fy, L, 30)
print(f"  純彎 c={c0:.3f}, Mn={M0_/1e5:.2f}, εt={et0:.4f}, φMn={phi_tied(et0,fy)*M0_/1e5:.2f}")

print("=" * 70)
print("RC-2017-1  擴柱 70(彎曲)x40，圖2 應力應變，16 根 #8（原 8 + 新 8）")
fc, fy = 210, 4200
Ab = 5.067
h, b = 70, 40


def layers2017(c0):
    # 新增：x=6.5（4 根）、63.5（4 根）；原柱：15+c0（3）、35（2）、55-c0（3）
    return [(6.5, 4 * Ab), (15 + c0, 3 * Ab), (35, 2 * Ab), (55 - c0, 3 * Ab), (63.5, 4 * Ab)]


def fig2_stress(e):
    if e <= 0:
        return 0.0
    if e <= 0.002:
        return fc * e / 0.002
    return fc * (1 - 0.2 * (e - 0.002) / 0.001)


Ag, Ast = h * b, 16 * Ab
# e=0
best0 = max(((fig2_stress(e) * (Ag - Ast) + min(fy, Es * e) * Ast), e) for e in np.linspace(0.0015, 0.003, 15001))
print(f"  e=0：P0,max={best0[0]/1000:.2f} tf at ε={best0[1]:.5f}")
print(f"   ε=0.002：{(fc*(Ag-Ast)+Es*0.002*Ast)/1000:.2f}；ε=0.003：{(0.8*fc*(Ag-Ast)+fy*Ast)/1000:.2f}；規範0.85f'c：{(0.85*fc*(Ag-Ast)+fy*Ast)/1000:.2f}")
print(f"   只計新增 8 根：{max(fig2_stress(e)*(Ag-8*Ab)+min(fy,Es*e)*8*Ab for e in np.linspace(0.0015,0.003,15001))/1000:.2f}")


def pm_fig2(c, Ls, n=2000):
    phi_c = ecu / c
    y = (np.arange(n) + 0.5) * h / n
    eps = ecu - phi_c * y
    fcs = np.array([fig2_stress(e) for e in eps])
    dA = b * h / n
    P = fcs.sum() * dA
    M = (fcs * dA * (h / 2 - y)).sum()
    for d, As in Ls:
        es = ecu - phi_c * d
        F = (max(-fy, min(fy, Es * es)) - fig2_stress(es)) * As
        P += F
        M += F * (h / 2 - d)
    return P, M


for c0, lab in [(6.5, "原柱鋼筋距原柱面 6.5"), (8.6, "原柱鋼筋距原柱面 8.6（量圖）")]:
    Ls = layers2017(c0)
    res = max((pm_fig2(c, Ls)[1], c) for c in np.arange(5, 70, 0.25))
    cc = minimize_scalar(lambda c: -pm_fig2(c, Ls)[1], bounds=(res[1] - 1, res[1] + 1), method="bounded").x
    P, M = pm_fig2(cc, Ls)
    print(f"  {lab}: max Mn={M/1e5:.2f} tf-m at c={cc:.3f}, Pn={P/1000:.2f} tf")
Ls8 = [(6.5, 4 * Ab), (63.5, 4 * Ab)]
res = max((pm_fig2(c, Ls8)[1], c) for c in np.arange(5, 70, 0.25))
print(f"  只計新增 8 根: max Mn={res[0]/1e5:.2f} at c≈{res[1]}")
Ls = layers2017(6.5)
cb = ecu / (ecu + fy / Es) * 63.5
Pb, Mb = pm_fig2(cb, Ls)
print(f"  平衡點 cb={cb:.2f}: Pn={Pb/1000:.2f}, Mn={Mb/1e5:.2f}")
# Whitney 對照
Lw = layers2017(6.5)
rw = max((whitney(c, h, b, fc, fy, Lw, 35)[1], c) for c in np.arange(5, 70, 0.05))
print(f"  對照（規範 Whitney 0.85f'c）max Mn={rw[0]/1e5:.2f} at c={rw[1]:.2f}, Pn={whitney(rw[1],h,b,fc,fy,Lw,35)[0]/1000:.1f}")

print("=" * 70)
print("RC-2019-2  70(彎曲)x50，5-#8@7、5-#8@63，Pu=291 tf，壓力控制 φ=0.65")
h, b, fc, fy = 70, 50, 280, 4200
L = [(7, 5 * 5.07), (63, 5 * 5.07)]
Ag, Ast = 3500, 10 * 5.07
Po = 0.85 * fc * (Ag - Ast) + fy * Ast
Pn_t = 291e3 / 0.65
print(f"  Pn=291/0.65={Pn_t/1000:.2f}；Po={Po/1000:.1f}；φPn,max={0.52*Po/1000:.1f}")
c = brentq(lambda c: whitney(c, h, b, fc, fy, L, 35)[0] - Pn_t, 1, 300)
P, M, et = whitney(c, h, b, fc, fy, L, 35)
print(f"  c={c:.3f}, a={0.85*c:.3f}, εt={et:.5f}（εty={fy/Es:.5f}）φ={phi_tied(et,fy)}")
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}, fs={max(-fy,min(fy,Es*es)):.0f}")
show("Pn,Mn", P, M)
print(f"  Mu,max=φMn={0.65*M/1e5:.2f} tf-m")
c2 = brentq(lambda c: whitney_nodisp(c, h, b, fc, fy, L, 35)[0] - Pn_t, 1, 300)
print(f"  對照不扣位移混凝土 φMn={0.65*whitney_nodisp(c2,h,b,fc,fy,L,35)[1]/1e5:.2f}")

print("=" * 70)
print("RC-2021-2  50x50，3/2/3 @6.5/25/43.5，c=14.5，f'c=280")
h, b, fc, fy = 50, 50, 280, 4200
L = [(6.5, 3 * 5.067), (25, 2 * 5.067), (43.5, 3 * 5.067)]
c = 14.5
P, M, et = whitney(c, h, b, fc, fy, L, 25)
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}, fs={max(-fy,min(fy,Es*es)):.0f}")
print(f"  a={0.85*c:.4f}")
show("結果", P, M)
print(f"  ex=Mn/Pn={M/P:.2f} cm；εt={et:.5f}")
Pn2, Mn2 = whitney_nodisp(c, h, b, fc, fy, L, 25)
print(f"  對照不扣位移混凝土：Pn={Pn2/1000:.2f}, Mn={Mn2/1e5:.2f}, ex={Mn2/Pn2:.2f}")

print("=" * 70)
print("RC-2024-3  40x40，3/2/3 @8/20/32，c=32，f'c=280")
h, b, fc, fy = 40, 40, 280, 4200
L = [(8, 3 * 5.07), (20, 2 * 5.07), (32, 3 * 5.07)]
c = 32
P, M, et = whitney(c, h, b, fc, fy, L, 20)
for d, As in L:
    es = ecu * (c - d) / c
    print(f"   d={d}: εs={es:.5f}, fs={max(-fy,min(fy,Es*es)):.0f}")
print(f"  a={0.85*c:.2f}")
show("結果", P, M)
Pn2, Mn2 = whitney_nodisp(c, h, b, fc, fy, L, 20)
print(f"  對照不扣位移混凝土：Pn={Pn2/1000:.2f}, Mn={Mn2/1e5:.2f}")
print(f"  e={M/P:.2f} cm；φ=0.65 → φPn={0.65*P/1000:.2f}, φMn={0.65*M/1e5:.2f}")

print("=" * 70)
print("補充（比對後追加，非盲解主結果）：RC-2011-3 φu、φy 都在 P=0.9Pb/1.3，線彈性 Ec=15000√f'c")
h, b, fc, fy = 60, 40, 350, 4200
L = [(6, 3 * 8.143), (54, 3 * 8.143)]
cb = ecu / (ecu + fy / Es) * 54
Pb = whitney(cb, h, b, fc, fy, L, 30)[0]
Ps = 0.9 * Pb / 1.3
cs = brentq(lambda c: whitney(c, h, b, fc, fy, L, 30)[0] - Ps, 1, 60)
for model, Ec in [("hognestad", None), ("linear", 15000 * math.sqrt(fc)), ("linear", 12000 * math.sqrt(fc))]:
    cy, phiy, etop, My = yield_curv(h, b, fc, L, Ps, model, Ec)
    print(f"  [{model} {Ec}] c_u={cs:.3f} c_y={cy:.3f} → μφ={ecu/cs/phiy:.2f}")
