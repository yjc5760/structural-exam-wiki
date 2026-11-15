# -*- coding: utf-8 -*-
"""SM-U1-1 批 1 階段 E：SM-2005-2、SM-2007-1 解題圖解插回解析（可重複執行）。在 SM/ 下執行。
圖由各題 gen_<id>.py 產生，數值取自解析 §4（盲解比對一致）。"""
J = {
 "SM-2005-2": ("$$\\boxed{\\text{通過 \\#4 篩之試樣乾密度為 } 2.08 \\text{ g/cm}^3}$$\n",
   "![SM-2005-2 圖 1：挖洞體積 315 cm³ 的體積分解柱，下方為通過 #4 細料（土粒＋孔隙）281.06 cm³，上方疊三格粗顆粒實體積 1/2″ 7.301、3/8″ 10.766、#4 15.878 cm³（合計 33.945 cm³）；右側列正解 584.53/281.06 = 2.080 g/cm³，以及只扣重量不扣體積的 1.856、全試樣乾密度 2.109 兩種錯誤算法](figs/SM-2005-2-fig-1-oversize-correction.svg)\n\n*圖 1　過大顆粒修正：分子分母都只留細料。它攔的是「扣了粗粒重量、卻沒扣粗粒佔的 33.9 cm³」——那樣會得 1.856 g/cm³（低估約 11%）；不扣粗粒則是全試樣乾密度 2.109，不是本題所求。*\n",
   "§4", "figs/SM-2005-2-fig-1-oversize-correction.svg"),
 "SM-2007-1": ("**答案：含水量變化為 $\\boxed{20.29\\%}$ （減少）**\n",
   "![SM-2007-1 圖 1：壓縮前後兩根等比例的三相柱，土粒高 H_s = 1.0870 cm 兩邊相同並以虛線對齊；水（飽和）由 1.4130 cm 減為 0.8130 cm，頂端高差 ΔH = 0.60 cm 全是排出的水（19.0 cm³ = 19.0 g）；柱下標 e = 1.300 → 0.748、w = 47.79% → 27.50%、γ_sat = 17.15 → 19.46 kN/m³](figs/SM-2007-1-fig-1-compression-phase.svg)\n\n*圖 1　一維壓縮時土粒高度 $H_s = H_0/(1+e_0)$ 不變，少掉的 0.6 cm 全是孔隙水。它攔兩種錯誤：把 $\\Delta e$ 的分母寫成 $H_0$（會得 $e_1 = 1.06$），以及以為壓縮後孔隙進了空氣而不再用 $S = 1$ 的 $\\gamma_{sat}$ 與 $w = e/G_s$。*\n",
   "§4", "figs/SM-2007-1-fig-1-compression-phase.svg"),
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
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("done", q)
