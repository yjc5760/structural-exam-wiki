# -*- coding: utf-8 -*-
"""SM-U3-3 批 1 階段 E：把解題圖解插回解析 .md（可重複執行）。在 SM/ 下執行。"""
J = {
 "SM-2021-4": ("$$ \\boxed{\\text{FS} \\approx 0.98} $$\n", "after",
   "![SM-2021-4 圖 2：依比例尺量測的邊坡與 5 個切片，水位以下淺藍、以上淡橘；O 的虛線半徑各通過 W1–W5 的作用點，標註 α 60°、42°、30°、13°、0° 與量得的半徑角 61°、44°、29°、12°、0° 相符；各切片 W 分別為 555.9、846.4、765.6、578.6、227.7 kN/m，u 為 0、17.5、40.7、50.8、21.8 kPa；FS = 1522.1 / 1560.8 = 0.975](figs/SM-2021-4-fig-2-slices.svg)\n\n*圖 2　量測幾何與各切片 $W_n$、$u_n$、$\\alpha_n$。標註 $\\alpha$ 就是 O 到 $W_n$ 作用點的半徑角，所畫圓弧則不是以 O 為圓心的正圓；攔下「改用圓弧弦角（FS ≈ 1.37）」「切片 1 也計水壓」「沿用自編切片表」三種錯誤。*\n", "§4 Step 5", "figs/SM-2021-4-fig-2-slices.svg"),
 "SM-2006-3": ("*(註：若採用 $\\gamma_w = 10 \\text{ kN/m}^3$ 計算，FS 將約為 0.46，結論相同)*\n", "after",
   "\n![SM-2006-3 圖 2：左右兩格分別為常時與豪雨；滑動塊體夾在坡趾鉛直面（高 2 m，被動土壓向右）與坡肩後鉛直面（高 12 m，主動土壓向左）之間，底面沿黏土薄層 20 m 提供 T = 240 kN/m；常時 Pa = 351.4、Pp = 189.3、FS = 1.22；豪雨 Pa' = 125.6 加靜水推力 706.3，Pp' = 130.4 加 19.6，FS = 0.47](figs/SM-2006-3-fig-2-blocks.svg)\n\n*圖 2　三塊體法自由體，常時與豪雨並列。豪雨時 $s_u L$ 不變，驅動力八成以上來自坡肩後 12 m 的靜水推力；攔下「豪雨時把黏土改用有效應力」與「漏算張力裂縫積水」兩種錯誤。*\n", "§4 Step 3", "figs/SM-2006-3-fig-2-blocks.svg"),
 "SM-2008-4": ("$$\\boxed{FS = 0.74}$$\n", "after",
   "\n![SM-2008-4 圖 2：三角形塊體 ABC 沿 AC（40°）滑動；重心處 W = 503.2 向下、KhW = 100.7 水平向坡外；沿 AC 驅動 400.6、正向力 N = 320.8、抗滑 cL + N tan28° = 296.7，FS = 0.74；㈡ 地錨垂直 AC，每公尺 346.1 kN、每支 692 kN](figs/SM-2008-4-fig-2-forces.svg)\n\n*圖 2　重量與水平地震力沿滑動面分解。地震力向坡外時同時增加驅動、減少正向力；攔下「$K_hW\\sin40^\\circ$ 加到 $N$」與「把每公尺地錨力當每支荷重」兩種錯誤。*\n", "§4（一）Step 4", "figs/SM-2008-4-fig-2-forces.svg"),
 "SM-2024-2": ("$$\\boxed{i = 0.5}$$\n", "after",
   "\n![SM-2024-2 圖 2：自由水面與水平夾 30°，水由右上往左下流；流線平行自由水面、等勢線與之垂直；沿流線走 Δs，高程降 Δs sinθ，水力坡降 i = sin30° = 0.50，Dupuit 近似 tanθ = 0.577 只作對照](figs/SM-2024-2-fig-2-gradient.svg)\n\n*圖 2　自由水層的水力坡降。自由水面上壓力水頭為 0，水頭損失等於高程差，分母取沿流線長度；攔下「用水平距離得 $\\tan\\theta$」與「誤用坡角 $\\beta$ = 42°」兩種錯誤。*\n", "§4（三）", "figs/SM-2024-2-fig-2-gradient.svg"),
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
    d = "\n".join(lines).encode("utf-8")
    with open(p, "r+b") as f:
        f.seek(0); f.write(d); f.truncate()
    print("done", q)
