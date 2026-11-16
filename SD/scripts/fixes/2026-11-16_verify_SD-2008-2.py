#!/usr/bin/env python3
"""SD-2008-2 勘誤驗算（2026-11-16）：12 層示例 r_i 與 r_i/r_i+1（兩路：累加式與層力倒三角分配），弱層判定、殘留檢查。
用法：python3 <本檔> <SD 科目資料夾>；最後印 MISMATCHES: n"""
import sys, re
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
md = (SD/"raw/solutions/SD-2008-2/SD-2008-2.md").read_text(encoding="utf-8")
mism = []
N = 12
# 路徑一：V_i = Σ_{j≥i} j
V1 = [sum(range(i, N+1)) for i in range(1, N+1)]
# 路徑二：倒三角層力 F_x = V_base·w h_x/Σ w h（等重等高），由上往下累加
Vb = 78.0; F = [Vb*x/sum(range(1, N+1)) for x in range(1, N+1)]
V2 = [sum(F[i:]) for i in range(N)]
if any(abs(a-b) > 1e-9 for a, b in zip(V1, V2)): mism.append(("V two paths", V1, V2))
Vu = [V1[(i//3)*3] for i in range(N)]
r = [Vu[i]/V1[i] for i in range(N)]
q = [r[i]/r[i+1] for i in range(N-1)]
# 與正本表格逐格比對
for i in range(N):
    m = re.search(rf"^\| {i+1} \| (\d+) \| (\d+) \| ([\d.]+) \| ([^|]+)\|", md, re.M)
    if not m: mism.append(("row", i+1)); continue
    if int(m.group(1)) != V1[i] or int(m.group(2)) != Vu[i] or abs(float(m.group(3))-round(r[i],3)) > 1e-9:
        mism.append(("row val", i+1, m.groups()))
    if i < N-1:
        g = float(re.findall(r"[\d.]+", m.group(4))[0])
        if abs(g-round(q[i],3)) > 1e-9: mism.append(("ratio", i+1, g, q[i]))
weak = [i+1 for i in range(N-1) if q[i] < 0.8]
if weak != [10, 11]: mism.append(("weak", weak))
trans = [q[i] for i in (2, 5, 8)]
if abs(min(trans)-1.040) > 5e-4 or abs(max(trans)-1.357) > 5e-4: mism.append(("transition range", trans))
for s in ("第 10 層（0.697）", "第 11 層（0.522）", "1.040～1.357", "第 1、4、7、10 層"):
    if s not in md: mism.append(("text", s))
# 殘留：強度對強度的比較式、表 1-1 出處
body = "\n".join(l for l in md[md.index("## 2."):md.index("*修正日期")].splitlines() if not l.startswith("*圖"))  # 頁尾與圖說可提到被攔下的錯誤
for bad in ("\\frac{V_{u,i}}{V_{u,i+1}}", "規範容許比值", "表 1-1 立面不規則第 5 項「強度不連續性弱層」）：**弱層", "強度突降層」，極限強度比值不足", "強度突變比"):
    if bad in body: mism.append(("residual", bad))
if "r_i = \\frac{V_{u,i}}{V_i} \\;\\geq\\; 0.8\\,r_{i+1}" not in md: mism.append("new formula missing")
print("r =", [round(x,3) for x in r]); print("weak stories:", weak)
for x in mism: print("MISMATCH", x)
print("MISMATCHES:", len(mism))
