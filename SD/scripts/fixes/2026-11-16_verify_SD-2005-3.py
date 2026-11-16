#!/usr/bin/env python3
"""SD-2005-3 獨立重算（2026-11-16）：現行規範 §2.6 T=0.070hn^(3/4)、§2.11 Ft=0.07TV≤0.25V，倒三角形分配。
路徑 1：公式逐層；路徑 2：numpy 矩陣（剪力＝上三角累加）＋手算屋頂；並解析正本表格比對。"""
import os, re
import numpy as np
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2005-3", "SD-2005-3.md")
md = open(P, encoding="utf-8").read()
h = np.array([4.0 + 3.2*i for i in range(12)]); W = np.array([400] + [300]*10 + [200.0]); V = 450.0
hn = h[-1]; T = 0.070*hn**0.75; Ft = min(0.07*T*V, 0.25*V); S = (W*h).sum()
F = (V-Ft)*W*h/S; F[-1] += Ft
U = np.triu(np.ones((12, 12))); Vs = U @ F          # 路徑 2：Vs[k]=Σ_{i≥k}F_i
Vs1 = [sum(F[k:]) for k in range(12)]
assert np.allclose(Vs, Vs1) and abs(Vs[0]-V) < 1e-9
assert abs((V-Ft)*7840/74240 + Ft - F[-1]) < 1e-9 and abs(S-74240) < 1e-9
F0 = V*W*h/S
mis = []
def chk(name, val, txt):
    if f"{val:.2f}" not in txt: mis.append((name, f"{val:.2f}"))
s4 = md[md.index("### Step 4"):md.index("## 5.")]
lv = ["2F"] + [f"{i}F" for i in range(3, 13)] + ["屋頂"]
for k, l in enumerate(lv):
    row = re.search(rf"^\| {l} \|.*$", s4, re.M).group(0); chk(f"F_{l}", F[k], row); chk(f"F0_{l}", F0[k], row)
for k in range(12):
    row = re.search(rf"^\| 第 {k+1} 層.*$", s4, re.M).group(0); chk(f"V_{k+1}", Vs[k], row)
for name, v in (("Ft", Ft), ("V-Ft", V-Ft)): chk(name, v, md)
for fmt in (".3f", ".4f"):
    if format(T, fmt) not in md: mis.append(("T", format(T, fmt)))
# 殘留：舊答案只准出現在 §5 與對照欄、頁尾
body = md[:md.index("## 5.")]
for old in ("65.46", "47.52", "112.98"):
    for line in body.splitlines():
        if old in line and "對照" not in line and not line.startswith("| ") and "常見誤讀" not in line:
            mis.append(("殘留", line[:60]))
print(f"T={T:.4f} s  Ft={Ft:.3f} t  F_roof={F[-1]:.3f}  V12={Vs[-1]:.3f}  V11={Vs[-2]:.3f}")
for m in mis: print("MISMATCH", m)
print("MISMATCHES:", len(mis))
