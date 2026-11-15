# -*- coding: utf-8 -*-
"""G9（SM-U2-1 批 1）階段 E：把解題圖解插回解析 .md（可重複執行）。在 SM/ 下執行。
SM-2017-3 為勘誤落實後補圖；SM-2009-2、SM-2020-4 為盲解一致題。"""
J = {
 "SM-2017-3": ("$$ \\boxed{ Q_a \\approx 176 \\text{ kN} } $$\n", "after",
   "\n![SM-2017-3 圖 2：上排為承載力控制的換算鏈，平鈑 q_ult 219 經 FS 得 q_a(P) 118.5，乘 B/P 得基腳 790 kN/m²，Qa 約 3090 kN；中排為沉陷量控制，基腳 1 cm 除以 3.025 得平鈑 0.331 cm，讀曲線 q 約 62，Qa 約 176 kN；下方壓力軸標出試驗曲線範圍 0–246 與 62、118.5、219、790 四個壓力的位置](figs/SM-2017-3-fig-2-conversion.svg)\n\n*圖 2　兩條換算路線與接觸壓力的位置（數值取自本節；圖 3-1 曲線不重繪）。攔下兩種錯誤：㈡ 把讀出的 q 再乘 $B/P$（沉陷換算已由 T&P 係數處理）；㈠ 基腳壓力 790 kN/m² 遠在試驗範圍外，卻外插曲線求沉陷。*\n", "§4 Step 3", "figs/SM-2017-3-fig-2-conversion.svg"),
 "SM-2009-2": ("兩者皆為合理之工程解答，唯 Terzaghi 法更能體現題目「下方為砂土層」之深度限制。\n", "after",
   "\n![SM-2009-2 圖 2：開挖深 6.34 m 的剖面，坑外寬 5.66 m 的 Terzaghi 破壞塊與以坑壁底為圓心的破壞弧，弧底正好切齊地表下 12 m 的砂層頂；外側水位地表下 3 m，砂層水壓 88.29 kPa 向上作用於坑底下 5.66 m 厚、重 96.22 kPa 的黏土塞；右欄列抗隆起 FS 2.58、2.13 與抗上舉 FS 1.09](figs/SM-2009-2-fig-2-heave.svg)\n\n*圖 2　㈡ 的兩種破壞機制（數值取自本節與 §5）。攔下兩種錯誤：不檢查破壞塊寬 $B/\\sqrt{2}$ 是否超過坑底下黏土厚 $T$；只算剪力隆起而漏掉砂層水壓造成的整塊上舉（FS 僅 1.09）。*\n", "§4（二）", "figs/SM-2009-2-fig-2-heave.svg"),
 "SM-2020-4": ("4. **結論對承載力公式敏感（2026-11-15 盲解比對補註）**", "afterline",
   "\n![SM-2020-4 圖 1：五種承載力式的 FS 點圖，Terzaghi 2.89、Meyerhof 2.82、Skempton 2.74、不計深度因數 2.61 都在 FS = 3 虛線左側，只有 Hansen/Vesic 型深度因數 3.02 在右側](figs/SM-2020-4-fig-1-fs-methods.svg)\n\n*圖 1　五種承載力式的 FS 與要求值 3 的相對位置（淨施加壓力 98.6 kPa）。攔下「只用一條公式就下結論」的錯誤：本題 FS 落在 3 附近，換公式就可能由不安全變成剛好安全。*\n", "§5 第 4 點", "figs/SM-2020-4-fig-1-fs-methods.svg"),
}
for q, (anchor, pos, block, sec, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    if pos == "after":
        t = t.replace(anchor, anchor + block)
    else:
        i = t.index(anchor); j = t.index("\n", i)
        t = t[:j + 1] + block + t[j + 1:]
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；%s 補解題圖解 %s（圖解補繪）；非勘誤）*" % (sec, fig))
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("done", q)
