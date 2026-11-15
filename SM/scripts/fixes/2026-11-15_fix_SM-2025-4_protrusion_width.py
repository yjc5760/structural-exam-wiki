# -*- coding: utf-8 -*-
"""FIX SM-2025-4（⚠️ 判讀殘留，答案不變）：§4 Step 1 凸出部寬改為直接取上方第一段尺寸線 40 m（原以 120−40−40 推得，沿用舊的尺寸線誤讀）。
在 SM/ 下執行；可重複執行。"""
p = "raw/solutions/SM-2025-4/SM-2025-4.md"
t = open(p, encoding="utf-8").read()
if "FIX：凸出部寬" in t:
    raise SystemExit("already fixed")
a = "- **矩形 1（上方凸出部）：** 寬度為 $120 - 40 - 40 = 40 \\text{ m}$，高度為 $40 \\text{ m}$。"
b = "- **矩形 1（上方凸出部）：** 寬度 $40 \\text{ m}$（上方第一段尺寸線即凸出部寬，題目正本 #2），高度為 $40 \\text{ m}$。"
assert t.count(a) == 1
t = t.replace(a, b)
a2 = "- **矩形 2（左側底版）：** 寬度為 $40 \\text{ m}$，高度為 $40 \\text{ m}$。"
b2 = "- **矩形 2（左側底版）：** 寬度為左側缺口 $120 - 40 - 40 = 40 \\text{ m}$（底寬扣凸出部寬與凸出部右緣到右端的 40 m），高度為 $40 \\text{ m}$。"
assert t.count(a2) == 1
t = t.replace(a2, b2)
t = t.rstrip("\n") + "\n\n*修正日期：2026-11-15（FIX：凸出部寬——§4 Step 1 矩形 1 寬度改為直接取尺寸線 40 m、矩形 2 寬度註明由 120 − 40 − 40 得左側缺口（原把 120 − 40 − 40 當凸出部寬，沿用階段 A 已指出的尺寸線誤讀）；答案 110.06 kPa 不變。驗證：腳本重算影響係數與應力增量 MISMATCHES: 0）*\n"
with open(p, "r+b") as f:
    f.seek(0); f.write(t.encode("utf-8")); f.truncate()
print("fixed")
