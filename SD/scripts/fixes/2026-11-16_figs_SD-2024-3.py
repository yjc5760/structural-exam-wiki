#!/usr/bin/env python3
"""SD-2024-3 圖解補繪（2026-11-16，非勘誤）：插入 figs/SD-2024-3-fig-1-vstar-site.svg、fig-2-reduction-chain.svg。可重複執行。"""
import sys
from pathlib import Path
p = Path(sys.argv[1], "raw/solutions/SD-2024-3/SD-2024-3.md"); t = p.read_text(encoding="utf-8")
if "SD-2024-3-fig-1-vstar-site.svg" in t:
    print("already"); sys.exit()
A = "所以設計時是 $V$、$V^*$、$V_M$ **取最大值**，不是取較小值。"
F1 = (A + "\n\n![SD-2024-3 中小度地震與設計地震力比值圖：V*/V 隨 Fu 變化，一般工址 Fu/3 與臺北盆地 0.4Fu 兩條直線，分別在 Fu＝3.0、2.5 穿過 V*＝V；Fu 上限（R＝4.8 長週期）一般工址 3.53→1.178、臺北盆地 2.90→1.160](figs/SD-2024-3-fig-1-vstar-site.svg)\n\n"
      "*圖 1　$V^*/V$ 隨 $F_u$ 的變化，兩條線是兩類工址（一般工址 $4.2\\alpha_y$、臺北盆地 $3.5\\alpha_y$），不是同一棟建築的兩個週期段。兩條線都可越過 1.0，所以設計取 $V$、$V^*$、$V_M$ 的最大值。它攔的是把 4.2／3.5 解成短週期／長週期、再「取較小者」的誤讀。*")
B = "三者相乘，順序不影響數值，但意義不可對調；$(\\cdot)_m$ 修正另在 $S_{aD}/F_u$ 上套用。"
F2 = (B + "\n\n![SD-2024-3 設計地震力折減鏈長條圖：以 I·SaD·W＝1 為基準，÷Fu（3.533）得 0.283、÷1.4 得 0.202、÷αy（1.5）得設計力 V＝0.135；中小度地震 V*＝1/(4.2×1.5)＝0.159](figs/SD-2024-3-fig-2-reduction-chain.svg)\n\n"
      "*圖 2　以 $R=4.8$ 長週期（$F_u=R_a=3.533$）、RC 強度設計 $\\alpha_y=1.5$ 為例（設 $S_{aD}/F_u\\le0.3$），彈性需求依序除以 $F_u$、1.4、$\\alpha_y$ 得設計力 $V=0.135$；$V^*$ 不除 $F_u$，$V^*/V=1.178=F_u/3$。它攔的是把 $\\alpha_y$ 當成代表贅餘度的超強係數、把 $\\div\\alpha_y$ 與 $\\div1.4$ 的意義對調。*")
for o, n in ((A, F1), (B, F2)):
    assert t.count(o) == 1, o[:40]; t = t.replace(o, n)
t = t.rstrip("\n") + "\n\n*修正日期：2026-11-16（非勘誤）圖解補繪：figs/SD-2024-3-fig-1-vstar-site.svg（V*/V 依工址分兩式）、figs/SD-2024-3-fig-2-reduction-chain.svg（折減鏈），由 gen_SD-2024-3.py 產生*\n"
p.write_text(t, encoding="utf-8"); print("done")
