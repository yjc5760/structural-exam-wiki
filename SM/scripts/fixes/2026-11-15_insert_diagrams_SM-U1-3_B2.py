# -*- coding: utf-8 -*-
"""SM-U1-3 批 2 階段 E：把解題圖解插回解析 .md（可重複執行）。在 SM/ 下執行。
圖由各題 gen_<id>.py 產生（數值取自解析 §4）。掛載碟覆寫既有檔用 r+b＋truncate。"""
S5 = "## 5. 關鍵爭議點"
J = {
 "SM-2016-1": (S5, "before",
   "![SM-2016-1 圖 2：左為表一四點連成的理想化 e–log σ' 折線，σ'0 = 48 kPa、e0 = 0.900 沿 Cs = 0.04983 再壓到 σ'f = 144 kPa，未達 σ'c = 150 kPa（ec = 0.875）；右為加載 3 年（Tv = 0.28125）單向排水的超額孔隙水壓等時線，A、B、C 點 23.37、43.18、56.42 kPa，紅虛線為誤當雙向排水的錯誤分布](figs/SM-2016-1-fig-2-path-isochrone.svg)\n\n*圖 2　左：應力路徑只走再壓段，攔下誤用 $C_c$ 段而高估沉陷；右：頂部排水、底部不透水，水壓由頂往下遞增，攔下誤當雙向排水（$H_{dr}$ = 2 m）把 C 點水壓算成接近 0。*\n\n",
   "§4（一）～（三）", "figs/SM-2016-1-fig-2-path-isochrone.svg"),
 "SM-2017-2": (S5, "before",
   "![SM-2017-2 圖 1：上為夯實曲線，5 個試驗點與過 ω = 10、12、16% 的拋物線峰值 γdmax = 18.66 kN/m³、ωOMC = 13.2%；下為 CBR 對含水量的試驗點連線，CBR = 10 與之交於乾側 ω = 10.67%、濕側 16.50%，對應 γd 18.33 與 18.05；要求 γd ≥ 18.33，R = 98.2%；灰色標出取 18.05 時乾側 ω = 9.7%、CBR = 8.3 的反例](figs/SM-2017-2-fig-1-compaction-cbr.svg)\n\n*圖 1　題目要求的夯實曲線，並把 CBR = 10 的乾、濕側邊界投影到夯實曲線上。攔下「取較低的 18.05 當要求值」：乾側同一 $\\gamma_d$ 的 CBR 只有約 8.3，不到 10。*\n\n",
   "§4", "figs/SM-2017-2-fig-1-compaction-cbr.svg"),
 "SM-2018-1": (S5, "before",
   "![SM-2018-1 圖 1：沉陷對時間曲線，S∞ = 780 mm，已知 200 天 234 mm；1～4 年沉陷 316.1、447.1、536.7、603.0 mm；t = 800 天處標 U = 60% 分界，紅虛線為續用 √t 外推的錯誤值 548、632 mm](figs/SM-2018-1-fig-1-settlement-time.svg)\n\n*圖 1　由 200 天 30% 推得的沉陷—時間曲線。攔下兩種錯：把 234 mm 當最終沉陷，以及 U 超過 60%（約 800 天）後仍用 $S\\propto\\sqrt{t}$ 外推。*\n\n",
   "§4", "figs/SM-2018-1-fig-1-settlement-time.svg"),
 "SM-2021-2": (S5, "before",
   "![SM-2021-2 圖 2：沉陷對時間曲線，Sc = 62.28 cm；30、60、90 天沉陷 14.31、20.24、24.79 cm；50 cm 對應 414.4 天（U = 80.28%）；紅虛線為誤取 Hdr = 5 m 的曲線](figs/SM-2021-2-fig-2-settlement-time.svg)\n\n*圖 2　雙向排水 $H_{dr}$ = 2.5 m 的沉陷—時間曲線。攔下誤取 $H_{dr}$ = 5 m：同一沉陷需 4 倍時間，50 cm 會落在 600 天之外。*\n\n",
   "§4", "figs/SM-2021-2-fig-2-settlement-time.svg"),
 "SM-2024-3": ("$\\Delta\\sigma_C' = 299.96 - 192.98 = \\boxed{106.98 \\text{ kPa}}$ (增加)\n", "after",
   "\n![SM-2024-3 圖 2：降水前後有效應力沿深度分布（0～30 m），C 點 192.98 → 299.96 kPa、D 點 252.83 → 359.81 kPa，黏土內增量皆 106.98 kPa；紅虛線為水位以上仍用 γsat 的錯誤分布（C 點增量 156.96 kPa）；黏土內以虛線標 σ'p = 300 kPa](figs/SM-2024-3-fig-2-stress-profile.svg)\n\n*圖 2　降水後 2–18 m 改用乾單位重，黏土內各深度有效應力增量相同。攔下水位以上沿用 $\\gamma_{sat}$（增量多算約 50 kPa），並顯示 D 點由 252.83 跨過 $\\sigma'_p$ = 300 到 359.81，㈣ 須分兩段計算。*\n",
   "§4（一）", "figs/SM-2024-3-fig-2-stress-profile.svg"),
}
def write(p, t):
    b = t.encode("utf-8")
    with open(p, "r+b") as f:
        f.seek(0); f.write(b); f.truncate()
for q, (anchor, pos, block, sec, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, (anchor + block) if pos == "after" else (block + anchor))
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    assert lines[k[0]].endswith("；非勘誤）*"), q
    lines[k[0]] = lines[k[0]][:-len("；非勘誤）*")] + "；%s 補解題圖解 %s（腳本 gen_%s.py）；非勘誤）*" % (sec, fig, q)
    write(p, "\n".join(lines))
    print("done", q)
