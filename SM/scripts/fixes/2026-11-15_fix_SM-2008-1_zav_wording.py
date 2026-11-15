# -*- coding: utf-8 -*-
"""FIX SM-2008-1：§5／圖 1 圖說「超出 1 m³ 一成一」改為約 1.1%（量級敘述錯誤）；
§2、§5 補 γw = 10 的對照（S = 96.7%，勉強可行），把「做不到」限定為 γw = 9.81 的結論。
數值答案（體積、重量、加水量）不變。在 SM/ 下執行；可重複執行（已修過則跳過）。
內附獨立重算：印出 MISMATCHES: n。"""
import sys

def recompute():
    gA = 19.6 / 1.09; gB = 20.6 / 1.11
    VB = 20 / (4 * gA + gB); VA = 4 * VB
    WsA, WsB = gA * VA, gB * VB
    add = 2.4 - (0.09 * WsA + 0.11 * WsB)
    out = {"gA": gA, "gB": gB, "VA": VA, "VB": VB, "WtA": 19.6 * VA, "WtB": 20.6 * VB,
           "WsA": WsA, "WsB": WsB, "add_kN": add, "add_L981": add / 9.81 * 1000, "add_L10": add / 10 * 1000}
    for gw, tag in ((9.81, "981"), (10.0, "10")):
        Vs = WsA / (2.65 * gw) + WsB / (2.70 * gw); Gm = 20 / (Vs * gw); Vw = 2.4 / gw
        e = Gm * gw / 20 - 1
        out.update({f"Vs_{tag}": Vs, f"Gm_{tag}": Gm, f"VsVw_{tag}": Vs + Vw, f"e_{tag}": e,
                    f"S_{tag}": 0.12 * Gm / e * 100, f"zav_{tag}": Gm * gw / (1 + 0.12 * Gm),
                    f"wmax_{tag}": (1 - Vs) * gw / 20 * 100, f"over_{tag}": (Vs + Vw - 1) * 100})
    # 借土區飽和度（Gs 各自，γw=9.81）
    for k, w, g, G in (("SA", .09, gA, 2.65), ("SB", .11, gB, 2.70)):
        e = G * 9.81 / g - 1; out[k] = w * G / e * 100
    # 雙路徑：總濕重 = 20 × 1.12
    out["wet_total"] = out["WtA"] + out["WtB"] + add
    return out

EXPECT = {"gA": 17.9817, "gB": 18.5586, "VA": 0.8841, "VB": 0.2210, "WtA": 17.328, "WtB": 4.553,
          "WsA": 15.898, "WsB": 4.101, "add_kN": 0.518, "add_L981": 52.8, "add_L10": 51.8,
          "Vs_981": 0.76641, "Gm_981": 2.660, "VsVw_981": 1.01106, "e_981": 0.3048, "S_981": 104.7,
          "zav_981": 19.78, "wmax_981": 11.46, "over_981": 1.106, "VsVw_10": 0.9919, "e_10": 0.3301,
          "S_10": 96.7, "zav_10": 20.16, "wmax_10": 12.41, "SA": 53.5, "SB": 69.5, "wet_total": 22.40}

def check():
    r = recompute(); bad = []
    for k, v in EXPECT.items():
        if abs(r[k] - v) > max(abs(v) * 0.002, 0.051 if v > 10 else 0.0006):
            bad.append((k, v, r[k]))
    for b in bad: print("MISMATCH", b)
    print("MISMATCHES:", len(bad)); return len(bad)

if __name__ == "__main__":
    if check(): sys.exit(1)
    p = "raw/solutions/SM-2008-1/SM-2008-1.md"
    t = open(p, encoding="utf-8").read()
    # 落實檢查補修（D→C）：§3 陷阱 2 的「超過零空氣孔隙線」限定 γw = 9.81
    a3 = "本題驗下去會發現塞不進（超出 1.1%），亦即考卷指定的夯實目標超過零空氣孔隙線。"
    b3 = ("本題驗下去會發現塞不進（取 $\\gamma_w$ = 9.81 時超出 1.1%），亦即考卷指定的夯實目標超過零空氣孔隙線"
          "（取 $\\gamma_w$ = 10 則剛好在線下，$S$ = 96.7%，見 §5 ⑤）。")
    a4 = "物理上做不到**\n"
    b4 = "物理上做不到**（以真實的 $\\gamma_w$ = 9.81 驗算；取 10 則勉強可行，見 ⑤）\n"
    if t.count(a4) == 1:
        t = t.replace(a4, b4); open(p, "w", encoding="utf-8", newline="\n").write(t); print("part2 fixed §5 heading")
    a5 = "「依附表之 $G_s$，本目標夯實狀態之"
    b5 = "「依附表之 $G_s$ 並取 $\\gamma_w$ = 9.81，本目標夯實狀態之"
    if t.count(a5) == 1:
        t = t.replace(a5, b5); open(p, "w", encoding="utf-8", newline="\n").write(t); print("part2 fixed §5 ④")
    if a3 in t:
        t = t.replace(a3, b3); open(p, "w", encoding="utf-8", newline="\n").write(t); print("part2 fixed §3")
    if "取 $\\gamma_w$ = 10 的對照" in t:
        raise SystemExit("already fixed")
    R = [
    ("本題的答案是**做不到**（$S = 104.7\\% > 100\\%$，見 §5）。",
     "本題的答案是**做不到**（取 $\\gamma_w$ = 9.81 時 $S = 104.7\\% > 100\\%$；若取 $\\gamma_w$ = 10 則 $S$ = 96.7%，"
     "勉強可行——目標落在 ZAV 線邊緣，見 §5）。"),
    ("但沒有它就看不出土粒加水已經超出 $1 \\text{ m}^3$ 一成一（$S = 104.7\\%$）。*",
     "但沒有它就看不出土粒加水已經超出 $1 \\text{ m}^3$ 約 1.1%（$S = 104.7\\%$，$\\gamma_w$ = 9.81）。*"),
    ("  **土粒加水已經超出 $1 \\text{ m}^3$ 一成一，連一點空氣都容不下。** 換算成飽和度：",
     "  **土粒加水已經超出 $1 \\text{ m}^3$ 約 1.1%（多出 0.011 m³），連一點空氣都容不下。** 換算成飽和度："),
    ("  本卷卷首已明寫「倘若條件不足，請自行合理假設」，指出並處理這個矛盾是加分項。\n",
     "  本卷卷首已明寫「倘若條件不足，請自行合理假設」，指出並處理這個矛盾是加分項。\n\n"
     "  **⑤ 取 $\\gamma_w$ = 10 的對照（結論對 $\\gamma_w$ 敏感）**：$G_{s,mix}$ = 2.660 不變，但\n"
     "  $$V_s = \\frac{20}{2.660 \\times 10} = 0.7519 \\text{ m}^3 \\ ,\\quad V_w = \\frac{2.4}{10} = 0.240 \\text{ m}^3 \\ ,\\quad\n"
     "  V_s + V_w = 0.9919 \\text{ m}^3 < 1 \\text{ m}^3$$\n"
     "  $$e = \\frac{2.660 \\times 10}{20} - 1 = 0.3301 \\ ,\\quad S = \\frac{0.12 \\times 2.660}{0.3301} = 96.7\\% \\ ,\\quad\n"
     "  \\gamma_{d,ZAV} = \\frac{26.60}{1.3192} = 20.16 \\text{ kN/m}^3 > 20$$\n"
     "  亦即以 $\\gamma_w$ = 10 計，目標狀態剛好落在 ZAV 線下方、勉強可行。三個小題的答案不受影響（加水量換成體積為 51.8 L）。\n"
     "  考卷數據本身就在零空氣孔隙線邊緣：以真實的 $\\gamma_w$ = 9.81 驗算越線，以常用的簡化值 10 驗算則未越線，"
     "委員很可能以 $\\gamma_w$ = 10 或乙土的 $G_s$ = 2.70 訂目標。作答時寫明採用的 $\\gamma_w$ 並附上檢核即可，"
     "不宜斷言「題目錯誤」。\n"),
    ]
    for a, b in R:
        assert t.count(a) == 1, a[:50]
        t = t.replace(a, b)
    assert "一成一" not in t  # 清殘留（頁尾修正日期之外）
    t = t.rstrip("\n") + ("\n\n*修正日期：2026-11-15（§5／圖 1 圖說「超出 1 m³ 一成一」改為約 1.1%（量級敘述錯誤）；"
        "§2、§3、§5 補 $\\gamma_w$ = 10 的對照（$S$ = 96.7%），「做不到」限定為 $\\gamma_w$ = 9.81 的結論；三個小題答案不變；"
        "Python 重算 27 個數值 MISMATCHES: 0；腳本 `scripts/fixes/2026-11-15_fix_SM-2008-1_zav_wording.py`）*\n")
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("fixed", p)
