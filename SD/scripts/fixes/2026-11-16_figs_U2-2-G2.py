#!/usr/bin/env python3
"""U2-2-G2 階段 E（2026-11-16）：插入 SD-2007-4 圖解，三題頁尾加「（非勘誤）圖解補繪」行。可重複執行。用法：python3 <本檔> <SD 科目資料夾>"""
import sys
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
p = SD/"raw/solutions/SD-2007-4/SD-2007-4.md"; t = p.read_text(encoding="utf-8")
img = "figs/SD-2007-4-fig-1-column-capacity.svg"
if img not in t:
    a = "> 鋼柱補充：斷面寬厚比符合高韌性要求以防局部挫屈，腹板剪力強度以柱端塑性彎矩推求，並同樣遵守強柱弱梁。\n"
    assert t.count(a) == 1
    t = t.replace(a, a + f"\n![SD-2007-4 柱的容量設計示意：左為一般柱，柱端 M_pr 反算 V_e、上下 l_o 圍束區箍筋加密；右為半高牆造成的短柱，有效淨高減半、V_e 加倍]({img})\n\n*圖 1　柱的容量設計剪力與短柱效應（尺寸示意；$l_o$ 與箍筋間距依混凝土結構設計規範 112 年版 18.4 節）。本圖攔下三種錯：柱箍筋間距套用梁的 $d/4$；以分析剪力 $V_u$ 而非 $M_{{pr}}$ 反算的 $V_e$ 設計柱剪力；忽略半高牆使有效淨高變短、$V_e$ 加倍。*\n")
FOOT = {
 "SD-2006-3": "figs/SD-2006-3-fig-1-spectrum.svg（現行規範譜形與因素加大的變化，§4 因素五）",
 "SD-2007-4": "figs/SD-2007-4-fig-1-column-capacity.svg（柱容量設計剪力、l_o 圍束區與短柱效應，§4 子題二）",
 "SD-2008-2": "figs/SD-2008-2-fig-1-strength-ratio.svg（每 3 層換斷面時 r_i 與 0.8 r_i+1 門檻，§4 子題二）",
}
for q, f in FOOT.items():
    pp = SD/f"raw/solutions/{q}/{q}.md"
    tt = t if q == "SD-2007-4" else pp.read_text(encoding="utf-8")
    line = f"*修正日期：{D}（非勘誤）圖解補繪：{f}；向量圖，腳本 gen_{q}.py，可重跑*"
    if line not in tt:
        tt = tt.rstrip("\n") + "\n\n" + line + "\n"
    pp.write_text(tt, encoding="utf-8")
    if q == "SD-2007-4": t = tt
print("done")
