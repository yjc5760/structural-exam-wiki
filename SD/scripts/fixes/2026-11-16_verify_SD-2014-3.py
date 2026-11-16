#!/usr/bin/env python3
"""SD-2014-3 勘誤驗證（2026-11-16）：動力分析總橫力調整（現行規範 3.3 節：規則 90%、不規則 100%，已超過者採動力值），
例題放大係數雙路徑互驗，並檢查解析正本數值與殘留。用法：python3 <本檔> <SD 科目資料夾>"""
import sys, re
from pathlib import Path
md = (Path(sys.argv[1]) / "raw/solutions/SD-2014-3/SD-2014-3.md").read_text(encoding="utf-8")
mis = []
def chk(name, ok):
    print(("OK  " if ok else "BAD ") + name)
    if not ok: mis.append(name)
def adjust(Vd, Vs, regular):          # 路徑 1：條文邏輯
    tgt = (0.9 if regular else 1.0) * Vs
    return max(Vd, tgt)
def factor(Vd, Vs, regular):          # 路徑 2：放大係數
    r = (0.9 if regular else 1.0) * Vs / Vd
    return max(r, 1.0)
Vs = 1.0
for Vd in [0.5, 0.7, 0.85, 0.95, 1.2]:
    for reg in (True, False):
        a = adjust(Vd, Vs, reg); b = Vd * factor(Vd, Vs, reg)
        chk(f"Vd={Vd} regular={reg}: 調整後 {a:.4f} 兩路徑一致", abs(a - b) < 1e-12)
chk("例題 0.9/0.70=1.286", f"{0.9/0.70:.3f}" == "1.286" and "1.286" in md)
chk("例題 1.0/0.70=1.429", f"{1.0/0.70:.3f}" == "1.429" and "1.429" in md)
chk("Vd 已超過目標時不縮小（1.2Vs→1.2Vs）", adjust(1.2, 1.0, True) == 1.2 and adjust(1.2, 1.0, False) == 1.2)
for s in ["0.9V_s", "1.0V_s", "3.3 節", "90%", "100%"]:
    chk(f"正本含「{s}」", s in md)
sec = md.split("## 2. ", 1)[1].split("### 5.1", 1)[0]
for old in ["S_{DS}/R", "0.4S_{DS}/R", "短週期地震下", "台北盆地邊緣"]:
    chk(f"殘留檢查：§2–§4 無「{old}」", old not in sec)
s52 = md.split("### 5.2", 1)[1]
for old in ["S_{DS}/R", "台北盆地邊緣"]:
    chk(f"殘留檢查：§5.2 起無「{old}」", old not in s52.split("*修正日期")[0])
print(f"MISMATCHES: {len(mis)}")
