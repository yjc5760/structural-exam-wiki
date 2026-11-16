#!/usr/bin/env python3
"""SD-2004-1 ㈠ 落實核對（概念題，無數值計算）：現行 111 年版 §2.16.1 的要素是否齊全、舊版寫法是否只留在 §5 對照。"""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2004-1", "SD-2004-1.md")
s = open(P, encoding="utf-8").read(); main = s[:s.index("**爭議零")]
mis = []
need = ["\\frac{IF_u}{4.2}", "\\frac{I\\,F_u}{4.2}", "0.005", "1.4 倍", "0.4S_{DS}", "I=1.0", "平移與扭轉", "Serviceability", "§2.16.1"]
for k in need:
    if k not in s: mis.append(("缺", k))
for old in ("V^*", "1/400", "91 年版", "91年版", "frac{1}{200} = 0.5"):
    if old in main.split("## 2.", 1)[1]: mis.append(("殘留", old))
for m in mis: print("MISMATCH", m)
print("MISMATCHES:", len(mis))
