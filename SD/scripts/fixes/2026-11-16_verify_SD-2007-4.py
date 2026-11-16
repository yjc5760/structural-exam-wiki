#!/usr/bin/env python3
"""SD-2007-4 勘誤驗算（2026-11-16）：回歸期換算（卜瓦松與二項式兩路）、s_o 公式範圍、正本中的條文數值與殘留檢查。
用法：python3 <本檔> <SD 科目資料夾>；最後印 MISMATCHES: n"""
import sys, math
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
md = (SD/"raw/solutions/SD-2007-4/SD-2007-4.md").read_text(encoding="utf-8")
mism = []
# 1. 回歸期：路徑一 卜瓦松 T = -n/ln(1-p)
T475 = -50/math.log(0.9); T2 = -50/math.log(0.98)
if round(T475, 1) != 474.6: mism.append(("T475", T475))
if round(T2) != 2475: mism.append(("T2%", T2))
# 路徑二：二項式反驗 1-(1-1/T)^50
p1 = 1-(1-1/475)**50; p2 = 1-math.exp(-50/475)
if abs(p1-0.1) > 1e-3 or abs(p2-0.1) > 1e-3: mism.append(("p back", p1, p2))
if abs(1/475*100-0.21) > 0.005: mism.append("annual 0.21%")
if abs(50/0.10-500) > 0: mism.append("first-order 500")
for s in ("474.6", "0.21\\%", "500 \\text{ 年偏大", "2475 年，規範取 2500 年"):
    if s not in md: mism.append(("text missing", s))
# 2. s_o = 10 + (35 - hx)/3 cm，10 ≤ s_o ≤ 15
for hx in (5, 10, 20, 35):
    so = min(max(10+(35-hx)/3, 10), 15)
    if not 10 <= so <= 15: mism.append(("so", hx, so))
if abs((10+(35-20)/3)-15) > 1e-12: mism.append("so(hx=20)=15")   # hx ≤ 20 cm 時上限 15 控制
# 3. 條文數值出現在正本（112 年版 18.4）
for s in ("\\frac{6}{5}\\sum M_{nb,beam}", "A_gf'_c/10", "A_gf'_c/20", "45\\text{ cm}", "l_u/6", "最小斷面尺寸的 1/4",
          "6 倍", "s_o = 10 + \\dfrac{35-h_x}{3}", "10 \\le s_o \\le 15", "不大於 15 cm", "1.25 f_y", "\\phi=0.75", "不得小於結構分析所得"):
    if s not in md: mism.append(("clause missing", s))
if abs(6/5-1.2) > 1e-12: mism.append("6/5")
# 4. 殘留：梁的 d/4、ACI、h_col、美國場址類別
body = "\n".join(l for l in md[md.index("## 2."):md.index("*修正日期")].splitlines() if not l.startswith("*圖"))  # 頁尾與圖說可提到被攔下的錯誤
for bad in ("$d/4$", "ACI", "h_{col}", "$S_D$", "S_E", "≈ 475 年（取整）", "2,475"):
    if bad in body: mism.append(("residual", bad))
print("T475 =", round(T475,2), "T2% =", round(T2,1), "p =", round(p1,4))
for x in mism: print("MISMATCH", x)
print("MISMATCHES:", len(mism))
