# -*- coding: utf-8 -*-
"""FIX SM-2020-1（⚠️ 觀念作圖，數值不變）：分布表補 B 點乾砂側、圖說改正「A→B 段 u 為負」「σ' 在 B 點局部峰值」。
在 SM/ 下執行；可重複執行。"""
p = "raw/solutions/SM-2020-1/SM-2020-1.md"
t = open(p, encoding="utf-8").read()
if "FIX：分布圖說" in t:
    raise SystemExit("already fixed")
R = [
("| B | 2.1 | 36.39 | -4.41 | 40.80 |",
 "| B（乾砂側） | 2.1 | 36.39 | 0.00 | 36.39 |\n| B（毛細區側） | 2.1 | 36.39 | -4.41 | 40.80 |"),
]
for a, b in R:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
i = t.index("*圖說：總應力 $\\sigma$、水壓力 $u$、有效應力 $\\sigma'$ 隨深度 $z$ 分布之折線圖")
j = t.index("\n", i)
t = t[:i] + r"""*分布說明：總應力 $\sigma$ 連續、分三段直線（斜率 17.33、18.97、17.65 kPa/m）。水壓力 $u$ 在 A→B 段（乾砂）為 0；B 點是毛細區頂，$u$ 由 0 跳到 $-4.41$ kPa，B→C 線性回升到 0（地下水位面），C→D 依靜水壓線性增加到 18.64 kPa。有效應力 $\sigma'$ 在 B 點由 36.39 跳增到 40.80 kPa（不連續），之後 B→C（斜率 14.07 kPa/m）、C→D（斜率 7.84 kPa/m）持續增加，並無局部峰值。*""" + t[j:]
t = t.rstrip("\n") + "\n\n*修正日期：2026-11-15（FIX：分布圖說——§4 Step 3 表補 B 點乾砂側（u = 0、σ' = 36.39 kPa），圖說原寫「A→B 段 u 為負值」「σ' 在 B 點出現局部峰值」改為 A→B 段 u = 0、B 點 u 與 σ' 不連續、σ' 一路增加；各點數值不變。驗證：腳本重算 σ、u、σ' 與分段斜率 MISMATCHES: 0；依 2026-11-15 獨立盲解比對）*\n"
with open(p, "r+b") as f:
    f.seek(0); f.write(t.encode("utf-8")); f.truncate()
print("fixed")
