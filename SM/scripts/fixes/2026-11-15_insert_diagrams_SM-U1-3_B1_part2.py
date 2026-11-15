# -*- coding: utf-8 -*-
"""SM-U1-3 批 1 階段 E（續）：SM-2014-4、SM-2015-1 沉陷—時間圖插回解析（可重複執行）。在 SM/ 下執行。"""
J = {
 "SM-2014-4": ("$$\\boxed{t = 377.33 \\text{ 天}}$$\n",
   "![SM-2014-4 圖 2：沉陷對時間曲線，最終沉陷 35.12 cm；單向排水 Hdr = 8 m 時 20 cm 在 377 天達到，虛線為誤取雙向排水 Hdr = 4 m 的曲線](figs/SM-2014-4-fig-2-settlement-time.svg)\n\n*圖 2　沉陷—時間曲線（Terzaghi 一維壓密）。攔下兩種錯誤：誤取雙向排水（虛線，時間只剩四分之一），以及照考卷漏印平方的 $T_v$ 式（會得 663 天）。*\n",
   "§4", "figs/SM-2014-4-fig-2-settlement-time.svg"),
 "SM-2015-1": ("$$ t = \\frac{30,240,000}{86,400} = \\boxed{350 \\text{ days}} $$\n",
   "![SM-2015-1 圖 1：預壓沉陷對時間曲線，最終沉陷 52.46 cm；雙向排水 Hdr = 4 m 時壓密 80% 為 41.97 cm、350 天，虛線為誤取單向排水 Hdr = 8 m 的曲線](figs/SM-2015-1-fig-1-settlement-time.svg)\n\n*圖 1　預壓沉陷—時間曲線。預載砂使黏土頂也成為排水面；攔下「誤取單向排水、時間算成 1400 天」的錯誤（虛線）。*\n",
   "§4", "figs/SM-2015-1-fig-1-settlement-time.svg"),
}
for q, (anchor, block, sec, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, anchor + "\n" + block)
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；%s 補解題圖解 %s；非勘誤）*" % (sec, fig))
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("done", q)
