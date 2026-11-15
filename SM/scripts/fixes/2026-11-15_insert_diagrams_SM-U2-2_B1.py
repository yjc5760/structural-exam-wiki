# -*- coding: utf-8 -*-
"""SM-U2-2 批 1（G5）階段 E：把解題圖解插回解析 .md（可重複執行；已插者跳過）。在 SM/ 下執行。
覆寫用 r+b＋truncate（掛載碟上 open(..., 'w') 偶回 Errno 22）。"""
def wr(p, s):
    b = s.encode("utf-8")
    with open(p, "r+b") as f:
        f.seek(0); f.write(b); f.truncate()
A = "## 5. 關鍵爭議點與進階探討 (Critical Issues & Advanced Discussion)"
J = {
 "SM-2005-4": ("$$ Q_{1.5} = 108\\pi + 27\\pi = 135\\pi \\text{ kN} \\approx \\boxed{424.12 \\text{ kN}} $$\n", "after",
   "\n![SM-2005-4 圖 2：剛性墩的荷重–沉陷曲線，橫軸沉陷 0 到 10 cm、縱軸荷重；摩擦分量在 2 cm 達 452.39 kN 後持平，端承分量到 8 cm 才達 452.39 kN；合計曲線在 1 cm 為 282.74 kN、1.5 cm 為 424.12 kN、8 cm 達 Qu = 904.78 kN，Qu/3 = 301.59 kN 對應約 1.07 cm](figs/SM-2005-4-fig-2-load-settlement.svg)\n\n*圖 2　荷重–沉陷曲線。極限載重要沉陷 8 cm 才發揮，位移限制 1～1.5 cm 時摩擦已動員五到七成、端承不到兩成；攔下「把 $Q_{s,max}$ 與 $Q_{p,max}$ 當成同時發生」的錯誤，也可直接看出㈠、㈡兩法的數值關係。*\n",
   "§4（二）", "figs/SM-2005-4-fig-2-load-settlement.svg"),
 "SM-2006-2": (A, "before",
   "![SM-2006-2 圖 1（概念圖）：無因次勁度 K 除以根號 ks S EA 對 λL 作圖，曲線為 tanh(λL)，由原點沿短樁漸近線 K ≈ ks S L 上升，λL = 3 時 0.995，趨近半無限長的 1](figs/SM-2006-2-fig-1-stiffness.svg)\n\n*圖 1（概念圖，無題給數值）　情況㈠的勁度隨 $\\lambda L$ 單調收斂到情況㈡的 $\\sqrt{EAk_sS}$。攔下符號弄反得到三角函數解（勁度隨樁長振盪、發散）的錯誤，並看出短樁極限 $K\\to k_sSL$。*\n\n",
   "§4 Step 4 後", "figs/SM-2006-2-fig-1-stiffness.svg"),
 "SM-2007-3": ("### Step 4: (三) 計算容許載重 $Q_a$", "before",
   "![SM-2007-3 圖 1：左為有效覆土壓沿深度，計算用值 0 到 10 m 線性增至 180 kPa 後維持，實際值虛線到 15 m 為 270 kPa；右為單位摩擦 0 到 10 m 由 0 增至 43.41 kPa 後維持，三角形 Qs1 = 340.93、矩形 Qs2 = 340.93 kN，樁底 Qp = 742.20 kN](figs/SM-2007-3-fig-1-critical-depth.svg)\n\n*圖 1　臨界深度 $20D=10$ m 以下 $\\sigma'_v$ 封頂，樁身摩擦分成三角形與矩形兩段，樁底也用 180 kPa。攔下「10 m 以下仍線性增加」與「樁底用 15 m 實際應力」兩種錯誤（後者另見 §5 字面讀法）。*\n\n",
   "§4 Step 3 後", "figs/SM-2007-3-fig-1-critical-depth.svg"),
 "SM-2012-3": (A, "before",
   "![SM-2012-3 圖 1：左為單位摩擦沿深度，上層黏土 0 到 8 m 為 45 kPa、下層 52.5 kPa 到樁底 15.22 m；右為由地表累積的抗拉力（摩擦加有效自重），8 m 處 586.21 kN，15.22 m 處達 1200 kN](figs/SM-2012-3-fig-1-uplift.svg)\n\n*圖 1　累積抗拉力隨深度增加，到 1200 kN 的深度就是貫入深度。攔下「只答進入下層的 7.22 m」與「自重項漏了也隨 $x$ 增加」的錯誤。*\n\n",
   "§4 Step 4 後", "figs/SM-2012-3-fig-1-uplift.svg"),
 "SM-2014-2": ("**Step 6: 總沉陷量計算**", "before",
   "![SM-2014-2 圖 2：左為樁身軸力沿深度，樁頂 4500 kN，18 m 處 2803.5 kN，樁底 Qwp = 1484.07 kN，摩擦承擔 Qws = 3015.93 kN；右為沉陷三成分長條，Se1 = 3.79、Se2 = 39.15、Se3 = 4.04 mm，合計 46.98 mm](figs/SM-2014-2-fig-2-load-transfer.svg)\n\n*圖 2　荷重傳遞與沉陷三成分。軸力曲線下的面積就是 $S_{e1}$ 的分子；樁底只剩約三分之一荷重，卻貢獻 83% 沉陷。攔下「把 4500 kN 全部當樁底荷重」與「$S_{e3}$ 式中 $P$ 當成荷重」的錯誤。*\n\n",
   "§4 Step 5 後", "figs/SM-2014-2-fig-2-load-transfer.svg"),
 "SM-2021-3": ("### Step 5：(一) 計算容許垂直支承力 ($Q_{a,\\text{comp}}$)", "before",
   "![SM-2021-3 圖 2：左為單位摩擦沿深度，砂土 0 到 6 m 由 0 增至 17.76 kPa、黏土 6 到 12 m 為 65 kPa，Qs1 = 100.46、Qs2 = 735.15 kN；右為極限受壓時樁身軸力，樁頂 1090.04 kN、6 m 處 989.58 kN、樁底 Qp = 254.43 kN，並列容許受壓 363.35 kN 與容許拉拔 326.69 kN](figs/SM-2021-3-fig-2-resistance.svg)\n\n*圖 2　上砂下黏兩種摩擦機制。砂土段用 $\\gamma'$ 所以 $f$ 很小、黏土段 $f=\\alpha c_u$ 與深度無關。攔下「水位在地表卻用 $\\gamma_{sat}$」與「拉拔也加樁底」的錯誤。*\n\n",
   "§4 Step 4 後", "figs/SM-2021-3-fig-2-resistance.svg"),
 "SM-2023-3": ("### Step 4: 計算 (二) 樁底極限支承力 $Q_p$", "before",
   "![SM-2023-3 圖 1：左為三層土的有效覆土壓沿深度，5 m 處 90、10 m 處 190 kPa 後封頂，實際值虛線到 25 m 為 343 kPa，水位與臨界深度都在 10 m；右為單位摩擦，SM 層 0 到 53.22、ML 層 5 到 10 m 增至 116.43 後定值到 15 m、SW 層 138.04 kPa，四段摩擦力 209.0、673.8、914.4、2168.3 kN，樁底 Qp = 1407.6 kN](figs/SM-2023-3-fig-1-critical-depth.svg)\n\n*圖 1　臨界深度 $Z_c=20D$ 恰在水位，10 m 以下計算用 $\\sigma'_v$ 固定 190 kPa；跨 $Z_c$ 的 ML 層拆成遞增段與定值段。攔下「10 m 以下繼續加 $\\gamma' z$」與「ML 整層用一個平均應力」的錯誤。數值取本解假設（$K=1.0$、$\\delta=\\phi$），替代假設見 §5。*\n\n",
   "§4 Step 3 後", "figs/SM-2023-3-fig-1-critical-depth.svg"),
 "SM-2024-4": ("*(註：實務上繪製樁身阻抗圖時，橫軸為單位摩擦阻抗 $f_s$ 或是軸力分布，建議於筆記中加入手繪圖加以輔助示意)*\n", "replace",
   "![SM-2024-4 圖 2：四格樁身阻抗分布圖。黏土：單位摩擦沿全長 37.20 kPa、軸力由 5000 kN 線性減到樁底 424.12 kN，樁長 39.15 m；砂土：單位摩擦 0 到 15 m 線性增至 32.64 kPa 後定值到 50.28 m，軸力先拋物線減到 15 m 處 4230.9 kN、再直線減到樁底 613.6 kN](figs/SM-2024-4-fig-2-resistance.svg)\n\n*圖 2　題目㈡要求的樁身阻抗分布圖（單位摩擦與軸力兩種畫法並列）。攔下「砂土 15D 以下 $f$ 繼續增加」與「端承漏了 $q_l$ 封頂」的錯誤；黏土 $f$ 與深度無關。*\n",
   "§4 Step 4", "figs/SM-2024-4-fig-2-resistance.svg"),
}
for q, (anchor, pos, block, sec, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, {"after": anchor + block, "before": block + anchor, "replace": block}[pos])
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；%s 補解題圖解 %s；非勘誤）*" % (sec, fig))
    wr(p, "\n".join(lines))
    print("done", q)
