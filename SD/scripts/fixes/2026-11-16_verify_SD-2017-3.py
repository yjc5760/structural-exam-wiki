#!/usr/bin/env python3
"""SD-2017-3 勘誤驗算（2026-11-16）：剛性牆束制短柱的剪力分配。
題意依題目正本（已確認）：可變形段 h=ℓ/2、ℓ/2、3ℓ/4、ℓ，兩端固定。
路徑 1：分數精確 k∝12/h³；路徑 2：每柱以 2 節點梁元素（4×4 勁度）組裝、柱頂共用平移且不轉動，解 Δ 求柱剪力。
用法：python3 <本檔> [SD 資料夾]；最後印 MISMATCHES。"""
import sys, re
from fractions import Fraction as F
import numpy as np
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
md = (SD/"raw/solutions/SD-2017-3/SD-2017-3.md").read_text(encoding="utf-8")
h = [F(1,2), F(1,2), F(3,4), F(1)]
k = [12/x**3 for x in h]; K = sum(k); V = [x/K for x in k]
# 路徑 2：梁元素，EI=1, ℓ=1；底端固定、頂端轉角 0，只留頂端平移 Δ
def col_shear(hh):
    L = float(hh); ke = np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])/L**3
    return ke[2,2]          # 頂端平移勁度（其餘自由度皆固定）
kk = [col_shear(x) for x in h]; D = 1/sum(kk); V2 = [x*D for x in kk]
mm = 0
def chk(name, a, b, tol=1e-9):
    global mm
    ok = abs(float(a)-float(b)) < tol; mm += (not ok); print(f"{'OK ' if ok else 'BAD'} {name}: {float(a):.6f} vs {float(b):.6f}")
for i in range(4): chk(f"V{i+1} 兩路徑", V[i], V2[i])
chk("K 總勁度 2092/9", K, F(2092,9)); chk("k3 = 256/9", k[2], F(256,9))
exp = {"V1": F(216,523), "V2": F(216,523), "V3": F(64,523), "V4": F(27,523)}
for i,(n,v) in enumerate(exp.items()): chk(n, V[i], v)
chk("V1+V2 比例 0.83", V[0]+V[1], 0.826, 1e-3)
# 正本內必須出現的數值字串、不得殘留的舊值（§1 常見誤讀、§5.1 讀圖提醒、頁尾以外）
for s in ["216}{523}", "64}{523}", "27}{523}", "0.413", "0.122", "0.052", "2092", "28.44", "83\\%"]:
    if s not in md: mm += 1; print("BAD 正本缺", s)
body = md.split("### 5.1")[0].split("## 2.")[1]
for s in ["768", "972", "64}{81}", "8}{81}", "h_3 = \\ell/4", "牆高 = $3\\ell/4$"]:
    if s in body: mm += 1; print("BAD §2–§4 殘留舊值", s)
print("MISMATCHES:", mm)
