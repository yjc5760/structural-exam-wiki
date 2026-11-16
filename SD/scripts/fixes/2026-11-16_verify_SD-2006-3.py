#!/usr/bin/env python3
"""SD-2006-3 勘誤驗算（2026-11-16）：現行規範譜形分段（表 2-5(a)）連續性、各因素對譜值的影響、§4 示意數值表。
用法：python3 <本檔> <SD 科目資料夾>；最後印 MISMATCHES: n"""
import sys, re
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
md = (SD/"raw/solutions/SD-2006-3/SD-2006-3.md").read_text(encoding="utf-8")
mism = []
def SaD(T, SDS, SD1):
    T0 = SD1/SDS
    if T <= 0.2*T0: return SDS*(0.4+3*T/T0)
    if T <= T0: return SDS
    if T <= 2.5*T0: return SD1/T
    return 0.4*SDS
# 1. 連續性（路徑一：閉合分段兩端代入）
SDS, SD1 = 0.60, 0.35; T0 = SD1/SDS
for Tb in (0.2*T0, T0, 2.5*T0):
    l, r = SaD(Tb*(1-1e-9), SDS, SD1), SaD(Tb*(1+1e-9), SDS, SD1)
    if abs(l-r) > 1e-6: mism.append(("continuity", Tb, l, r))
if abs(SaD(0, SDS, SD1)-0.4*SDS) > 1e-12: mism.append(("T=0", SaD(0,SDS,SD1)))
# 2. 路徑二：數值掃描 dSa/dT 的符號分區，與分段點一致
Ts = [i*0.0005 for i in range(1, 8001)]
v = [SaD(t, SDS, SD1) for t in Ts]
up_end = max(t for t, a, b in zip(Ts, v, v[1:]) if b-a > 1e-9)
dn = [t for t, a, b in zip(Ts, v, v[1:]) if a-b > 1e-9]
if abs(up_end-0.2*T0) > 1e-3: mism.append(("rise end", up_end, 0.2*T0))
if abs(min(dn)-T0) > 1e-3 or abs(max(dn)-2.5*T0) > 1e-3: mism.append(("fall zone", min(dn), max(dn)))
if abs(max(v)-SDS) > 1e-9: mism.append(("max", max(v)))
# 3. §4 示意數值表
rows = {"基準 $S_{aD}$": (0.60, 0.35),
        "$S_S^D$ 加大（$S_{DS}=0.72$）": (0.72, 0.35),
        "$S_1^D$ 加大（$S_{D1}=0.42$）": (0.60, 0.42)}
Tlist = [0.05, 0.3, 0.8, 1.5, 3.0]
for lab, (a, b) in rows.items():
    m = re.search(re.escape("| "+lab+" |")+r"([^\n]*)", md)
    if not m: mism.append(("row missing", lab)); continue
    vals = [float(x) for x in re.findall(r"\d+\.\d+", m.group(1))]
    calc = [SaD(T, a, b) for T in Tlist]
    for T, c, g in zip(Tlist, calc, vals):
        if abs(round(c+1e-12, 3)-g) > 1e-9: mism.append((lab, T, round(c,4), g))
    print(lab, [round(c,4) for c in calc])
if "$T_0^D=0.583$ s" not in md or abs(T0-0.583) > 5e-4: mism.append(("T0 text", T0))
# 4. 趨勢陳述：S_S^D 加大各週期不減；S_1^D 加大時極短週期降低（§4 因素二、§3 陷阱 5）
grid = [i*0.01 for i in range(1, 401)]
if any(SaD(t,0.72,0.35) < SaD(t,0.60,0.35)-1e-12 for t in grid): mism.append("SS up not monotone")
if not SaD(0.05,0.60,0.42) < SaD(0.05,0.60,0.35): mism.append("S1 up short-period drop not reproduced")
if any(SaD(t,0.60,0.42) < SaD(t,0.60,0.35)-1e-12 for t in grid if t > 0.2*0.7): mism.append("S1 up drop beyond 0.2T0")
# 近斷層（兩係數同乘 1.2）各週期不減
if any(SaD(t,0.72,0.42) < SaD(t,0.60,0.35)-1e-12 for t in grid): mism.append("near-fault not monotone")
# 5. 殘留：§2 起不得再出現 ASCE 7 架構當主線（只容許陷阱表、§5 舊解對照）
body = "\n".join(l for l in md[md.index("## 3.5"):md.index("## 5.")].splitlines() if not l.startswith("*圖"))  # 圖說可提到被攔下的錯誤
for bad in [r"\frac{2}{3}S_{MS}", "T_L", "SA～SF", "0.6T/T_0", "2475", "B(\\xi)", "I_e"]:
    if bad in body: mism.append(("residual in §3.5–§4", bad))
print("T0 =", round(T0,4), "rise end", up_end, "fall", min(dn), max(dn))
for x in mism: print("MISMATCH", x)
print("MISMATCHES:", len(mism))
