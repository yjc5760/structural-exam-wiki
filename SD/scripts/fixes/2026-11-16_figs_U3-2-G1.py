#!/usr/bin/env python3
"""U3-2-G1 階段 E（2026-11-16）：把解題圖解插回解析（非勘誤）。可重複執行。
SD-2004-2：figs/SD-2004-2-fig-2-deform-split.svg（gen_SD-2004-2.py）插在 §5 隔震層變形段之後；
SD-2005-1：figs/SD-2005-1-fig-1-hysteresis.svg（gen_SD-2005-1.py）插在 §4㈡ W_D 說明之後。
用法：python3 <本檔> <SD 科目資料夾>（須先執行 2026-11-16_errata_U3-2-G1.py）"""
import sys
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
ITEMS = {
 "SD-2004-2": ("> ⚠ 不要把 $x_2-x_1$ 當成隔震支承位移：它是上部結構（彈簧 $k$）的變形，$k_b \\ll k$ 時趨近 0。\n",
   "figs/SD-2004-2-fig-2-deform-split.svg",
   "![SD-2004-2 解題圖解：m_b＝0 時相對位移 v2 分配到隔震層（x1−ug＝k/(k+kb)·v2）與上部結構（x2−x1＝kb/(k+kb)·v2）；上為 k/kb＝25 的位移分段，下為兩比例隨 k/kb 的變化](figs/SD-2004-2-fig-2-deform-split.svg)\n"
   "*圖：相對位移 v2 在兩根串聯彈簧間的分配（數值取自本節，k/k_b＝25 時 0.9615／0.0385）。隔震（k_b≪k）時隔震層承擔幾乎全部 v2，x2−x1 是上部結構變形、趨近 0。*\n"),
 "SD-2005-1": ("其中 $F_y = A_{core} \\cdot \\sigma_y$（內芯降伏力），$\\delta_p = \\delta_{max} - \\delta_y$（軸向位移振幅扣除降伏位移）\n",
   "figs/SD-2005-1-fig-1-hysteresis.svg",
   "![SD-2005-1 解題圖解：BRB 彈性—完全塑性遲滯迴圈（μ＝5），迴圈面積 W_D＝16 F_yδ_y，割線勁度 K_eff 與三角形 E_so＝2.5 F_yδ_y，ξ_eq＝0.509；誤用初始勁度 K_e 得 0.051](figs/SD-2005-1-fig-1-hysteresis.svg)\n"
   "*圖：拉壓對稱的飽滿迴圈即 BRB 的消能來源。等效阻尼比以割線勁度 K_eff 計算（ξ＝W_D/(4πE_so)），μ＝5 時 0.509；若誤用初始勁度 K_e 會低估約 10 倍。*\n"),
}
for qid, (anchor, svg, block) in ITEMS.items():
    p = SD/f"raw/solutions/{qid}/{qid}.md"; t = p.read_text(encoding="utf-8")
    assert (SD/f"raw/solutions/{qid}/{svg}").exists(), svg
    if f"]({svg})" in t: print(qid, "skip"); continue
    assert t.count(anchor) == 1, (qid, t.count(anchor))
    t = t.replace(anchor, anchor + "\n" + block)
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（非勘誤）圖解補繪：{svg}（腳本 gen_{qid}.py，可重跑；數值取自已驗證正本，答案不變）*\n"
    p.write_text(t, encoding="utf-8"); print(qid, "fig inserted")
