#!/usr/bin/env python3
"""U3-2-G2 階段 E：把 struct-diagram 圖解插回 SD-2011-1、SD-2012-4 解析（非勘誤）。可重複執行。
用法：python3 <本檔> <SD 科目資料夾>"""
import sys
from pathlib import Path
S = Path(sys.argv[1])/"raw/solutions"

def patch(qid, inserts, footer):
    p = S/qid/f"{qid}.md"; t = p.read_text(encoding="utf-8")
    if "圖解補繪" in t and footer.split("圖解補繪：")[1][:20] in t:
        print(qid, "skip"); return
    for anchor, block in inserts:
        assert t.count(anchor) == 1, (qid, anchor[:30])
        t = t.replace(anchor, anchor + block)
    t = t.rstrip("\n") + "\n\n" + footer + "\n"
    p.write_text(t, encoding="utf-8"); print(qid, "done")

patch("SD-2011-1", [
 ("$$S_{d,2} = 0.600 \\times \\frac{(0.25)^2}{4\\pi^2} \\times 9.81 = 0.600 \\times 0.015519 = \\mathbf{0.009311 \\text{ m}}$$\n",
  "\n![設計反應譜兩段與兩個振態的取值：振態 2（T=0.25 s、ξ=5%）落在 0.2–1.0 s 段取 0.6/B_S=0.600；振態 1（T=2.0 s、ξ=10%）落在 1.0–2.5 s 段取 0.6/(T·B_1)=0.240；空心點為誤用 B_S 或誤用他振態阻尼比的值](figs/SD-2011-1-fig-1-spectrum.svg)\n\n"
  "*圖 1　兩個振態各自依週期選譜段、依自己的阻尼比查表。攔下兩種錯：振態 1 誤用 $B_S$（0.226），以及振態 2 套用振態 1 的 10% 阻尼（$B_S=1.33$ → 0.451，$S_{aD}$ 低估約 25%）。*\n"),
 ("> **物理意義：** 上部結構幾乎不變形（僅 ~1 cm），地震能量幾乎全部被隔震層吸收（23.3 cm）。這正是隔震設計的核心效益：保護上部結構免受地震損傷。\n",
  "\n![兩個振態的振態形狀（按比例）與各 DOF 的振態位移 Γφ·Sd，及振態向量分量順序的正交性檢核與 SRSS 結果](figs/SD-2011-1-fig-2-modes.svg)\n\n"
  "*圖 2　振態形狀、各振態位移與層間位移。(c) 的正交性檢核攔下分量順序讀反（〈基礎, 上部〉時 $\\sum W\\varphi_1\\varphi_2=166.5$ tf，不正交）；(a)(b) 標出每個振態先相減的層間量，提醒層間位移要在振態內相減後再 SRSS。*\n"),
], "*修正日期：2026-11-16（非勘誤）圖解補繪：圖 1 譜段與阻尼修正係數選用、圖 2 振態形狀與分量順序檢核（向量圖，腳本 `gen_SD-2011-1.py`，可重跑）*")

patch("SD-2012-4", [
 ("一致（`SD/scripts/fixes/2026-11-16_verify_SD-2012-4.py`）。\n",
  "\n![剛體假設與串聯模型對照：(a) 上部結構視為剛體時隔震層位移即 D_D；(b) 上部結構有柔性時，以 T_eD=3.0 s、T=1.0 s 為例，隔震層 0.949 D_D、上部變形 0.105 D_D、總位移 1.054 D_D](figs/SD-2012-4-fig-1-series.svg)\n\n"
  "*圖 1　剛體假設與串聯模型。攔下兩個觀念錯：把總位移當成 $D_D$（實際為 $D_D\\sqrt{1+(T/T_{eD})^2}$，較大），以及以為上部柔性會讓隔震層位移變大（實際隔震層只分到 $D'_D<D_D$）。*\n"),
 ("故 T/TeD ≈ 0.1～0.4，修正約 0.5～7%，較小但仍需考慮。\n",
  "\n![總位移、隔震層位移、上部變形與 D_D 之比隨 T/T_eD 的變化，並與舊解的上部變形 D'_D·T/T_eD、總位移=D_D 對照；兩式只在 T=T_eD 時相等](figs/SD-2012-4-fig-2-ratio.svg)\n\n"
  "*圖 2　各位移比隨 $T/T_{eD}$ 的變化。攔下「上部變形 $=D'_D\\,T/T_{eD}$」這種只在 $T=T_{eD}$ 碰巧成立的式子：常見設計範圍內它把上部變形高估為正解的 $T_{eD}/T$ 倍。*\n"),
], "*修正日期：2026-11-16（非勘誤）圖解補繪：圖 1 剛體假設與串聯模型位移分配、圖 2 位移比隨 T/TeD 變化（向量圖，腳本 `gen_SD-2012-4.py`，可重跑）*")
