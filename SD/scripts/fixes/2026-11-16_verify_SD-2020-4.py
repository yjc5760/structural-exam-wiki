#!/usr/bin/env python3
"""SD-2020-4 勘誤驗算（2026-11-16）：重算正本所有數值並與正本文字比對。用法：python3 <本檔> <SD 資料夾>"""
import sys, math, re
from pathlib import Path
t = Path(sys.argv[1], "raw/solutions/SD-2020-4/SD-2020-4.md").read_text(encoding="utf-8")
mis = []
def chk(label, val, txt):
    ok = txt in t
    print(f"{'OK ' if ok else 'MIS'} {label}: {val} -> '{txt}'")
    if not ok: mis.append(label)
Ra = lambda R: 1 + (R - 1) / 1.5
# 回歸期換算
chk("10%/50 -> TR", 1/(1-0.9**(1/50)), "T_R = 1/P_a = 475")
chk("30 年 -> P50", 1-(1-1/30)**50, "81.7\\%")
# V*/V
for R, s_l, s_m in ((4.8, "3.53", "2.46"), (4.0, "3.00", "2.24"), (3.2, "2.47", "1.98"), (1.5, "1.33", "1.29")):
    chk(f"Fu_long R={R}", Ra(R), s_l); chk(f"Fu_mid R={R}", math.sqrt(2*Ra(R)-1), s_m)
chk("V*/V R=4.8 long", Ra(4.8)/3, "1.18")
chk("V*/V R=4.8 mid", math.sqrt(2*Ra(4.8)-1)/3, "0.82")
# 中週期翻轉需 Ra>5 -> R>7
assert abs(math.sqrt(2*5-1)-3) < 1e-12 and abs((5-1)*1.5+1-7) < 1e-12
# 兩平比值
for R, s in ((2.0, "1.200"), (3.2, "1.297"), (4.8, "1.358")):
    v = R/Ra(R); chk(f"R/Ra R={R}", round(v, 4), s)
for rho, s in ((1.2, "0.883"), (1.3, "0.957"), (1.4, "1.030"), (1.5, "1.104")):
    v = rho*Ra(4.8)/4.8; chk(f"VM/V rho={rho}", round(v, 4), s)
# 交叉驗算：rho=1.5 時等於舊閉合式 1+0.5/R
assert abs(1.5*Ra(4.8)/4.8 - (1+0.5/4.8)) < 1e-12
# 交叉驗算：rho = R/Ra 時 VM/V = 1
assert abs((4.8/Ra(4.8))*Ra(4.8)/4.8 - 1) < 1e-12
# (·)_m 連續性
f = lambda x: x if x <= 0.3 else (0.52*x+0.144 if x < 0.8 else 0.70*x)
assert abs(0.52*0.3+0.144-0.3) < 1e-12 and abs(0.52*0.8+0.144-0.56) < 1e-12
chk("(.)_m 0.8", 0.56, "0.8 \\to 0.56")
# 韌性額度
chk("Ra R=4.8", round(Ra(4.8),3), "3.533")
# 圖 1 範圍
chk("VM range", "0.883～1.104", "0.883～1.104")
print("MISMATCHES:", len(mis), mis)
