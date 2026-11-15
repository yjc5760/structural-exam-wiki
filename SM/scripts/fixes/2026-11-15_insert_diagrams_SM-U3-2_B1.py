# -*- coding: utf-8 -*-
"""SM-U3-2 批 1 階段 E：SM-2009-4、SM-2016-3、SM-2016-4、SM-2018-4 解題自由體圖插回解析（可重複執行）。在 SM/ 下執行。"""
J = {
 "SM-2009-4": ("\\boxed{B = 2.49 \\text{ m}}\n$$\n",
   "\n![SM-2009-4 圖 2：B = 2.49 m 的梯形重力牆自由體圖；牆背三角形土壓平行 20° 地表，Pa = 134.20 kN/m 作用於 H/3，分塊牆重 W1 = 86.4、W2 = 136.08 kN/m，合力落在距牆趾 B/3 = 0.830 m，底壓為三角形（牆趾 215.6 kPa、牆踵 0）](figs/SM-2009-4-fig-2-fbd.svg)\n\n*圖 2　解得 B 後的自由體圖。攔下三種錯誤：把 Pa 畫成水平（應平行地表 20°）、漏算 Pav 或取錯力臂（作用在牆背，力臂 B）、把 B/3 量自牆踵；合力在 B/3 ⇔ e = B/6，底壓呈三角形、牆踵恰為 0。*\n",
   "figs/SM-2009-4-fig-2-fbd.svg"),
 "SM-2016-3": ("（等價寫法：極限承載力合力 $q_{ult}L' = 2414.0$ kN/m 與 $V = 810$ kN/m 之比，同為 2.98。）\n",
   "\n![SM-2016-3 圖 2：加勁土體外部穩定自由體圖；背面土壓為矩形（Ka·qs = 18.44 kPa）加三角形（底部 51.63 kPa），Pa1 = 99.6 kN/m @ 2.0 m、Pa2 = 110.6 kN/m @ 3.0 m；W = 540 與 Q = 270 kN/m 作用於 2.25 m；底面合力距牆趾 1.594 m、傾角 14.55°，Meyerhof 有效寬度 L' = 3.188 m 上均佈 q' = 254.08 kPa，虛線為梯形分布 337.3／22.7 kPa 對照](figs/SM-2016-3-fig-2-fbd.svg)\n\n*圖 2　外部穩定自由體圖。攔下本題原解的錯誤：底面合力傾斜 14.55°，承載力必須乘考卷第 4 頁的傾斜因數（$i_\\gamma$ 只剩 0.298）；另攔 $q_s$ 只算推力、漏算加勁區上的垂直力，以及有效寬度量錯起點。*\n",
   "figs/SM-2016-3-fig-2-fbd.svg"),
 "SM-2016-4": ("答：合力作用點位於距牆底 $3.08 \\text{ m}$ 處（沿牆背高度）。\n",
   "\n![SM-2016-4 圖 2：左圖為靜態自由體圖，Coulomb Pa = 238.9 kN/m 與牆背法線夾 15°、與水平夾 29.04° 斜向下作用於牆背 H/3（x = 4.333 m），牆重 W1 = 564、W2 = 188 kN/m，底壓 qmax = 339.0、qmin = 8.2 kPa，合力距趾 1.706 m、e = 0.794 m、B' = 3.412 m、θ = 13.53°；右圖為 M–O 分解：靜態 Pa @ 2.67 m、動態增量 ΔPae = 57.34 kN/m @ 4.8 m，合力 Pae = 296.26 kN/m @ 3.08 m](figs/SM-2016-4-fig-2-fbd.svg)\n\n*圖 2　靜態自由體圖與 M–O 合力作用點。攔下：把 β 當成背填土面傾角、Pa 方向畫成水平或只加 δB 不加牆背傾角、Pav 力臂取錯，以及把 Pae 全部放在 H/3（2.67 m）或 H/2。*\n",
   "figs/SM-2016-4-fig-2-fbd.svg"),
 "SM-2018-4": ("**答：抗滑移安全係數為 $\\boxed{1.55}$。**\n",
   "\n![SM-2018-4 圖 2：懸臂式擋土牆 Rankine 虛擬背自由體圖；虛擬背過踵端、高 H' = 9.204 m，三角形土壓平行 12° 地表，Pa = 246.92 kN/m @ 3.068 m（Pah = 241.51、Pav = 51.33 kN/m @ x = 5.6 m）；分塊重量 W1–W6（含踵上土 467.25、23.18 與趾上覆土 21.09 kN/m），底面抗滑力 FR = 374.7 kN/m](figs/SM-2018-4-fig-2-fbd.svg)\n\n*圖 2　Rankine 虛擬背自由體圖。攔下：H' 漏加底版厚或踵端上方的 3.5·tan12°、把踵上土當外力而非牆體一部分、Pav 力臂取牆背而非虛擬背（5.6 m），以及把 Pa 畫成水平。*\n",
   "figs/SM-2018-4-fig-2-fbd.svg"),
}
for q, (anchor, block, fig) in J.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if fig in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, anchor + block)
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；§4 補解題圖解 %s；非勘誤）*" % fig)
    data = "\n".join(lines).encode("utf-8")
    with open(p, "r+b") as f:
        f.write(data); f.truncate()
    print("done", q)
