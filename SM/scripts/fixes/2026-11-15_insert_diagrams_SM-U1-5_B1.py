# -*- coding: utf-8 -*-
"""SM-U1-5 批 1 階段 E：把解題圖解插回解析 .md（可重複執行）。在 SM/ 下執行。圖由各題 gen_<id>.py 產生。"""
J = {
 "SM-2002-4": ("**Step 4: 重作試驗之規劃與要求**", "before",
   "![SM-2002-4 圖 1：橫軸有效應力，三組試驗壓密壓力 49、73.5、147 kPa（OCR 4.08、2.72、1.36）全在現地有效覆土壓 199.8 kPa 左側的過壓密段；試驗擬合的 c' = 15、φ' = 25° 包絡線以實線畫在試驗範圍內、虛線外插到設計應力範圍，另以點線示意過原點的正常壓密段包絡線；右側標出建議重做的壓密壓力約 200、300、400 kPa](figs/SM-2002-4-fig-1-pressure-vs-sv0.svg)\n\n"
   "*圖 1　把試驗壓密壓力和現地 $\\sigma'_{v0}$ 畫在同一條軸上，三組全部落在左側。攔下「沒和現地應力比較就接受 $c'$ = 15」的錯誤；NC 段包絡線為示意（題目未給）。*\n\n", "§4 Step 3", "figs/SM-2002-4-fig-1-pressure-vs-sv0.svg"),
 "SM-2003-4": ("**答：其不排水（UU 三軸試驗）剪力強度為 $\\boxed{30.76 \\text{ kPa}}$**\n", "after",
   "\n![SM-2003-4 圖 1：破壞時的有效應力莫爾圓，σ'3f = 30.76、σ'1f = σ'v0 = 92.28 kPa，與 φ' = 30° 過原點包絡線相切，半徑 Su = 30.76；虛線為 Af = 0.5 時的對照圓（46.14～138.42，Su = 46.14）](figs/SM-2003-4-fig-1-mohr-af.svg)\n\n"
   "*圖 1　$A_f$ = 1 時 $\\sigma'_{1f}$ 恰回到 $\\sigma'_{v0}$；考卷沒給 $A_f$，改取 0.5 圓就變大 1.5 倍。攔下「以為 $S_u$ 只由 $\\sigma'_{v0}$ 與 $\\phi'$ 決定、忘了交代 $A_f$ 假設」的錯誤。*\n", "§4 Step 2", "figs/SM-2003-4-fig-1-mohr-af.svg"),
 "SM-2012-1": ("$$ \\boxed{ \\Delta u_f = 39.12 \\text{ kPa} } $$\n", "after",
   "\n![SM-2012-1 圖 1：破壞時的總應力圓（83.47～183.47 kPa）與 φcu = 22° 線相切，有效應力圓（44.35～144.35 kPa）與 φ' = 32° 線相切，兩圓半徑同為 Su = 50，水平相距 Δuf = 39.12 kPa](figs/SM-2012-1-fig-1-two-mohr.svg)\n\n"
   "*圖 1　總應力圓切 $\\phi_{cu}$ 線定出 $\\sigma_3 = \\sigma'_{v0}$，左移 $\\Delta u_f$ 後切 $\\phi'$ 線。攔下「用 $\\phi'$ 反算 $\\sigma'_{v0}$」與「把 50 kPa 當破壞面剪應力」兩種錯誤。*\n", "§4 Step 3", "figs/SM-2012-1-fig-1-two-mohr.svg"),
 "SM-2025-2": ("$$ \\boxed{ \\Delta\\sigma = 160 \\text{ kN/m}^2 } $$\n", "after",
   "\n![SM-2025-2 圖 1：試體一（40～80）、試體二（80～150）的有效應力莫爾圓與包絡線 τ = 3.78 + σ' tan15.83° 相切，試體三 CD（200～360）亦相切；灰虛線為未扣孔隙水壓的總應力圓（75～115、150～220）](figs/SM-2025-2-fig-1-mohr-cphi.svg)\n\n"
   "*圖 1　兩個有效圓定出一條不過原點的包絡線，試體三的圓沿同一條線長大到 360。攔下「沒扣孔隙水壓就用總應力圓求參數」與「硬設 $c'$ = 0」的錯誤。*\n", "§4 Step 3", "figs/SM-2025-2-fig-1-mohr-cphi.svg"),
 "SM-2007-2": ("## 5. 關鍵爭議點與進階探討", "before",
   "![SM-2007-2 圖 1（示意）：左為 SUU，數個等半徑總應力圓與一條水平包絡線 τf = cu，另以藍虛線畫出唯一的有效應力圓；右為 UUU，圓隨圍壓先變大再維持等大，包絡線初段傾斜、後段轉水平](figs/SM-2007-2-fig-1-suu-uuu.svg)\n\n"
   "*圖 1（示意，無數值）　題目㈡要求的繪圖。差別只在 $B$ 值：飽和時圍壓全給孔隙水、圓等大；不飽和時圍壓部分變成有效應力、圓先變大。攔下「UU 試驗一律 $\\phi_u$ = 0」的錯誤。*\n\n", "§4（二）", "figs/SM-2007-2-fig-1-suu-uuu.svg"),
}
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
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；%s 補解題圖解 %s；非勘誤）*" % (sec, fig))
    data = "\n".join(lines).encode("utf-8")
    with open(p, "r+b") as fh:   # 掛載磁碟不允許 O_TRUNC，改用覆寫（新內容較長）
        fh.seek(0); fh.write(data)
        try: fh.truncate()
        except OSError: pass
    print("done", q)
