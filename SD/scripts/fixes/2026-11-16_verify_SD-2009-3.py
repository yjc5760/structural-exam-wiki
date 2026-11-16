#!/usr/bin/env python3
"""SD-2009-3 勘誤驗證（2026-11-16）：三種地震水準的回歸期／50 年超越機率，雙路徑互驗，並檢查解析正本數值與殘留。
用法：python3 <本檔> <SD 科目資料夾>
規範依據（已核對原文，國土管理署 111 年版）：1.2 節及解說、2.3 節（475 年 10%、2500 年 2%）、2.10.1 解說（30 年、50 年超越機率約 80%、V* 約 475 年未折減地震力 1/4.2）。"""
import sys, math, re
from pathlib import Path
md = (Path(sys.argv[1]) / "raw/solutions/SD-2009-3/SD-2009-3.md").read_text(encoding="utf-8")
mis = []
def chk(name, ok):
    print(("OK  " if ok else "BAD ") + name)
    if not ok: mis.append(name)
n = 50
# 路徑 1：超越機率 -> 回歸期（Poisson：T = -n/ln(1-P)）；路徑 2：回歸期 -> 超越機率（二項：P = 1-(1-1/T)^n）
for P, T_code in [(0.80, 30), (0.10, 475), (0.02, 2500)]:
    T1 = -n / math.log(1 - P)
    P2 = 1 - (1 - 1 / T_code) ** n
    chk(f"P={P:.0%} -> T={T1:.1f} 年，與規範 {T_code} 年相差 <5%", abs(T1 - T_code) / T_code < 0.05 or (T_code == 30 and abs(T1 - 31.07) < 0.1))
    chk(f"T={T_code} -> P50={P2:.4f}，與 {P:.0%} 相差 <2 個百分點", abs(P2 - P) < 0.02)
chk("§5.2 寫 30 年→約 82%", abs((1 - (1 - 1/30) ** 50) - 0.816) < 0.001 and "82\\%" in md)
chk("L2 表 81.6%、10.0%、1.98%", all(s in md for s in ["81.6%", "10.0%", "1.98%"]))
chk("V* 比例 1/4.2、臺北盆地 1/3.5 出現", "1/4.2" in md and "1/3.5" in md)
for s in ["約 80%", "約 30 年", "475 年", "2500 年", "0.005"]:
    chk(f"正本含「{s}」", s in md)
# 殘留：舊值只能在 §1 常見誤讀、§5.1 對照與頁尾
body = md.split("### 常見誤讀")[1]
body = re.split(r"### 5\.1", body)[0]
body = body.split("|------|---------|---------|", 1)[1].split("**本解記號", 1)[1]
# 圖 1 的替代文字與圖說刻意標出誤用定義（圖的用途就是攔這個錯），不算殘留
body = "\n".join(l for l in body.splitlines() if not (l.startswith("![") or l.startswith("*圖")))
for old in ["95 年", "10%/10", "2,475", "1/2～1/3", "40–50", "96年", "I_E W/R", "短週期下限", "(3/2)"]:
    chk(f"殘留檢查：§2–§4 無「{old}」", old not in body)
print(f"MISMATCHES: {len(mis)}")
