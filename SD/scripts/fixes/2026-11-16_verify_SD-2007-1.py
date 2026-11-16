#!/usr/bin/env python3
"""SD-2007-1 勘誤驗算（2026-11-16）：等位移／等能量推導（sympy 閉合解＋數值面積積分兩路）、R_a 的 2/3 分配、§2.4 與 §5-4 數值、殘留檢查。
用法：python3 <本檔> <SD 科目資料夾>；最後印 MISMATCHES: n"""
import sys, math
from pathlib import Path
import sympy as sp
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
md = (SD/"raw/solutions/SD-2007-1/SD-2007-1.md").read_text(encoding="utf-8")
mism = []
# 1. 等能量：sympy 解 (1/2)Fe ue = (1/2)Fy uy + Fy(mu uy - uy)
Fe, Fy, k, mu = sp.symbols("F_e F_y k mu", positive=True)
sol = sp.solve(sp.Eq(Fe**2/(2*k), Fy**2/(2*k) + Fy*(Fy/k)*(mu-1)), Fe)
ratio = sp.simplify(sol[0]/Fy)
if sp.simplify(ratio - sp.sqrt(2*mu-1)) != 0: mism.append(("energy", ratio))
# 路徑二：數值積分 EPP 曲線下面積，反求 Fe/Fy
for m in (2.0, 3.0, 3.5333333, 4.6):
    n = 200000; uy = 1.0; um = m*uy
    area = sum(min(((i+0.5)*um/n)/uy, 1.0) for i in range(n))*um/n   # Fy=k=1
    fe = math.sqrt(2*area)
    if abs(fe - math.sqrt(2*m-1)) > 1e-6: mism.append(("numeric energy", m, fe))
# 等位移：Fe/k = mu Fy/k
if sp.simplify(sp.solve(sp.Eq(Fe/k, mu*Fy/k), Fe)[0]/Fy - mu) != 0: mism.append("equal disp")
# 2. R_a：(R_a-1) = 2/3 (R-1)  <=> R_a = 1+(R-1)/1.5；臺北盆地 1/2 <=> 除數 2.0
Rs = sp.symbols("R", positive=True)
if sp.simplify((1+(Rs-1)/sp.Rational(3,2) - 1) - sp.Rational(2,3)*(Rs-1)) != 0: mism.append("Ra 2/3")
if sp.simplify((1+(Rs-1)/2 - 1) - sp.Rational(1,2)*(Rs-1)) != 0: mism.append("Ra basin")
# 3. §2.4 數值例（R = 4.8）
R = 4.8; Ra = 1+(R-1)/1.5; Fm = math.sqrt(2*Ra-1)
checks = [("1 + 2.533 = 3.533", abs((R-1)/1.5-2.5333) < 1e-3 and abs(Ra-3.5333) < 1e-3),
          ("\\sqrt{6.067} = 2.46", abs(2*Ra-1-6.0667) < 1e-3 and abs(Fm-2.463) < 1e-3),
          ("F_u\\big|_{\\text{長週期}} = 3.53", abs(Ra-3.53) < 5e-3),
          ("約 26%", abs((1-Ra/R)-0.264) < 5e-3)]
for s, ok in checks:
    if s not in md: mism.append(("text missing", s))
    if not ok: mism.append(("value", s))
if not Fm < Ra: mism.append("sqrt(2Ra-1) < Ra")
# 4. 圖腳本常數與正本一致
g = (SD/"raw/solutions/SD-2007-1/gen_SD-2007-1.py").read_text(encoding="utf-8")
for s in ("R      = 4.8", "ALPHA_Y = 1.5", "OVERSTR = 1.4", "RA      = 1 + (R - 1) / 1.5"):
    if s not in g: mism.append(("gen const", s))
# 5. 殘留：ASCE 7 的 2/3 與 1.5 倍只能出現在 §1 常見誤讀與 §5 舊解註記
lines = [l for l in md.splitlines() if ("S_{MS}" in l or "1.5 倍" in l or "1.5S_{aD}" in l or "1.5\\,S_{aD}" in l)]
for l in lines:
    if not (l.startswith("| $R_a$ 的 1.5") or l.startswith("（本庫勘誤前")):
        mism.append(("residual", l[:60]))
if "只准用掉 $R$ 的 2/3" in md or "只准用掉 } R \\text{ 的 2/3" in md: mism.append("residual R 2/3")
print("Ra =", round(Ra,4), "Fu_mid =", round(Fm,4), "energy ratio:", ratio)
for x in mism: print("MISMATCH", x)
print("MISMATCHES:", len(mism))
