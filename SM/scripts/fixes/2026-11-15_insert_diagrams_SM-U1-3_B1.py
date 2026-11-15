# -*- coding: utf-8 -*-
"""SM-U1-3 批 1 階段 E：把解題圖解插回解析 .md（可重複執行）。在 SM/ 下執行。"""
J = {
 "SM-2011-3": ("$$ \\boxed{\\Delta\\sigma_{avg} = 55.56 \\text{ kPa}} $$\n", "after",
   "![SM-2011-3 圖 2：左為 2:1 法應力增量沿基底下深度的曲線，黏土層頂 111.11、中點 49.38、底 27.78 kPa，平均 55.56 kPa 以虛線標示；右為中點值與平均值兩種算法的沉陷分段長條，回脹段都是 29.37 mm，Cc 段 4.94 與 16.28 mm](figs/SM-2011-3-fig-2-avg-stress.svg)\n\n*圖 2　「平均」新增應力要沿層厚平均。2:1 分布上凹，中點值必低於平均；本題終應力在 $p_c'$ 附近，攔下「把中點值當平均、沉陷少算 25%」的錯誤。*\n", "§4 Step 3", "figs/SM-2011-3-fig-2-avg-stress.svg"),
 "SM-2015-4": ("**3. 計算沉陷量 $S_c$：**", "before",
   "![SM-2015-4 圖 2：黏土層 9 到 17 m 深，抽水前後孔隙水壓與有效應力沿深度的分布；抽水後孔隙水壓由靜水壓變為頂部 9.81、底部 137.34 kPa 的直線，有效應力頂部增加 39.0 kPa、底部減少 10.0 kPa，中點由 127.9 增為 142.4 kPa](figs/SM-2015-4-fig-2-seepage.svg)\n\n*圖 2　抽水後黏土內為向上穩態滲流：底部水頭不變、頂部降 5 m，孔隙水壓變成線性分布。攔下「以為黏土整層孔隙水壓都降 $5\\gamma_w$」與「忘了上方砂改用 $\\gamma_{dry}$ 使總應力也減少」兩種錯誤。*\n", "§4 步驟三", "figs/SM-2015-4-fig-2-seepage.svg"),
 "SM-2005-3": ("$$\\boxed{S_{total} = 27.58 \\text{ cm}}$$\n", "after",
   "![SM-2005-3 圖 1：橫軸有效應力 0 到 300 kPa，縱軸體積變化係數；附表四段階梯中，σ'0 = 25.5 到 σ'f = 225.5 kPa 之間的陰影面積分別為 10.7、12.0、4.2、0.7 cm，合計 27.58 cm](figs/SM-2005-3-fig-1-mv-steps.svg)\n\n*圖 1　$m_v$ 依有效應力分段，沉陷等於層厚乘陰影面積。攔下「整段用同一個 $m_v$」的錯誤：全用第一格會算成 62 cm，全用最後一格只有 3 cm。*\n", "§4（二）", "figs/SM-2005-3-fig-1-mv-steps.svg"),
 "SM-2009-1": ("### Step 2:", "before",
   "![SM-2009-1 圖 1（示意）：實驗室標準夯實曲線與現地高能量夯實曲線，現地曲線較高、最佳含水量較低；原設定含水量的鉛直線落在實驗室曲線乾側、現地曲線濕側，兩者都高於 95% 實驗室最大乾單位重](figs/SM-2009-1-fig-1-compaction.svg)\n\n*圖 1（示意，無數值）　題目要求的繪圖。能量提高後同一含水量由乾側變成濕側，相對夯實度仍合格但結構轉為分散、透水性下降；攔下「只看相對夯實度合格就以為達標」的錯誤。*\n\n", "§4 Step 1", "figs/SM-2009-1-fig-1-compaction.svg"),
 "SM-2012-2": ("### (二) 由(一)推得", "before",
   "![SM-2012-2 圖 1（示意）：e–log σ' 曲線上依序標出最大曲率點 A、水平線、切線、角平分線、正常壓密段延伸線，角平分線與延伸線的交點對應的應力為預壓密應力 σ'p](figs/SM-2012-2-fig-1-casagrande.svg)\n\n*圖 1（示意曲線）　題目㈠要求的作圖，編號對應上列六步。攔下「把最大曲率點直接當 $\\sigma'_p$」的錯誤：$\\sigma'_p$ 是角平分線與正常壓密段延伸線的交點。*\n\n", "§4（一）", "figs/SM-2012-2-fig-1-casagrande.svg"),
}
for q, (anchor, pos, block, sec, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, (anchor + "\n" + block) if pos == "after" else (block + anchor))
    old = "；非勘誤）*"
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace(old, "；%s 補解題圖解 %s；非勘誤）*" % (sec, fig))
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("done", q)
