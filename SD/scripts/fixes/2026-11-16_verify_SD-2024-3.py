#!/usr/bin/env python3
"""SD-2024-3 勘誤驗算（2026-11-16）：論述題，重算正本中的數值關係並檢查舊觀念已清除。用法：python3 <本檔> <SD 資料夾>"""
import sys, math, re
from pathlib import Path
t = Path(sys.argv[1], "raw/solutions/SD-2024-3/SD-2024-3.md").read_text(encoding="utf-8")
body = t.split("## 2.", 1)[1].split("**4. 舊解對照")[0].replace("規範沒有另訂 $\\alpha_{yM}$", "")      # §1 常見誤讀、§5 舊解對照、頁尾除外
mis = []
def chk(label, ok):
    print("OK " if ok else "MIS", label)
    if not ok: mis.append(label)
chk("4.2 = 1.4×3", abs(1.4*3-4.2) < 1e-12 and "4.2=1.4\\times3" in t)
chk("3.5 = 1.4×2.5", abs(1.4*2.5-3.5) < 1e-12 and "3.5=1.4\\times2.5" in t)
chk("V*/V 一般 = Fu/3", abs(1.4/4.2-1/3) < 1e-12 and "=\\frac{F_u}{3}" in t)
chk("V*/V 盆地 = 0.4Fu", abs(1.4/3.5-0.4) < 1e-12 and "=0.4F_u" in t)
chk("盆地翻轉 Fu>2.5", abs(1/0.4-2.5) < 1e-12 and "盆地 $F_u>2.5$" in t)
chk("Ra 一般 2/3", abs((1+(4.8-1)/1.5-1)/(4.8-1)-2/3) < 1e-12 and "R_a=1+(R-1)/1.5" in t)
chk("Ra 盆地 1/2", abs((1+(4.8-1)/2.0-1)/(4.8-1)-1/2) < 1e-12 and "1+(R-1)/2.0" in t)
# 回歸期
chk("10%/50 → 475", round(-50/math.log(0.9)) == 475 and "475年" in t)
chk("2%/50 → 2475", round(-50/math.log(0.98)) == 2475 and "2475年" in t)
chk("30年 → 50年約80%", abs(1-(1-1/30)**50-0.817) < 0.002 and "約 80% / 50年" in t)
# 以 SaM 彈性設計 / V = (SaM/SaD)·Fu
I, a, W, SaD, SaM, Fu = 1.0, 1.0, 1.0, 0.6, 0.8, 3.0
chk("(SaM/SaD)·Fu", abs((I*SaM/(1.4*a)*W)/(I*SaD/(1.4*a*Fu)*W) - SaM/SaD*Fu) < 1e-12)
# 等能量 μ = (Fu²+1)/2 與 Fu = √(2μ−1) 互逆
mu = 3.0; chk("等能量互逆", abs(((math.sqrt(2*mu-1))**2+1)/2 - mu) < 1e-12)
# 舊觀念殘留（§2–§5 本文，不含 §1 常見誤讀與 §5 舊解對照）
for bad in ("短週期區", "長週期區", "取兩者中較小", "αyM", "\\alpha_{yM}", "\\alpha_{y,sys}", "mu_{actual}", "≈ 1.4（台灣", "V*（小）", "2.5\\sim3"):
    chk(f"殘留清除：{bad}", bad not in body)
# 圖 1／圖 2 圖說數值
Ra = 1+(4.8-1)/1.5; Rt = 1+(4.8-1)/2.0
for lab, v, txt in (("Fu 上限一般", Ra*1.4/4.2, "1.178"), ("Fu 上限盆地", Rt*1.4/3.5, "1.160"), ("Ra 盆地", Rt, "2.90"),
                    ("V_u", 1/Ra, "0.283"), ("V_y", 1/Ra/1.4, "0.202"), ("V", 1/Ra/1.4/1.5, "0.135"), ("V*", 1/(4.2*1.5), "0.159")):
    chk(f"{lab} {v:.4f}", (f"{v:.3f}" == txt or f"{v:.2f}" == txt) and txt in t)
print("MISMATCHES:", len(mis), mis)
